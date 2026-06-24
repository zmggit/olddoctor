import os

def conver():
    for filename in os.listdir("./rag/knowledge"):
        if filename.endswith(".txt"):
            filepath = os.path.join("./rag/knowledge", filename)
            try:
                with open(filepath, "r", encoding="gbk") as f:
                    content = f.read()
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"✅ {filename} 转换成功")
            except Exception as e:
                print(f"❌ {filename} 失败: {e}")