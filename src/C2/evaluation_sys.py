import sys
import json 
from pathlib import Path # if you haven't already done so
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

# Additionally remove the current file's directory from sys.path
try:
    sys.path.remove(str(parent))
except ValueError: # Already removed
    pass


print(sys.path)
from commonlib.openai_common_module import get_completion_default,moderations_input
import C2.function_utils as function_utils
'''
注意：限于模型对中文理解能力较弱，中文 Prompt 可能会随机出现不成功，可以多次运行；也非常欢迎同学探究更稳定的中文 Prompt
'''
def process_user_message_ch(user_input, all_messages, debug=True):
    """
    对用户信息进行预处理
    
    参数:
    user_input : 用户输入
    all_messages : 历史信息
    debug : 是否开启 DEBUG 模式,默认开启
    """
    # 分隔符
    delimiter = "```"
    
    # 第一步: 使用 OpenAI 的 Moderation API 检查用户输入是否合规或者是一个注入的 Prompt
    response = moderations_input(input=user_input)
    moderation_output = response["results"][0]

    # 经过 Moderation API 检查该输入不合规
    if moderation_output["flagged"]:
        print("第一步：输入被 Moderation 拒绝")
        return "抱歉，您的请求不合规"

    # 如果开启了 DEBUG 模式，打印实时进度
    if debug: print("第一步：输入通过 Moderation 检查")
    
    # 第二步：抽取出商品和对应的目录，类似于之前课程中的方法，做了一个封装
    category_and_product_response = function_utils.find_category_and_product_only(user_input, function_utils.get_products_and_category())
    #print(category_and_product_response)
    # 将抽取出来的字符串转化为列表
    category_and_product_list = function_utils.read_string_to_list(category_and_product_response)
    #print(category_and_product_list)

    if debug: print("第二步：抽取出商品列表")

    # 第三步：查找商品对应信息
    product_information = function_utils.generate_output_string(category_and_product_list)
    if debug: print("第三步：查找抽取出的商品信息")

    # 第四步：根据信息生成回答
    system_message = f"""
        您是一家大型电子商店的客户服务助理。\
        请以友好和乐于助人的语气回答问题，并提供简洁明了的答案。\
        请确保向用户提出相关的后续问题。
    """
    # 插入 message
    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': f"{delimiter}{user_input}{delimiter}"},
        {'role': 'assistant', 'content': f"相关商品信息:\n{product_information}"}
    ]
    # 获取 GPT3.5 的回答
    # 通过附加 all_messages 实现多轮对话
    final_response = get_completion_default(all_messages + messages)
    if debug:print("第四步：生成用户回答")
    # 将该轮信息加入到历史信息中
    all_messages = all_messages + messages[1:]

    # 第五步：基于 Moderation API 检查输出是否合规
    response = moderations_input(input=final_response)
    moderation_output = response["results"][0]

    # 输出不合规
    if moderation_output["flagged"]:
        if debug: print("第五步：输出被 Moderation 拒绝")
        return "抱歉，我们不能提供该信息"

    if debug: print("第五步：输出经过 Moderation 检查")

    # 第六步：模型检查是否很好地回答了用户问题
    user_message = f"""
    用户信息: {delimiter}{user_input}{delimiter}
    代理回复: {delimiter}{final_response}{delimiter}

    回复是否足够回答问题
    如果足够，回答 Y
    如果不足够，回答 N
    仅回答上述字母即可
    """
    # print(final_response)
    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': user_message}
    ]
    # 要求模型评估回答
    evaluation_response = get_completion_default(messages)
    # print(evaluation_response)
    if debug: print("第六步：模型评估该回答")

    # 第七步：如果评估为 Y，输出回答；如果评估为 N，反馈将由人工修正答案
    if "Y" in evaluation_response:  # 使用 in 来避免模型可能生成 Yes
        if debug: print("第七步：模型赞同了该回答.")
        return final_response, all_messages
    else:
        if debug: print("第七步：模型不赞成该回答.")
        neg_str = "很抱歉，我无法提供您所需的信息。我将为您转接到一位人工客服代表以获取进一步帮助。"
        return neg_str, all_messages

user_input = "请告诉我关于 smartx pro phone 和 the fotosnap camera 的信息。另外，请告诉我关于你们的tvs的情况。"
response,_ = process_user_message_ch(user_input,[])
print(response)