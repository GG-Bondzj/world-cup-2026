# -*- coding: utf-8 -*-
"""
从 matches.json 生成所有 HTML 页面。
运行：python scripts/generate_html.py
"""
import json, os, re
from datetime import datetime, timezone, timedelta
from pathlib import Path

PROJECT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent

# 北京时间 (UTC+8)
CST = timezone(timedelta(hours=8))

FLAGS = {
    '墨西哥':'🇲🇽','南非':'🇿🇦','韩国':'🇰🇷','捷克':'🇨🇿',
    '加拿大':'🇨🇦','波黑':'🇧🇦','卡塔尔':'🇶🇦','瑞士':'🇨🇭',
    '巴西':'🇧🇷','摩洛哥':'🇲🇦','海地':'🇭🇹','苏格兰':'🏴󠁧󠁢󠁳󠁣󠁴󠁿',
    '美国':'🇺🇸','巴拉圭':'🇵🇾','澳大利亚':'🇦🇺','土耳其':'🇹🇷',
    '德国':'🇩🇪','科特迪瓦':'🇨🇮','厄瓜多尔':'🇪🇨','库拉索':'🇨🇼',
    '荷兰':'🇳🇱','日本':'🇯🇵','突尼斯':'🇹🇳','瑞典':'🇸🇪',
    '比利时':'🇧🇪','埃及':'🇪🇬','伊朗':'🇮🇷','新西兰':'🇳🇿',
    '西班牙':'🇪🇸','沙特':'🇸🇦','乌拉圭':'🇺🇾','佛得角':'🇨🇻',
    '法国':'🇫🇷','塞内加尔':'🇸🇳','挪威':'🇳🇴','伊拉克':'🇮🇶',
    '阿根廷':'🇦🇷','阿尔及利亚':'🇩🇿','奥地利':'🇦🇹','约旦':'🇯🇴',
    '葡萄牙':'🇵🇹','刚果金':'🇨🇩','乌兹别克斯坦':'🇺🇿','哥伦比亚':'🇨🇴',
    '英格兰':'🏴󠁧󠁢󠁥󠁮󠁧󠁿','克罗地亚':'🇭🇷','巴拿马':'🇵🇦','加纳':'🇬🇭',
}

DAY_NAMES = {0:'周一',1:'周二',2:'周三',3:'周四',4:'周五',5:'周六',6:'周日'}

