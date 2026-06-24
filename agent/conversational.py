from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_deepseek import ChatDeepSeek
from config import DEEPSEEK_API_KEY, DEEPSEEK_MODEL


llm = ChatDeepSeek(
    model=DEEPSEEK_MODEL,
    temperature=0.3,
    api_key=DEEPSEEK_API_KEY,
    max_tokens=2048
)

def get_chat_history(session_id: str = "default_user"):
    store = SQLChatMessageHistory(
        session_id=session_id,
        connection_string="sqlite:///chat_history.db"
    )
    return store.messages

def save_context(user_input: str, ai_output: str,session_id: str = "default_user"):
    store = SQLChatMessageHistory(
        session_id=session_id,
        connection_string="sqlite:///chat_history.db"
    )
    store.add_user_message(user_input)
    store.add_ai_message(ai_output)
