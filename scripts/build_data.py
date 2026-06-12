# -*- coding: utf-8 -*-
"""直接构建完整世界杯数据 JSON"""
import json, re, os
from pathlib import Path

PROJECT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent

GROUPS = {
    'A': ['墨西哥', '南非', '韩国', '捷克'],
    'B': ['加拿大', '波黑', '卡塔尔', '瑞士'],
    'C': ['巴西', '摩洛哥', '海地', '苏格兰'],
    'D': ['美国', '巴拉圭', '澳大利亚', '土耳其'],
    'E': ['德国', '科特迪瓦', '厄瓜多尔', '库拉索'],
    'F': ['荷兰', '日本', '突尼斯', '瑞典'],
    'G': ['比利时', '埃及', '伊朗', '新西兰'],
    'H': ['西班牙', '沙特', '乌拉圭', '佛得角'],
    'I': ['法国', '塞内加尔', '挪威', '伊拉克'],
    'J': ['阿根廷', '阿尔及利亚', '奥地利', '约旦'],
    'K': ['葡萄牙', '刚果金', '乌兹别克斯坦', '哥伦比亚'],
    'L': ['英格兰', '克罗地亚', '巴拿马', '加纳'],
}

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

def strip_html(text):
    return re.sub(r'<[^>]+>', '', text).strip()

def parse_matches_from_html(filepath):
    """从紧凑的 HTML 中提取比赛数据"""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    matches = []
    # 按 class="match-item 分割
    parts = re.split(r'<div class="match-item[^"]*"[^>]*>', html)[1:]
    
    for part in parts:
        # 截取到对应的 </div> 闭合（近似）
        m = {'status': 'pending'}
        
        # 时间
        tm = re.search(r'class="match-time">(.*?)</div>', part)
        if tm:
            time_text = strip_html(tm.group(1))
            m['time'] = time_text
            if '已结束' in time_text:
                m['status'] = 'finished'
            dm = re.search(r'(\d+)月(\d+)日\s*(\d{2}:\d{2})', time_text)
            if dm:
                m['month'] = int(dm.group(1))
                m['day'] = int(dm.group(2))
                m['kickoff'] = dm.group(3)
        
        # 球队
        team_spans = re.findall(r'<span>([^<]*)</span>', part)
        teams = []
        for t in team_spans:
            t = t.strip()
            if any(f in t for f in FLAGS.values()) or any(n in t for n in FLAGS.keys()):
                teams.append(t)
        if len(teams) >= 2:
            m['home'] = teams[0]
            m['away'] = teams[1]
        
        # 比分
        for sp in team_spans:
            sc = re.search(r'(\d+)\s*[-:]\s*(\d+)', sp.strip())
            if sc:
                m['score_home'] = int(sc.group(1))
                m['score_away'] = int(sc.group(2))
                m['status'] = 'finished'
        
        # 状态文字
        if '等待开赛' in part:
            if m.get('status') != 'finished':
                m['status'] = 'pending'
        if '已结束' in part and '等待开赛' not in part:
            m['status'] = 'finished'
        
        # 场馆
        vm = re.search(r'class="match-venue">([^<]*)</div>', part)
        if vm:
            m['venue'] = strip_html(vm.group(1))
        
        # 高亮
        if 'match-highlight' in part or '🔥' in part:
            m['highlight'] = True
        
        # 标签
        tg = re.search(r'class="match-tag">([^<]*)</span>', part)
        if tg:
            m['tag'] = strip_html(tg.group(1))
        
        # 赛事详情
        rm = re.search(r'class="match-result">([^<]*)</div>', part)
        if rm:
            m['events'] = strip_html(rm.group(1))
        
        if m.get('home'):
            matches.append(m)
    
    return matches