COMMON_CSS = '''<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); min-height: 100vh; color: #fff; }
.container { max-width: 1200px; margin: 0 auto; padding: 20px; }
.header { text-align: center; padding: 40px 20px; background: linear-gradient(90deg, rgba(255,215,0,0.1), rgba(255,140,0,0.1)); border-radius: 20px; margin-bottom: 30px; }
.header h1 { font-size: 2.8em; background: linear-gradient(90deg, #ffd700, #ff8c00); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 10px; }
.header .subtitle { font-size: 1.3em; color: #aaa; margin-bottom: 20px; }
.header .dates { color: #ffd700; font-size: 1.1em; }
.info-bar { display: flex; justify-content: center; gap: 20px; margin-bottom: 30px; flex-wrap: wrap; }
.info-item { background: rgba(255,255,255,0.1); padding: 15px 30px; border-radius: 12px; text-align: center; }
.info-item .label { font-size: 0.9em; color: #888; }
.info-item .value { font-size: 1.4em; font-weight: bold; color: #ffd700; }
.nav-section { margin-bottom: 30px; }
.nav-title { font-size: 1.5em; color: #ffd700; margin-bottom: 20px; padding-bottom: 10px; border-bottom: 2px solid rgba(255,215,0,0.3); }
.nav-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 15px; }
.nav-card { background: rgba(255,255,255,0.08); padding: 20px; border-radius: 12px; text-decoration: none; color: #fff; transition: all 0.3s ease; border: 1px solid transparent; display: block; }
.nav-card:hover { background: rgba(255,215,0,0.15); border-color: #ffd700; transform: translateY(-3px); }
.back-link { display: inline-block; margin-bottom: 20px; color: #ffd700; text-decoration: none; padding: 8px 16px; background: rgba(255,215,0,0.1); border-radius: 8px; }
.back-link:hover { background: rgba(255,215,0,0.2); }
.footer { text-align: center; color: #666; padding: 20px; font-size: 0.9em; }
.standings-section, .matches-section { background: rgba(255,255,255,0.05); border-radius: 16px; padding: 20px; margin-bottom: 30px; }
.section-title { font-size: 1.3em; color: #ffd700; margin-bottom: 15px; display: flex; align-items: center; gap: 10px; }
.standings-table { width: 100%; border-collapse: collapse; }
.standings-table th, .standings-table td { padding: 12px 10px; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.1); }
.standings-table th { background: rgba(255,215,0,0.1); color: #ffd700; font-weight: bold; font-size: 0.9em; }
.standings-table td { font-size: 0.95em; }
.standings-table .rank-1 { color: #ffd700; font-weight: bold; }
.standings-table .rank-2 { color: #c0c0c0; font-weight: bold; }
.standings-table .rank-3 { color: #cd7f32; font-weight: bold; }
.team-cell { display: flex; align-items: center; gap: 8px; justify-content: flex-start; }
.team-flag { font-size: 1.3em; }
.team-name { font-weight: 500; }
.match-item { background: rgba(0,0,0,0.2); border-radius: 12px; padding: 15px 20px; margin-bottom: 12px; border-left: 4px solid #ffd700; }
.match-item:last-child { margin-bottom: 0; }
.match-item.match-highlight { background: rgba(255,215,0,0.1); border-left-color: #ff6b6b; }
.match-time { color: #ffd700; font-size: 0.95em; margin-bottom: 8px; }
.match-teams { display: flex; align-items: center; justify-content: space-between; font-size: 1.1em; margin-bottom: 8px; }
.match-vs { color: #888; font-size: 0.85em; }
.match-score { font-size: 1.3em; font-weight: bold; color: #4ade80; margin-left: 15px; }
.match-score.pending { color: #666; font-size: 0.9em; }
.match-venue { color: #888; font-size: 0.85em; }
.match-result { margin-top: 8px; padding: 8px; background: rgba(74,222,128,0.1); border-radius: 8px; font-size: 0.9em; color: #4ade80; }
.match-group { display: inline-block; background: rgba(255,215,0,0.2); color: #ffd700; padding: 3px 10px; border-radius: 15px; font-size: 0.8em; margin-right: 10px; }
.match-tag { display: inline-block; background: #ff8c00; color: #1a1a2e; padding: 3px 10px; border-radius: 15px; font-size: 0.8em; font-weight: bold; }
@media (max-width: 768px) { .header h1 { font-size: 1.8em; } .info-bar { gap: 10px; } .nav-grid { grid-template-columns: 1fr; } }
</style>'''

def flag(name):
    return FLAGS.get(name, name)

def calc_standings(group_data):
    """计算小组积分榜"""
    teams = {t: {'name':t, 'played':0, 'won':0, 'drawn':0, 'lost':0, 'gf':0, 'ga':0, 'pts':0} for t in group_data['teams']}

    for m in group_data['matches']:
        # 只统计状态为finished且有比分数据的比赛
        if m.get('status') != 'finished':
            continue
        # 检查是否有有效比分（必须是数字）
        sh = m.get('score_home')
        sa = m.get('score_away')
        if sh is None or sa is None:
            continue
        try:
            sh = int(sh)
            sa = int(sa)
        except (ValueError, TypeError):
            continue

        home = m.get('home_name') or clean_team(m.get('home',''))
        away = m.get('away_name') or clean_team(m.get('away',''))
        if home not in teams or away not in teams:
            continue

        teams[home]['played'] += 1
        teams[away]['played'] += 1
        teams[home]['gf'] += sh
        teams[home]['ga'] += sa
        teams[away]['gf'] += sa
        teams[away]['ga'] += sh

        # 修复：正确的胜负逻辑
        if sh > sa:
            teams[home]['won'] += 1
            teams[away]['lost'] += 1
            teams[home]['pts'] += 3
        elif sh < sa:
            teams[away]['won'] += 1
            teams[home]['lost'] += 1
            teams[away]['pts'] += 3
        else:
            teams[home]['drawn'] += 1
            teams[away]['drawn'] += 1
            teams[home]['pts'] += 1
            teams[away]['pts'] += 1

    # 排序：积分 -> 净胜球 -> 进球
    sorted_teams = sorted(teams.values(), key=lambda t: (-t['pts'], -(t['gf']-t['ga']), -t['gf']))
    return sorted_teams

