import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore

from config import EMBED_MODEL
import os


# embed_model = HuggingFaceEmbedding(model_name=EMBED_MODEL)
# 本地使用调试快一点
embed_model = HuggingFaceEmbedding(model_name="./models/bge-base-zh-v1.5")


# 关键：全局设置 embed_model，否则默认用 OpenAI
Settings.embed_model = embed_model

### 构建 rag 向量数据库
def build_or_load_local_index():
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

CHROMA_HOST = "localhost"
CHROMA_PORT = 8000
COLLECTION_NAME = "tcm_knowledge"
##跳过代理
os.environ['no_proxy'] = 'localhost,127.0.0.1,::1'


def build_or_load_db_index():
    chroma_client = chromadb.HttpClient(
        host=CHROMA_HOST,
        port=CHROMA_PORT,
        tenant="default_tenant",
        database="default_database"
    )

    # 测试连接
    try:
        chroma_client.heartbeat()
        print("✅ ChromaDB 连接成功")
    except Exception as e:
        raise ConnectionError(f"❌ ChromaDB 连接失败: {e}")

    chroma_collection = chroma_client.get_or_create_collection(COLLECTION_NAME)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    if chroma_collection.count() > 0:
        print(f"✅ 已加载现有索引，共 {chroma_collection.count()} 条")
        index = VectorStoreIndex.from_vector_store(vector_store)
    else:
        print("正在构建中医知识索引...")
        documents = SimpleDirectoryReader("./rag/knowledge").load_data()
        index = VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context
        )
        print("✅ 索引构建完成")

    return index