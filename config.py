import os
from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_MODEL = "deepseek-r1"   # 或 deepseek-chat

# 嵌入模型（中文效果好）
EMBED_MODEL = "BAAI/bge-m3"