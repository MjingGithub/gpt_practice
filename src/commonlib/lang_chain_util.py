import os
open_api_key =  os.environ.get("OPENAI_API_KEY")
LANGSMITH_API_KEY =  os.environ.get("LANGSMITH_API_KEY")

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

# model = init_chat_model("gpt-4o-mini", model_provider="openai")

messages = [
    SystemMessage("Translate the following from English into Italian"),
    HumanMessage("hi!"),
]
# We don't need to specify configurable=True if a model isn't specified.
model = init_chat_model("gpt-4o-mini",model_provider="openai",temperature=0,configurable_fields=("model", "model_provider"))

def invokeAIResponseFrom_langChain(prompt):
    response = model.invoke(prompt)
    # print("tokens:",response.response_metadata)
    return response.content

## 输出固定格式的响应
def invokeAI_with_structured_output(prompt,structured_sample):
    structured_llm  = model.with_structured_output(structured_sample)
    response = structured_llm.invoke(prompt)
    print(response)


from langchain_core.prompts import ChatPromptTemplate

template = ChatPromptTemplate([
    ("system", "You are a helpful AI bot. Your name is {name}."),
    ("human", "Hello, how are you doing?"),
    ("ai", "I'm doing well, thanks!"),
    ("human", "{user_input}"),
])

prompt_value = template.invoke(
    {
        "name": "Bob",
        "user_input": "What is your name?"
    }
)

# invokeAIResponseFrom_langChain(prompt_value)

template_string = ChatPromptTemplate([("system","把由三个反引号分隔的文本翻译成一种{style}风格。文本: ```{text}```")])

prompt_value = template_string.invoke(
    {
        "style": "正式普通话 用一个平静、尊敬的语气",
        "text": "阿，我很生气，因为我的搅拌机盖掉了，把奶昔溅到了厨房的墙上！更糟糕的是，保修不包括打扫厨房的费用。我现在需要你的帮助，伙计！"
    }
)

# invokeAIResponseFrom_langChain(prompt_value)



'''
    结构化输出
'''
# from langchain.output_parsers import ResponseSchema
# from langchain.output_parsers import StructuredOutputParser


# gift_schema = ResponseSchema(name="礼物",
#                              description="这件物品是作为礼物送给别人的吗？如果是，则回答 是的，如果否或未知，则回答 不是。")

# delivery_days_schema = ResponseSchema(name="交货天数",
#                                       description="产品需要多少天才能到达？如果没有找到该信息，则输出-1。")

# price_value_schema = ResponseSchema(name="价钱",
#                                     description="提取有关价值或价格的任何句子，并将它们输出为逗号分隔的 Python 列表")


# response_schemas = [gift_schema, 
#                     delivery_days_schema,
#                     price_value_schema]
# output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
# format_instructions = output_parser.get_format_instructions()
# print(format_instructions)

customer_review = """
这款吹叶机非常神奇。 它有四个设置：
吹蜡烛、微风、风城、龙卷风。 
两天后就到了，正好赶上我妻子的
周年纪念礼物。 
我想我的妻子会喜欢它到说不出话来。 
到目前为止，我是唯一一个使用它的人，而且我一直
每隔一天早上用它来清理草坪上的叶子。 
它比其他吹叶机稍微贵一点，
但我认为它的额外功能是值得的。
"""

system_prompt = ChatPromptTemplate([("system","""对于以下文本，请从中提取以下信息：

礼物：该商品是作为礼物送给别人的吗？ 
如果是，则回答 是的；如果否或未知，则回答 不是。

交货天数：产品需要多少天
到达？ 如果没有找到该信息，则输出-1。

价钱：提取有关价值或价格的任何句子，
并将它们输出为逗号分隔的 Python 列表。

使用以下键将输出格式化为 JSON：
礼物
交货天数
价钱

文本: {text} """)])

# prompt_template = system_prompt.invoke(
#      {
#         "format_instructions": format_instructions,
#         "text": customer_review
#     })
# invokeAIResponseFrom_langChain(prompt_template)
# print(messages[0].content)



# 另一种方式格式化输出
# 更多信息见：https://python.langchain.com/docs/how_to/structured_output/
# from typing import Optional
# from typing_extensions import Annotated, TypedDict
# from pydantic import BaseModel, Field
# # Pydantic
# class Joke(TypedDict):
#     """Joke to tell user."""

#     礼物: str = Annotated[str, ..., "这件物品是作为礼物送给别人的吗？如果是，则回答 是的，如果否或未知，则回答 不是。"]
#     交货天数: str =Annotated[Optional[int], None, "产品需要多少天才能到达？如果没有找到该信息，则输出-1。"]
#     价钱: str = Annotated[str, ..., "提取有关价值或价格的任何句子，并将它们输出为逗号分隔的 Python 列表"]

# prompt = system_prompt.invoke({ "text": customer_review})
# invokeAI_with_structured_output(prompt,Joke)

# invokeAIResponseFrom_langChain("""用1000字以内概括说明，LangGraph是什么，请参考以下链接中的文档说明：
#                                https://python.langchain.com/docs/versions/migrating_memory/""")