def clean_team(text):
    """从带国旗的文本中提取纯队名"""
    if not text:
        return ''
    text = text.strip()
    # 去掉所有国旗 emoji（FLAGS 的 value 是 emoji，key 是队名）
    for name, emoji in FLAGS.items():
        text = text.replace(emoji, '')
    return text.strip()

def clean_home_away(m):
    """清理队名，添加 home_name/away_name 字段"""
    m['home_name'] = clean_team(m.get('home', ''))
    m['away_name'] = clean_team(m.get('away', ''))

def match_html(m, group_mode=False):
    """生成单个比赛的 HTML"""
    clean_home_away(m)
    h_name = m['home_name']
    a_name = m['away_name']
    h_flag = flag(h_name)
    a_flag = flag(a_name)

    status = m.get('status', 'pending')
    time_str = m.get('time', '')
    venue = m.get('venue', '')
    highlight = m.get('highlight', False)
    tag = m.get('tag', '')

    item_class = 'match-item match-highlight' if highlight else 'match-item'

    # 清理 venue 中可能已有的 📍 前缀，避免重复
    venue_clean = venue.replace('📍 ', '').replace('📍', '').strip()

    if status == 'finished':
        # 清理 time_str 中可能已有的 ✅ 已结束，避免重复
        time_base = time_str.replace(' ✅ 已结束', '').strip()
        time_display = time_base + ' ✅ 已结束'
        score_h = m.get('score_home', 0) or 0
        score_a = m.get('score_away', 0) or 0
        score_html = f'<span class="match-score">{score_h}-{score_a}</span>'
    else:
        time_display = time_str
        score_html = '<span class="match-vs">vs</span>'

    html = f'<div class="{item_class}">\n'
    html += f'    <div class="match-time">{time_display}</div>\n'
    html += f'    <div class="match-teams">\n'
    html += f'        <span>{h_flag} {h_name}</span>\n'
    html += f'        {score_html}\n'
    html += f'        <span>{a_name} {a_flag}</span>\n'
    html += f'    </div>\n'

    if venue_clean:
        html += f'    <div class="match-venue">📍 {venue_clean}</div>\n'

    if tag:
        html += f'    <div style="margin-top:10px;"><span class="match-tag">🔥 {tag}</span></div>\n'

    if m.get('events'):
        html += f'    <div class="match-result">{m["events"]}</div>\n'

    html += '</div>\n'
    return html

