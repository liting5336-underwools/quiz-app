import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
json_path = os.path.join(project_root, 'src', 'data', 'questions.json')

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# All fixes - multi-character only to avoid breaking correct words
# Single-char replacements are ONLY for OCR garbage characters, not real Chinese chars
fixes = [
    # Multi-character fixes (must come before single-char)
    ('面命', '革命'),
    ('目盾', '矛盾'),
    ('目头', '矛头'),
    ('赤不通', '走不通'),
    ('独穴', '独立'),
    ('无益', '日益'),
    ('甘产', '产生'),
    ('臣然', '自然'),
    ('斤非', '方面'),
    ('西斤', '西方'),
    ('瓜解', '瓦解'),
    ('成穴', '成立'),
    ('土地改面', '土地改革'),
    ('方产阶级', '无产阶级'),
    ('君主穴宪制', '君主立宪制'),
    ('鸦爿战争', '鸦片战争'),
    ('产甘', '产生'),
    ('臣强不息', '自强不息'),
    ('臣强', '自强'),
    ('臣由', '自由'),
    ('臣尊', '自尊'),
    ('臣己', '自己'),
    ('臣足', '自主'),
    ('臣主', '自主'),
    ('臣我', '自我'),
    ('确穴', '确立'),
    ('建穴', '建立'),
    ('创穴', '创立'),
    ('变面', '变革'),
    ('改面', '改革'),
    ('斤针', '方针'),
    ('斤向', '方向'),
    ('斤法', '方法'),
    ('斤式', '方式'),
    ('双斤', '双方'),
    ('南斤', '南方'),
    ('地斤', '地方'),
    ('斤位', '方位'),
    ('无本', '日本'),
    ('无军', '日军'),
    ('抗无', '抗日'),
    ('对无', '对日'),
    ('无满华', '日满华'),
    ('比泽东', '毛泽东'),
    ('蒋介矢', '蒋介石'),
    ('请石', '请示'),
    ('瓜窑堡', '瓦窑堡'),
    ('马无事变', '马日事变'),
    ('实血', '实行'),
    ('皿的', '目的'),
    ('皿标', '目标'),
    ('题皿', '题目'),
    ('甘活', '生活'),
    ('甘命线', '生命线'),
    ('曰', '月'),
    ('赤', '走'),
    ('穴', '立'),
    ('甘', '产'),
    ('臣', '自'),
    ('斤', '方'),
    ('面', '革'),
    ('目', '矛'),
    ('瓜', '瓦'),
    ('皿', '目'),
    ('血', '行'),
    ('矢', '石'),
    ('艮', '色'),
    ('非', '面'),
    ('爿', '片'),
    ('⻓', '长'),
    ('⺠', '民'),
    ('⻢', '马'),
    ('⻔', '门'),
    ('⻛', '风'),
    ('⻘', '青'),
    ('⻰', '龙'),
    ('⻉', '贝'),
    ('⻋', '车'),
    ('⻜', '飞'),
    ('⻝', '食'),
    ('⻥', '鱼'),
    ('⻦', '鸟'),
    ('⻩', '黄'),
    ('⻬', '齐'),
    ('⻭', '齿'),
    ('⻮', '齿'),
    ('⻱', '龟'),
]

# Remove dangerous single-char replacements that would break correct words
# '无' -> '日' would break '无产阶级' -> '日产阶级'
# '无' is kept as-is since it's a valid character in many contexts
dangerous = ['无', '独', '产', '自', '方', '革', '矛', '走', '日', '瓦']
fixes = [(o,n) for (o,n) in fixes if o not in dangerous]

count = 0
for q in data:
    for old, new in fixes:
        if old in q['question']:
            q['question'] = q['question'].replace(old, new)
            count += 1
        if old in q['explanation']:
            q['explanation'] = q['explanation'].replace(old, new)
            count += 1
        q['options'] = [o.replace(old, new) for o in q['options']]

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Fixed {count} occurrences")
