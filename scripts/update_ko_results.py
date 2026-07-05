#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update 2026 World Cup matches.json with 1/16 (7/3-7/4) and 1/8 (7/5 first 2 matches) results."""
import json

with open('data/matches.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

# === Update 1/16 final 6 matches (7/3 and 7/4) ===
# Slot 11 (idx 10): Spain 3-0 Austria
d['knockout']['round16']['matches'][10] = {
    'time': '7月3日 03:00 ✅ 已结束',
    'home': '🇪🇸 西班牙',
    'away': '奥地利 🇦🇹',
    'score_home': 3,
    'score_away': 0,
    'status': 'finished',
    'events': "进球：奥亚萨瓦尔(36'、89'库库雷利亚助攻梅开二度)、波罗(66'头球巴埃纳助攻) | 西班牙轻松晋级 | 库库雷利亚2次助攻",
    'venue': '📍 1/16决赛 · 洛杉矶SoFi体育场',
    'tag': '★ H组第1 vs J组第2',
    'group': 'H组'
}

# Slot 12 (idx 11): Portugal 2-1 Croatia
d['knockout']['round16']['matches'][11] = {
    'time': '7月3日 07:00 ✅ 已结束',
    'home': '🇵🇹 葡萄牙',
    'away': '克罗地亚 🇭🇷',
    'score_home': 2,
    'score_away': 1,
    'status': 'finished',
    'events': "进球：葡萄牙 拉莫斯(94'绝杀) | 克罗地亚：佩特科维奇下半场扳平被VAR改判越位无效、加时绝平进球被吹 | C罗下半场被换下 | 葡萄牙晋级16强将战瑞士",
    'venue': '📍 1/16决赛 · 多伦多BMO体育场',
    'highlight': True,
    'tag': '★ K组第2 vs L组第2',
    'group': 'K组'
}

# Slot 13 (idx 12): Switzerland 2-0 Algeria
d['knockout']['round16']['matches'][12] = {
    'time': '7月3日 11:00 ✅ 已结束',
    'home': '🇨🇭 瑞士',
    'away': '阿尔及利亚 🇩🇿',
    'score_home': 2,
    'score_away': 0,
    'status': 'finished',
    'events': "进球：恩博洛(上半场)、恩多耶(下半场开场凌空抽射) | 瑞士连续4届闯入16强 | 阿尔及利亚主帅佩特科维奇曾执教瑞士7年",
    'venue': '📍 1/16决赛 · 温哥华BC Place',
    'tag': '★ B组第1 vs J组第3',
    'group': 'B组'
}

# Slot 14 (idx 13): Australia 1-1(2-4pens) Egypt
d['knockout']['round16']['matches'][13] = {
    'time': '7月4日 02:00 ✅ 已结束',
    'home': '🇦🇺 澳大利亚',
    'away': '埃及 🇪🇬',
    'score_home': 1,
    'score_away': 1,
    'status': 'finished',
    'events': "进球：埃及 阿舒尔(14'哈菲兹助攻头球) | 澳大利亚：哈尼(下半场乌龙) | 点球大战：苏塔、赫林顿失点 埃及4-2晋级 | 埃及门将单场扑出2粒点球",
    'venue': '📍 1/16决赛 · 达拉斯AT&T体育场',
    'tag': '★ D组第2 vs G组第2',
    'group': 'D组'
}

# Slot 15 (idx 14): Argentina 3-2 Cape Verde (after extra time)
d['knockout']['round16']['matches'][14] = {
    'time': '7月4日 06:00 ✅ 已结束',
    'home': '🇦🇷 阿根廷',
    'away': '佛得角 🇨🇻',
    'score_home': 3,
    'score_away': 2,
    'status': 'finished',
    'events': "进球：阿根廷 阿尔马达(45+3'加时)、梅西(加时)、劳塔罗(加时) | 佛得角门将罗查全场神扑封神，梅西失点 | 卫冕冠军加时苦战晋级",
    'venue': '📍 1/16决赛 · 迈阿密Hard Rock体育场',
    'highlight': True,
    'tag': '★ J组第1 vs H组第2',
    'group': 'J组'
}

# Slot 16 (idx 15): Colombia 1-0 Ghana
d['knockout']['round16']['matches'][15] = {
    'time': '7月4日 09:30 ✅ 已结束',
    'home': '🇨🇴 哥伦比亚',
    'away': '加纳 🇬🇭',
    'score_home': 1,
    'score_away': 0,
    'status': 'finished',
    'events': "进球：迪亚斯(下半场破门) | 哥伦比亚稳健晋级16强 | 1/8决赛将对阵瑞士",
    'venue': '📍 1/16决赛 · 堪萨斯城箭头体育场',
    'tag': '★ K组第1 vs D组第3',
    'group': 'K组'
}

# === Update 1/8 final: 7/5 first 2 matches ===
# 1/8 #1 (idx 0): Morocco 3-0 Canada
d['knockout']['round8']['matches'][0] = {
    'time': '7月5日 01:00 ✅ 已结束',
    'home': '🇨🇦 加拿大',
    'away': '摩洛哥 🇲🇦',
    'score_home': 0,
    'score_away': 3,
    'status': 'finished',
    'events': "进球：乌纳希(50'阿什拉夫助攻、82'迪亚斯助攻梅开二度)、拉希米(90+8'迪亚斯反击助攻) | 摩洛哥本届首支8强球队！连续两届闯入8强 | 加拿大成美加墨首支出局球队",
    'venue': '📍 1/8决赛 · 西雅图Lumen Field',
    'tag': '★ 加拿大队史首进16强 vs 非洲黑马摩洛哥'
}

# 1/8 #2 (idx 1): France 1-0 Paraguay
d['knockout']['round8']['matches'][1] = {
    'time': '7月5日 05:00 ✅ 已结束',
    'home': '🇵🇾 巴拉圭',
    'away': '法国 🇫🇷',
    'score_home': 0,
    'score_away': 1,
    'status': 'finished',
    'events': "进球：姆巴佩(70'点球，杜埃造点) | 双方一度发生冲突 | 法国点球绝杀晋级8强，下轮对阵摩洛哥",
    'venue': '📍 1/8决赛 · 达拉斯AT&T体育场',
    'tag': '★ 巴拉圭黑马 vs 高卢雄鸡 — 姆巴佩继续冲击纪录'
}

# === Update 1/8 placeholders ===
# 1/8 #5 (idx 4, 7/7 03:00): winner of round16[10] vs round16[11] = Portugal vs Switzerland
d['knockout']['round8']['matches'][4] = {
    'time': '7月7日 03:00',
    'home': '🇵🇹 葡萄牙',
    'away': '🇨🇭 瑞士',
    'venue': '📍 1/8决赛 · 多伦多BMO体育场',
    'tag': '★ K组第2 葡萄牙 vs B组第1 瑞士',
    'status': 'pending'
}

# 1/8 #7 (idx 6, 7/8 00:00): winner of round16[12] vs round16[13] = Switzerland vs Egypt
d['knockout']['round8']['matches'][6] = {
    'time': '7月8日 00:00',
    'home': '🇨🇭 瑞士',
    'away': '埃及 🇪🇬',
    'venue': '📍 1/8决赛 · 温哥华BC Place',
    'tag': '★ 瑞士 vs 埃及',
    'status': 'pending'
}

# 1/8 #8 (idx 7, 7/8 04:00): winner of round16[14] vs round16[15] = Argentina vs Colombia
d['knockout']['round8']['matches'][7] = {
    'time': '7月8日 04:00',
    'home': '🇦🇷 阿根廷',
    'away': '哥伦比亚 🇨🇴',
    'venue': '📍 1/8决赛 · 迈阿密Hard Rock体育场',
    'highlight': True,
    'tag': '★ 南美德比 — 梅西 vs J罗',
    'status': 'pending'
}

# === Add 0703, 0704, 0705 to dates section ===
d['dates']['0703'] = {
    'matches': [
        {
            'status': 'finished',
            'time': '03:00 ✅ 已结束',
            'home': '🇪🇸 西班牙',
            'away': '奥地利 🇦🇹',
            'tag': '🔥 1/16决赛',
            'group': '1/16决赛',
            'score_home': 3,
            'score_away': 0
        },
        {
            'status': 'finished',
            'time': '07:00 ✅ 已结束',
            'home': '🇵🇹 葡萄牙',
            'away': '克罗地亚 🇭🇷',
            'tag': '🔥 1/16决赛',
            'group': '1/16决赛',
            'score_home': 2,
            'score_away': 1
        },
        {
            'status': 'finished',
            'time': '11:00 ✅ 已结束',
            'home': '🇨🇭 瑞士',
            'away': '阿尔及利亚 🇩🇿',
            'tag': '🔥 1/16决赛',
            'group': '1/16决赛',
            'score_home': 2,
            'score_away': 0
        }
    ]
}

d['dates']['0704'] = {
    'matches': [
        {
            'status': 'finished',
            'time': '02:00 ✅ 已结束',
            'home': '🇦🇺 澳大利亚',
            'away': '埃及 🇪🇬',
            'tag': '🔥 1/16决赛',
            'group': '1/16决赛',
            'score_home': 1,
            'score_away': 1
        },
        {
            'status': 'finished',
            'time': '06:00 ✅ 已结束',
            'home': '🇦🇷 阿根廷',
            'away': '佛得角 🇨🇻',
            'highlight': True,
            'tag': '🔥 1/16决赛',
            'group': '1/16决赛',
            'score_home': 3,
            'score_away': 2
        },
        {
            'status': 'finished',
            'time': '09:30 ✅ 已结束',
            'home': '🇨🇴 哥伦比亚',
            'away': '加纳 🇬🇭',
            'tag': '🔥 1/16决赛',
            'group': '1/16决赛',
            'score_home': 1,
            'score_away': 0
        }
    ]
}

d['dates']['0705'] = {
    'matches': [
        {
            'status': 'finished',
            'time': '01:00 ✅ 已结束',
            'home': '🇨🇦 加拿大',
            'away': '摩洛哥 🇲🇦',
            'highlight': True,
            'tag': '🔥 1/8决赛',
            'group': '1/8决赛',
            'score_home': 0,
            'score_away': 3
        },
        {
            'status': 'finished',
            'time': '05:00 ✅ 已结束',
            'home': '🇵🇾 巴拉圭',
            'away': '法国 🇫🇷',
            'highlight': True,
            'tag': '🔥 1/8决赛',
            'group': '1/8决赛',
            'score_home': 0,
            'score_away': 1
        }
    ]
}

# Save
with open('data/matches.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print("✅ matches.json updated successfully")
print(f"  - round16: 6 matches updated (slots 11-16)")
print(f"  - round8: 5 matches updated (slots 1, 2, 5, 7, 8)")
print(f"  - dates: 0703, 0704, 0705 added")