def gen_index(data, output_dir):
    """生成首页 index.html"""
    groups = data['groups']

    # 小组卡片
    group_cards = ''
    for g in 'ABCDEFGHIJKL':
        gd = groups[g]
        teams_str = '、'.join(gd['teams'])
        group_cards += f'''            <a href="group-{g.lower()}.html" class="nav-card">
                <div style="display:flex;align-items:center;gap:15px;">
                    <div style="background:linear-gradient(135deg,#ffd700,#ff8c00);color:#1a1a2e;width:50px;height:50px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:1.2em;">{g}</div>
                    <div>
                        <div style="font-size:1.2em;font-weight:bold;color:#ffd700;">{g}组</div>
                        <div style="font-size:0.9em;color:#aaa;margin-top:5px;">{teams_str}</div>
                    </div>
                </div>
            </a>\n'''

    # 日期卡片 - 从数据中生成
    date_cards = ''
    day_labels = {
        '0612': ('6月12日', '周五 · 揭幕战', '2场'),
        '0613': ('6月13日', '周六', '2场'),
        '0614': ('6月14日', '周日', '4场'),
        '0615': ('6月15日', '周一', '4场'),
        '0616': ('6月16日', '周二', '4场'),
        '0617': ('6月17日', '周三 · 焦点', '4场'),
        '0618': ('6月18日', '周四 · 焦点', '4场'),
        '0619': ('6月19日', '周五', '4场'),
        '0620': ('6月20日', '周六', '4场'),
        '0621': ('6月21日', '周日', '4场'),
        '0622': ('6月22日', '周一', '4场'),
        '0623': ('6月23日', '周二', '4场'),
        '0624': ('6月24日', '周三', '4场'),
        '0625': ('6月25日', '周四', '6场'),
        '0626': ('6月26日', '周五', '6场'),
        '0627': ('6月27日', '周六 · 焦点', '6场'),
        '0628': ('6月28日', '周日 · 小组赛结束', '6场'),
    }

    for key in sorted(data['dates'].keys()):
        dd = data['dates'][key]
        if key in day_labels:
            day, week, count = day_labels[key]
        else:
            day = f'{key[:2]}月{key[2:]}日'
            week = ''
            count = f'{len(dd["matches"])}场'
        date_cards += f'''            <a href="date-{key}.html" class="nav-card">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <div style="font-size:1.1em;font-weight:bold;">{day}</div>
                        <div style="font-size:0.9em;color:#aaa;">{week}</div>
                    </div>
                    <span style="background:rgba(255,215,0,0.2);color:#ffd700;padding:5px 12px;border-radius:20px;font-size:0.85em;">{count}</span>
                </div>
            </a>\n'''

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>2026年美加墨世界杯赛程</title>
    {COMMON_CSS}
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏆 2026年美加墨世界杯</h1>
            <div class="subtitle">FIFA World Cup USA / Mexico / Canada</div>
            <div class="dates">📅 2026年6月12日 - 7月20日</div>
        </div>

        <div class="info-bar">
            <div class="info-item"><div class="label">参赛球队</div><div class="value">48支</div></div>
            <div class="info-item"><div class="label">总场次</div><div class="value">104场</div></div>
            <div class="info-item"><div class="label">比赛天数</div><div class="value">39天</div></div>
            <div class="info-item"><div class="label">主办国</div><div class="value">美加墨</div></div>
        </div>

        <div class="nav-section">
            <div class="nav-title">🏆 淘汰赛专区</div>
            <div style="margin-bottom:25px;"><div style="font-size:1.2em;color:#ff6b6b;margin-bottom:15px;">🎯 1/8决赛 (7月5日-7月8日)</div><div class="nav-grid"><a href="knockout.html#round8" class="nav-card"><div>🎯 1/8决赛</div><div style="font-size:0.85em;color:#aaa;">7月5日-7月8日 · 8场</div></a></div></div>
            <div style="margin-bottom:25px;"><div style="font-size:1.2em;color:#ff6b6b;margin-bottom:15px;">💎 1/4决赛 (7月10日-7月12日)</div><div class="nav-grid"><a href="knockout.html#quarter" class="nav-card"><div>💎 1/4决赛</div><div style="font-size:0.85em;color:#aaa;">7月10日-7月12日 · 4场</div></a></div></div>
            <div style="margin-bottom:25px;"><div style="font-size:1.2em;color:#ff6b6b;margin-bottom:15px;">🌟 半决赛 (7月15日-7月16日)</div><div class="nav-grid"><a href="knockout.html#semi" class="nav-card"><div>🌟 半决赛</div><div style="font-size:0.85em;color:#aaa;">7月15日-7月16日 · 2场</div></a></div></div>
            <div style="margin-bottom:25px;"><div style="font-size:1.2em;color:#ff6b6b;margin-bottom:15px;">⚔️ 1/16决赛 (6月29日-7月4日)</div><div class="nav-grid"><a href="knockout.html#round16" class="nav-card"><div>⚔️ 1/16决赛</div><div style="font-size:0.85em;color:#aaa;">6月29日-7月4日 · 8场</div></a></div></div>
            <div style="margin-bottom:25px;"><div style="font-size:1.2em;color:#ff6b6b;margin-bottom:15px;">🥉 季军赛 (7月19日)</div><div class="nav-grid"><a href="knockout.html#third" class="nav-card"><div>🥉 季军赛</div><div style="font-size:0.85em;color:#aaa;">7月19日 03:00</div></a></div></div>
            <div style="margin-bottom:25px;"><div style="font-size:1.2em;color:#ff6b6b;margin-bottom:15px;">🏆 决赛 (7月20日)</div><div class="nav-grid"><a href="knockout.html#final" class="nav-card" style="background:linear-gradient(135deg,rgba(255,215,0,0.2),rgba(255,140,0,0.3));border-color:#ffd700;"><div>🏆 决赛</div><div style="font-size:0.85em;color:#aaa;">7月20日 03:00 · 纽约</div></a></div></div>
        </div>

        <div class="nav-section">
            <div class="nav-title">⚽ 按小组查看（带积分榜）</div>
            <div class="nav-grid">
{group_cards}            </div>
        </div>

        <div class="nav-section">
            <div class="nav-title">📅 按日期查看（比赛结果）</div>
            <div class="nav-grid">
{date_cards}                <a href="knockout.html" class="nav-card" style="background:linear-gradient(135deg,rgba(255,215,0,0.2),rgba(255,140,0,0.2));">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <div style="font-size:1.1em;font-weight:bold;color:#ffd700;">淘汰赛阶段</div>
                            <div style="font-size:0.9em;color:#aaa;">6月29日 - 7月20日</div>
                        </div>
                        <span style="background:#ffd700;color:#1a1a2e;padding:5px 12px;border-radius:20px;font-size:0.85em;">32场</span>
                    </div>
                </a>
            </div>
        </div>

        <div class="nav-section">
            <div class="nav-title">🎖️ 决赛之路</div>
            <div style="background:linear-gradient(135deg,rgba(255,215,0,0.1),rgba(255,140,0,0.1));border-radius:16px;padding:30px;text-align:center;border:1px solid rgba(255,215,0,0.3);">
                <div style="display:flex;align-items:center;justify-content:center;gap:30px;margin-bottom:20px;">
                    <div style="width:150px;height:80px;background:rgba(0,0,0,0.3);border-radius:12px;display:flex;align-items:center;justify-content:center;border:2px dashed rgba(255,215,0,0.5);"><span style="color:#666;">待定</span></div>
                    <div style="font-size:1.5em;font-weight:bold;color:#ffd700;">VS</div>
                    <div style="width:150px;height:80px;background:rgba(0,0,0,0.3);border-radius:12px;display:flex;align-items:center;justify-content:center;border:2px dashed rgba(255,215,0,0.5);"><span style="color:#666;">待定</span></div>
                </div>
                <div style="color:#888;"><a href="knockout.html#final" style="color:#ffd700;text-decoration:none;">查看完整淘汰赛晋级之路 →</a></div>
            </div>
        </div>

        <div class="footer">
            <p>📌 赛事时间可能存在调整，请以官方最新公布为准</p>
            <p>🏆 2026年美加墨世界杯 · 北京时间</p>
            <p style="margin-top:10px;color:#888;">🔄 每日自动更新 · 数据驱动</p>
        </div>
    </div>
