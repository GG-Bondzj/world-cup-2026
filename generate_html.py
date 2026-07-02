# -*- coding: utf-8 -*-
"""
从 matches.json 生成所有 HTML 页面。
运行：python scripts/generate_html.py
"""
import json, os, re
from datetime import datetime, timezone, timedelta
from pathlib import Path

PROJECT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

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
:root { --gold: #f59e0b; --gold-dark: #d97706; --amber: #fbbf24; --purple: #8b5cf6; --navy: #0f172a; --card-bg: rgba(255,255,255,0.06); --card-hover: rgba(245,158,11,0.12); }
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Microsoft YaHei', 'PingFang SC', 'Segoe UI', sans-serif; background: linear-gradient(160deg, #0a0a1a 0%, #0f172a 30%, #1a1040 60%, #0f172a 100%); min-height: 100vh; color: #e2e8f0; overflow-x: hidden; }
body::before { content:''; position:fixed; top:0; left:0; width:100%; height:100%; background: radial-gradient(ellipse at 10% 20%, rgba(245,158,11,0.06) 0%, transparent 40%), radial-gradient(ellipse at 90% 80%, rgba(139,92,246,0.05) 0%, transparent 40%); pointer-events:none; z-index:-1; }
.container { max-width: 1200px; margin: 0 auto; padding: 20px; }

/* 头部 */
.header { text-align: center; padding: 50px 20px; background: radial-gradient(ellipse at center, rgba(245,158,11,0.15) 0%, transparent 70%); border-radius: 24px; margin-bottom: 30px; position:relative; overflow:hidden; }
.header::before { content:''; position:absolute; top:-50%; left:-50%; width:200%; height:200%; background: conic-gradient(from 0deg, transparent, rgba(245,158,11,0.08), transparent, rgba(139,92,246,0.06), transparent); animation: headerSpin 25s linear infinite; }
@keyframes headerSpin { from{transform:rotate(0deg)} to{transform:rotate(360deg)} }
.header > * { position:relative; z-index:1; }
.header h1 { font-size: 3em; background: linear-gradient(135deg, #fbbf24, #f59e0b, #d97706, #fbbf24); background-size: 300% 300%; -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 8px; letter-spacing: 3px; animation: shimmer 4s ease infinite; }
@keyframes shimmer { 0%,100%{background-position:0% 50%} 50%{background-position:100% 50%} }
.header .subtitle { font-size: 1.15em; color: #94a3b8; margin-bottom: 16px; letter-spacing: 4px; text-transform: uppercase; }
.header .dates { color: #f59e0b; font-size: 1.1em; }

/* 阶段指示器 */
.stage-indicator { display:flex; align-items:center; justify-content:center; gap:8px; background:linear-gradient(135deg,rgba(245,158,11,0.15),rgba(139,92,246,0.1)); border-radius:20px; padding:18px 28px; margin-bottom:30px; border:1px solid rgba(245,158,11,0.25); position:relative; overflow:hidden; }
.stage-indicator::before { content:''; position:absolute; top:0; left:0; width:100%; height:2px; background: linear-gradient(90deg, transparent, #f59e0b, transparent); }
.stage-dot { width:12px; height:12px; border-radius:50%; background:#f59e0b; animation: pulse 1.5s ease-in-out infinite; box-shadow: 0 0 10px #f59e0b; }
.stage-dot.live { background:#ef4444; animation: pulse 0.8s ease-in-out infinite; box-shadow: 0 0 15px #ef4444; }
@keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.6;transform:scale(1.1)} }
.stage-label { font-size:1.2em; font-weight:bold; color:#f59e0b; }
.stage-detail { color:#94a3b8; font-size:0.95em; }

/* 信息栏 */
.info-bar { display: flex; justify-content: center; gap: 18px; margin-bottom: 35px; flex-wrap: wrap; }
.info-item { background: var(--card-bg); padding: 18px 32px; border-radius: 16px; text-align: center; border:1px solid rgba(255,255,255,0.06); backdrop-filter:blur(10px); transition:all 0.3s cubic-bezier(0.4,0,0.2,1); position:relative; overflow:hidden; }
.info-item::before { content:''; position:absolute; bottom:0; left:0; width:100%; height:3px; background: linear-gradient(90deg, transparent, #f59e0b, transparent); opacity:0; transition:opacity 0.3s; }
.info-item:hover { border-color: rgba(245,158,11,0.4); transform:translateY(-4px); box-shadow: 0 12px 35px rgba(245,158,11,0.15); }
.info-item:hover::before { opacity:1; }
.info-item .label { font-size: 0.9em; color: #64748b; margin-bottom:6px; }
.info-item .value { font-size: 1.6em; font-weight: bold; background:linear-gradient(135deg,#fbbf24,#f59e0b); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }

/* 版块 */
.nav-section { margin-bottom: 40px; }
.nav-title { font-size: 1.5em; color: #f59e0b; margin-bottom: 22px; padding-bottom: 14px; border-bottom: 1px solid rgba(245,158,11,0.2); display:flex; align-items:center; gap:10px; }
.nav-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 14px; }
.nav-card { background: var(--card-bg); padding: 20px; border-radius: 16px; text-decoration: none; color: #e2e8f0; transition: all 0.3s cubic-bezier(0.4,0,0.2,1); border: 1px solid rgba(255,255,255,0.05); display: block; backdrop-filter:blur(10px); position:relative; overflow:hidden; }
.nav-card::before { content:''; position:absolute; top:0; left:0; width:4px; height:100%; background: linear-gradient(180deg, #f59e0b, #d97706); opacity:0; transition:opacity 0.3s; }
.nav-card:hover { background: var(--card-hover); border-color: rgba(245,158,11,0.35); transform: translateY(-4px); box-shadow: 0 12px 35px rgba(245,158,11,0.12); }
.nav-card:hover::before { opacity:1; }
.back-link { display: inline-block; margin-bottom: 20px; color: #f59e0b; text-decoration: none; padding: 10px 20px; background: rgba(245,158,11,0.1); border-radius: 12px; transition:all 0.3s; font-size:0.9em; }
.back-link:hover { background: rgba(245,158,11,0.2); }

/* 淘汰赛预览卡片（首页） */
.ko-card-locked { min-width:120px; max-width:180px; width:45%; min-height:60px; background:linear-gradient(135deg,rgba(245,158,11,0.15),rgba(217,119,6,0.08)); border-radius:12px; display:flex; align-items:center; justify-content:center; border:2px solid rgba(245,158,11,0.5); padding:8px 12px; transition:all 0.4s cubic-bezier(0.4,0,0.2,1); }
.ko-card-locked:hover { border-color:#fbbf24; box-shadow:0 0 30px rgba(245,158,11,0.25); transform:scale(1.03); }
.ko-card-flag { font-weight:bold; color:#fbbf24; font-size:0.9em; text-align:center; line-height:1.3; }
.ko-card-next { min-width:120px; max-width:180px; width:45%; min-height:60px; background:linear-gradient(135deg,rgba(139,92,246,0.12),rgba(109,40,217,0.06)); border-radius:12px; display:flex; align-items:center; justify-content:center; border:2px solid rgba(139,92,246,0.4); padding:8px 12px; transition:all 0.4s; }
.ko-card-next:hover { border-color:#a78bfa; box-shadow:0 0 25px rgba(139,92,246,0.2); }
.ko-card-label { color:#a78bfa; font-size:0.85em; font-weight:bold; text-align:center; }

/* 对阵卡片 */
.ko-match-pair { background:rgba(255,255,255,0.04); border-radius:14px; padding:16px; border:1px solid rgba(255,255,255,0.06); transition:all 0.3s; display:flex; flex-direction:column; align-items:center; }
.ko-match-pair:hover { background:rgba(255,255,255,0.07); border-color:rgba(245,158,11,0.3); box-shadow:0 8px 25px rgba(245,158,11,0.1); transform:translateY(-2px); }
.ko-match-pair.finished { border-left:3px solid #22c55e; }

/* 对阵预览区域 */
.ko-preview-section { background: linear-gradient(135deg, rgba(245,158,11,0.06), rgba(139,92,246,0.03)); border-radius: 20px; padding: 28px; border: 1px solid rgba(245,158,11,0.15); margin-bottom: 30px; }
.ko-preview-title { display: flex; align-items: center; gap: 12px; margin-bottom: 20px; }
.ko-preview-title .icon { font-size: 1.5em; }
.ko-preview-title .label { font-size: 1.3em; color: #f59e0b; font-weight: bold; }
.ko-preview-title .date { color: #888; font-size: 0.9em; margin-left: auto; }

/* 比赛卡片 */
.match-card { background: rgba(255,255,255,0.05); border-radius: 14px; padding: 18px; margin-bottom: 12px; border-left: 4px solid #f59e0b; transition:all 0.3s; }
.match-card:hover { background: rgba(255,255,255,0.08); }
.match-card.finished { border-left-color: #22c55e; opacity:0.85; }
.match-card.live { border-left-color: #ef4444; animation: liveGlow 2s ease-in-out infinite; }
@keyframes liveGlow { 0%,100%{box-shadow:0 0 8px rgba(239,68,68,0.3)} 50%{box-shadow:0 0 20px rgba(239,68,68,0.5)} }
.match-header { display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; }
.match-time-badge { color:#f59e0b; font-weight:bold; font-size:0.9em; display:flex; align-items:center; gap:6px; }
.match-status-badge { font-size:0.8em; padding:3px 12px; border-radius:20px; font-weight:bold; }
.match-status-badge.done { background:rgba(34,197,94,0.15); color:#22c55e; }
.match-status-badge.live { background:rgba(239,68,68,0.15); color:#ef4444; animation: pulse 1.5s ease-in-out infinite; }
.match-status-badge.upcoming { background:rgba(245,158,11,0.15); color:#f59e0b; }
.match-teams-row { display:flex; align-items:center; justify-content:space-between; font-size:1.05em; }
.match-teams-row .team { flex:1; display:flex; align-items:center; gap:8px; }
.match-teams-row .team.right { justify-content:flex-end; text-align:right; }
.match-score-display { font-size:1.4em; font-weight:bold; color:#f59e0b; margin:0 20px; min-width:50px; text-align:center; }
.match-score-display.pending { color:#555; font-size:1em; }
.match-events { margin-top:8px; padding:8px 12px; background:rgba(255,255,255,0.03); border-radius:8px; font-size:0.8em; color:#94a3b8; }

.footer { text-align: center; color: #555; padding: 30px 20px; font-size: 0.85em; border-top:1px solid rgba(255,255,255,0.05); margin-top:40px; }
.standings-section, .matches-section { background: var(--card-bg); border-radius: 16px; padding: 24px; margin-bottom: 30px; border:1px solid rgba(255,255,255,0.05); }
.section-title { font-size: 1.3em; color: #f59e0b; margin-bottom: 18px; display: flex; align-items: center; gap: 10px; }
.standings-table { width: 100%; border-collapse: collapse; }
.standings-table th, .standings-table td { padding: 12px 10px; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.06); }
.standings-table th { background: rgba(245,158,11,0.08); color: #f59e0b; font-weight: bold; font-size: 0.85em; text-transform:uppercase; letter-spacing:1px; }
.standings-table td { font-size: 0.95em; }
.standings-table tr:hover td { background:rgba(255,255,255,0.03); }
.standings-table .rank-1 { color: #fbbf24; font-weight: bold; font-size:1.1em; }
.standings-table .rank-2 { color: #c0c0c0; font-weight: bold; }
.standings-table .rank-3 { color: #cd7f32; font-weight: bold; }
.team-cell { display:flex; align-items:center; gap:8px; justify-content:center; }
.team-flag { font-size:1.2em; }
.team-name { text-align:left; }

@media (max-width: 768px) {
    .header h1 { font-size:2em; }
    .nav-grid { grid-template-columns:1fr; }
    .info-bar { gap:8px; }
    .info-item { padding:12px 16px; }
}
.team-cell { display: flex; align-items: center; gap: 8px; justify-content: flex-start; }
.team-flag { font-size: 1.3em; }
.team-name { font-weight: 500; }
.match-item { background: rgba(0,0,0,0.2); border-radius: 12px; padding: 15px 20px; margin-bottom: 12px; border-left: 4px solid #ffd700; }
.match-item:last-child { margin-bottom: 0; }
.match-item.match-highlight { background: rgba(255,215,0,0.1); border-left-color: #ff6b6b; }
.match-time { color: #ffd700; font-size: 0.95em; margin-bottom: 8px; }
.match-teams { display: flex; align-items: center; justify-content: space-between; font-size: 1.1em; margin-bottom: 8px; }
.match-vs { color: #888; font-size: 0.85em; }
.match-score { font-size: 1.3em; font-weight: bold; color: #f59e0b; margin-left: 15px; }
.match-score.pending { color: #555; font-size: 0.9em; }
.match-venue { color: #64748b; font-size: 0.85em; }
.match-result { margin-top: 8px; padding: 8px 12px; background: rgba(245,158,11,0.1); border-radius: 8px; font-size: 0.88em; color: #fbbf24; }
.match-group { display: inline-block; background: rgba(245,158,11,0.15); color: #f59e0b; padding: 3px 10px; border-radius: 15px; font-size: 0.8em; margin-right: 10px; }
.match-tag { display: inline-block; background: linear-gradient(135deg,#f59e0b,#d97706); color: #0a0a1a; padding: 3px 10px; border-radius: 15px; font-size: 0.8em; font-weight: bold; }
@media (max-width: 768px) { .header h1 { font-size: 1.8em; } .info-bar { gap: 10px; } .nav-grid { grid-template-columns: 1fr; } }
</style>'''

def flag(name):
    return FLAGS.get(name, name)

def _add_flag_to_team(team_str):
    """为球队名添加国旗 emoji"""
    import re
    # 已经是完整格式 "🇨🇦 加拿大" 的不处理
    if re.match(r'^[🇦-👿]\s', team_str):
        return team_str
    # 查找球队名并添加国旗
    for team_name, team_flag in FLAGS.items():
        if team_name in team_str:
            return f'{team_flag} {team_str}'
    return team_str

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

def _ko_preview_card(team_name, ko):
    """生成对阵预览中的单队卡片。自动解析占位符、识别已填队名、处理待定"""
    import re as _re
    if not team_name:
        return '<div style="min-width:130px;max-width:190px;width:48%;height:64px;background:rgba(0,0,0,0.25);border-radius:12px;display:flex;align-items:center;justify-content:center;border:2px dashed rgba(255,255,255,0.15);padding:6px 10px;"><span style="color:#555;font-weight:bold;font-size:0.95em;">❓ 待定</span></div>'

    # 1. 尝试解析 knockout 占位符 → 实际队名
    resolved = resolve_knockout_team(ko, team_name)
    if resolved:
        return f'<div class="ko-card-locked"><div class="ko-card-flag">{resolved}</div></div>'

    # 2. 已填实际队名
    clean = clean_team(team_name)
    if clean and clean in FLAGS:
        return f'<div class="ko-card-locked"><div class="ko-card-flag">{flag(clean)} {clean}</div></div>'

    # 3. 占位符（如 "1/8胜者1", "半决赛负者1"）
    test = clean_team(team_name)
    if _re.search(r'(1/\d+|半决赛|季军赛|决赛)?(胜者|负者)\d+', test) or '胜者' in test or '负者' in test:
        return f'<div class="ko-card-next"><div class="ko-card-label">🔮 {test}</div></div>'

    # 4. 待定
    return '<div style="min-width:130px;max-width:190px;width:48%;height:64px;background:rgba(0,0,0,0.25);border-radius:12px;display:flex;align-items:center;justify-content:center;border:2px dashed rgba(255,255,255,0.15);padding:6px 10px;"><span style="color:#555;font-weight:bold;font-size:0.95em;">❓ 待定</span></div>'


def _ko_stage_preview(ko, stage_key, icon, label, dates, anchor, pair_count=0):
    """生成淘汰赛某阶段的对阵预览区域（首页用）"""
    s = ko[stage_key]
    matches = s['matches']

    if pair_count == 0:
        count = len(matches)
        # 统计已完赛和即将开赛的数量
        done = sum(1 for m in matches if m.get('status') == 'finished')
        live = sum(1 for m in matches if m.get('status') == 'live')
        suffix = ''
        if done > 0:
            suffix = f' ⚡{done}/{count}场已完赛'
        return f'''            <div style="margin-bottom:25px;">
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:15px;">
                    <span style="font-size:1.3em;">{icon}</span>
                    <span style="font-size:1.2em;color:#f59e0b;font-weight:bold;">{label}</span>
                    <span style="color:#888;font-size:0.9em;">⏰ {dates}</span>
                    {'<span style="background:#f59e0b;color:#1a1a2e;padding:4px 12px;border-radius:20px;font-size:0.8em;font-weight:bold;">🔥 进行中</span>' if live > 0 else ''}
                </div>
                <div class="nav-grid"><a href="knockout.html#{anchor}" class="nav-card">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div><div style="font-size:1.1em;font-weight:bold;">{icon} {label}</div><div style="font-size:0.85em;color:#aaa;">{dates} · {count}场{suffix}</div></div>
                        <span style="background:linear-gradient(135deg,#f59e0b,#d97706);color:#1a1a2e;padding:5px 14px;border-radius:20px;font-size:0.85em;font-weight:bold;">{count}场</span>
                    </div>
                </a></div>
            </div>'''

    # 对阵预览模式 — 显示所有对阵（pair_count 个）
    pairs_html = ''
    display_count = min(pair_count, len(matches))
    for i in range(display_count):
        m = matches[i]
        h = _ko_preview_card(m.get('home', ''), ko)
        a = _ko_preview_card(m.get('away', ''), ko)
        # 比赛时间（只取时间部分，去掉状态标签）
        time_str = m.get('time', '')
        # 提取纯时间，如 "7月5日 01:00 ✅ 已结束" → "7月5日 01:00"
        time_clean = time_str.split(' ✅')[0].split(' 🔴')[0] if time_str else ''
        
        # 状态与比分
        status = m.get('status', 'pending')
        extra = ''
        status_badge = ''
        if status == 'finished' and m.get('score_home') is not None:
            pk = ''
            if m.get('penalty_home') is not None:
                pk = f' (点球 {m["penalty_home"]}-{m["penalty_away"]})'
            extra = f'<div style="font-size:0.9em;color:#fbbf24;font-weight:bold;margin-top:4px;">✅ {m["score_home"]}:{m["score_away"]}{pk}</div>'
            status_badge = '<span style="font-size:0.65em;padding:2px 8px;border-radius:10px;background:rgba(34,197,94,0.15);color:#22c55e;">已结束</span>'
        elif status == 'live':
            extra = f'<div style="font-size:0.9em;color:#ef4444;font-weight:bold;margin-top:4px;">🔴 LIVE {m.get("score_home","?")}-{m.get("score_away","?")}</div>'
            status_badge = '<span style="font-size:0.65em;padding:2px 8px;border-radius:10px;background:rgba(239,68,68,0.15);color:#ef4444;">进行中</span>'
        else:
            status_badge = '<span style="font-size:0.65em;padding:2px 8px;border-radius:10px;background:rgba(245,158,11,0.12);color:#f59e0b;">即将开赛</span>'
        
        # 标签/备注
        tag = m.get('tag', '')
        tag_html = f'<div style="font-size:0.72em;color:#94a3b8;margin-top:4px;text-align:center;line-height:1.3;">{tag}</div>' if tag else ''
        
        pairs_html += f'''                <div class="ko-match-pair">
                    <div style="display:flex;align-items:center;justify-content:center;gap:10px;">
                        {h}
                        <div style="font-size:1em;font-weight:bold;color:#f59e0b;text-shadow:0 0 10px rgba(245,158,11,0.3);min-width:28px;text-align:center;">⚡</div>
                        {a}
                    </div>
                    {extra}
                    <div style="display:flex;align-items:center;gap:8px;margin-top:6px;">
                        {status_badge}
                        <span style="font-size:0.78em;color:#64748b;">{time_clean}</span>
                    </div>
                    {tag_html}
                </div>\n'''

    # 阶段统计
    done = sum(1 for m in matches if m.get('status') == 'finished')
    live = sum(1 for m in matches if m.get('status') == 'live')
    pending = len(matches) - done - live
    stage_badge = ''
    if live > 0:
        stage_badge = f'<span style="background:linear-gradient(135deg,#ef4444,#f87171);color:#fff;padding:4px 14px;border-radius:20px;font-size:0.8em;font-weight:bold;">🔴 进行中 {live}场</span>'
    elif done == len(matches):
        stage_badge = f'<span style="background:linear-gradient(135deg,#22c55e,#4ade80);color:#0a0a1a;padding:4px 14px;border-radius:20px;font-size:0.8em;font-weight:bold;">✅ 已结束</span>'
    else:
        stage_badge = f'<span style="background:linear-gradient(135deg,#f59e0b,#fbbf24);color:#0a0a1a;padding:4px 14px;border-radius:20px;font-size:0.8em;font-weight:bold;">⚡ {done}/{len(matches)} 已完赛</span>'

    return f'''            <div style="margin-bottom:32px;">
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:18px;flex-wrap:wrap;">
                    <span style="font-size:1.4em;">{icon}</span>
                    <span style="font-size:1.25em;color:#f59e0b;font-weight:bold;">{label}</span>
                    <span style="color:#888;font-size:0.9em;">⏰ {dates}</span>
                    {stage_badge}
                </div>
                <div style="background:linear-gradient(135deg,rgba(245,158,11,0.06),rgba(139,92,246,0.03));border-radius:20px;padding:28px 24px;border:1px solid rgba(245,158,11,0.15);">
                    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:16px;">
{pairs_html}                    </div>
                    <div style="text-align:center;margin-top:20px;">
                        <a href="knockout.html#{anchor}" style="color:#f59e0b;text-decoration:none;font-size:0.9em;padding:10px 24px;background:rgba(245,158,11,0.1);border-radius:20px;transition:all 0.3s;display:inline-block;" onmouseover="this.style.background='rgba(245,158,11,0.2)'" onmouseout="this.style.background='rgba(245,158,11,0.1)'">查看完整{label}对阵 ➜</a>
                    </div>
                </div>
            </div>'''


def gen_index(data, output_dir):
    """生成首页 index.html（淘汰赛专区+小组+日期）"""
    from datetime import datetime as _dt
    groups = data['groups']
    ko = data['knockout']

    # === 当前阶段判断 ===
    now = _dt.now()
    r16 = ko['round16']['matches']
    r8 = ko['round8']['matches']
    qf = ko['quarter']['matches']
    sf = ko['semi']['matches']
    fin = ko['final']['matches']

    r16_done = sum(1 for m in r16 if m.get('status') == 'finished')
    r16_live = sum(1 for m in r16 if m.get('status') == 'live')
    r8_done = sum(1 for m in r8 if m.get('status') == 'finished')
    all_matches = 104  # 总场次
    # 粗略计数已完赛场次
    total_done = 0
    for g in groups.values():
        total_done += sum(1 for m in g['matches'] if m.get('status') == 'finished')
    total_done += r16_done + r8_done + sum(1 for m in qf if m.get('status') == 'finished')
    total_done += sum(1 for m in sf if m.get('status') == 'finished')
    total_done += sum(1 for m in fin if m.get('status') == 'finished')
    progress_pct = min(100, round(total_done / all_matches * 100))

    # 当前活跃阶段
    if r16_live > 0:
        stage_info = ('⚔️', '1/16决赛进行中', f'已完成 {r16_done}/16 场', 'live')
    elif r16_done < 16:
        stage_info = ('⚔️', '1/16决赛阶段', f'已完成 {r16_done}/16 场，剩余 {16-r16_done} 场', 'upcoming')
    elif r16_done >= 16 and r8_done < 8:
        stage_info = ('🎯', '1/8决赛阶段', f'已完成 {r8_done}/8 场', 'upcoming')
    elif r8_done >= 8:
        stage_info = ('💎', '1/4决赛阶段', '激烈角逐中', 'upcoming')
    else:
        stage_info = ('⚔️', '1/16决赛阶段', '淘汰赛火热进行中', 'upcoming')

    # === 小组卡片（加国旗） ===
    group_cards = ''
    for g in 'ABCDEFGHIJKL':
        gd = groups[g]
        teams_with_flags = '  '.join(f'{flag(t)}{t}' for t in gd['teams'])
        group_cards += f'''            <a href="group-{g.lower()}.html" class="nav-card">
                <div style="display:flex;align-items:center;gap:12px;">
                    <div style="background:linear-gradient(135deg,#f59e0b,#d97706);color:#0a0a1a;width:44px;height:44px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:1.1em;flex-shrink:0;">{g}</div>
                    <div style="min-width:0;">
                        <div style="font-size:1.1em;font-weight:bold;color:#fbbf24;">{g}组</div>
                        <div style="font-size:0.8em;color:#64748b;margin-top:4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{teams_with_flags}</div>
                    </div>
                </div>
            </a>\n'''

    # === 日期卡片 ===
    day_icons = {
        '0612': '🎆', '0613': '☀️', '0614': '⚽', '0615': '🔥',
        '0616': '⚽', '0617': '🌟', '0618': '💫', '0619': '⚽',
        '0620': '⚽', '0621': '⚽', '0622': '⚽', '0623': '⚽',
        '0624': '⚽', '0625': '⚡', '0626': '⚡', '0627': '🔥', '0628': '🏁',
    }
    day_labels = {
        '0612': ('6月12日', '周五', '揭幕战'),
        '0613': ('6月13日', '周六', ''),
        '0614': ('6月14日', '周日', ''),
        '0615': ('6月15日', '周一', ''),
        '0616': ('6月16日', '周二', ''),
        '0617': ('6月17日', '周三', '梅西首秀'),
        '0618': ('6月18日', '周四', 'C罗最后一届'),
        '0619': ('6月19日', '周五', ''),
        '0620': ('6月20日', '周六', ''),
        '0621': ('6月21日', '周日', ''),
        '0622': ('6月22日', '周一', ''),
        '0623': ('6月23日', '周二', ''),
        '0624': ('6月24日', '周三', ''),
        '0625': ('6月25日', '周四', '小组收官'),
        '0626': ('6月26日', '周五', '小组收官'),
        '0627': ('6月27日', '周六', '姆巴佩vs哈兰德'),
        '0628': ('6月28日', '周日', '小组赛收官'),
    }

    date_cards = ''
    for key in sorted(data['dates'].keys()):
        dd = data['dates'][key]
        if key in day_labels:
            day, week, highlight = day_labels[key]
        else:
            day = f'{key[:2]}月{key[2:]}日'; week = ''; highlight = ''
        icon = day_icons.get(key, '📅')
        date_cards += f'''            <a href="date-{key}.html" class="nav-card">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <div style="font-size:1.1em;font-weight:bold;">{icon} {day}</div>
                        <div style="font-size:0.85em;color:#64748b;">{week}{' · '+highlight if highlight else ''}</div>
                    </div>
                    <span style="background:rgba(245,158,11,0.15);color:#f59e0b;padding:4px 12px;border-radius:20px;font-size:0.8em;font-weight:bold;">{len(dd['matches'])}场</span>
                </div>
            </a>\n'''

    # === 淘汰赛各阶段预览 ===
    # 每个阶段显示全部对阵
    ko_stages = [
        ('round16', '⚔️', '1/16决赛', '6月29日-7月4日', 'round16', 16),
        ('round8', '🎯', '1/8决赛', '7月5日-7月8日', 'round8', 8),
        ('quarter', '💎', '1/4决赛', '7月10日-7月12日', 'quarter', 4),
        ('semi', '🌟', '半决赛', '7月15日-7月16日', 'semi', 2),
        ('third', '🥉', '季军赛', '7月19日', 'third', 1),
        ('final', '🏆', '决赛', '7月20日', 'final', 1),
    ]
    ko_sections = '\n'.join(_ko_stage_preview(ko, *args) for args in ko_stages)

    # === 阶段指示器 HTML ===
    stage_color = '#ef4444' if stage_info[3] == 'live' else '#f59e0b'
    stage_html = f'''        <div class="stage-indicator">
            <span style="font-size:1.5em;">{stage_info[0]}</span>
            <span class="stage-dot" style="background:{stage_color};{ 'animation:pulse 1.5s ease-in-out infinite;box-shadow:0 0 12px '+stage_color+';' if stage_info[3]=='live' else '' }"></span>
            <span class="stage-label" style="color:{stage_color};">{stage_info[1]}</span>
            <span style="color:#94a3b8;font-size:0.9em;">· {stage_info[2]}</span>
            <span style="margin-left:auto;color:#64748b;font-size:0.85em;">📊 进度 {progress_pct}%</span>
        </div>'''

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏆 2026年美加墨世界杯 · 赛程</title>
    {COMMON_CSS}
</head>
<body>
    <div class="container">
        <div class="header">
            <div style="font-size:0.9em;color:#f59e0b;letter-spacing:4px;margin-bottom:8px;">⚽ FIFA WORLD CUP 2026 ⚽</div>
            <h1>🏆 2026年美加墨世界杯</h1>
            <div class="subtitle">United States · Mexico · Canada</div>
            <div class="dates">🇺🇸🇲🇽🇨🇦 2026.06.12 — 07.20  ·  48支球队  ·  104场比赛</div>
        </div>

{stage_html}

        <div class="info-bar">
            <div class="info-item"><div class="label">🏟️ 已完赛</div><div class="value">{total_done}/{all_matches}</div></div>
            <div class="info-item"><div class="label">⚽ 总进球</div><div class="value">—</div></div>
            <div class="info-item"><div class="label">🌍 参赛国</div><div class="value">48</div></div>
            <div class="info-item"><div class="label">🏆 决赛</div><div class="value">07.20</div></div>
        </div>

        <div class="nav-section">
            <div class="nav-title">🏆 淘汰赛专区 <span style="font-size:0.7em;color:#64748b;font-weight:normal;">KNOCKOUT STAGE</span></div>
{ko_sections}
        </div>

        <div class="nav-section">
            <div class="nav-title">🌍 小组赛回顾 <span style="font-size:0.7em;color:#64748b;font-weight:normal;">GROUP STAGE</span></div>
            <div class="nav-grid">
{group_cards}            </div>
        </div>

        <div class="nav-section">
            <div class="nav-title">📅 按日期查看 <span style="font-size:0.7em;color:#64748b;font-weight:normal;">BY DATE</span></div>
            <div class="nav-grid">
{date_cards}            </div>
        </div>

        <div class="footer">
            <p>⚽ 2026年美加墨世界杯 · 北京时间 (UTC+8)</p>
            <p style="margin-top:6px;">📌 赛事时间以官方公布为准 · 🔄 每日自动更新</p>
            <p style="margin-top:10px;color:#475569;">Made with ❤️ by GG-Bond</p>
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

def resolve_knockout_team(ko, ref_str):
    """解析占位符如 '1/16胜者11' → 实际队名（含国旗）；无法确定返回 None"""
    import re
    m = re.match(r'(1/16|1/8|1/4|半决赛|季军赛|决赛)?(胜者|负者)(\d+)', ref_str)
    if not m:
        return None  # 不是占位符

    stage_map = {'1/16': 'round16', '1/8': 'round8', '1/4': 'quarter',
                 '半决赛': 'semi', '季军赛': 'third', '决赛': 'final'}
    prefix = m.group(1) or ''
    outcome = m.group(2)  # '胜者' or '负者'
    num = int(m.group(3))  # 1-based
    idx = num - 1

    # 推断来源阶段
    stage = None
    for k, v in stage_map.items():
        if prefix == k:
            stage = v
            break
    if stage is None:
        return None

    try:
        src = ko[stage]['matches'][idx]
    except (KeyError, IndexError):
        return None

    if src.get('status') != 'finished':
        return None

    sh = src.get('score_home')
    sa = src.get('score_away')
    if sh is None or sa is None or sh == sa:
        return None  # 平局无法自动判断（需看点球）

    if outcome == '胜者':
        return src['home'] if sh > sa else src['away']
    else:
        return src['away'] if sh > sa else src['home']


def gen_knockout(data, output_dir):
    """生成淘汰赛页面（自动级联解析）"""
    ko_css = '''<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Microsoft YaHei', 'PingFang SC', 'Segoe UI', sans-serif; background: linear-gradient(160deg, #0a0a1a 0%, #0f172a 30%, #1a1040 60%, #0f172a 100%); min-height: 100vh; color: #e2e8f0; overflow-x:hidden; }
.container { max-width: 1100px; margin: 0 auto; padding: 20px; }

/* 动态背景 */
body::before { content:''; position:fixed; top:0; left:0; width:100%; height:100%; background: radial-gradient(ellipse at 20% 20%, rgba(245,158,11,0.08) 0%, transparent 50%), radial-gradient(ellipse at 80% 80%, rgba(139,92,246,0.06) 0%, transparent 50%); pointer-events:none; z-index:0; }

/* 头部 */
.header { text-align: center; padding: 40px 20px; background: radial-gradient(ellipse at center, rgba(245,158,11,0.15) 0%, transparent 70%); border-radius: 20px; margin-bottom: 30px; position:relative; overflow:hidden; }
.header::before { content:''; position:absolute; top:-30%; left:-30%; width:160%; height:160%; background: conic-gradient(from 0deg, transparent, rgba(245,158,11,0.08), transparent, rgba(139,92,246,0.06), transparent); animation: headerSpin 15s linear infinite; }
@keyframes headerSpin { from{transform:rotate(0deg)} to{transform:rotate(360deg)} }
.header > * { position:relative; z-index:1; }
.header h1 { font-size: 2.8em; background: linear-gradient(135deg, #fbbf24, #f59e0b, #d97706, #fbbf24); background-size: 300% 300%; -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 10px; animation: shimmer 3s ease infinite; }
@keyframes shimmer { 0%,100%{background-position:0% 50%} 50%{background-position:100% 50%} }
.back-link { display: inline-block; margin-bottom: 20px; color: #f59e0b; text-decoration: none; padding: 8px 18px; background: rgba(245,158,11,0.1); border-radius: 10px; transition:all 0.3s; position:relative; z-index:2; }
.back-link:hover { background: rgba(245,158,11,0.2); }

/* 阶段区块 */
.stage-section { background: rgba(255,255,255,0.03); border-radius: 20px; padding: 28px; margin-bottom: 24px; border:1px solid rgba(255,255,255,0.06); position:relative; overflow:hidden; }
.stage-section::before { content:''; position:absolute; top:0; left:0; width:100%; height:3px; background: linear-gradient(90deg, transparent, rgba(245,158,11,0.5), transparent); }
.stage-section.round16 { border-color: rgba(245,158,11,0.15); }
.stage-section.round16::before { background: linear-gradient(90deg, transparent, #f59e0b, transparent); }
.stage-section.round8 { border-color: rgba(139,92,246,0.15); }
.stage-section.round8::before { background: linear-gradient(90deg, transparent, #8b5cf6, transparent); }
.stage-section.quarter { border-color: rgba(236,72,153,0.15); }
.stage-section.quarter::before { background: linear-gradient(90deg, transparent, #ec4899, transparent); }
.stage-section.semi { border-color: rgba(59,130,246,0.2); }
.stage-section.semi::before { background: linear-gradient(90deg, transparent, #3b82f6, transparent); }
.stage-section.final::before, .stage-section.third::before { background: linear-gradient(90deg, transparent, #fbbf24, transparent, #ef4444); }
.stage-title { color: #f59e0b; font-size: 1.5em; margin-bottom: 22px; padding-bottom: 12px; border-bottom: 1px solid rgba(245,158,11,0.15); display: flex; align-items: center; gap: 12px; flex-wrap:wrap; }
.stage-badge { background: linear-gradient(135deg, #f59e0b, #d97706); color: #0a0a1a; padding: 6px 18px; border-radius: 25px; font-size: 0.85em; font-weight: bold; box-shadow: 0 4px 15px rgba(245,158,11,0.3); }
.stage-badge.final { background: linear-gradient(135deg, #fbbf24, #f59e0b, #ef4444); animation: finalPulse 2s ease-in-out infinite; }
.stage-badge.third { background: linear-gradient(135deg, #cd7f32, #b8860b); }
@keyframes finalPulse { 0%,100%{box-shadow:0 4px 15px rgba(245,158,11,0.4)} 50%{box-shadow:0 4px 25px rgba(245,158,11,0.7)} }

/* 进度条 */
.stage-progress { height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; margin-top: 20px; overflow: hidden; }
.stage-progress-bar { height: 100%; border-radius: 3px; transition: width 0.5s ease; }
.stage-progress-done { background: linear-gradient(90deg, #22c55e, #4ade80); }
.stage-progress-live { background: linear-gradient(90deg, #ef4444, #f87171); animation: pulse 1s infinite; }
.stage-progress-pending { background: linear-gradient(90deg, #6366f1, #8b5cf6); }

/* 比赛卡片 */
.match-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 16px; }
.match-item { background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02)); border-radius: 16px; padding: 22px; border:1px solid rgba(255,255,255,0.06); transition:all 0.4s cubic-bezier(0.4,0,0.2,1); position:relative; overflow:hidden; }
.match-item::before { content:''; position:absolute; top:0; left:0; width:4px; height:100%; background: #8b5cf6; transition:all 0.3s; }
.match-item:hover { background: linear-gradient(135deg, rgba(255,255,255,0.08), rgba(255,255,255,0.04)); transform: translateY(-3px); box-shadow: 0 12px 40px rgba(0,0,0,0.3); }
.match-item:hover::before { width:6px; background: #f59e0b; }
.match-item.finished { opacity:0.9; }
.match-item.finished::before { background: #22c55e; }
.match-item.live { border-color: rgba(239,68,68,0.3); animation: liveGlow 2s ease-in-out infinite; }
.match-item.live::before { background: #ef4444; }
@keyframes liveGlow { 0%,100%{box-shadow:0 0 15px rgba(239,68,68,0.2)} 50%{box-shadow:0 0 30px rgba(239,68,68,0.4)} }
.match-item.highlight { border-color: rgba(245,158,11,0.2); background: linear-gradient(135deg, rgba(245,158,11,0.08), rgba(217,119,6,0.03)); }
.match-item.highlight::before { background: #f59e0b; }
.match-item.final-item { border-color: rgba(251,191,36,0.3); background: linear-gradient(135deg, rgba(245,158,11,0.12), rgba(239,68,68,0.06)); box-shadow: 0 0 40px rgba(245,158,11,0.1); }
.match-item.final-item::before { background: linear-gradient(180deg, #fbbf24, #f59e0b); }
.match-item.third-item { border-color: rgba(205,127,50,0.3); background: linear-gradient(135deg, rgba(205,127,50,0.08), rgba(184,134,11,0.04)); }
.match-item.third-item::before { background: linear-gradient(180deg, #cd7f32, #b8860b); }

/* 比分和时间 */
.match-time { color: #f59e0b; font-weight: bold; margin-bottom: 14px; font-size: 0.95em; display:flex; align-items:center; gap:8px; }
.match-teams { display: flex; justify-content: space-between; align-items: center; font-size: 1.15em; margin-bottom: 12px; }
.match-team { display:flex; align-items:center; gap:10px; flex:1; }
.match-team.right { justify-content: flex-end; text-align:right; }
.match-team-name { font-weight: 500; }
.match-vs { color: #64748b; font-size: 0.85em; font-weight: bold; }
.match-score { font-size: 1.4em; font-weight: bold; color: #f59e0b; margin: 12px 0; text-align:center; padding: 10px; background: rgba(245,158,11,0.1); border-radius: 10px; }
.match-score.final-score { color: #fbbf24; font-size: 1.8em; text-shadow: 0 0 20px rgba(245,158,11,0.5); background: linear-gradient(135deg, rgba(251,191,36,0.15), rgba(245,158,11,0.08)); animation: scoreGlow 2s ease-in-out infinite; }
@keyframes scoreGlow { 0%,100%{box-shadow:0 0 15px rgba(251,191,36,0.2)} 50%{box-shadow:0 0 30px rgba(251,191,36,0.4)} }
.match-score.pending { color: #475569; font-size: 1em; background: rgba(255,255,255,0.03); }
.match-badge { display: inline-block; padding: 5px 14px; border-radius: 15px; font-size: 0.82em; margin-bottom: 12px; font-weight:bold; }
.match-badge.live { background: rgba(239,68,68,0.15); color: #ef4444; animation: pulse 2s infinite; }
.match-badge.done { background: rgba(34,197,94,0.15); color: #22c55e; }
.match-badge.upcoming { background: rgba(139,92,246,0.12); color: #a78bfa; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.5} }
.events-line { color: #94a3b8; font-size: 0.82em; margin-top: 10px; line-height: 1.5; }

/* 决赛特有 */
.final-crown { font-size: 2em; text-align: center; margin-bottom: 10px; animation: float 3s ease-in-out infinite; }
@keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-8px)} }
.final-venue { margin-top: 14px; color: #fbbf24; font-weight: bold; display: flex; align-items: center; gap: 8px; justify-content: center; }
.final-date { color: #f59e0b; font-size: 1.1em; font-weight: bold; margin-bottom: 8px; }

/* 页脚 */
.footer { text-align: center; color: #555; padding: 30px 20px; margin-top: 30px; font-size:0.85em; border-top:1px solid rgba(255,255,255,0.05); }

/* 响应式 */
@media (max-width: 768px) { .match-grid { grid-template-columns: 1fr; } .header h1 { font-size: 2em; } .stage-title { font-size: 1.3em; } }
</style>'''

    ko = data['knockout']
    stages_html = ''

    for stage_key in ['round16', 'round8', 'quarter', 'semi', 'third', 'final']:
        s = ko[stage_key]
        matches = s['matches']
        stage_class = stage_key  # round16, round8, quarter, semi, final, third
        badge_class = 'final' if stage_key in ('final', 'third') else ''

        # 计算进度
        done = sum(1 for m in matches if m.get('status') == 'finished')
        live = sum(1 for m in matches if m.get('status') == 'live')
        total = len(matches)
        progress_class = 'stage-progress-live' if live > 0 else ('stage-progress-done' if done == total else 'stage-progress-pending')
        progress_width = min(100, (done + live) / total * 100) if total > 0 else 0

        matches_html = ''
        for idx, m in enumerate(matches):
            # 自动解析占位符
            home_raw = m['home']
            away_raw = m['away']
            home_display = resolve_knockout_team(ko, home_raw) or home_raw
            away_display = resolve_knockout_team(ko, away_raw) or away_raw

            # 添加国旗
            home_html = _add_flag_to_team(home_display)
            away_html = _add_flag_to_team(away_display)

            status = m.get('status')
            sh = m.get('score_home')
            sa = m.get('score_away')
            events = m.get('events', '')
            pk = m.get('penalty', '')
            has_pk = m.get('penalty_home') is not None

            # 判断 item class
            is_final = stage_key == 'final'
            is_third = stage_key == 'third'
            item_class = 'final-item' if is_final else ('third-item' if is_third else ('highlight' if stage_key == 'semi' else ''))
            if status == 'finished':
                item_class += ' finished'
            if status == 'live':
                item_class += ' live'

            # 状态徽章
            if status == 'finished':
                badge_html = '<span class="match-badge done">✅ 已结束</span>'
            elif status == 'live':
                badge_html = '<span class="match-badge live">🔴 LIVE 正在直播</span>'
            else:
                badge_html = '<span class="match-badge upcoming">⏳ 即将开赛</span>'

            # 比分行
            if status == 'finished' and sh is not None and sa is not None:
                score_class = 'final-score' if is_final else ''
                pk_str = ''
                if has_pk:
                    pk_str = f' <span style="font-size:0.8em;color:#fbbf24;">(点球 {m["penalty_home"]}-{m["penalty_away"]})</span>'
                score_html = f'<div class="match-score {score_class}">{sh} - {sa}{pk_str}</div>'
            elif status == 'live' and sh is not None and sa is not None:
                score_html = f'<div class="match-score" style="color:#ef4444;">{sh} - {sa}</div>'
            else:
                score_html = '<div class="match-score pending">⚽ 等待开赛 ⚽</div>'

            # 事件描述
            events_html = ''
            if events:
                events_html = f'<div class="events-line">📝 {events}</div>'

            pk_info = ''
            if pk and status == 'finished':
                pk_info = f'<div class="events-line" style="color:#fbbf24;">⚽ 点球：{pk}</div>'

            # 决赛特殊内容
            extra_html = ''
            if is_final:
                extra_html = f'''                    <div class="final-crown">👑</div>
                    <div class="final-date">📅 {m.get('time', '7月20日 03:00')}</div>
                    <div class="final-venue">📍 {ko['final'].get('venue', '纽约大都会人寿体育场')}</div>'''
            elif is_third:
                extra_html = f'<div class="final-venue" style="color:#cd7f32;">📍 {m.get("time", "7月19日 03:00")} · {ko["third"].get("venue", "纽约大都会人寿体育场")}</div>'

            matches_html += f'''                <div class="match-item {item_class}" id="{stage_key}{'-'+str(idx+1) if idx > 0 else ''}">
                    {badge_html}
                    <div class="match-teams">
                        <div class="match-team"><span>{home_html}</span></div>
                        <span class="match-vs">VS</span>
                        <div class="match-team right"><span>{away_html}</span></div>
                    </div>
                    {score_html}
                    {pk_info}
                    {events_html}
                    {extra_html}
                </div>\n'''

        # 添加进度条
        progress_html = f'''            <div class="stage-progress">
                <div class="stage-progress-bar {progress_class}" style="width: {progress_width}%;"></div>
            </div>
            <div style="margin-top:8px;font-size:0.8em;color:#64748b;text-align:right;">{done}{'✅' if done==total else ''} / {total} 场 {live if live>0 else ''} {'🔥进行中' if live>0 else ''}</div>'''

        stages_html += f'''        <div class="stage-section {stage_class}">
            <div class="stage-title">
                <span class="stage-badge {badge_class}">{s['icon']} {s['label']}</span>
                <span style="color:#94a3b8;font-size:0.85em;font-weight:normal;margin-left:auto;">{s['dates']}</span>
            </div>
            <div class="match-grid">
{matches_html}            </div>
            {progress_html}
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
            <p>🔄 每日自动更新 · 对阵自动级联解析</p>
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