def build_data():
    world_cup_dir = PROJECT_DIR / 'world_cup'
    data = {'groups': {}, 'dates': {}, 'knockout': {}}
    
    # 解析小组 HTML
    for gname in GROUPS:
        fpath = world_cup_dir / f'group-{gname.lower()}.html'
        if fpath.exists():
            matches = parse_matches_from_html(str(fpath))
            for m in matches:
                m['group'] = f'{gname}组'
                # 补充日期时间
                if 'time' in m and 'month' not in m:
                    dm = re.search(r'(\d+)月(\d+)日\s*(\d{2}:\d{2})', m['time'])
                    if dm:
                        m['month'] = int(dm.group(1))
                        m['day'] = int(dm.group(2))
                        m['kickoff'] = dm.group(3)
            data['groups'][gname] = {
                'teams': GROUPS[gname],
                'matches': matches
            }
            print(f"  ✅ {gname}组: {len(matches)} 场比赛")
        else:
            print(f"  ❌ {gname}组: 文件不存在")
    
    # 解析日期 HTML  
    for f in sorted(world_cup_dir.glob('date-*.html')):
        key = f.stem.replace('date-', '')
        matches = parse_matches_from_html(str(f))
        for m in matches:
            if 'group' not in m:
                m['group'] = ''
        data['dates'][key] = {'matches': matches}
        print(f"  ✅ {key}: {len(matches)} 场")
    
    # 淘汰赛
    kf = world_cup_dir / 'knockout.html'
    if kf.exists():
        ko_matches = parse_matches_from_html(str(kf))
    else:
        ko_matches = []
    
    data['knockout'] = {
        'round16': {'label': '1/16决赛', 'dates': '6月29日 - 7月4日', 'icon': '⚔️', 'matches': [
            {'time':'6月29日 03:00','home':'A组第1','away':'B组第2'},
            {'time':'6月29日 08:00','home':'B组第1','away':'A组第2'},
            {'time':'6月30日 03:00','home':'C组第1','away':'D组第2'},
            {'time':'6月30日 08:00','home':'D组第1','away':'C组第2'},
            {'time':'7月1日 03:00','home':'E组第1','away':'F组第2'},
            {'time':'7月1日 08:00','home':'F组第1','away':'E组第2'},
            {'time':'7月2日 03:00','home':'G组第1','away':'H组第2'},
            {'time':'7月2日 08:00','home':'H组第1','away':'G组第2'},
            {'time':'7月3日 03:00','home':'I组第1','away':'J组第2'},
            {'time':'7月3日 08:00','home':'J组第1','away':'I组第2'},
            {'time':'7月4日 03:00','home':'K组第1','away':'L组第2'},
            {'time':'7月4日 08:00','home':'L组第1','away':'K组第2'},
        ]},
        'round8': {'label': '1/8决赛', 'dates': '7月5日 - 7月8日', 'icon': '🎯', 'matches': [
            {'time':'7月5日 03:00','home':'1/16胜者1','away':'1/16胜者2'},
            {'time':'7月5日 08:00','home':'1/16胜者3','away':'1/16胜者4'},
            {'time':'7月6日 03:00','home':'1/16胜者5','away':'1/16胜者6'},
            {'time':'7月6日 08:00','home':'1/16胜者7','away':'1/16胜者8'},
            {'time':'7月7日 03:00','home':'1/16胜者9','away':'1/16胜者10'},
            {'time':'7月7日 08:00','home':'1/16胜者11','away':'1/16胜者12'},
            {'time':'7月8日 03:00','home':'1/16胜者13','away':'1/16胜者14'},
            {'time':'7月8日 08:00','home':'1/16胜者15','away':'1/16胜者16'},
        ]},
        'quarter': {'label': '1/4决赛', 'dates': '7月10日 - 7月12日', 'icon': '💎', 'matches': [
            {'time':'7月10日 03:00','home':'1/8胜者1','away':'1/8胜者2'},
            {'time':'7月10日 08:00','home':'1/8胜者3','away':'1/8胜者4'},
            {'time':'7月11日 03:00','home':'1/8胜者5','away':'1/8胜者6'},
            {'time':'7月11日 08:00','home':'1/8胜者7','away':'1/8胜者8'},
        ]},
        'semi': {'label': '半决赛', 'dates': '7月15日 - 7月16日', 'icon': '🌟', 'matches': [
            {'time':'7月15日 03:00','home':'1/4胜者1','away':'1/4胜者2'},
            {'time':'7月16日 03:00','home':'1/4胜者3','away':'1/4胜者4'},
        ]},
        'third': {'label': '季军赛', 'dates': '7月19日', 'icon': '🥉', 'matches': [
            {'time':'7月19日 03:00','home':'半决赛负者1','away':'半决赛负者2'},
        ]},
        'final': {'label': '决赛', 'dates': '7月20日', 'icon': '🏆', 'venue': '纽约大都会人寿体育场', 'matches': [
            {'time':'7月20日 03:00','home':'半决赛胜者1','away':'半决赛胜者2'},
        ]},
    }
    
    return data


if __name__ == '__main__':
    print("🔍 从 HTML 提取完整比赛数据...\n")
    data = build_data()
    
    output_path = PROJECT_DIR / 'data' / 'matches.json'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(str(output_path), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    total = sum(len(g['matches']) for g in data['groups'].values())
    print(f"\n✅ matches.json 已保存")
    print(f"   小组: 12 个, 比赛: {total} 场")
    print(f"   日期: {len(data['dates'])} 页")
