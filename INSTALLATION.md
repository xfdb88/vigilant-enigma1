# Instagram Scraper - 完整安装与使用指南

## 目录
- [系统要求](#系统要求)
- [安装方法](#安装方法)
- [使用教程](#使用教程)
- [常见问题](#常见问题)
- [高级配置](#高级配置)

---

## 系统要求

### 最低配置
- **操作系统**: Windows 10+, macOS 10.15+, Linux (Ubuntu 20.04+)
- **Python**: 3.8 或更高版本
- **内存**: 至少 2GB RAM
- **磁盘空间**: 至少 500MB 可用空间
- **网络**: 稳定的互联网连接

### 推荐配置
- **Python**: 3.10+ 
- **内存**: 4GB+ RAM
- **网络**: 带宽 10Mbps+

---

## 安装方法

### 方法 1：使用预编译可执行文件（最简单）

**适合**: 不熟悉 Python 的用户

1. **下载分发包**
   ```
   下载: instagram-scraper-dist.zip
   ```

2. **解压文件**
   ```
   - Windows: 右键 -> 解压到当前文件夹
   - Mac/Linux: unzip instagram-scraper-dist.zip
   ```

3. **运行程序**
   ```
   - Windows: 双击 run.bat
   - Mac/Linux: 在终端运行 ./run.sh
   ```

### 方法 2：从源码安装（推荐开发者）

**适合**: 熟悉 Python 的用户，需要自定义功能

#### Step 1: 安装 Python

**Windows:**
```bash
# 从 python.org 下载并安装 Python 3.8+
# 安装时勾选 "Add Python to PATH"
```

**Mac:**
```bash
# 使用 Homebrew
brew install python@3.11
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

#### Step 2: 克隆仓库

```bash
git clone https://github.com/xfdb88/vigilant-enigma1.git
cd vigilant-enigma1
```

#### Step 3: 创建虚拟环境（推荐）

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

#### Step 4: 安装依赖

```bash
# 安装 Python 包
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install chromium
```

#### Step 5: 配置环境

```bash
# 复制配置文件
cp .env.example .env

# 编辑配置（可选）
# Windows: notepad .env
# Mac/Linux: nano .env
```

---

## 使用教程

### 快速开始

#### 1. 准备输入文件

编辑 `data/input.csv`，添加要抓取的 Instagram 用户名：

```csv
username
instagram
natgeo
cristiano
```

**格式说明:**
- 第一行是标题行（username）
- 每行一个用户名
- 不要包含 @ 符号
- 不要包含空行

#### 2. 运行程序

```bash
# 使用 CLI 界面（推荐）
python run.py

# 或直接运行 CLI
python src/cli.py

# 或直接运行爬虫（不显示界面）
python src/scraper.py
```

#### 3. 界面操作

程序启动后会显示主菜单：

```
╔═══════════════════════════════════════════════════════════╗
║        Instagram Public Profile Scraper v1.0              ║
╚═══════════════════════════════════════════════════════════╝

Main Menu:
1. Scrape profiles from CSV file  # 批量抓取
2. Scrape a single profile        # 单个抓取
3. View configuration             # 查看配置
4. Exit                           # 退出
```

**选项说明:**

- **选项 1**: 从 CSV 文件批量抓取
  - 系统会提示输入文件路径（默认: data/input.csv）
  - 显示预览前 5 个用户名
  - 确认后开始抓取
  - 结果自动保存到 data/output.csv

- **选项 2**: 抓取单个用户
  - 输入 Instagram 用户名
  - 立即显示抓取结果
  - 可选择是否保存到 CSV

- **选项 3**: 查看当前配置
  - 显示所有配置项
  - 包括超时、重试次数、速率限制等

- **选项 4**: 退出程序

#### 4. 查看结果

结果保存在 `data/output.csv`，包含以下字段：

| 字段 | 说明 | 示例 |
|------|------|------|
| username | 用户名 | natgeo |
| display_name | 显示名称 | National Geographic |
| bio | 个人简介 | Experience the world... |
| email | 邮箱地址 | contact@example.com |
| phone | 电话号码 | +1-234-567-8900 |
| links | 链接 | https://natgeo.com |
| gender | 性别 | - |
| age | 年龄 | - |
| region | 地区 | - |
| warning_code | 警告代码 | PRIVATE / 404 / 429 |
| error | 错误信息 | Profile not found |

**注意事项:**
- email, phone, links 从用户简介中提取，可能为空
- gender, age, region 目前无法从公开页面获取
- warning_code 说明：
  - `PRIVATE`: 私密账户
  - `404`: 用户不存在
  - `429`: 请求过于频繁

---

## 高级配置

### 环境变量配置

编辑 `.env` 文件进行高级配置：

```env
# ============================================
# Instagram 登录配置（可选）
# ============================================
# 如果需要访问更多信息，可以配置登录
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password

# ============================================
# 代理配置（可选）
# ============================================
# 使用代理可以避免 IP 被封禁
PROXY_SERVER=http://proxy.example.com:8080
PROXY_USERNAME=proxy_user
PROXY_PASSWORD=proxy_pass

# ============================================
# 请求配置
# ============================================
# 请求超时时间（秒）
REQUEST_TIMEOUT=30

# 最大重试次数
MAX_RETRIES=3

# 重试延迟（秒）
RETRY_DELAY=5

# 请求间隔（秒）- 重要！避免被限速
RATE_LIMIT_DELAY=2
```

### 配置建议

#### 避免被限速
```env
# 增加请求间隔
RATE_LIMIT_DELAY=5

# 使用代理
PROXY_SERVER=http://your-proxy:8080
```

#### 提高成功率
```env
# 增加超时时间
REQUEST_TIMEOUT=60

# 增加重试次数
MAX_RETRIES=5

# 增加重试延迟
RETRY_DELAY=10
```

#### 快速抓取（风险高）
```env
# 减少延迟（可能被封）
RATE_LIMIT_DELAY=1
REQUEST_TIMEOUT=20
MAX_RETRIES=2
```

---

## 常见问题

### Q1: 安装 Playwright 时出错？

**问题:**
```
playwright install chromium 报错
```

**解决方案:**
```bash
# 方法 1: 使用管理员权限
sudo playwright install chromium  # Linux/Mac
# 以管理员身份运行 PowerShell (Windows)

# 方法 2: 指定安装路径
PLAYWRIGHT_BROWSERS_PATH=$HOME/.playwright playwright install chromium
```

### Q2: 运行时提示 "Browser not found"？

**解决方案:**
```bash
# 重新安装浏览器
playwright install chromium

# 或设置环境变量
export PLAYWRIGHT_BROWSERS_PATH=/path/to/browsers
```

### Q3: 被 Instagram 限速（429 错误）？

**解决方案:**
1. 增加 `RATE_LIMIT_DELAY` 到 5-10 秒
2. 使用代理服务器
3. 减少批量抓取数量
4. 等待几小时后重试

### Q4: 某些字段总是为空？

**原因:**
- Instagram 公开信息有限
- email/phone 需要用户在简介中主动提供
- gender/age/region 无法从公开页面获取

**建议:**
- 专注于可获取的字段（username, display_name, bio）
- 使用登录账号可能获取更多信息

### Q5: 私密账户如何处理？

**答案:**
- 私密账户无法获取详细信息
- 会在 `warning_code` 标记为 "PRIVATE"
- 需要关注该账户才能查看内容
- 本工具不支持自动关注

### Q6: 如何批量抓取大量用户？

**建议:**
1. 分批处理（每次 50-100 个）
2. 设置较长的 `RATE_LIMIT_DELAY`
3. 使用代理轮换
4. 监控日志文件 `scraper.log`
5. 定期备份 output.csv

### Q7: 可以商用吗？

**答案:**
- 本工具采用 MIT 许可证
- 但需遵守 Instagram 服务条款
- 商用需自行承担法律风险
- 建议仅用于教育和研究

---

## 日志和调试

### 查看日志

程序运行时会生成 `scraper.log` 文件：

```bash
# 实时查看日志
tail -f scraper.log

# 查看最后 50 行
tail -50 scraper.log

# 搜索错误
grep ERROR scraper.log
```

### 日志级别

修改 `src/scraper.py` 中的日志级别：

```python
logging.basicConfig(
    level=logging.DEBUG,  # 改为 DEBUG 查看详细信息
    ...
)
```

---

## 性能优化

### 提高速度

1. **并发抓取** (需修改代码):
   ```python
   # 使用异步 Playwright
   from playwright.async_api import async_playwright
   ```

2. **减少等待时间**:
   ```python
   # src/scraper.py 中
   time.sleep(1)  # 减少到 1 秒
   ```

3. **使用缓存**:
   - 缓存已抓取的用户
   - 避免重复抓取

### 降低资源占用

1. **使用无头模式** (已默认):
   ```python
   headless=True
   ```

2. **关闭图片加载**:
   ```python
   # 在 browser.new_page() 后添加
   page.route("**/*.{png,jpg,jpeg,gif}", lambda route: route.abort())
   ```

---

## 技术支持

### 报告问题

如遇到问题，请提供：
1. 错误信息截图
2. `scraper.log` 日志文件
3. 操作系统和 Python 版本
4. input.csv 示例（可脱敏）

### 提交 Issue

访问: https://github.com/xfdb88/vigilant-enigma1/issues

### 贡献代码

欢迎 Pull Request！

---

## 附录

### 完整文件结构

```
vigilant-enigma1/
├── src/
│   ├── __init__.py
│   ├── scraper.py       # 核心爬虫逻辑
│   └── cli.py           # CLI 界面
├── tests/
│   ├── __init__.py
│   └── test_scraper.py  # 单元测试
├── data/
│   ├── input.csv        # 输入文件
│   └── output.csv       # 输出文件（自动生成）
├── build.py             # 构建脚本
├── run.py               # 快速启动脚本
├── setup.py             # 安装配置
├── requirements.txt     # 依赖列表
├── .env.example         # 配置模板
├── .env                 # 实际配置（需创建）
├── .gitignore          # Git 忽略文件
├── MANIFEST.in         # 打包清单
├── README.md           # 项目说明
├── INSTALLATION.md     # 本文件
├── LICENSE             # 许可证
└── scraper.log         # 日志文件（自动生成）
```

### 依赖说明

| 包名 | 版本 | 用途 |
|------|------|------|
| playwright | 1.40.0 | 浏览器自动化 |
| httpx | 0.25.2 | HTTP 客户端 |
| beautifulsoup4 | 4.12.2 | HTML 解析 |
| python-dotenv | 1.0.0 | 环境变量管理 |
| lxml | 4.9.3 | XML/HTML 解析器 |
| rich | 13.7.0 | 终端美化 |
| PyInstaller | 6.3.0 | 打包工具 |

---

**文档更新**: 2025-10-16
**版本**: v1.0.0
**作者**: vigilant-enigma1