</body>
</html>'''

    with open(output_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("  ✅ index.html")

def gen_group(data, group_name, output_dir):
    """生成小组页面"""
    gd = data['groups'][group_name]
    standings = calc_standings(gd)

    # 积分榜
    rows = ''
    for i, t in enumerate(standings):
        rank_class = {0:'rank-1', 1:'rank-2', 2:'rank-3'}.get(i, '')
        gf_ga = f"{t['gf']}/{t['ga']}"
        rows += f'''                <tr>
                    <td class="{rank_class}">{i+1}</td>
                    <td><div class="team-cell"><span class="team-flag">{flag(t['name'])}</span><span class="team-name">{t['name']}</span></div></td>
                    <td>{t['played']}</td><td>{t['won']}</td><td>{t['drawn']}</td><td>{t['lost']}</td>
                    <td>{gf_ga}</td><td>{t['pts']}</td>
                </tr>\n'''

    # 比赛
    matches_html = ''
    for m in gd['matches']:
        matches_html += match_html(m, group_mode=True)

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{group_name}组 - 2026年世界杯赛程</title>
    {COMMON_CSS}
</head>
<body>
    <div class="container">
        <a href="index.html" class="back-link">← 返回首页</a>
        <div class="header">
            <h1>🏆 {group_name}组</h1>
            <p style="color:#aaa;margin-top:10px;">{' / '.join(gd['teams'])}</p>
        </div>
        <div class="standings-section">
            <div class="section-title">📊 小组积分榜</div>
            <table class="standings-table">
                <thead><tr><th>排名</th><th>球队</th><th>赛</th><th>胜</th><th>平</th><th>负</th><th>进/失</th><th>积分</th></tr></thead>
                <tbody>
{rows}                </tbody>
            </table>
            <p style="margin-top:15px;color:#666;font-size:0.85em;">📌 积分规则：胜=3分 平=1分 负=0分</p>
        </div>
        <div class="matches-section">
            <div class="section-title">⚽ 小组赛程</div>
{matches_html}        </div>
        <div class="footer"><p>📌 赛事时间可能存在调整，请以官方最新公布为准</p><p>🔄 每日自动更新</p></div>
    </div>
</body>
</html>'''

    with open(output_dir / f'group-{group_name.lower()}.html', 'w', encoding='utf-8') as f:
        f.write(html)

