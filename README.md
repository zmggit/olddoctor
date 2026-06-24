# OldDoctor - 中医AI助手

基于 RAG + LLM 的中医智能辨证论治系统。结合《神农本草经》《吴普本草》《本草经集注》《食疗本草》等经典典籍，使用 DeepSeek 大模型进行多轮对话诊断。

## 功能特性

- **知识检索** — 基于 LlamaIndex + ChromaDB 的 RAG 检索，从中医典籍中召回相关知识
- **智能辨证** — DeepSeek LLM 结合检索上下文进行证型诊断、方剂推荐
- **多轮对话** — SQLite 持久化上下文记忆，支持连续问诊，预留多用户扩展
- **舌诊识别** — 基于图像分类模型的舌苔自动分析（`collect/tongue/`）

## 环境准备

### 1. 安装 uv 包管理器

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. 下载嵌入模型

```bash
uv pip install huggingface_hub
hf download BAAI/bge-base-zh-v1.5 --local-dir ./models/bge-base-zh-v1.5
```

### 3. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env，填入 DEEPSEEK_API_KEY
```

### 4. 同步依赖

```bash
uv sync
```

## 启动 ChromaDB（生产模式）

```bash
chroma run --host localhost --port 8000
```

## 运行

```bash
uv run main.py
```

交互命令：输入症状描述进行问诊，输入 `退出` / `quit` / `q` 结束对话。

## 开发

```bash
uv run pytest              # 运行测试
uv run ruff check .        # 代码检查
```

## 项目结构

```
├── main.py                # 入口，对话循环
├── config.py              # 环境变量配置
├── agent/
│   └── conversational.py  # LLM 初始化、对话记忆
├── prompts/
│   ├── system_prompt.py   # 系统提示词
│   └── fewshot.py         # Few-shot 示例
├── rag/
│   ├── index.py           # RAG 索引构建/加载
│   ├── knowledge/         # 中医典籍 txt 文件
│   └── test/
│       ├── cover.py       # GBK → UTF-8 编码转换
│       └── test_cover.py
├── collect/
│   └── tongue/
│       └── tongue_recognizer.py  # 舌苔图像识别
├── utils/
│   └── safety.py          # 安全免责声明
└── models/                # 本地嵌入模型
```

## 配置项

| 环境变量 | 说明 | 必填 |
|----------|------|------|
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 | 是 |
| `DEEPSEEK_MODEL` | 模型名称（默认 deepseek-chat） | 否 |
| `EMBED_MODEL` | 嵌入模型路径 | 否 |
| `HF_TOKEN` | HuggingFace Token | 否 |

## 依赖

| 包 | 用途 |
|---|---|
| `langchain-deepseek` | DeepSeek LLM 对话接口 |
| `llama-index-core` | RAG 框架：文档加载、索引、检索 |
| `chromadb` | 向量数据库 |
| `transformers` + `tokenizers` | HuggingFace 嵌入与图像模型 |
| `uv` | 包管理与运行环境 |
