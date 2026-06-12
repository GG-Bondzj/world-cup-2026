# -*- coding: utf-8 -*-
"""
从日期 HTML 文件重建完整赛程 JSON（日期页解析最可靠）。
"""
import json
import re
import os
from pathlib import Path

PROJECT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent

FLAG_NAMES = {
    '🇲🇽': '墨西哥', '🇿🇦': '南非', '🇰🇷': '韩国', '🇨🇿': '捷克',
    '🇨🇦': '加拿大', '🇧🇦': '波黑', '🇶🇦': '卡塔尔', '🇨🇭': '瑞士',
    '🇧🇷': '巴西', '🇲🇦': '摩洛哥', '🇭🇹': '海地',
    '🇺🇸': '美国', '🇵🇾': '巴拉圭', '🇦🇺': '澳大利亚', '🇹🇷': '土耳其',
    '🇩🇪': '德国', '🇨🇮': '科特迪瓦', '🇪🇨': '厄瓜多尔', '🇨🇼': '库拉索',
    '🇳🇱': '荷兰', '🇯🇵': '日本', '🇹🇳': '突尼斯', '🇸🇪': '瑞典',
    '🇧🇪': '比利时', '🇪🇬': '埃及', '🇮🇷': '伊朗', '🇳🇿': '新西兰',
    '🇪🇸': '西班牙', '🇸🇦': '沙特', '🇺🇾': '乌拉圭', '🇨🇻': '佛得角',
    '🇫🇷': '法国', '🇸🇳': '塞内加尔', '🇳🇴': '挪威', '🇮🇶': '伊拉克',
    '🇦🇷': '阿根廷', '🇩🇿': '阿尔及利亚', '🇦🇹': '奥地利', '🇯🇴': '约旦',
    '🇵🇹': '葡萄牙', '🇨🇩': '刚果金', '🇺🇿': '乌兹别克斯坦', '🇨🇴': '哥伦比亚',
    '🇭🇷': '克罗地亚', '🇵🇦': '巴拿马', '🇬🇭': '加纳',
}

# 小组队伍
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

def extract_team_name(text):
    """从包含国旗的文本中提取纯队名"""
    text = text.strip()
    # 去掉国旗
    for flag in FLAG_NAMES:
        text = text.replace(flag, '')
    return text.strip()

def get_flag(name):
    """获取国旗"""
    for flag, n in FLAG_NAMES.items():
        if n == name:
            return flag
    return '🏴' if '苏格兰' in name or '英格兰' in name else name

