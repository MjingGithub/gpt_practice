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
from commonlib.openai_common_module import get_completion_with_token
messages =  [  
{'role':'system', 
 'content':'你是一个助理， 并以 Seuss 苏斯博士的风格作出回答。'},    
{'role':'user', 
 'content':'就快乐的小鲸鱼为主题给我写一首短诗'},  
] 
response, token_dict =get_completion_with_token(messages)
print(response)
print(token_dict)