def gen_date(data, date_key, output_dir):
    """生成日期页面"""
    dd = data['dates'][date_key]
    matches = dd['matches']

    month = int(date_key[:2])
    day = int(date_key[2:])
    dt = datetime(2026, month, day)
    day_name = DAY_NAMES.get(dt.weekday(), '')
    total = len(matches)

    # 特殊标签
    special = {
        '0612': ('🏆 揭幕战', '世界杯开幕日'),
        '0628': ('📋 小组赛收官', '小组赛结束'),
    }
    title, week = special.get(date_key, (f'{month}月{day}日', day_name))

    matches_html = ''
    for m in matches:
        clean_home_away(m)
        h_name = m['home_name']
        a_name = m['away_name']
        h_flag = flag(h_name)
        a_flag = flag(a_name)

        status = m.get('status', 'pending')
        highlight = m.get('highlight', False)
        tag = m.get('tag', '')
        group_label = m.get('group', '')
        venue = m.get('venue', '')

        item_class = 'match-item highlight' if highlight else 'match-item'

        if status == 'finished':
            time_display = f'{m.get("kickoff","")} ✅ 已结束'
            score_h = m.get('score_home', 0) or 0
            score_a = m.get('score_away', 0) or 0
            score_text = f'{score_h}-{score_a}'
            score_html = f'<span class="match-score">{score_text}</span>'
        else:
            time_display = m.get('time', '')
            score_html = '<span class="match-vs">vs</span>'

        info_parts = []
        if group_label:
            info_parts.append(f'<span class="match-group">{group_label}</span>')
        if venue:
            info_parts.append(f'<span class="match-venue">📍 {venue}</span>')
        info_html = '<div>' + ''.join(info_parts) + '</div>' if info_parts else ''

        tag_html = f'<div style="margin-top:10px;"><span class="match-tag">🔥 {tag}</span></div>' if tag else ''

        events_html = f'<div style="margin-top:8px;color:#888;font-size:0.85em;">{m["events"]}</div>' if m.get('events') else ''

        matches_html += f'''            <div class="{item_class}">
                <div class="match-time">{time_display}</div>
                <div class="match-teams">
                    <span>{h_flag} {h_name}</span>
                    {score_html}
                    <span>{a_flag} {a_name}</span>
                </div>
                {info_html}
                {tag_html}
                {events_html}
            </div>\n'''

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - 2026年美加墨世界杯</title>
    {COMMON_CSS}
</head>
<body>
    <div class="container">
        <a href="index.html" class="back-link">← 返回首页</a>
        <div class="header"><h1>{title}</h1></div>
        <div style="text-align:center;margin-bottom:25px;padding:15px;background:rgba(255,255,255,0.05);border-radius:12px;">
            <div style="font-size:1.5em;font-weight:bold;color:#ffd700;">{month}月{day}日 {day_name}</div>
            <div style="color:#888;margin-top:5px;">{week}</div>
        </div>
        <div style="background:rgba(255,255,255,0.05);border-radius:15px;padding:25px;">
            <div style="color:#ffd700;font-size:1.3em;margin-bottom:20px;padding-bottom:10px;border-bottom:2px solid rgba(255,215,0,0.3);">📋 今日赛程 ({total}场)</div>
{matches_html}        </div>
    </div>
