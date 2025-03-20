import uuid

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent


@tool
def get_user_age(name: str) -> str:
    """Use this tool to find the user's age."""
    # This is a placeholder for the actual implementation
    if "bob" in name.lower():
        return "42 years old"
    return "41 years old"

"""
我们使用了 MemorySaver 这个检查点，这是一个简单的内存检查点，所有的对话历史都保存在内存中。对于一个正式的应用来说，
我们需要将对话历史持久化到数据库中，可以考虑使用 SqliteSaver 或 PostgresSaver 等，LangGraph 也支持自定义检查点，
实现其他数据库的持久化，比如 MongoDB 或 Redis。
LangGraph 在第一次运行时自动保存状态，当再次使用相同的线程 ID 调用图时，图会加载其保存的状态，使得智能体可以从停下的地方继续。
"""
memory = MemorySaver()
model = init_chat_model("gpt-4o-mini",model_provider="openai",temperature=0,configurable_fields=("model", "model_provider"))

app = create_react_agent(
    model,
    tools=[get_user_age],
    checkpointer=memory,
)

# The thread id is a unique key that identifies
# this particular conversation.
# We'll just generate a random uuid here.
# This enables a single application to manage conversations among multiple users.
thread_id = uuid.uuid4()
config = {"configurable": {"thread_id": thread_id}}

# Tell the AI that our name is Bob, and ask it to use a tool to confirm
# that it's capable of working like an agent.
input_message = HumanMessage(content="hi! I'm bob. What is my age?")

for event in app.stream({"messages": [input_message]}, config, stream_mode="values"):
    event["messages"][-1].pretty_print()

# Confirm that the chat bot has access to previous conversation
# and can respond to the user saying that the user's name is Bob.
input_message = HumanMessage(content="do you remember my name?")

for event in app.stream({"messages": [input_message]}, config, stream_mode="values"):
    event["messages"][-1].pretty_print()