def parse_group_html(filepath):
    """用逐行解析方式解析小组 HTML"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    matches = []
    
    # 找到所有 match-item 块
    # 使用简单的状态机
    lines = content.split('\n')
    in_match = False
    match_block = ''
    depth = 0
    
    for line in lines:
        if '<div class="match-item' in line:
            in_match = True
            match_block = line
            depth = 1
            continue
        
        if in_match:
            match_block += '\n' + line
            depth += line.count('<div') - line.count('</div')
            
            if depth <= 0:
                in_match = False
                # 解析这个 block
                m = {}
                
                # 时间
                tm = re.search(r'class="match-time">(.*?)</div>', match_block)
                if tm:
                    time_text = tm.group(1).strip()
                    m['time'] = time_text
                    # 解析日期时间
                    dm = re.search(r'(\d+)月(\d+)日\s*(\d{2}:\d{2})', time_text)
                    if dm:
                        m['month'] = int(dm.group(1))
                        m['day'] = int(dm.group(2))
                        m['kickoff'] = dm.group(3)
                    if '已结束' in time_text:
                        m['status'] = 'finished'
                
                # 球队 - 从 <span> 中提取包含国旗的
                all_spans = re.findall(r'<span[^>]*>(.*?)</span>', match_block)
                
                # 找队名
                team_spans = []
                for s in all_spans:
                    s_stripped = s.strip()
                    # 检查是否包含国旗或已知队名
                    has_flag = any(flag in s_stripped for flag in FLAG_NAMES)
                    has_name = any(name in s_stripped for name in FLAG_NAMES.values())
                    if has_flag or has_name:
                        team_spans.append(s_stripped)
                
                if len(team_spans) >= 2:
                    m['home'] = team_spans[0]
                    m['away'] = team_spans[1]
                
                # 比分
                for sp in all_spans:
                    sp = sp.strip()
                    sc = re.match(r'^(\d+)\s*[-:]\s*(\d+)$', sp)
                    if sc or re.search(r'\d+[-:]\d+', sp):
                        nums = re.findall(r'(\d+)[-:](\d+)', sp)
                        if nums:
                            m['score_home'] = int(nums[0][0])
                            m['score_away'] = int(nums[0][1])
                            m['status'] = 'finished'
                
                # 判断状态
                if '等待开赛' in match_block or 'pending' in match_block:
                    if m.get('status') != 'finished':
                        m['status'] = 'pending'
                
                # 场馆
                vm = re.search(r'class="match-venue">(.*?)</div>', match_block)
                if vm:
                    m['venue'] = vm.group(1).strip()
                
                # 高亮
                if 'match-highlight' in match_block or 'highlight' in match_block.lower():
                    m['highlight'] = True
                
                # 赛事结果详情
                rm = re.search(r'class="match-result">(.*?)</div>', match_block)
                if rm:
                    m['events'] = rm.group(1).strip()
                
                if m.get('home') and m.get('away'):
                    matches.append(m)
                else:
                    m['_debug'] = match_block[:200]
                    matches.append(m)
    
    return matches


def parse_date_html(filepath):
    """解析日期 HTML"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    matches = []
    lines = content.split('\n')
    in_match = False
    match_block = ''
    depth = 0
    
    for line in lines:
        if '<div class="match-item' in line:
            in_match = True
            match_block = line
            depth = 1
            continue
        
        if in_match:
            match_block += '\n' + line
            depth += line.count('<div') - line.count('</div')
            
            if depth <= 0:
                in_match = False
                m = {}
                
                tm = re.search(r'class="match-time">(.*?)</div>', match_block)
                if tm:
                    time_text = tm.group(1).strip()
                    m['time'] = time_text
                    if '已结束' in time_text:
                        m['status'] = 'finished'
                
                all_spans = re.findall(r'<span[^>]*>(.*?)</span>', match_block)
                
                team_spans = []
                for s in all_spans:
                    s_stripped = s.strip()
                    has_flag = any(flag in s_stripped for flag in FLAG_NAMES)
                    has_name = any(name in s_stripped for name in FLAG_NAMES.values())
                    if has_flag or has_name:
                        team_spans.append(s_stripped)
                
                if len(team_spans) >= 2:
                    m['home'] = team_spans[0]
                    m['away'] = team_spans[1]
                
                for sp in all_spans:
                    sp = sp.strip()
                    if 'match-score' in match_block and re.search(r'\d+[-:]\d+', sp):
                        nums = re.findall(r'(\d+)[-:](\d+)', sp)
                        if nums:
                            m['score_home'] = int(nums[0][0])
                            m['score_away'] = int(nums[0][1])
                            m['status'] = 'finished'
                
                if '等待开赛' in match_block or 'pending' in match_block:
                    if m.get('status') != 'finished':
                        m['status'] = 'pending'
                
                gm = re.search(r'class="match-group">(.*?)</span>', match_block)
                if gm:
                    m['group'] = gm.group(1).strip() + '组'
                
                vm = re.search(r'class="match-venue">([^<]*)</span>', match_block)
                if vm:
                    m['venue'] = vm.group(1).strip()
                
                tg = re.search(r'class="match-tag">(.*?)</span>', match_block)
                if tg:
                    m['tag'] = tg.group(1).strip()
                
                if 'highlight' in match_block.lower() or 'match-highlight' in match_block:
                    m['highlight'] = True
                
                em = re.search(r'进球.*?</div>', match_block)
                if em:
                    m['events'] = re.sub(r'<[^>]+>', '', em.group(0)).strip()
                
                if m.get('home'):
                    matches.append(m)
    
    return matches