</body>
</html>'''

    with open(output_dir / f'date-{date_key}.html', 'w', encoding='utf-8') as f:
        f.write(html)

def _resolve_winner(m):
    """根据比赛结果返回胜者名字（含国旗），平局/未结束返回 None"""
    if m.get('status') != 'finished':
        return None
    sh = m.get('score_home')
    sa = m.get('score_away')
    if sh is None or sa is None:
        return None
    try:
        sh = int(sh); sa = int(sa)
    except (ValueError, TypeError):
        return None
    if sh == sa:
        return None  # 淘汰赛不应平局；如出现则不晋级
    return m['home'] if sh > sa else m['away']

def _build_advancement_map(round_matches, prev_winners):
    """根据模板的占位符（1/16胜者1..N），生成占位符->实际队伍名的映射"""
    mapping = {}
    for idx, m in enumerate(round_matches, 1):
        for side in ('home', 'away'):
            val = m.get(side, '')
            if val in prev_winners:
                mapping[val] = prev_winners[val]
    return mapping

def _advance_round(prev_matches):
    """根据上一轮比赛结果，返回胜者映射 {'1/16胜者1': '🇧🇷 巴西', ...}"""
    winners = {}
    for idx, m in enumerate(prev_matches, 1):
        winner = _resolve_winner(m)
        if winner is None:
            return {}  # 任意一场未结束则停止晋级
        winners[f'1/16胜者{idx}'] = winner
        winners[f'1/8胜者{idx}'] = winner
        winners[f'1/4胜者{idx}'] = winner
        winners[f'半决赛胜者{idx}'] = winner
        winners[f'半决赛负者{idx}'] = winner
    return winners

def _render_ko_match(m, item_class, stage_key, finals_venue):
    """生成单个淘汰赛比赛的 HTML 片段"""
    status = m.get('status', 'pending')
    time_str = m.get('time', '')
    if status == 'finished' and '✅ 已结束' not in time_str:
        time_display = time_str + ' ✅ 已结束'
    else:
        time_display = time_str

    # 比分渲染
    if status == 'finished':
        sh = m.get('score_home', 0) or 0
        sa = m.get('score_away', 0) or 0
        score_html = f'<span class="match-score">{sh}-{sa}</span>'
    else:
        score_html = '<span class="match-score pending">等待开赛</span>'

    venue_line = ''
    if stage_key == 'final':
        venue_line = f'<div style="margin-top:12px;color:#ffd700;font-weight:bold;">📍 {finals_venue}</div>'
    elif m.get('venue'):
        venue_clean = m['venue'].replace('📍 ', '').replace('📍', '').strip()
        venue_line = f'<div class="match-venue">📍 {venue_clean}</div>'

    # events 注释
    events_html = ''
    if m.get('events'):
        events_html = f'<div style="margin-top:8px;padding:6px 10px;background:rgba(74,222,128,0.1);border-radius:6px;font-size:0.85em;color:#4ade80;">{m["events"]}</div>'

    return f'''                <div class="match-item {item_class}">
                    <div class="match-time">{time_display}{' 🏆' if stage_key == 'final' else ''}</div>
                    <div class="match-teams">
                        <span>{m['home']}</span>
                        <span class="match-vs">vs</span>
                        <span>{m['away']}</span>
                    </div>
                    {score_html}
                    {venue_line}
                    {events_html}
                </div>'''

def gen_knockout(data, output_dir):
    """生成淘汰赛页面：1/16 显示实际数据，已结束比赛按结果晋级到 1/8（8强）"""
    ko_css = '''<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); min-height: 100vh; color: #fff; }
