#!/usr/bin/env python3
"""手动更新比赛结果到 matches.json"""
import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'matches.json')

# 已确认的比赛结果 (截至2026-06-15 08:30 北京时间)
RESULTS = [
    # ===== A组 =====
    # 6月12日 03:00 墨西哥2-0南非（揭幕战）- 已在JSON中
    # 6月12日 10:00 韩国2-1捷克 - 已在JSON中

    # ===== B组 =====
    {
        "group": "B", "day": 13, "home_key": "加拿大", "away_key": "波黑",
        "score_home": 1, "score_away": 1,
        "events": "进球：拉林(76'替补扳平) | 波黑：卢基奇(34')"
    },
    {
        "group": "B", "day": 14, "home_key": "卡塔尔", "away_key": "瑞士",
        "score_home": 1, "score_away": 1,
        "events": "进球：扈希(90+2'绝平) | 瑞士：恩博洛点球"
    },

    # ===== C组 =====
    {
        "group": "C", "day": 14, "home_key": "巴西", "away_key": "摩洛哥",
        "score_home": 1, "score_away": 1,
        "events": "进球：维尼修斯(32') | 摩洛哥：塞巴里(21')"
    },
    {
        "group": "C", "day": 14, "home_key": "海地", "away_key": "苏格兰",
        "score_home": 0, "score_away": 1,
        "events": "进球：苏格兰 麦金(上半场)"
    },

    # ===== D组 =====
    {
        "group": "D", "day": 13, "home_key": "美国", "away_key": "巴拉",
        "score_home": 4, "score_away": 1,
        "events": "进球：巴洛贡×2、乌龙球、雷纳 | 巴拉圭1球"
    },
    {
        "group": "D", "day": 14, "home_key": "澳大利亚", "away_key": "土耳其",
        "score_home": 2, "score_away": 0,
        "events": "进球：伊兰昆达(上半场)、梅特卡夫(下半场)"
    },

    # ===== E组 =====
    {
        "group": "E", "day": 15, "home_key": "德国", "away_key": "库拉索",
        "score_home": 7, "score_away": 1,
        "events": "进球：恩梅查(6'、45+')点球哈弗茨、施洛特贝克(38')、穆西亚拉(47')、布朗(68')、温达夫(78')、哈弗茨(88') | 库拉索：科梅嫩西亚(21'队史首球)"
    },

    # ===== F组 =====
    {
        "group": "F", "day": 15, "home_key": "荷兰", "away_key": "日本",
        "score_home": 2, "score_away": 2,
        "events": "进球：范戴克(51')、萨默维尔(64') | 日本：中村敬斗(57')、小川航基(89'折射)"
    },
]

def update_match(data, group, day, home_key, away_key, score_home, score_away, events):
    """更新指定比赛的结果"""
    matches = data['groups'][group]['matches']
    for m in matches:
        if m['day'] == day and home_key in m['home'] and away_key in m['away']:
            m['status'] = 'finished'
            m['score_home'] = score_home
            m['score_away'] = score_away
            m['events'] = events
            # 更新时间显示
            kickoff = m.get('kickoff', '')
            m['time'] = f"6月{day}日 {kickoff} ✅ 已结束"
            print(f"  ✅ 更新: {m['home']} {score_home}-{score_away} {m['away']}")
            return True
        # 也匹配 away 包含 home_key 的情况（客场在前）
        if m['day'] == day and home_key in m['away'] and away_key in m['home']:
            m['status'] = 'finished'
            m['score_home'] = score_away
            m['score_away'] = score_home
            m['events'] = events
            kickoff = m.get('kickoff', '')
            m['time'] = f"6月{day}日 {kickoff} ✅ 已结束"
            print(f"  ✅ 更新(交换): {m['home']} {score_away}-{score_home} {m['away']}")
            return True
    print(f"  ⚠️  未找到: 第{group}组 {day}日 {home_key} vs {away_key}")
    return False

with open(DATA_FILE, encoding='utf-8') as f:
    data = json.load(f)

print("开始更新比赛结果...")
for r in RESULTS:
    update_match(data, r['group'], r['day'], r['home_key'], r['away_key'],
                 r['score_home'], r['score_away'], r['events'])

with open(DATA_FILE, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n✅ matches.json 已更新!")

# 统计已完成比赛数量
finished = sum(
    1 for g in data['groups'].values()
    for m in g['matches']
    if m['status'] == 'finished'
)
print(f"📊 已完成比赛: {finished} 场")
