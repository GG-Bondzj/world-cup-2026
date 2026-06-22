#!/usr/bin/env python3
"""Update matches.json with results for June 17-22, 2026"""
import json

with open("data/matches.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# ============================================================
# June 17 (0617) - I组 & J组 第1轮
# ============================================================

# I组: France 3-1 Senegal
for m in data["groups"]["I"]["matches"]:
    if m["day"] == 17 and m["home"].startswith("🇫🇷"):
        m["status"] = "finished"
        m["time"] = "6月17日 03:00 ✅ 已结束"
        m["score_home"] = 3
        m["score_away"] = 1
        m["events"] = "进球：姆巴佩(66'、90+7'世界波)、巴尔科拉(82'挑射) | 塞内加尔：姆巴耶(90+5')"
        m["highlight"] = True
# I组: Norway 4-1 Iraq
for m in data["groups"]["I"]["matches"]:
    if m["day"] == 17 and m["home"].startswith("🇳🇴"):
        m["status"] = "finished"
        m["time"] = "6月17日 06:00 ✅ 已结束"
        m["score_home"] = 4
        m["score_away"] = 1
        m["events"] = "进球：哈兰德(29'、43')、厄斯蒂高(76')、侯赛因乌龙 | 伊拉克：艾曼·侯赛因(39'头球)"

# J组: Argentina 3-0 Algeria
for m in data["groups"]["J"]["matches"]:
    if m["day"] == 17 and m["home"].startswith("🇦🇷"):
        m["status"] = "finished"
        m["time"] = "6月17日 09:00 ✅ 已结束"
        m["score_home"] = 3
        m["score_away"] = 0
        m["events"] = "进球：梅西帽子戏法(17'、60'、76') — 以16球并列世界杯历史射手王"
        m["highlight"] = True
# J组: Austria 3-1 Jordan
for m in data["groups"]["J"]["matches"]:
    if m["day"] == 17 and m["home"].startswith("🇦🇹"):
        m["status"] = "finished"
        m["time"] = "6月17日 12:00 ✅ 已结束"
        m["score_home"] = 3
        m["score_away"] = 1
        m["events"] = "进球：施密德(21')、鲍姆加特纳、阿瑙托维奇 | 约旦：阿尔纳迈特"

# ============================================================
# June 18 (0618) - K组 & L组 第1轮
# ============================================================

# K组: Portugal 1-1 Congo DR
for m in data["groups"]["K"]["matches"]:
    if m["day"] == 18 and m["home"].startswith("🇵🇹"):
        m["status"] = "finished"
        m["time"] = "6月18日 01:00 ✅ 已结束"
        m["score_home"] = 1
        m["score_away"] = 1
        m["events"] = "进球：内维斯(6'头球) | 刚果金：维萨(45+5'头球) | C罗打满全场0射正"
        m["highlight"] = True
# K组: Uzbekistan 1-3 Colombia
for m in data["groups"]["K"]["matches"]:
    if m["day"] == 18 and m["home"].startswith("🇺🇿"):
        m["status"] = "finished"
        m["time"] = "6月18日 10:00 ✅ 已结束"
        m["score_home"] = 1
        m["score_away"] = 3
        m["events"] = "进球：法伊祖拉耶夫(60'队史首球) | 哥伦比亚：穆尼奥斯(41')、迪亚斯(65')、坎帕斯(90+')"

# L组: England 4-2 Croatia
for m in data["groups"]["L"]["matches"]:
    if m["day"] == 18 and m["home"].startswith("🏴"):
        m["status"] = "finished"
        m["time"] = "6月18日 04:00 ✅ 已结束"
        m["score_home"] = 4
        m["score_away"] = 2
        m["events"] = "进球：凯恩(12'点球、42'头球)、贝林厄姆(47')、拉什福德(85') | 克罗地亚：巴图里纳(36'世界波)、穆萨(45+5')"
        m["highlight"] = True
# L组: Panama 0-1 Ghana
for m in data["groups"]["L"]["matches"]:
    if m["day"] == 18 and m["home"].startswith("🇵🇦"):
        m["status"] = "finished"
        m["time"] = "6月18日 07:00 ✅ 已结束"
        m["score_home"] = 0
        m["score_away"] = 1
        m["events"] = "进球：加纳队破门得分"

# ============================================================
# June 19 (0619) - A组 & B组 第2轮
# ============================================================

# A组: South Africa 1-1 Czech Republic
for m in data["groups"]["A"]["matches"]:
    if m["day"] == 19 and m["home"].startswith("🇿🇦"):
        m["status"] = "finished"
        m["time"] = "6月19日 00:00 ✅ 已结束"
        m["score_home"] = 1
        m["score_away"] = 1
        m["events"] = "进球：莫库纳(83'点球) | 捷克：萨迪莱克(6')"
# A组: Mexico 1-0 South Korea
for m in data["groups"]["A"]["matches"]:
    if m["day"] == 19 and m["home"].startswith("🇲🇽"):
        m["status"] = "finished"
        m["time"] = "6月19日 09:00 ✅ 已结束"
        m["score_home"] = 1
        m["score_away"] = 0
        m["events"] = "进球：罗莫(50'——韩国门将金承奎出击失误送礼) | 墨西哥提前出线！"

# B组: Switzerland 4-1 Bosnia
for m in data["groups"]["B"]["matches"]:
    if m["day"] == 19 and m["home"].startswith("🇨🇭"):
        m["status"] = "finished"
        m["time"] = "6月19日 03:00 ✅ 已结束"
        m["score_home"] = 4
        m["score_away"] = 1
        m["events"] = "进球：曼赞比(74'、90')、巴尔加斯(84')、扎卡(点球) | 波黑：马赫米奇(90+') | 波黑红牌：穆哈雷莫维奇(80')"
# B组: Canada 6-0 Qatar
for m in data["groups"]["B"]["matches"]:
    if m["day"] == 19 and m["home"].startswith("🇨🇦"):
        m["status"] = "finished"
        m["time"] = "6月19日 06:00 ✅ 已结束"
        m["score_home"] = 6
        m["score_away"] = 0
        m["events"] = "进球：戴维帽子戏法(29'、45+'、90+')、拉林(16')、萨利巴(64')、卡塔尔乌龙(75') | 卡塔尔2人红牌"

# ============================================================
# June 20 (0620) - C组 & D组 第2轮
# ============================================================

# C组: Scotland 0-1 Morocco
for m in data["groups"]["C"]["matches"]:
    if m["day"] == 20 and m["away"].startswith("摩洛哥"):
        m["status"] = "finished"
        m["time"] = "6月20日 03:00 ✅ 已结束"
        m["score_home"] = 0
        m["score_away"] = 1
        m["events"] = "进球：赛巴里(2'闪电破门)"
# C组: Brazil 3-0 Haiti
for m in data["groups"]["C"]["matches"]:
    if m["day"] == 20 and m["home"].startswith("🇧🇷"):
        m["status"] = "finished"
        m["time"] = "6月20日 09:00 ✅ 已结束"
        m["score_home"] = 3
        m["score_away"] = 0
        m["events"] = "进球：库尼亚(23'、36')、维尼修斯(45+3') | 海地成首支被淘汰球队"

# D组: USA 2-0 Australia
for m in data["groups"]["D"]["matches"]:
    if m["day"] == 20 and m["home"].startswith("🇺🇸"):
        m["status"] = "finished"
        m["time"] = "6月20日 03:00 ✅ 已结束"
        m["score_home"] = 2
        m["score_away"] = 0
        m["events"] = "进球：乌龙球(11')、弗里曼(43'头球) | 美国两连胜提前出线"
# D组: Paraguay 1-0 Turkey
for m in data["groups"]["D"]["matches"]:
    if m["day"] == 20 and m["home"].startswith("🇵🇾"):
        m["status"] = "finished"
        m["time"] = "6月20日 12:00 ✅ 已结束"
        m["score_home"] = 1
        m["score_away"] = 0
        m["events"] = "进球：加拉尔萨(2'闪击)"

# ============================================================
# June 21 (0621) - E组 & F组 第2轮
# ============================================================

# E组: Germany 2-1 Ivory Coast
for m in data["groups"]["E"]["matches"]:
    if m["day"] == 21 and m["home"].startswith("🇩🇪"):
        m["status"] = "finished"
        m["time"] = "6月21日 04:00 ✅ 已结束"
        m["score_home"] = 2
        m["score_away"] = 1
        m["events"] = "进球：温达夫(68'、绝杀) | 科特迪瓦：凯西(30') | 德国提前一轮锁定小组第一出线"
# E组: Ecuador 0-0 Curacao
for m in data["groups"]["E"]["matches"]:
    if m["day"] == 21 and m["home"].startswith("🇪🇨"):
        m["status"] = "finished"
        m["time"] = "6月21日 08:00 ✅ 已结束"
        m["score_home"] = 0
        m["score_away"] = 0
        m["events"] = "库拉索门将鲁姆15次扑救创本届纪录 | 马宁执法出示6张黄牌"

# F组: Netherlands 5-1 Sweden
for m in data["groups"]["F"]["matches"]:
    if m["day"] == 21 and m["home"].startswith("🇳🇱"):
        m["status"] = "finished"
        m["time"] = "6月21日 01:00 ✅ 已结束"
        m["score_home"] = 5
        m["score_away"] = 1
        m["events"] = "进球：布罗比(5'、17')、加克波(47'、54')、萨默维尔 | 瑞典：埃兰加"
# F组: Tunisia 0-4 Japan
for m in data["groups"]["F"]["matches"]:
    if m["day"] == 21 and m["home"].startswith("🇹🇳"):
        m["status"] = "finished"
        m["time"] = "6月21日 12:00 ✅ 已结束"
        m["score_home"] = 0
        m["score_away"] = 4
        m["events"] = "进球：镰田大地(4')、上田绮世(31')、中村敬斗、久保健英 | 日本队史首次单场4球"

# ============================================================
# June 22 (0622) - G组 & H组 第2轮
# ============================================================

# G组: Belgium 0-0 Iran
for m in data["groups"]["G"]["matches"]:
    if m["day"] == 22 and m["home"].startswith("🇧🇪"):
        m["status"] = "finished"
        m["time"] = "6月22日 03:00 ✅ 已结束"
        m["score_home"] = 0
        m["score_away"] = 0
        m["events"] = "伊朗任意球破门VAR判无效 | 比利时恩戈伊红牌 | 比利时门将库尔图瓦屡献神扑"
# G组: New Zealand 1-3 Egypt
for m in data["groups"]["G"]["matches"]:
    if m["day"] == 22 and m["home"].startswith("🇳🇿"):
        m["status"] = "finished"
        m["time"] = "6月22日 09:00 ✅ 已结束"
        m["score_home"] = 1
        m["score_away"] = 3
        m["events"] = "进球：苏尔曼(上半场) | 埃及：齐科头球、萨拉赫推射、特雷泽盖(萨拉赫助攻) — 埃及92年队史世界杯首胜！"

# H组: Spain 4-0 Saudi Arabia
for m in data["groups"]["H"]["matches"]:
    if m["day"] == 22 and m["home"].startswith("🇪🇸"):
        m["status"] = "finished"
        m["time"] = "6月22日 00:00 ✅ 已结束"
        m["score_home"] = 4
        m["score_away"] = 0
        m["events"] = "进球：亚马尔(11'世界杯首球)、奥亚萨瓦尔(21'、23')、坦巴蒂乌龙(49') | 西班牙前25分钟3球创纪录"
# H组: Uruguay 2-2 Cape Verde
for m in data["groups"]["H"]["matches"]:
    if m["day"] == 22 and m["home"].startswith("🇺🇾"):
        m["status"] = "finished"
        m["time"] = "6月22日 06:00 ✅ 已结束"
        m["score_home"] = 2
        m["score_away"] = 2
        m["events"] = "进球：阿劳霍(44')、卡诺比奥(45+') | 佛得角：皮纳(21'任意球队史首球)、瓦雷拉(61') | 佛得角两连平创奇迹！"


# ============================================================
# Now update the dates section
# ============================================================

date_updates = {
    "0617": {
        "matches": [
            {"status": "finished", "time": "03:00 ✅ 已结束", "home": "🇫🇷 法国", "away": "塞内加尔 🇸🇳", "highlight": True, "tag": "🔥 焦点战", "group": "I组", "score_home": 3, "score_away": 1},
            {"status": "finished", "time": "06:00 ✅ 已结束", "home": "🇳🇴 挪威", "away": "伊拉克 🇮🇶", "group": "I组", "score_home": 4, "score_away": 1},
            {"status": "finished", "time": "09:00 ✅ 已结束", "home": "🇦🇷 阿根廷", "away": "阿尔及利亚 🇩🇿", "tag": "★ 梅西首秀", "group": "J组", "score_home": 3, "score_away": 0},
            {"status": "finished", "time": "12:00 ✅ 已结束", "home": "🇦🇹 奥地利", "away": "约旦 🇯🇴", "group": "J组", "score_home": 3, "score_away": 1},
        ]
    },
    "0618": {
        "matches": [
            {"status": "finished", "time": "01:00 ✅ 已结束", "home": "🇵🇹 葡萄牙", "away": "刚果金 🇨🇩", "tag": "★ C罗最后一届", "group": "K组", "score_home": 1, "score_away": 1},
            {"status": "finished", "time": "04:00 ✅ 已结束", "home": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 英格兰", "away": "克罗地亚 🇭🇷", "group": "L组", "score_home": 4, "score_away": 2},
            {"status": "finished", "time": "07:00 ✅ 已结束", "home": "🇵🇦 巴拿马", "away": "加纳 🇬🇭", "group": "L组", "score_home": 0, "score_away": 1},
            {"status": "finished", "time": "10:00 ✅ 已结束", "home": "🇺🇿 乌兹别克斯坦", "away": "哥伦比亚 🇨🇴", "group": "K组", "score_home": 1, "score_away": 3},
        ]
    },
    "0619": {
        "matches": [
            {"status": "finished", "time": "00:00 ✅ 已结束", "home": "🇿🇦 南非", "away": "捷克 🇨🇿", "group": "A组", "score_home": 1, "score_away": 1},
            {"status": "finished", "time": "03:00 ✅ 已结束", "home": "🇨🇭 瑞士", "away": "波黑 🇧🇦", "group": "B组", "score_home": 4, "score_away": 1},
            {"status": "finished", "time": "06:00 ✅ 已结束", "home": "🇨🇦 加拿大", "away": "卡塔尔 🇶🇦", "group": "B组", "score_home": 6, "score_away": 0},
            {"status": "finished", "time": "09:00 ✅ 已结束", "home": "🇲🇽 墨西哥", "away": "韩国 🇰🇷", "group": "A组", "score_home": 1, "score_away": 0},
        ]
    },
    "0620": {
        "matches": [
            {"status": "finished", "time": "03:00 ✅ 已结束", "home": "🇺🇸 美国", "away": "澳大利亚 🇦🇺", "group": "D组", "score_home": 2, "score_away": 0},
            {"status": "finished", "time": "03:00 ✅ 已结束", "home": "🏴󠁧󠁢󠁳󠁣󠁴󠁿 苏格兰", "away": "摩洛哥 🇲🇦", "group": "C组", "score_home": 0, "score_away": 1},
            {"status": "finished", "time": "09:00 ✅ 已结束", "home": "🇧🇷 巴西", "away": "海地 🇭🇹", "group": "C组", "score_home": 3, "score_away": 0},
            {"status": "finished", "time": "12:00 ✅ 已结束", "home": "🇵🇾 巴拉圭", "away": "土耳其 🇹🇷", "group": "D组", "score_home": 1, "score_away": 0},
        ]
    },
    "0621": {
        "matches": [
            {"status": "finished", "time": "01:00 ✅ 已结束", "home": "🇳🇱 荷兰", "away": "瑞典 🇸🇪", "group": "F组", "score_home": 5, "score_away": 1},
            {"status": "finished", "time": "04:00 ✅ 已结束", "home": "🇩🇪 德国", "away": "科特迪瓦 🇨🇮", "group": "E组", "score_home": 2, "score_away": 1},
            {"status": "finished", "time": "08:00 ✅ 已结束", "home": "🇪🇨 厄瓜多尔", "away": "库拉索 🇨🇼", "group": "E组", "score_home": 0, "score_away": 0},
            {"status": "finished", "time": "12:00 ✅ 已结束", "home": "🇹🇳 突尼斯", "away": "日本 🇯🇵", "group": "F组", "score_home": 0, "score_away": 4},
        ]
    },
    "0622": {
        "matches": [
            {"status": "finished", "time": "00:00 ✅ 已结束", "home": "🇪🇸 西班牙", "away": "沙特 🇸🇦", "group": "H组", "score_home": 4, "score_away": 0},
            {"status": "finished", "time": "03:00 ✅ 已结束", "home": "🇧🇪 比利时", "away": "伊朗 🇮🇷", "group": "G组", "score_home": 0, "score_away": 0},
            {"status": "finished", "time": "06:00 ✅ 已结束", "home": "🇺🇾 乌拉圭", "away": "佛得角 🇨🇻", "group": "H组", "score_home": 2, "score_away": 2},
            {"status": "finished", "time": "09:00 ✅ 已结束", "home": "🇳🇿 新西兰", "away": "埃及 🇪🇬", "group": "G组", "score_home": 1, "score_away": 3},
        ]
    },
}

for date_key, date_data in date_updates.items():
    data["dates"][date_key] = date_data

# Write back
with open("data/matches.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ matches.json updated successfully!")
print(f"Updated dates: {', '.join(date_updates.keys())}")
print(f"Total matches updated: {sum(len(d['matches']) for d in date_updates.values())}")
