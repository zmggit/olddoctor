# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

OldDoctor 是一个基于 RAG + LLM 的中医AI助手，结合经典中医典籍进行辨证论治。使用 DeepSeek 作为对话模型，LlamaIndex + ChromaDB 实现知识检索，HuggingFace BGE 模型做中文嵌入。

## 常用命令

```bash
# 同步依赖
uv sync

# 运行主程序
uv run main.py

# 运行测试
uv run pytest

# 代码检查
uv run ruff check .

# 导出依赖
uv pip freeze > requirements.txt
```

## 架构概览

**启动流程** (`main.py`): 设置 `TOKENIZERS_PARALLELISM=false` 避免 tokenizer 并行警告 → 构建/加载 RAG 索引 → 创建 retriever（top_k=8）→ 进入交互式对话循环。

**对话循环** (`main.py`): 每轮对话依次执行：
1. 获取多轮对话历史 (`agent/conversational.py` 中的 `SQLChatMessageHistory`，SQLite 持久化)
2. RAG 检索相关中医典籍片段
3. 拼接 system prompt + 对话历史 + 用户输入 + 检索上下文 → 调用 DeepSeek LLM
4. 追加安全免责声明 (`utils/safety.py`)
5. 保存本轮对话到 SQLite (`chat_history.db`)

**对话记忆** (`agent/conversational.py`): 使用 `SQLChatMessageHistory` 将对话历史持久化到本地 SQLite 数据库。`get_chat_history(session_id)` 和 `save_context(user_input, ai_output, session_id)` 均接受可选的 `session_id` 参数（默认 `"default_user"`），为多用户场景预留扩展能力。

**RAG 索引** (`rag/index.py`): 提供两种索引模式：
- `build_or_load_db_index()` — 连接 ChromaDB Server（localhost:8000），用于生产（已设置 `no_proxy` 跳过本地代理）
- `build_or_load_local_index()` — 本地文件存储（./storage），用于开发调试

当前 `main.py` 使用 ChromaDB 模式。嵌入模型使用本地 `./models/bge-base-zh-v1.5`。

**知识库** (`rag/knowledge/`): 包含四本中医经典典籍的 txt 文件（神农本草经、吴普本草、本草经集注、食疗本草）。部分文件可能为 GBK 编码，使用 `rag/test/cover.py` 可转换为 UTF-8。

**舌诊识别** (`collect/tongue/tongue_recognizer.py`): 基于 HuggingFace Transformers 图像分类模型的舌苔自动分析模块。`TongueRecognizer` 类加载开源舌诊分类模型，支持从图片路径分析舌象特征（舌质、舌苔、颜色等），返回文字描述和置信度。

**配置** (`config.py`): 通过 `.env` 文件加载环境变量，需要 `DEEPSEEK_API_KEY`，可选 `DEEPSEEK_MODEL`、`EMBED_MODEL`、`HF_TOKEN`。

## 关键依赖

| 包 | 用途 |
|---|---|
| `langchain-deepseek` | DeepSeek LLM 对话 |
| `llama-index` | RAG 框架，文档加载、索引构建、检索 |
| `chromadb` | 向量数据库（需单独启动 ChromaDB Server） |
| `transformers` + `tokenizers` | HuggingFace 嵌入模型与舌诊图像分类 |
| `torch` | 舌诊模型推理 |
| `Pillow` | 舌苔图片读取 |
| `uv` | 包管理和运行环境 |
