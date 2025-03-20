# from langchain.chains import LLMChain
# from langchain.memory import ConversationBufferMemory
# from langchain_core.messages import SystemMessage
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.prompts.chat import (
#     ChatPromptTemplate,
#     HumanMessagePromptTemplate,
#     MessagesPlaceholder,
# )
# from langchain_openai import ChatOpenAI
# import os
# # open_api_key =  os.environ.get("OPENAI_API_KEY")

# # print(open_api_key)
# prompt = ChatPromptTemplate(
#     [
#         MessagesPlaceholder(variable_name="chat_history"),
#         HumanMessagePromptTemplate.from_template("{text}"),
#     ]
# )

# memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# legacy_chain = LLMChain(
#     llm=ChatOpenAI(),
#     prompt=prompt,
#     memory=memory,
# )

# legacy_result = legacy_chain.invoke({"text": "my name is bob"})
# print(legacy_result)

# # legacy_result = legacy_chain.invoke({"text": "what was my name"})

import uuid

from IPython.display import Image, display
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain.chat_models import init_chat_model

# Define a new graph
workflow = StateGraph(state_schema=MessagesState)

# Define a chat model
# model = ChatOpenAI()

model = init_chat_model("gpt-4o-mini",model_provider="openai",temperature=0,configurable_fields=("model", "model_provider"))


# Define the function that calls the model
def call_model(state: MessagesState):
    response = model.invoke(state["messages"])
    # We return a list, because this will get added to the existing list
    return {"messages": response}


# Define the two nodes we will cycle between
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)


# Adding memory is straight forward in langgraph!
memory = MemorySaver()

app = workflow.compile(
    checkpointer=memory
)


# The thread id is a unique key that identifies
# this particular conversation.
# We'll just generate a random uuid here.
# This enables a single application to manage conversations among multiple users.
thread_id = uuid.uuid4()
config = {"configurable": {"thread_id": thread_id}}


input_message = HumanMessage(content="hi! I'm bob")
for event in app.stream({"messages": [input_message]}, config, stream_mode="values"):
    event["messages"][-1].pretty_print()

# Here, let's confirm that the AI remembers our name!
input_message = HumanMessage(content="what was my name?")
for event in app.stream({"messages": [input_message]}, config, stream_mode="values"):
    event["messages"][-1].pretty_print()