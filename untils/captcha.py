# THE WINTER IS COMING! the old driver will be driving who was a man of the world!
# -*- coding: utf-8 -*- python 3.6.7, create time is 18-12-26 上午11:18 GMT+8

import hashlib
import requests
from datetime import datetime

RUOUSER = 'yaoxiangyu556696'
RUOPASS = 'yao556696'

# 若快 12306打码 直接传入本地文件路径
def getCode(img):
    url = "http://api.ruokuai.com/create.json"
    fileBytes = open(img, "rb").read()
    paramDict = {
        'username': RUOUSER,
        'password': RUOPASS,
        'typeid': 6113, # 专门用来识别12306图片验证的类型id
        'timeout': 90,
        'softid': 117157, # 推广用的
        'softkey': '70acaa1e477a4374a7736264a24b974b' # 推广用的
    }
    paramKeys = ['username',
                 'password',
                 'typeid',
                 'timeout',
                 'softid',
                 'softkey'
                 ]
    result = http_upload_image(url, paramKeys, paramDict, fileBytes)
    return result['Result']


# 若快12306打码 上传图片
def http_upload_image(url, paramKeys, paramDict, filebytes):
    timestr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    boundary = '------------' + hashlib.md5(timestr.encode("utf8")).hexdigest().lower()
    boundarystr = '\r\n--%s\r\n' % (boundary)

    bs = b''
    for key in paramKeys:
        bs = bs + boundarystr.encode('ascii')
        param = "Content-Disposition: form-data; name=\"%s\"\r\n\r\n%s" % (key, paramDict[key])
        # print param
        bs = bs + param.encode('utf8')
    bs = bs + boundarystr.encode('ascii')

    header = 'Content-Disposition: form-data; name=\"image\"; filename=\"%s\"\r\nContent-Type: image/gif\r\n\r\n' % ('sample')
    bs = bs + header.encode('utf8')

    bs = bs + filebytes
    tailer = '\r\n--%s--\r\n' % (boundary)
    bs = bs + tailer.encode('ascii')

    headers = {'Content-Type': 'multipart/form-data; boundary=%s' % boundary,
               'Connection': 'Keep-Alive',
               'Expect': '100-continue',
               }
    response = requests.post(url, params='', data=bs, headers=headers)
    return response.json()


if __name__ == '__main__':
    # 测试
    ret = getCode('../capcha.png')
    print(ret)