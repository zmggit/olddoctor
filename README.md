
# 注意不可相差过大
Chrome 是 148，ChromeDriver 是 147
# 修改配置文件
`cp .env.example .env`
# 1. 安装 uv（推荐方式）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 创建新项目
uv init olddoctor
cd olddoctor

# 3. 添加依赖
uv add requests numpy
uv add --dev pytest ruff

# 4. 同步环境（类似 pip install -r requirements.txt）
uv sync

# 5. 运行项目
uv run main.py
uv run pytest

# 6. 管理 Python 版本
uv python pin 3.14.4          # 锁定版本
uv python install           # 自动安装

# uv 导出
uv pip freeze > requirements.txt
# uv 安装
uv pip install -r requirements.txt

rm -rf .venv
uv python install 3.12
uv venv --python 3.14

uv llama_index.embeddings.huggingface install 