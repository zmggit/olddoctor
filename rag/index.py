from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from config import EMBED_MODEL
import os

embed_model = HuggingFaceEmbedding(model_name=EMBED_MODEL)

def build_or_load_index():
    persist_dir = "./storage"
    if os.path.exists(persist_dir):
        storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
        index = load_index_from_storage(storage_context)
        print("✅ 已加载现有索引")
    else:
        print("正在构建中医知识索引...")
        documents = SimpleDirectoryReader("./rag/knowledge").load_data()
        index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
        index.storage_context.persist(persist_dir=persist_dir)
        print("✅ 索引构建完成")
    return index