def build_data():
    world_cup_dir = PROJECT_DIR / 'world_cup'
    data = {'groups': {}, 'dates': {}, 'knockout': {}}
    
    # 解析小组
    for gname, teams in GROUPS.items():
        fpath = world_cup_dir / f'group-{gname.lower()}.html'
        if fpath.exists():
            matches = parse_group_html(str(fpath))
            for m in matches:
                m['group'] = f'{gname}组'
                if 'time' in m:
                    dm = re.search(r'(\d+)月(\d+)日\s*(\d{2}:\d{2})', m['time'])
                    if dm:
                        m['month'] = int(dm.group(1))
                        m['day'] = int(dm.group(2))
                        m['kickoff'] = dm.group(3)
            data['groups'][gname] = {'teams': teams, 'matches': matches}
            ok = sum(1 for m in matches if m.get('home'))
            print(f"  {gname}组: {len(matches)} 场 (有效 {ok})")
    
    # 解析日期页
    for f in sorted(world_cup_dir.glob('date-*.html')):
        key = f.stem.replace('date-', '')
        matches = parse_date_html(str(f))
        if matches:
            data['dates'][key] = {'matches': matches}
            print(f"  {key}: {len(matches)} 场")
    
    # 淘汰赛
    data['knockout'] = {
        'round16': {
            'label': '1/16决赛', 'dates': '6月29日 - 7月4日', 'icon': '⚔️',
            'matches': [
                {'time': '6月29日 03:00', 'home': 'A组第1', 'away': 'B组第2'},
                {'time': '6月29日 08:00', 'home': 'B组第1', 'away': 'A组第2'},
                {'time': '6月30日 03:00', 'home': 'C组第1', 'away': 'D组第2'},
                {'time': '6月30日 08:00', 'home': 'D组第1', 'away': 'C组第2'},
                {'time': '7月1日 03:00', 'home': 'E组第1', 'away': 'F组第2'},
                {'time': '7月1日 08:00', 'home': 'F组第1', 'away': 'E组第2'},
                {'time': '7月2日 03:00', 'home': 'G组第1', 'away': 'H组第2'},
                {'time': '7月2日 08:00', 'home': 'H组第1', 'away': 'G组第2'},
                {'time': '7月3日 03:00', 'home': 'I组第1', 'away': 'J组第2'},
                {'time': '7月3日 08:00', 'home': 'J组第1', 'away': 'I组第2'},
                {'time': '7月4日 03:00', 'home': 'K组第1', 'away': 'L组第2'},
                {'time': '7月4日 08:00', 'home': 'L组第1', 'away': 'K组第2'},
            ]
        },
        'round8': {
            'label': '1/8决赛', 'dates': '7月5日 - 7月8日', 'icon': '🎯',
            'matches': [
                {'time': '7月5日 03:00', 'home': '1/16胜者1', 'away': '1/16胜者2'},
                {'time': '7月5日 08:00', 'home': '1/16胜者3', 'away': '1/16胜者4'},
                {'time': '7月6日 03:00', 'home': '1/16胜者5', 'away': '1/16胜者6'},
                {'time': '7月6日 08:00', 'home': '1/16胜者7', 'away': '1/16胜者8'},
                {'time': '7月7日 03:00', 'home': '1/16胜者9', 'away': '1/16胜者10'},
                {'time': '7月7日 08:00', 'home': '1/16胜者11', 'away': '1/16胜者12'},
                {'time': '7月8日 03:00', 'home': '1/16胜者13', 'away': '1/16胜者14'},
                {'time': '7月8日 08:00', 'home': '1/16胜者15', 'away': '1/16胜者16'},
            ]
        },
        'quarter': {
            'label': '1/4决赛', 'dates': '7月10日 - 7月12日', 'icon': '💎',
            'matches': [
                {'time': '7月10日 03:00', 'home': '1/8胜者1', 'away': '1/8胜者2'},
                {'time': '7月10日 08:00', 'home': '1/8胜者3', 'away': '1/8胜者4'},
                {'time': '7月11日 03:00', 'home': '1/8胜者5', 'away': '1/8胜者6'},
                {'time': '7月11日 08:00', 'home': '1/8胜者7', 'away': '1/8胜者8'},
            ]
        },
        'semi': {
            'label': '半决赛', 'dates': '7月15日 - 7月16日', 'icon': '🌟',
            'matches': [
                {'time': '7月15日 03:00', 'home': '1/4胜者1', 'away': '1/4胜者2'},
                {'time': '7月16日 03:00', 'home': '1/4胜者3', 'away': '1/4胜者4'},
            ]
        },
        'third': {
            'label': '季军赛', 'dates': '7月19日', 'icon': '🥉',
            'matches': [
                {'time': '7月19日 03:00', 'home': '半决赛负者1', 'away': '半决赛负者2'},
            ]
        },
        'final': {
            'label': '决赛', 'dates': '7月20日', 'icon': '🏆', 'venue': '纽约大都会人寿体育场',
            'matches': [
                {'time': '7月20日 03:00', 'home': '半决赛胜者1', 'away': '半决赛胜者2'},
            ]
        },
    }
    
    return data


if __name__ == '__main__':
    print("🔍 解析 HTML 提取数据...\n")
    data = build_data()
    
    output_path = PROJECT_DIR / 'data' / 'matches.json'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(str(output_path), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    total_group = sum(len(g['matches']) for g in data['groups'].values())
    total_date = sum(len(d['matches']) for d in data['dates'].values())
    
    print(f"\n✅ 数据已保存: {output_path}")
    print(f"   小组赛: {total_group} 场")
    print(f"   日期页: {total_date} 场")
