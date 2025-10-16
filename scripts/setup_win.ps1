param(
  [switch]$Httpx = $false
)

$ErrorActionPreference = "Stop"

Write-Host "=> 创建虚拟环境"
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
python -m pip install -U pip

Write-Host "=> 安装项目（含可选项）"
pip install -e ".[all]"

Write-Host "=> 安装浏览器内核"
python -m playwright install chromium

if (!(Test-Path ".env") -and (Test-Path ".env.example")) {
  Copy-Item .env.example .env
  Write-Host "已创建 .env，请填写 IG_USERNAME/IG_PASSWORD"
}

if (!(Test-Path "data")) { New-Item -ItemType Directory -Path data | Out-Null }
if (!(Test-Path "data\input.csv")) {
@"
username
natgeo
nasa
"@ | Out-File -Encoding utf8 "data\input.csv"
}

Write-Host "=> 运行抓取"
if ($Httpx) {
  Write-Host "使用 httpx+Cookies 模式（需先完成一次登录以生成 .playwright/state.json）"
  igscrape -i data\input.csv -o data\output.csv --httpx
} else {
  igscrape -i data\input.csv -o data\output.csv
}

Write-Host "完成，结果见 data\output.csv"
Write-Host "提示：传入 -Httpx 可演示 httpx 抓取方式"
