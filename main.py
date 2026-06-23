from rag.index import build_or_load_index
from agent.conversational import memory, llm
from utils.safety import add_safety_note
from prompts.system_prompt import SYSTEM_PROMPT
from config import DEEPSEEK_API_KEY

index = build_or_load_index()
retriever = index.as_retriever(similarity_top_k=8)

print("中医AI助手已启动（多轮对话模式）\n")


def chat():
    while True:
        user_input = input("\n您：")
        if user_input.lower() in ["退出", "quit", "q"]:
            print("再见！")
            break

        # 1. 多轮对话历史
        chat_history = memory.load_memory_variables({})["chat_history"]

        # 2. RAG 检索
        retrieved = retriever.retrieve(user_input)
        context = "\n\n".join([node.text for node in retrieved])

        # 3. 最终 Prompt
        prompt = f"""
{SYSTEM_PROMPT}

对话历史：
{chat_history}

用户最新描述：{user_input}

检索到的中医知识：
{context}

请进行综合辨证论治。
"""

        response = llm.invoke(prompt)
        final_response = add_safety_note(response.content)

        print("\n中医AI：", final_response)

        # 保存记忆
        memory.save_context({"input": user_input}, {"output": response.content})


if __name__ == "__main__":
    if not DEEPSEEK_API_KEY:
        print("错误：请设置 DEEPSEEK_API_KEY")
    else:
        chat()