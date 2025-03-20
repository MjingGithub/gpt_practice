from openai import OpenAI
import os
api_key =  os.environ.get("OPENAI_API_KEY")
baseUrl = "https://api.openai.com/v1"
deep_seek_api_key =  os.environ.get("DEEP_SEEK_KEY")
deep_seek_baseUrl= "https://api.deepseek.com/v1"
print(api_key)
client = OpenAI(api_key=api_key,base_url=baseUrl)
# 导入第三方库
def get_completion(prompt, model="gpt-4o-mini",temperature=0):
    messages = [{"role": "system", "content": "You are a helpful assistant."},{"role":"user","content":prompt}]
    response = client.chat.completions.create(
        messages=messages,
        model=model,
        store=True,
        temperature=temperature, # 值越低则输出文本随机性越低
    )
    return response.choices[0].message.content

# 默认存储对话的接口
def get_completion_default(messages, model="gpt-4o-mini",temperature=0):
    response = client.chat.completions.create(
        messages=messages,
        model=model,
        store=False,
        temperature=temperature, # 值越低则输出文本随机性越低
    )
    return response.choices[0].message.content

# 指定最大token数量，并返回消耗token数
def get_completion_with_token(messages, model="gpt-4o-mini",temperature=0,max_tokens=500):
    '''
     使用 OpenAI 的 GPT-3 模型生成聊天回复，并返回生成的回复内容以及使用的 token 数量。

    参数:
    messages: 聊天消息列表。
    model: 使用的模型名称。默认为"gpt-3.5-turbo"。
    temperature: 控制生成回复的随机性。值越大，生成的回复越随机。默认为 0。
    max_tokens: 生成回复的最大 token 数量。默认为 500。

    返回:
    content: 生成的回复内容。
    token_dict: 包含'prompt_tokens'、'completion_tokens'和'total_tokens'的字典，分别表示提示的 token 数量、生成的回复的 token 数量和总的 token 数量。
    '''
    response = client.chat.completions.create(
        messages=messages,
        model=model,
        store=True,
        temperature=temperature, # 值越低则输出文本随机性越低
        max_tokens=max_tokens,
    )
    content =  response.choices[0].message.content
    token_dict = {
    'prompt_tokens':response.usage.prompt_tokens,
    'completion_tokens':response.usage.completion_tokens,
    'total_tokens':response.usage.total_tokens,
    }
    return content,token_dict

def moderations_input(model="omni-moderation-2024-09-26",input=""):
    ''' 
        评估用户输入合法性
    '''
    return client.moderations.create(model=model,input=input,)

# deepseek
def get_completion_deepSeek(messages, model="deepseek-chat",temperature=0):
    response = client.chat.completions.create(
        messages=messages,
        model=model,
        store=False,
        temperature=temperature, # 值越低则输出文本随机性越低
    )
    return response.choices[0].message.content