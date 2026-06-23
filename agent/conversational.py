from langchain.memory import ConversationBufferWindowMemory
from langchain_deepseek import ChatDeepSeek
from config import DEEPSEEK_API_KEY, DEEPSEEK_MODEL
from prompts.fewshot import FEW_SHOT_EXAMPLES

memory = ConversationBufferWindowMemory(k=12, return_messages=True)

llm = ChatDeepSeek(
    model=DEEPSEEK_MODEL,
    temperature=0.3,
    api_key=DEEPSEEK_API_KEY,
    max_tokens=2048
)

def get_conversation_chain():
    return memory