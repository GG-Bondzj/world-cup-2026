# -*- coding: utf-8 -*-
"""
尝试从公开 API 获取比赛比分，更新 matches.json。
如果找不到数据则不做任何修改。
运行：python scripts/update_scores.py
"""
import json, re, os, sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

PROJECT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent
DATA_FILE = PROJECT_DIR / 'data' / 'matches.json'

# 北京时间
CST = timezone(timedelta(hours=8))

def load_data():
    with open(str(DATA_FILE), 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(str(DATA_FILE), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def clean_team(name):
    """清理队名"""
    flags = ['🇲🇽','🇿🇦','🇰🇷','🇨🇿','🇨🇦','🇧🇦','🇶🇦','🇨🇭',
             '🇧🇷','🇲🇦','🇭🇹','🇺🇸','🇵🇾','🇦🇺','🇹🇷','🇩🇪',
             '🇨🇮','🇪🇨','🇨🇼','🇳🇱','🇯🇵','🇹🇳','🇸🇪','🇧🇪',
             '🇪🇬','🇮🇷','🇳🇿','🇪🇸','🇸🇦','🇺🇾','🇨🇻','🇫🇷',
             '🇸🇳','🇳🇴','🇮🇶','🇦🇷','🇩🇿','🇦🇹','🇯🇴','🇵🇹',
             '🇨🇩','🇺🇿','🇨🇴','🇭🇷','🇵🇦','🇬🇭','🏴']
    for f in flags:
        name = name.replace(f, '')
    return name.strip()

def try_fetch_from_sofascore():
    """尝试从 SofaScore API 获取比分"""
    try:
        import requests
        # 尝试获取世界杯相关赛事
        url = "https://api.sofascore.com/api/v1/sport/football/events/live"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            matches = []
            for event in data.get('events', []):
                tournament = event.get('tournament', {}).get('name', '')
                if 'World Cup' in tournament or '世界杯' in tournament:
                    home = event.get('homeTeam', {}).get('name', '')
                    away = event.get('awayTeam', {}).get('name', '')
                    home_score = event.get('homeScore', {}).get('current', 0)
                    away_score = event.get('awayScore', {}).get('current', 0)
                    status = event.get('status', {}).get('type', '')
                    matches.append({
                        'home': home, 'away': away,
                        'score_home': home_score, 'score_away': away_score,
                        'status': 'finished' if status == 'finished' else 'live'
                    })
            if matches:
                print(f"  SofaScore: 找到 {len(matches)} 场世界杯比赛")
                return matches
    except Exception as e:
        print(f"  SofaScore: 获取失败 ({e})")
    return []

def try_fetch_from_espn():
    """尝试从 ESPN API 获取比分"""
    try:
        import requests
        url = "https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/scoreboard"
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            matches = []
            for event in data.get('events', []):
                competitions = event.get('competitions', [])
                for comp in competitions:
                    for competitor in comp.get('competitors', []):
                        pass
                    home = comp['competitors'][0]['team']['displayName'] if len(comp.get('competitors',[])) > 0 else ''
                    away = comp['competitors'][1]['team']['displayName'] if len(comp.get('competitors',[])) > 1 else ''
                    home_score = int(comp['competitors'][0].get('score','0')) if len(comp.get('competitors',[])) > 0 else 0
                    away_score = int(comp['competitors'][1].get('score','0')) if len(comp.get('competitors',[])) > 1 else 0
                    is_finished = comp.get('status',{}).get('type',{}).get('completed', False)
                    matches.append({
                        'home': home, 'away': away,
                        'score_home': home_score, 'score_away': away_score,
                        'status': 'finished' if is_finished else 'pending'
                    })
            if matches:
                print(f"  ESPN: 找到 {len(matches)} 场比赛")
                return matches
    except Exception as e:
        print(f"  ESPN: 获取失败 ({e})")
    return []

def update_matches(data, fetched_matches):
    """用获取的比分更新 matches.json"""
    updated = 0
    
    # 尝试匹配球队名
    for group_name, group_data in data['groups'].items():
        for m in group_data['matches']:
            if m.get('status') == 'finished':
                continue  # 已有比分，跳过
            
            home = clean_team(m.get('home', ''))
            away = clean_team(m.get('away', ''))
            
            for fm in fetched_matches:
                f_home = fm.get('home', '').lower()
                f_away = fm.get('away', '').lower()
                
                # 模糊匹配
                if (home.lower() in f_home or f_home in home.lower()) and \
                   (away.lower() in f_away or f_away in away.lower()):
                    m['score_home'] = fm.get('score_home', 0)
                    m['score_away'] = fm.get('score_away', 0)
                    m['status'] = 'finished'
                    m['time'] = m.get('time', '') + ' ✅ 已结束'
                    updated += 1
                    print(f"  ✅ 更新: {home} {m['score_home']}-{m['score_away']} {away}")
    
    return updated

def main():
    print("🔍 尝试获取比分数据...\n")
    
    data = load_data()
    
    # 尝试多个来源
    sources = [try_fetch_from_sofascore, try_fetch_from_espn]
    all_fetched = []
    
    for source_func in sources:
        try:
            fetched = source_func()
            if fetched:
                all_fetched.extend(fetched)
                break  # 成功获取就停止
        except Exception as e:
            print(f"  错误: {e}")
    
    if all_fetched:
        updated = update_matches(data, all_fetched)
        if updated > 0:
            save_data(data)
            print(f"\n✅ 更新了 {updated} 场比赛结果")
        else:
            print("\n⚠️  没有匹配到需要更新的比赛")
    else:
        print("\n⚠️  未获取到比分数据（API 可能不可用或今天没有比赛）")
        print("   将使用现有数据生成页面")

if __name__ == '__main__':
    main()
