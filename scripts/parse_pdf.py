#!/usr/bin/env python3
"""
Parse the Chinese Modern History exam PDF and extract questions into JSON format.
"""

import pdfplumber
import json
import re
import os
import sys
import unicodedata

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# Mapping of Kangxi Radicals to their standard CJK equivalents
KANGXI_TO_CJK = {
    0x2F00: '\u4e00',  # ⼀ -> 一
    0x2F01: '\u4e28',  # ⼁ -> 丨
    0x2F02: '\u4e36',  # ⼂ -> 丶
    0x2F03: '\u4e3f',  # ⼃ -> 丿
    0x2F04: '\u4e59',  # ⼄ -> 乙
    0x2F05: '\u4e85',  # ⼅ -> 亅
    0x2F06: '\u4e8c',  # ⼆ -> 二
    0x2F07: '\u4ea0',  # ⼇ -> 亠
    0x2F08: '\u4eba',  # ⼈ -> 人
    0x2F09: '\u513f',  # ⼉ -> 儿
    0x2F0A: '\u5165',  # ⼊ -> 入
    0x2F0B: '\u516b',  # ⼋ -> 八
    0x2F0C: '\u5182',  # ⼌ -> 冂
    0x2F0D: '\u5196',  # ⼍ -> 冖
    0x2F0E: '\u51ab',  # ⼎ -> 冫
    0x2F0F: '\u51e0',  # ⼏ -> 几
    0x2F10: '\u51f5',  # ⼐ -> 凵
    0x2F11: '\u5200',  # ⼑ -> 刀
    0x2F12: '\u529b',  # ⼒ -> 力
    0x2F13: '\u52f9',  # ⼓ -> 勹
    0x2F14: '\u5315',  # ⼔ -> 匕
    0x2F15: '\u531a',  # ⼕ -> 匚
    0x2F16: '\u5338',  # ⼖ -> 匸
    0x2F17: '\u5341',  # ⼗ -> 十
    0x2F18: '\u535c',  # ⼘ -> 卜
    0x2F19: '\u5369',  # ⼙ -> 卩
    0x2F1A: '\u5382',  # ⼚ -> 厂
    0x2F1B: '\u53b6',  # ⼛ -> 厶
    0x2F1C: '\u53c8',  # ⼜ -> 又
    0x2F1D: '\u53e3',  # ⼝ -> 口
    0x2F1E: '\u56d7',  # ⼞ -> 囗
    0x2F1F: '\u571f',  # ⼟ -> 土
    0x2F20: '\u58eb',  # ⼠ -> 士
    0x2F21: '\u5902',  # ⼡ -> 夂
    0x2F22: '\u590a',  # ⼢ -> 夊
    0x2F23: '\u5915',  # ⼣ -> 夕
    0x2F24: '\u5927',  # ⼤ -> 大
    0x2F25: '\u5973',  # ⼥ -> 女
    0x2F26: '\u5b50',  # ⼦ -> 子
    0x2F27: '\u5b80',  # ⼧ -> 宀
    0x2F28: '\u5bf8',  # ⼨ -> 寸
    0x2F29: '\u5c0f',  # ⼩ -> 小
    0x2F2A: '\u5c22',  # ⼪ -> 尢
    0x2F2B: '\u5c38',  # ⼫ -> 尸
    0x2F2C: '\u5c6e',  # ⼬ -> 屮
    0x2F2D: '\u5c71',  # ⼭ -> 山
    0x2F2E: '\u5ddb',  # ⼮ -> 巛
    0x2F2F: '\u5de5',  # ⼯ -> 工
    0x2F30: '\u5df1',  # ⼰ -> 己
    0x2F31: '\u5dfe',  # ⼱ -> 巾
    0x2F32: '\u5e72',  # ⼲ -> 干
    0x2F33: '\u5e7a',  # ⼳ -> 幺
    0x2F34: '\u5e7f',  # ⼴ -> 广
    0x2F35: '\u5ef4',  # ⼵ -> 廴
    0x2F36: '\u5efe',  # ⼶ -> 廾
    0x2F37: '\u5f0b',  # ⼷ -> 弋
    0x2F38: '\u5f13',  # ⼸ -> 弓
    0x2F39: '\u5f50',  # ⼹ -> 彐
    0x2F3A: '\u5f61',  # ⼺ -> 彡
    0x2F3B: '\u5f73',  # ⼻ -> 彳
    0x2F3C: '\u5fc3',  # ⼼ -> 心
    0x2F3D: '\u6208',  # ⼽ -> 戈
    0x2F3E: '\u6236',  # ⼾ -> 戶
    0x2F3F: '\u624b',  # ⼿ -> 手
    0x2F40: '\u652f',  # ⽀ -> 支
    0x2F41: '\u6534',  # ⽁ -> 攴
    0x2F42: '\u6587',  # ⽂ -> 文
    0x2F43: '\u6597',  # ⽃ -> 斗
    0x2F44: '\u659b',  # ⽄ -> 斤
    0x2F45: '\u65a4',  # ⽅ -> 方
    0x2F46: '\u65b9',  # ⽆ -> 无
    0x2F47: '\u65e0',  # ⽇ -> 日
    0x2F48: '\u65e5',  # ⽈ -> 曰
    0x2F49: '\u66f0',  # ⽉ -> 月
    0x2F4A: '\u6708',  # ⽊ -> 木
    0x2F4B: '\u6728',  # ⽋ -> 欠
    0x2F4C: '\u6b20',  # ⽌ -> 止
    0x2F4D: '\u6b62',  # ⽍ -> 歹
    0x2F4E: '\u6b79',  # ⽎ -> 殳
    0x2F4F: '\u6bb3',  # ⽏ -> 毋
    0x2F50: '\u6bcb',  # ⽐ -> 比
    0x2F51: '\u6bd4',  # ⽑ -> 毛
    0x2F52: '\u6bdb',  # ⽒ -> 氏
    0x2F53: '\u6c0f',  # ⽓ -> 气
    0x2F54: '\u6c14',  # ⽔ -> 水
    0x2F55: '\u6c34',  # ⽕ -> 火
    0x2F56: '\u706b',  # ⽖ -> 爪
    0x2F57: '\u722a',  # ⽗ -> 父
    0x2F58: '\u7236',  # ⽘ -> 爻
    0x2F59: '\u723b',  # ⽙ -> 爿
    0x2F5A: '\u723f',  # ⽚ -> 片
    0x2F5B: '\u7247',  # ⽛ -> 牙
    0x2F5C: '\u7259',  # ⽜ -> 牛
    0x2F5D: '\u725b',  # ⽝ -> 犬
    0x2F5E: '\u72ac',  # ⽞ -> 玄
    0x2F5F: '\u7384',  # ⽟ -> 玉
    0x2F60: '\u7389',  # ⽠ -> 瓜
    0x2F61: '\u74dc',  # ⽡ -> 瓦
    0x2F62: '\u74e6',  # ⽢ -> 甘
    0x2F63: '\u7518',  # ⽣ -> 生
    0x2F64: '\u751f',  # ⽤ -> 用
    0x2F65: '\u7528',  # ⽥ -> 田
    0x2F66: '\u7530',  # ⽦ -> 疋
    0x2F67: '\u758b',  # ⽧ -> 疒
    0x2F68: '\u7592',  # ⽨ -> 癶
    0x2F69: '\u7676',  # ⽩ -> 白
    0x2F6A: '\u767d',  # ⽪ -> 皮
    0x2F6B: '\u76ae',  # ⽫ -> 皿
    0x2F6C: '\u76bf',  # ⽬ -> 目
    0x2F6D: '\u76ee',  # ⽭ -> 矛
    0x2F6E: '\u77db',  # ⽮ -> 矢
    0x2F6F: '\u77e2',  # ⽯ -> 石
    0x2F70: '\u77f3',  # ⽰ -> 示
    0x2F71: '\u793a',  # ⽱ -> 禸
    0x2F72: '\u79b8',  # ⽲ -> 禾
    0x2F73: '\u79be',  # ⽳ -> 穴
    0x2F74: '\u7a74',  # ⽴ -> 立
    0x2F75: '\u7acb',  # ⽵ -> 竹
    0x2F76: '\u7af9',  # ⽶ -> 米
    0x2F77: '\u7c73',  # ⽷ -> 糸
    0x2F78: '\u7cf8',  # ⽸ -> 缶
    0x2F79: '\u7f36',  # ⽹ -> 网
    0x2F7A: '\u7f51',  # ⽺ -> 羊
    0x2F7B: '\u7f8a',  # ⽻ -> 羽
    0x2F7C: '\u7fbd',  # ⽼ -> 老
    0x2F7D: '\u8001',  # ⽽ -> 而
    0x2F7E: '\u800c',  # ⽾ -> 耒
    0x2F7F: '\u8012',  # ⽿ -> 耳
    0x2F80: '\u8033',  # ⾀ -> 聿
    0x2F81: '\u807f',  # ⾁ -> 肉
    0x2F82: '\u8089',  # ⾂ -> 臣
    0x2F83: '\u81e3',  # ⾃ -> 自
    0x2F84: '\u81ea',  # ⾄ -> 至
    0x2F85: '\u81f3',  # ⾅ -> 臼
    0x2F86: '\u81fc',  # ⾆ -> 舌
    0x2F87: '\u820c',  # ⾇ -> 舛
    0x2F88: '\u821b',  # ⾈ -> 舟
    0x2F89: '\u821f',  # ⾉ -> 艮
    0x2F8A: '\u826e',  # ⾊ -> 色
    0x2F8B: '\u8272',  # ⾋ -> 艸
    0x2F8C: '\u8278',  # ⾌ -> 虍
    0x2F8D: '\u864d',  # ⾍ -> 虫
    0x2F8E: '\u866b',  # ⾎ -> 血
    0x2F8F: '\u8840',  # ⾏ -> 行
    0x2F90: '\u884c',  # ⾐ -> 衣
    0x2F91: '\u8863',  # ⾑ -> 襾
    0x2F92: '\u897e',  # ⾒ -> 見
    0x2F93: '\u898b',  # ⾓ -> 角
    0x2F94: '\u89d2',  # ⾔ -> 言
    0x2F95: '\u8a00',  # ⾕ -> 谷
    0x2F96: '\u8c37',  # ⾖ -> 豆
    0x2F97: '\u8c46',  # ⾗ -> 豕
    0x2F98: '\u8c55',  # ⾘ -> 豸
    0x2F99: '\u8c78',  # ⾙ -> 貝
    0x2F9A: '\u8c9d',  # ⾚ -> 赤
    0x2F9B: '\u8d64',  # ⾛ -> 走
    0x2F9C: '\u8d70',  # ⾜ -> 足
    0x2F9D: '\u8db3',  # ⾝ -> 身
    0x2F9E: '\u8eab',  # ⾞ -> 車
    0x2F9F: '\u8eca',  # ⾟ -> 辛
    0x2FA0: '\u8f9b',  # ⾠ -> 辰
    0x2FA1: '\u8fb0',  # ⾡ -> 辵
    0x2FA2: '\u8fb5',  # ⾢ -> 邑
    0x2FA3: '\u9091',  # ⾣ -> 酉
    0x2FA4: '\u9149',  # ⾤ -> 釆
    0x2FA5: '\u91c6',  # ⾥ -> 里
    0x2FA6: '\u91cc',  # ⾦ -> 金
    0x2FA7: '\u91d1',  # ⾧ -> 長
    0x2FA8: '\u9577',  # ⾨ -> 門
    0x2FA9: '\u9580',  # ⾩ -> 阜
    0x2FAA: '\u961c',  # ⾪ -> 隶
    0x2FAB: '\u96b6',  # ⾫ -> 隹
    0x2FAC: '\u96b9',  # ⾬ -> 雨
    0x2FAD: '\u96e8',  # ⾭ -> 靑
    0x2FAE: '\u9751',  # ⾮ -> 非
    0x2FAF: '\u975e',  # ⾯ -> 面
    0x2FB0: '\u9762',  # ⾰ -> 革
    0x2FB1: '\u9769',  # ⾱ -> 韋
    0x2FB2: '\u97cb',  # ⾲ -> 韭
    0x2FB3: '\u97ed',  # ⾳ -> 音
    0x2FB4: '\u97f3',  # ⾴ -> 頁
    0x2FB5: '\u9801',  # ⾵ -> 風
    0x2FB6: '\u98a8',  # ⾶ -> 飛
    0x2FB7: '\u98db',  # ⾷ -> 食
    0x2FB8: '\u98df',  # ⾸ -> 首
    0x2FB9: '\u9996',  # ⾺ -> 馬
    0x2FBA: '\u99ac',  # ⾻ -> 骨
    0x2FBB: '\u9aa8',  # ⾼ -> 高
    0x2FBC: '\u9ad8',  # ⾽ -> 髟
    0x2FBD: '\u9adf',  # ⾾ -> 鬥
    0x2FBE: '\u9b25',  # ⾿ -> 鬯
    0x2FBF: '\u9b2f',  # ⿀ -> 鬲
    0x2FC0: '\u9b32',  # ⿁ -> 鬼
    0x2FC1: '\u9b3c',  # ⿂ -> 魚
    0x2FC2: '\u9b5a',  # ⿃ -> 鳥
    0x2FC3: '\u9ce5',  # ⿄ -> 鹵
    0x2FC4: '\u9e75',  # ⿅ -> 鹿
    0x2FC5: '\u9e7f',  # ⿆ -> 麥
    0x2FC6: '\u9ea5',  # ⿇ -> 麻
    0x2FC7: '\u9ebb',  # ⿈ -> 黃
    0x2FC8: '\u9ec3',  # ⿉ -> 黍
    0x2FC9: '\u9ecd',  # ⿊ -> 黑
    0x2FCA: '\u9ed1',  # ⿋ -> 黹
    0x2FCB: '\u9ef9',  # ⿌ -> 黽
    0x2FCC: '\u9efd',  # ⿍ -> 鼎
    0x2FCD: '\u9f0e',  # ⿎ -> 鼓
    0x2FCE: '\u9f13',  # ⿏ -> 鼠
    0x2FCF: '\u9f20',  # ⿐ -> 鼻
    0x2FD0: '\u9f3b',  # ⿑ -> 齊
    0x2FD1: '\u9f4a',  # ⿒ -> 齒
    0x2FD2: '\u9f52',  # ⿓ -> 龍
    0x2FD3: '\u9f8d',  # ⿔ -> 龜
    0x2FD4: '\u9f9c',  # ⿕ -> 龠
    0x2FD5: '\u9fa0',
}


