#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从维基百科自动获取世界杯比赛结果，更新 matches.json
依赖：仅使用标准库 + 环境变量中的大模型 API Key
"""
import os
import sys
import json
import datetime
import re
import urllib.request
import urllib.error

API_KEY = os.environ.get("CODING_API_KEY", "")
API_URL = "https://zhenze-huhehaote.cmecloud.cn/api/coding/v1/chat/completions"
MATCHES_FILE = "data/matches.json"

WIKI_API = "https://zh.wikipedia.org/w/api.php"

UA = "WorldCup2026-AutoUpdater/1.0 (https://github.com/GG-Bondzj/world-cup-2026)"


def call_ai(prompt, max_tokens=4000):
    if not API_KEY:
        return None
    payload = {
        "model": "cm-code-latest",
        "messages": [
            {"role": "system", "content": "你是2026世界杯数据整理助手。从维基百科文本中精确提取比赛结果。如果某场比赛在文本中没有明确结果，跳过它不要编造。"},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.1
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API_URL, data=data,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"[WARN] AI失败: {e}", file=sys.stderr)
        return None


def fetch_wiki_text(title, lang="zh"):
    """从维基百科 API 拉取纯文本"""
    base = f"https://{lang}.wikipedia.org/w/api.php"
    u = f"{base}?action=query&prop=extracts&explaintext&format=json&titles={urllib.parse.quote(title)}&redirects=1"
    req = urllib.request.Request(u, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    pages = data.get("query", {}).get("pages", {})
    for pid, pdata in pages.items():
        return pdata.get("extract", "") or ""
    return ""


def load_matches():
    with open(MATCHES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_matches(data):
    with open(MATCHES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def find_pending_matches(matches_data, target_date_str):
    """查找指定日期之前所有未结束的比赛"""
    pending = []
    target = datetime.datetime.strptime(target_date_str, "%Y-%m-%d").date()

    def check_list(match_list):
        for m in match_list:
            if not isinstance(m, dict):
                continue
            if m.get("status") in ("pending", "scheduled", "未开始", "等待开赛"):
                m_date = datetime.date(2026, m.get("month", 6), m.get("day", 1))
                if m_date <= target:
                    pending.append(m)

    groups = matches_data.get("groups", {})
    for g, gdata in groups.items():
        check_list(gdata.get("matches", []))

    ko = matches_data.get("knockout", {})
    for stage in ["round16", "round8", "quarter", "semi", "third", "final"]:
        stage_data = ko.get(stage, {})
        if isinstance(stage_data, list):
            check_list(stage_data)
        elif isinstance(stage_data, dict):
            if "matches" in stage_data and isinstance(stage_data["matches"], list):
                check_list(stage_data["matches"])
            for k, v in stage_data.items():
                if isinstance(v, list):
                    check_list(v)
    return pending


def build_extraction_prompt(pending, wiki_text, today_str):
    """让大模型从维基百科文本中提取结果"""
    items = []
    for m in pending:
        items.append({
            "id": f"{m.get('group', m.get('stage', '?'))}-{m.get('month', 6):02d}{m.get('day', 1):02d}-{m.get('kickoff', '')}",
            "home": m.get("home", ""),
            "away": m.get("away", ""),
            "date": f"2026-{m.get('month', 6):02d}-{m.get('day', 1):02d}",
        })
    return f"""今天是 {today_str}。请从下方【维基百科文本】中，找出【待查询比赛列表】每场的最终比分和进球事件。

【待查询比赛列表】
{json.dumps(items, ensure_ascii=False, indent=2)}

【维基百科文本】（只关注2026年6月12日之后的比赛）
{wiki_text[:18000]}

**严格规则**：
1. 只填写在维基百科文本中**明确出现**比分的比赛
2. 如果维基百科文本中没有某场比赛的结果，**不要编造**，score_home和score_away都填null
3. events字段简述进球者+时间，如"基尼奥尔斯(9')、希门尼斯(67')"
4. 淘汰赛如有点球大战，penalties填"X-Y"，并把extra_time设为true

