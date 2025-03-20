from langchain_deepseek import ChatDeepSeek
import os
deep_seek_api_key =  os.environ.get("DEEP_SEEK_KEY")
deep_seek_baseUrl= "https://api.deepseek.com/v1"
llm = ChatDeepSeek(
    model="...",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=deep_seek_api_key,
    # other params...
)

messages = [
    ("system", "You are a helpful translator. Translate the user sentence to French."),
    ("human", "I love programming."),
]
llm.invoke(messages)