def normalize_kangxi(text):
    """Convert Kangxi radical characters to their standard CJK equivalents."""
    result = []
    for ch in text:
        code = ord(ch)
        if 0x2F00 <= code <= 0x2FD5 and code in KANGXI_TO_CJK:
            result.append(KANGXI_TO_CJK[code])
        else:
            result.append(ch)
    return ''.join(result)


def find_pdf():
    """Find the PDF file in common locations."""
    candidates = [
        os.path.join(PROJECT_ROOT, "..", "中国近代史期末复习资料.pdf"),
        os.path.join(PROJECT_ROOT, "中国近代史期末复习资料.pdf"),
        os.path.join(os.path.expanduser("~/Desktop"), "中国近代史期末复习资料.pdf"),
    ]
    for path in candidates:
        normalized = os.path.normpath(path)
        if os.path.exists(normalized):
            return normalized
    return None


def extract_text_from_pdf(pdf_path):
    """Extract text from PDF using pdfplumber."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def clean_text(text):
    """Clean up the extracted text."""
    lines = text.split('\n')
    cleaned = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.isdigit() and len(stripped) <= 4:
            continue
        if '2026-07-02' in stripped:
            continue
        if stripped == '中国近代史期末复习资料.md':
            continue
        # Remove page number markers like "1 / 43"
        if re.match(r'^\d+\s*/\s*\d+$', stripped):
            continue
        cleaned.append(stripped)
    return '\n'.join(cleaned)


def split_options_line(line):
    """Split a line that may contain multiple options like 'A. xxx B. xxx' into individual options."""
    result = []
    matches = list(re.finditer(r'([A-D])[.、]\s*', line))
    for idx, m in enumerate(matches):
        letter = m.group(1)
        start = m.end()
        if idx + 1 < len(matches):
            end = matches[idx + 1].start()
        else:
            end = len(line)
        text = line[start:end].strip().rstrip()
        result.append((letter, text))
    return result


def parse_questions(text):
    """Parse the cleaned text into structured question data."""
    questions = []
    lines = text.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Match question number pattern
        question_match = re.match(r'^(\d+)[.、]\s*(.*)', line)
        if not question_match:
            i += 1
            continue
        
        q_id = int(question_match.group(1))
        q_text = question_match.group(2).strip()
        
        # Collect multi-line question text
        i += 1
        while i < len(lines):
            next_line = lines[i].strip()
            if re.match(r'^[A-D][.、]', next_line):
                break
            if re.match(r'^\d+[.、]', next_line):
                break
            # Check for any 【...】 marker
            if '【' in next_line and '】' in next_line:
                break
            q_text += ' ' + next_line
            i += 1
        
        # Parse options
        options = {}
        while i < len(lines):
            line = lines[i].strip()
            
            if re.match(r'^[A-D][.、]', line):
                parsed_options = split_options_line(line)
                for letter, text in parsed_options:
                    if letter not in options:
                        options[letter] = text
                i += 1
            else:
                break
        
        # Parse answer, explanation
        answer = ""
        explanation = ""
        while i < len(lines):
            line = lines[i].strip()
            
            # Match answer - look for 【...】 containing 正确 and 答 and 案
            if '【' in line and '】' in line and '正确' in line:
                ans_match = re.search(r'【[^】]*正确[^】]*】\s*([A-D])', line)
                if ans_match:
                    answer = ans_match.group(1)
                i += 1
                continue
            
            # Match explanation - look for 【...】 containing 题 and 目 and 解析
            if '【' in line and '】' in line and '题' in line and '解析' in line:
                expl_match = re.search(r'【[^】]*题[^】]*解析[^】]*】\s*(.*)', line)
                if expl_match:
                    explanation = expl_match.group(1).strip()
                i += 1
                continue
            
            # Skip core考点 lines
            if '【' in line and '】' in line and '核心' in line:
                i += 1
                continue
            
            # If we hit a new question, stop
            if re.match(r'^\d+[.、]', line):
                break
            
            i += 1
        
        # Build options list in order
        options_list = []
        for key in ['A', 'B', 'C', 'D']:
            if key in options:
                options_list.append(f"{key}. {options[key]}")
        
        questions.append({
            "id": q_id,
            "type": "single",
            "question": q_text,
            "options": options_list,
            "answer": answer,
            "explanation": explanation
        })
    
    return questions


def main():
    pdf_path = find_pdf()
    if not pdf_path:
        print("Error: Cannot find PDF file '中国近代史期末复习资料.pdf'")
        sys.exit(1)
    
    print(f"Found PDF: {pdf_path}")
    print("Extracting text from PDF...")
    
    text = extract_text_from_pdf(pdf_path)
    print(f"Extracted {len(text)} characters")
    
    # Normalize Kangxi radicals to standard CJK
    text = normalize_kangxi(text)
    print("Normalized Kangxi radicals")
    
    text = clean_text(text)
    print(f"After cleaning: {len(text)} characters")
    
    print("Parsing questions...")
    questions = parse_questions(text)
    print(f"Parsed {len(questions)} questions")
    
    # Write output
    output_path = os.path.join(PROJECT_ROOT, "src", "data", "questions.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    
    print(f"Questions saved to: {output_path}")
    
    # Summary
    with_answers = sum(1 for q in questions if q['answer'])
    with_explanations = sum(1 for q in questions if q['explanation'])
    print(f"\nSummary:")
    print(f"  Total questions: {len(questions)}")
    print(f"  With answers: {with_answers}")
    print(f"  With explanations: {with_explanations}")
    
    # Check for issues
    issues = []
    for q in questions:
        if len(q['options']) < 4:
            issues.append(f"Q{q['id']}: {len(q['options'])} options")
        if not q['explanation']:
            issues.append(f"Q{q['id']}: no explanation")
    
    if issues:
        print(f"\nIssues ({len(issues)}):")
        for issue in issues[:10]:
            print(f"  {issue}")
        if len(issues) > 10:
            print(f"  ... and {len(issues)-10} more")


if __name__ == "__main__":
    main()
