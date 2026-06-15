# MEMORY.md - 长期记忆

## 环境信息
- 系统：Windows 11
- 用户：Zhu
- Managed Python：3.13.12 (`C:\Users\Zhu\.workbuddy\binaries\python\versions\3.13.12\python.exe`)
- Managed Node：22.12.0

## 已安装技能
- **wx4-skill**：微信自动化（wx4py v0.2.1），位于 `~/.workbuddy/skills/wx4-skill/`
- **企业微信套件 (wecom-unified)**：wecom-cli，已安装但未授权

## 关键路径
- WorkBuddy 安装路径：`C:\Program Files\WorkBuddy\WorkBuddy.exe`
- 启动文件夹：`C:\Users\Zhu\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\`

## 平台信息
- **移动千里眼**：https://qly.cmviot.cn（视频监控平台），用于工作查询设备
- 千里眼账号：13987878816
- Playwright 已安装（Chromium），路径：`C:\Users\Zhu\.workbuddy\binaries\node\workspace\`
  - 运行命令：`NODE_PATH="C:/Users/Zhu/.workbuddy/binaries/node/workspace/node_modules" "C:/Users/Zhu/.workbuddy/binaries/node/versions/22.12.0/node.exe"`

## 重要联系人
- **爱人：王珈懿**（微信备注名：`哇！🚒`，微信搜索关键词：`哇`）
  - 别名：懿宝
  - 发消息时使用搜索关键词 `哇` 即可匹配到该联系人

## 世界杯项目
- **仓库**：https://github.com/GG-Bondzj/world-cup-2026
- **固定链接**：https://gg-bondzj.github.io/world-cup-2026/
- **架构**：数据驱动（data/matches.json → scripts/generate_html.py → world_cup/*.html）
- **自动化**：每日17:00自动更新（WorkBuddy 定时任务 + GitHub Actions 双保险）
- **部署**：推送 → GitHub Actions 自动部署到 Pages
- **注意事项**：
  - 更新流程：编辑 matches.json → 运行 generate_html.py → cp world_cup/*.html . → git push
  - GitHub Pages Source 需设置为 "GitHub Actions"
  - GitHub 网络有时不通，需重试推送
