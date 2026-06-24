import os
from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL")   # 或 deepseek-chat

# 嵌入模型（中文效果好）
EMBED_MODEL = os.getenv("EMBED_MODEL")

HF_TOKEN = os.getenv("HF_TOKEN")