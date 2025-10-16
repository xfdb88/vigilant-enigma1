set -euo pipefail

echo "=> 创建虚拟环境"
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -U pip

echo "=> 安装项目（含可选项）"
pip install -e ".[all]"

echo "=> 安装浏览器内核"
python -m playwright install chromium

[ -f .env ] || { [ -f .env.example ] && cp -n .env.example .env && echo "已创建 .env，请填写 IG_USERNAME/IG_PASSWORD"; }
mkdir -p data
[ -f data/input.csv ] || cat > data/input.csv <<'CSV'
username
natgeo
nasa
CSV

echo "=> 运行抓取"
igscrape -i data/input.csv -o data/output.csv

echo "完成，结果见 data/output.csv"
