# Instagram Public Profile Scraper (MIT)

运行前请在 .env 填写 IG_USERNAME/IG_PASSWORD；若遇风控，设置 HEADLESS=false 并降低 RATE_LIMIT_QPS。

一键脚本

- Windows（PowerShell）：scripts\setup_win.ps1
- macOS/Linux（bash）：bash scripts/setup_unix.sh

手动运行

- 安装：pip install -e ".[all]" && playwright install chromium
- 执行：igscrape -i data/input.csv -o data/output.csv

功能

- 从 data/input.csv 读取用户名（列名：username）
- 输出 data/output.csv 字段：username, display_name, bio, email, phone, links, gender, age, region, warning_code, error
- 速率限制（QPS）、重试、.env（账号/代理/并发/日志级别）、结构化日志
- 默认 Playwright 登录后抓取；提供 httpx+Cookies 示例

合规与免责声明

- 仅抓取用户公开信息；遵守 Instagram 服务条款与 robots.txt；控制请求频率（建议 RATE_LIMIT_QPS=0.3）。
- 启发式字段（email/phone/gender/age/region）可能不准确，请自行验证。
- MIT 许可证，使用者自负合规与风险。
