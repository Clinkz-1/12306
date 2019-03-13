import requests
import re
import json

# 获取列车电报码,并写入文件
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
}

url = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js"
resp = requests.get(url,headers=headers)

telcode_str = re.search(r"var station_names ='(.*)';",resp.content.decode()).group(1)
telcode_dict = {}
for code in telcode_str.split('@')[1:]:
    telcode_dict[code.split('|')[1]] = code.split('|')[2]

with open('./untils/telcode.py','w',encoding='utf-8') as f :
    f.write("telcode_dict = ")
    f.write(json.dumps(telcode_dict,ensure_ascii=False, indent=4))