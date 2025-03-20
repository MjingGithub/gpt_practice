import json 
import os
print(os.getcwd())  # 打印当前工作目录
# 产品信息
# 打开并读取JSON文件
with open('products.json', 'r', encoding='utf-8') as file:
    products = json.load(file)
def get_product_by_name(name):
    """
    根据产品名称获取产品

    参数:
    name: 产品名称
    """
    return products.get(name, None)

def get_products_by_category(category):
    """
    根据类别获取产品

    参数:
    category: 产品类别
    """
    return [product for product in products.values() if product["category"] == category]

def generate_output_string(data_list):
    output_string=''
    """
    根据输入的数据列表生成包含产品或类别信息的字符串。

    参数:
    data_list: 包含字典的列表，每个字典都应包含 "products" 或 "category" 的键。

    返回:
    output_string: 包含产品或类别信息的字符串。
    """
    if data_list is None:
        return output_string

    for data in data_list:
        try:
            if "products" in data:
                products_list = data["products"]
                for product_name in products_list:
                    product = get_product_by_name(product_name)
                    if product:
                        output_string += json.dumps(product, indent=4) + "\n"
                    else:
                        print(f"Error: Product '{product_name}' not found")
            elif "category" in data:
                category_name = data["category"]
                category_products = get_products_by_category(category_name)
                for product in category_products:
                    output_string += json.dumps(product, indent=4) + "\n"
            else:
                print("Error: Invalid object format")
        except Exception as e:
            print(f"Error: {e}")

    return output_string 


def read_string_to_list(input_string):
    """
    将输入的字符串转换为 Python 列表。

    参数:
    input_string: 输入的字符串，应为有效的 JSON 格式。

    返回:
    list 或 None: 如果输入字符串有效，则返回对应的 Python 列表，否则返回 None。
    """
    if input_string is None:
        return None

    try:
        # 将输入字符串中的单引号替换为双引号，以满足 JSON 格式的要求
        input_string = input_string.replace("'", "\"")  
        data = json.loads(input_string)
        return data
    except json.JSONDecodeError:
        print("Error: Invalid JSON string")
        return None   
    