.container { max-width: 1100px; margin: 0 auto; padding: 20px; }
.header { text-align: center; padding: 40px 20px; background: linear-gradient(90deg, rgba(255,215,0,0.2), rgba(255,140,0,0.2)); border-radius: 20px; margin-bottom: 30px; }
.header h1 { font-size: 2.5em; background: linear-gradient(90deg, #ffd700, #ff8c00); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 10px; }
.back-link { display: inline-block; margin-bottom: 20px; color: #ffd700; text-decoration: none; padding: 8px 16px; background: rgba(255,215,0,0.1); border-radius: 8px; }
.back-link:hover { background: rgba(255,215,0,0.2); }
.stage-section { background: rgba(255,255,255,0.05); border-radius: 15px; padding: 25px; margin-bottom: 20px; }
.stage-title { color: #ffd700; font-size: 1.5em; margin-bottom: 20px; padding-bottom: 10px; border-bottom: 2px solid rgba(255,215,0,0.3); display: flex; align-items: center; gap: 10px; }
.stage-badge { background: linear-gradient(135deg, #ffd700, #ff8c00); color: #1a1a2e; padding: 5px 15px; border-radius: 20px; font-size: 0.8em; font-weight: bold; }
.final-badge { background: linear-gradient(135deg, #ffd700, #ff4500); }
.match-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 15px; }
.match-item { background: rgba(255,255,255,0.08); border-radius: 12px; padding: 20px; border-left: 4px solid #7F77DD; }
.match-item.highlight { border-left-color: #D85A30; background: linear-gradient(135deg, rgba(255,215,0,0.1), rgba(255,100,0,0.1)); }
.match-item.final-item { border-left-color: #ffd700; background: linear-gradient(135deg, rgba(255,215,0,0.15), rgba(255,140,0,0.15)); }
.match-time { color: #ffd700; font-weight: bold; margin-bottom: 12px; font-size: 0.95em; }
.match-teams { display: flex; justify-content: space-between; align-items: center; font-size: 1.1em; }
.match-vs { color: #888; font-size: 0.85em; }
.match-score { font-size: 1.3em; font-weight: bold; color: #4ade80; margin-left: 15px; }
.match-score.pending { color: #666; font-size: 0.9em; }
.match-venue { color: #888; font-size: 0.85em; margin-top: 8px; }
.footer { text-align: center; color: #666; padding: 20px; margin-top: 30px; }
@media (max-width: 768px) { .match-grid { grid-template-columns: 1fr; } }
</style>'''

    ko = data['knockout']
    finals_venue = ko['final'].get('venue', '纽约大都会人寿体育场')

    # 计算晋级映射
    r16_winners = _advance_round(ko['round16']['matches'])  # {'1/16胜者1': '🇿🇦 南非', ...}
    r8_winners = _advance_round(ko['round8']['matches']) if r16_winners and len(r16_winners) >= 16 else {}
    q_winners = _advance_round(ko['quarter']['matches']) if r8_winners and len(r8_winners) >= 8 else {}

    stages_html = ''

    for stage_key in ['round16', 'round8', 'quarter', 'semi', 'third', 'final']:
        s = ko[stage_key]
        badge_class = 'final-badge' if stage_key == 'final' else ''

        # 选择本轮要使用的晋级映射
        if stage_key == 'round16':
            adv = r16_winners  # round16 不需要替换，但保留一致
        elif stage_key == 'round8':
            adv = r16_winners
        elif stage_key == 'quarter':
            adv = r8_winners
        elif stage_key in ('semi', 'third', 'final'):
            adv = q_winners
        else:
            adv = {}

        matches_html = ''
        for m in s['matches']:
            # 复制以免污染原数据
            mm = dict(m)
            # 用晋级映射替换占位符
            for side in ('home', 'away'):
                if mm.get(side) in adv:
                    mm[side] = adv[mm[side]]

            item_class = 'final-item' if stage_key == 'final' else ('highlight' if mm.get('highlight') or stage_key == 'semi' else '')
            matches_html += _render_ko_match(mm, item_class, stage_key, finals_venue)

        stages_html += f'''        <div class="stage-section">
            <div class="stage-title"><span class="stage-badge {badge_class}">{s['icon']} {s['label']}</span> {s['dates']}</div>
            <div class="match-grid">
{matches_html}            </div>
        </div>\n'''

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>淘汰赛阶段 - 2026年美加墨世界杯</title>
    {ko_css}
</head>
<body>
    <div class="container">
        <a href="index.html" class="back-link">← 返回首页</a>
        <div class="header"><h1>🏆 淘汰赛阶段</h1></div>
{stages_html}
        <div class="footer">
            <p>📌 赛事时间可能存在调整，请以官方最新公布为准</p>
            <p>🔄 每日自动更新</p>
        </div>
    </div>
</body>
</html>'''

    with open(output_dir / 'knockout.html', 'w', encoding='utf-8') as f:
        f.write(html)

def gen_all(data_path=None):
    """生成所有 HTML 页面"""
    if data_path is None:
        data_path = PROJECT_DIR / 'data' / 'matches.json'

    with open(str(data_path), 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 输出到 world_cup/ 目录
    output_dir = PROJECT_DIR / 'world_cup'
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"🏗️  从 {data_path} 生成 HTML...")
    print(f"   输出目录: {output_dir}\n")

    gen_index(data, output_dir)

    for g in 'ABCDEFGHIJKL':
        gen_group(data, g, output_dir)
        print(f"  ✅ group-{g.lower()}.html")

    for key in sorted(data['dates'].keys()):
        gen_date(data, key, output_dir)
        print(f"  ✅ date-{key}.html")

    gen_knockout(data, output_dir)
    print(f"  ✅ knockout.html")

    print(f"\n✅ 完成！共生成 {1 + 12 + len(data['dates']) + 1} 个 HTML 文件")

if __name__ == '__main__':
    gen_all()