只输出**严格JSON数组**，结构：
[
  {{
    "id": "对应上面id",
    "score_home": 整数或null,
    "score_away": 整数或null,
    "events": "字符串或'未知'",
    "extra_time": true/false,
    "penalties": "字符串或null"
  }}
]

只输出JSON数组，不要任何解释、注释或markdown标记。"""


def parse_ai_response(text):
    if not text:
        return []
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except Exception as e:
        print(f"[WARN] JSON解析失败: {e}", file=sys.stderr)
        print(f"[WARN] 原文前500字符: {text[:500]}", file=sys.stderr)
        return []


def apply_updates(matches_data, updates, pending_matches):
    if not updates:
        return 0
    by_id = {u.get("id"): u for u in updates if u.get("id")}
    count = 0
    for m in pending_matches:
        mid = f"{m.get('group', m.get('stage', '?'))}-{m.get('month', 6):02d}{m.get('day', 1):02d}-{m.get('kickoff', '')}"
        u = by_id.get(mid)
        if not u:
            continue
        sh = u.get("score_home")
        sa = u.get("score_away")
        if sh is None or sa is None:
            continue
        m["score_home"] = int(sh)
        m["score_away"] = int(sa)
        if u.get("events") and u["events"] != "未知":
            m["events"] = u["events"]
        elif "events" not in m or not m.get("events"):
            m["events"] = f"最终比分 {sh}-{sa}"
        m["status"] = "finished"
        time_label = m.get("time", "")
        if "已结束" not in time_label:
            m["time"] = f"{time_label} ✅ 已结束".strip()
        if u.get("penalties"):
            m["penalties"] = u["penalties"]
            m["went_extra"] = True
        if u.get("extra_time"):
            m["went_extra"] = True
        count += 1
        print(f"  ✓ {m.get('home')} {sh}-{sa} {m.get('away')}")
    return count


def main():
    if not API_KEY:
        print("[ERROR] 未设置 CODING_API_KEY", file=sys.stderr)
        sys.exit(1)

    today = datetime.date.today()
    today_str = today.strftime("%Y-%m-%d")
    print(f"=== 维基百科AI更新 [{today_str}] ===")

    # 1) 加载本地数据
    data = load_matches()
    pending = find_pending_matches(data, today_str)
    print(f"待更新比赛: {len(pending)} 场")

    if not pending:
        print("无待更新比赛，退出")
        return

    # 2) 抓取维基百科
    print("抓取维基百科...")
    wiki_text = ""
    for title in [
        "2026年国际足联世界杯",
        "2026年国际足联世界杯小组赛",
        "2026年国际足联世界杯淘汰赛",
    ]:
        try:
            text = fetch_wiki_text(title, "zh")
            if text:
                wiki_text += f"\n\n=== {title} ===\n{text}"
                print(f"  ✓ {title}: {len(text)} 字符")
        except Exception as e:
            print(f"  ✗ {title}: {e}", file=sys.stderr)

    if not wiki_text:
        print("[ERROR] 维基百科抓取全部失败")
        sys.exit(1)

    # 3) 让大模型从维基百科文本提取
    prompt = build_extraction_prompt(pending, wiki_text, today_str)
    print(f"调用大模型提取结果（prompt {len(prompt)} 字符）...")
    response = call_ai(prompt, max_tokens=8000)
    if not response:
        print("[ERROR] 大模型无响应")
        sys.exit(1)

    updates = parse_ai_response(response)
    known = sum(1 for u in updates if u.get("score_home") is not None)
    print(f"大模型提取到 {known}/{len(updates)} 场结果")

    # 4) 写回
    applied = apply_updates(data, updates, pending)
    print(f"成功更新 {applied} 场")

    if applied > 0:
        save_matches(data)
        print(f"已写入 {MATCHES_FILE}")
    else:
        print("无有效更新")


if __name__ == "__main__":
    main()
