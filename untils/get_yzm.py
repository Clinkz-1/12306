import requests
from lxml import etree



def get_yzm(filename):
    url = "http://littlebigluo.qicp.net:47720/"
    files = {'pic_xxfile': (filename, open('./'+filename , 'rb'), 'image/png')}

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
    }
    resp = requests.post(url, files = files, headers=headers)
    html_str = resp.content.decode()
    html = etree.HTML(html_str)
    answer_list = html.xpath("//b/text()")[0].split(" ")
    answer=''
    for i in answer_list:
        answer += i
    return answer

if __name__ == '__main__':
    print(get_yzm('yz_img.png'))

