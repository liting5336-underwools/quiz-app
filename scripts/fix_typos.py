import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
json_path = os.path.join(project_root, 'src', 'data', 'questions.json')

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Fix mappings - longer strings first to avoid partial replacements
fixes = [
    # Multi-character fixes (must come before single-char)
    ('面命', '革命'),
    ('目盾', '矛盾'),
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
