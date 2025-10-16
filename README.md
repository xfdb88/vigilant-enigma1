# Instagram Public Profile Scraper

一个用于抓取 Instagram 公开用户信息的 Python 爬虫项目。

## ⚠️ 法律声明与合规 (Legal Disclaimer & Compliance)

**重要：本工具仅用于教育目的 (IMPORTANT: This tool is for educational purposes only)**

### 使用条款 (Terms of Use)

使用本工具前，您必须同意以下条款：

1. **仅抓取公开信息** - 只能抓取 Instagram 上公开可见的用户资料信息
2. **遵守服务条款** - 必须遵守 Instagram 的服务条款和使用政策
3. **数据保护法规** - 遵守所有适用的数据保护法律法规，包括但不限于：
   - GDPR (欧盟通用数据保护条例)
   - CCPA (加州消费者隐私法案)
   - 其他地区的隐私法规
4. **禁止滥用** - 不得将本工具用于：
   - 骚扰、垃圾信息或未经授权的数据收集
   - 侵犯他人隐私权
   - 任何非法活动
5. **责任自负** - 使用者需对使用本工具的行为承担全部责任

**开发者不对本软件的任何滥用行为负责。**

---

## 功能特性 (Features)

✅ 使用 Playwright 进行浏览器自动化
✅ httpx + BeautifulSoup4 解析 HTML
✅ 从 CSV 文件批量读取用户名
✅ 导出详细的 CSV 结果
✅ 速率限制与自动重试机制
✅ .env 配置文件支持（账号/代理）
✅ 友好的命令行界面（CLI）
✅ 详细的日志记录
✅ 单元测试
✅ 一键打包为可执行程序

## 数据字段 (Output Fields)

输出的 CSV 文件包含以下字段：

- `username` - Instagram 用户名
- `display_name` - 显示名称
- `bio` - 个人简介
- `email` - 邮箱（从简介中提取）
- `phone` - 电话（从简介中提取）
- `links` - 链接（从简介中提取）
- `gender` - 性别
- `age` - 年龄
- `region` - 地区
- `warning_code` - 警告代码（如私密账户、404等）
- `error` - 错误信息

## 快速开始 (Quick Start)

### 方法 1：使用预编译版本（推荐）

1. 下载 `instagram-scraper-dist.zip`
2. 解压到任意目录
3. 运行 `run.bat`（Windows）或 `run.sh`（Linux/Mac）
4. 按照界面提示操作

### 方法 2：从源码运行

#### 安装依赖

```bash
# 克隆仓库
git clone https://github.com/xfdb88/vigilant-enigma1.git
cd vigilant-enigma1

# 安装 Python 依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install chromium
```

#### 配置环境

```bash
# 复制配置文件
cp .env.example .env

# 编辑 .env 文件（可选）
# 可配置代理、账号、速率限制等
```

#### 准备输入文件

编辑 `data/input.csv`，每行一个 Instagram 用户名：

```csv
username
instagram
natgeo
cristiano
```

#### 运行程序

```bash
# 使用 CLI 界面
python src/cli.py

# 或直接运行脚本
python src/scraper.py
```

## 使用说明 (Usage Guide)

### CLI 界面

运行 `python src/cli.py` 后会看到主菜单：

```
1. Scrape profiles from CSV file  # 从 CSV 文件批量抓取
2. Scrape a single profile        # 抓取单个用户
3. View configuration             # 查看配置
4. Exit                           # 退出
```

### 配置选项

编辑 `.env` 文件可自定义以下选项：

```env
# Instagram 账号（可选，用于访问更多内容）
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password

# 代理设置（可选）
PROXY_SERVER=http://proxy.example.com:8080
PROXY_USERNAME=proxy_user
PROXY_PASSWORD=proxy_pass

# 请求配置
REQUEST_TIMEOUT=30        # 请求超时（秒）
MAX_RETRIES=3            # 最大重试次数
RETRY_DELAY=5            # 重试延迟（秒）
RATE_LIMIT_DELAY=2       # 请求间隔（秒）
```

## 打包分发 (Build & Distribution)

### 构建可执行程序

```bash
# 运行构建脚本
python build.py
```

这将创建：
- `dist/instagram-scraper.exe`（Windows）或 `instagram-scraper`（Linux/Mac）
- `instagram-scraper-dist.zip` - 完整的分发包

### 分发包内容

解压 `instagram-scraper-dist.zip` 后包含：

```
instagram-scraper-dist/
├── instagram-scraper.exe    # 可执行程序
├── src/                     # 源代码
├── data/                    # 数据目录
│   └── input.csv           # 示例输入
├── requirements.txt        # Python 依赖
├── .env.example           # 配置模板
├── README.txt             # 使用说明
├── LICENSE                # MIT 许可证
├── run.bat                # Windows 启动脚本
└── run.sh                 # Linux/Mac 启动脚本
```

## 测试 (Testing)

运行单元测试：

```bash
python -m pytest tests/
# 或
python -m unittest discover tests/
```

## 技术栈 (Tech Stack)

- **Python 3.8+** - 主要编程语言
- **Playwright** - 浏览器自动化
- **httpx** - HTTP 客户端
- **BeautifulSoup4** - HTML 解析
- **Rich** - 终端界面美化
- **python-dotenv** - 环境变量管理
- **PyInstaller** - 打包可执行程序

## 项目结构 (Project Structure)

```
vigilant-enigma1/
├── src/
│   ├── scraper.py         # 核心爬虫逻辑
│   └── cli.py             # CLI 界面
├── tests/
│   └── test_scraper.py    # 单元测试
├── data/
│   ├── input.csv          # 输入文件
│   └── output.csv         # 输出文件（自动生成）
├── build.py               # 构建脚本
├── requirements.txt       # 依赖列表
├── .env.example          # 配置模板
├── README.md             # 本文件
└── LICENSE               # MIT 许可证
```

## 常见问题 (FAQ)

### Q: 为什么有些字段为空？
A: Instagram 的公开信息有限，很多字段（如 email、phone）需要从用户简介中提取，如果用户未在简介中提供则为空。

### Q: 遇到 "Rate limited" 错误怎么办？
A: 增加 `.env` 中的 `RATE_LIMIT_DELAY` 值，例如设置为 5 秒。

### Q: 可以使用代理吗？
A: 可以，在 `.env` 文件中配置 `PROXY_SERVER` 等选项。

### Q: 是否需要 Instagram 账号？
A: 不是必需的，但登录后可能可以访问更多信息。

### Q: 如何处理私密账户？
A: 私密账户会在 `warning_code` 字段标记为 "PRIVATE"，无法获取详细信息。

## 许可证 (License)

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 贡献 (Contributing)

欢迎提交 Issue 和 Pull Request！

## 免责声明 (Disclaimer)

本工具仅供学习和研究使用。使用者需自行承担使用本工具的一切后果和责任。开发者不对任何滥用行为或由此产生的法律问题负责。

---

**MIT License** | **Educational Use Only** | **Use Responsibly**
