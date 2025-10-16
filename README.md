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

## 常见问题与排查

- 未安装浏览器内核
  - 执行：playwright install chromium
- 登录/安全验证/2FA
  - 设置 HEADLESS=false，使用可视化窗口完成一次登录；降低 RATE_LIMIT_QPS；必要时删除 .playwright/state.json 后重试
- 429/验证码/被限流
  - 降低 QPS（建议 0.2–0.5），配置 PROXY_URL，增加 RETRY_ATTEMPTS/RETRY_BACKOFF
- Windows 脚本执行策略
  - PowerShell 以管理员运行，或在当前会话放宽：Set-ExecutionPolicy -Scope Process Bypass
- 解析为空或 httpx 抓不到内容
  - 先用 Playwright 登录一次生成 .playwright/state.json，再用 --httpx；必要时提高超时 TIMEOUT_SECONDS
- 依赖安装问题（如 lxml）
  - 升级 pip：python -m pip install -U pip；确保使用与平台匹配的预编译轮子；Windows 需安装 VC Build Tools

## 在脚本中演示 --httpx

- Windows（PowerShell）：scripts\setup_win.ps1 -Httpx
- macOS/Linux（bash）：bash scripts/setup_unix.sh --httpx
