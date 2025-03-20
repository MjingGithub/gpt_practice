import sys
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
from commonlib.openai_common_module import get_completion_default
import C2.function_utils as function_utils


'''
    setp1:大模型，根据商品信息和提问，提取相关商品和分类
'''
delimiter = "####"
system_message = f"""
你将提供服务查询。
服务查询将使用{delimiter}字符分隔。

仅输出一个 Python 对象列表，其中每个对象具有以下格式：
    'category': <计算机和笔记本电脑、智能手机和配件、电视和家庭影院系统、游戏机和配件、音频设备、相机和摄像机中的一个>,
或者
    'products': <必须在下面的允许产品列表中找到的产品列表>

类别和产品必须在客户服务查询中找到。
如果提及了产品，则必须将其与允许产品列表中的正确类别相关联。
如果未找到产品或类别，则输出空列表。

允许的产品：

计算机和笔记本电脑类别：
TechPro Ultrabook
BlueWave Gaming Laptop
PowerLite Convertible
TechPro Desktop
BlueWave Chromebook

智能手机和配件类别：
SmartX ProPhone
MobiTech PowerCase
SmartX MiniPhone
MobiTech Wireless Charger
SmartX EarBuds

电视和家庭影院系统类别：
CineView 4K TV
SoundMax Home Theater
CineView 8K TV
SoundMax Soundbar
CineView OLED TV
c
游戏机和配件类别：
GameSphere X
ProGamer Controller
GameSphere Y
ProGamer Racing Wheel
GameSphere VR Headset

音频设备类别：
AudioPhonic Noise-Canceling Headphones
WaveSound Bluetooth Speaker
AudioPhonic True Wireless Earbuds
WaveSound Soundbar
AudioPhonic Turntable

相机和摄像机类别：
FotoSnap DSLR Camera
ActionCam 4K
FotoSnap Mirrorless Camera
ZoomMaster Camcorder
FotoSnap Instant Camera

仅输出 Python 对象列表，不包含其他字符信息。
"""
user_message_1 = f"""
 请查询 SmartX ProPhone 智能手机和 FotoSnap 相机，包括单反相机。
 另外，请查询关于电视产品的信息。 """
messages =  [  
{'role':'system', 
 'content': system_message},    
{'role':'user', 
 'content': f"{delimiter}{user_message_1}{delimiter}"},  
] 
category_and_product_response_1 = get_completion_default(messages)
print(category_and_product_response_1)


'''
    step2:根据step1产生的分类信息生成包含产品或类别信息的字符串
'''

print(function_utils.get_product_by_name("TechPro Ultrabook"))
print(function_utils.get_products_by_category("电脑和笔记本"))

category_and_product_list = function_utils.read_string_to_list(category_and_product_response_1)
print(category_and_product_list)

product_information_for_user_message_1 = function_utils.generate_output_string(category_and_product_list)
print(product_information_for_user_message_1)


'''
    step3:将Python字符串读取并召回相关产品和详细信息输入给大模型，作为背景知识，请求大模型回答问题
'''

system_message = f"""
您是一家大型电子商店的客服助理。
请以友好和乐于助人的口吻回答问题，并尽量简洁明了。
请确保向用户提出相关的后续问题。
"""
user_message_1 = f"""
请介绍一下 SmartX ProPhone 智能手机和 FotoSnap 相机，包括单反相机。
另外，介绍关于电视产品的信息。"""
messages =  [  
{'role':'system',
 'content': system_message},   
{'role':'user',
 'content': user_message_1},  
{'role':'assistant',
 'content': f"""相关产品信息:\n\
 {product_information_for_user_message_1}"""},   
]
final_response = get_completion_default(messages)
print(final_response)