import requests
import json
import time
import base64
import re

from untils.captcha import getCode
from untils.get_yzm import get_yzm
from untils.telcode import telcode_dict
from untils.parse_trains_info import parseTrainsInfo,showTrainsInfo
from untils.parse_people import parsePeople,showPeople
from untils.seat_type import seat_type_dict
from untils.parse_date import parseDate

class Get12306:
    def __init__(self,username, password,train_date =None,from_station=None,to_station=None):
        self.username = username
        self.password = password
        self.train_date = train_date
        self.from_station = from_station
        self.to_station = to_station
        self.s = requests.session()
        self.s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"

    def get_cookies(self):
        """获取cookies"""
        url = 'https://www.12306.cn/index/'
        self.s.get(url)

        # 重定向到登陆界面
        url = 'https://kyfw.12306.cn/otn/login/conf'
        self.s.headers['Referer'] = 'https://kyfw.12306.cn/otn/resources/login.html'
        self.s.post(url)

        url = 'https://kyfw.12306.cn/otn/index12306/getLoginBanner'
        self.s.get(url)

        # 检查用户是否登录
        url = 'https://kyfw.12306.cn/passport/web/auth/uamtk-static'
        resp = self.s.post(url, data={'appid': 'otn'})
        print(resp.content.decode())

        # 获取登录二维码
        url = 'https://kyfw.12306.cn/passport/web/create-qr64'
        resp = self.s.post(url, data={'appid': 'otn'})
        print(resp.text)
        uuid = json.loads(resp.content.decode())['uuid']

        # 查询二维码状态
        url = 'https://kyfw.12306.cn/passport/web/checkqr'
        resp = self.s.post(url, data={'appid': 'otn', 'uuid': uuid})
        print(resp.content.decode())

    def deal_img(self):
        """处理验证码"""
        date_temp = int(time.time()*1000)
        # 补全请求的时间戳参数
        url = 'https://kyfw.12306.cn/passport/captcha/captcha-image64?login_site=E&module=login&rand=sjrand&_={}'.format(date_temp)
        resp = self.s.get(url)
        # 获取验证码图片数据,base64解密并保存
        img_b64 = json.loads(resp.content.decode())['image']
        img_bytes = base64.b64decode(img_b64)
        with open('yz_img.png', 'wb') as f:
            f.write(img_bytes)

        # 从验证码图片中获取每个答案的坐标
        answer_dict = {"1": "42,35,",
                       "2": "106,37,",
                       "3": "183,39,",
                       "4": "250,41,",
                       "5": "44,108,",
                       "6": "105,112,",
                       "7": "185,115,",
                       "8": "256,106,",
                       }

        answer_num = input("请输入正确答案序号(自动输入zd):")
        # answer_num = 'zd'
        if answer_num == 'zd':
            try:
                answer_num = get_yzm('yz_img.png')
                print("通过机器学习验证")
            except Exception:
                answer_num = getCode('./yz_img.png')
                print("通过第三方平台验证")
        self.answer = ''
        for i in answer_num:
            self.answer+=answer_dict[i]
        self.answer=self.answer[:-1]
        print(self.answer)

        # 发送图片验证请求
        date_temp = int(time.time() * 1000)
        url = 'https://kyfw.12306.cn/passport/captcha/captcha-check?answer={}&rand=sjrand&login_site=E&_={}'.format(
            self.answer, date_temp)
        resp = self.s.get(url)
        print(json.loads(resp.content.decode()))

    def login(self):
        """登陆操作"""
        url = "https://kyfw.12306.cn/passport/web/login"
        data = {'username': self.username,
                'password': self.password,
                'appid': 'otn',
                'answer': self.answer}
        resp = self.s.post(url, data=data)
        print(json.loads(resp.content.decode()))

        # 登录的后续动作
        url = 'https://kyfw.12306.cn/otn/login/userLogin'
        self.s.get(url)

        # 登陆后的页面跳转
        url = 'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin'
        self.s.get(url)
        self.s.headers['Referer'] = url

        # 获取newapptk
        url = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
        resp = self.s.post(url, data={'appid': 'otn'})
        newapptk = json.loads(resp.content.decode())['newapptk']
        print(json.loads(resp.content.decode()))

        # 登陆后验证
        url = 'https://kyfw.12306.cn/otn/uamauthclient'
        resp = self.s.post(url, data={'tk': newapptk })
        print(json.loads(resp.content.decode()))

    def get_trains_info(self):
        """获取列车信息"""
        # 更改referer,进入列车查询界面
        url = 'https://kyfw.12306.cn/otn/leftTicket/init'
        resp = self.s.get(url)
        # 解决queryX变化的问题
        query_key = re.search(r"var CLeftTicketUrl = '(.+?)';",resp.content.decode()).group(1)
        self.s.headers['Referer'] = url

        # 要查询列车的信息
        # self.train_date = input('请输入出行的日期（格式为“2019-02-01”）：')
        # self.from_station = input('请输入出发的城市或车站：')
        # self.to_station = input('请输入到达的城市或车站：')
        from_station_code = telcode_dict[self.from_station]
        to_station_code = telcode_dict[self.to_station]

        # 获取查询列车的信息
        url = "https://kyfw.12306.cn/otn/{}?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT".format(
            query_key,self.train_date,from_station_code,to_station_code)
        resp = self.s.get(url)
        trains_info = json.loads(resp.content)['data']['result']
        # 解析并构造车次信息列表
        trains_info_list = parseTrainsInfo(trains_info)
        # 优化打印效果
        showTrainsInfo(trains_info_list)

        # 选择车次trains_info_list的下标来选择
        self.train_dict = trains_info_list[int(input('请输入选择的车次的下标：'))]
        # 获取后续所需要的参数
        self.leftTicket = self.train_dict['leftTicket']
        self.secretStr = self.train_dict['secretStr']
        self.train_location = self.train_dict['train_location']

        # 检查用户是否登录
        url = 'https://kyfw.12306.cn/otn/login/checkUser'
        resp = self.s.post(url, data={'_json_att': ''})
        print(json.loads(resp.content.decode()))

    def pre_submit(self):
        """购票前确认"""
        # 发送订单请求
        url = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
        data = {
            'secretStr': self.secretStr,
            'train_date': self.train_date,
            'back_train_date': self.train_date,
            'tour_flag': 'dc',  # dc 单程 wf 往返
            'purpose_codes': 'ADULT',  # 成人
            'query_from_station_name': self.from_station,  # 车站/城市信息字典[from_station]
            'query_to_station_name': self.to_station,  # 车站/城市信息字典[to_station]
            'undefined': ''
        }
        resp = self.s.post(url, data=data)
        print(json.loads(resp.content.decode()))

        # 进入订单页面获取 key_check_isChange REPEAT_SUBMIT_TOKEN
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        resp = self.s.post(url, data={'_json_att': ''})  # 返回html
        self.REPEAT_SUBMIT_TOKEN = re.search("var globalRepeatSubmitToken = '(.*?)'", resp.content.decode()).group(1)
        self.key_check_isChange = re.search("','key_check_isChange':'(.*?)','", resp.content.decode()).group(1)

    def get_people_seat_info(self):
        """获取乘车人信息和坐位信息"""
        # 获取乘车人信息
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
        data = {
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.REPEAT_SUBMIT_TOKEN
        }
        resp = self.s.post(url, data=data)
        people_list = parsePeople(json.loads(resp.content.decode()))
        showPeople(people_list)
        # 选择乘车人
        try:
            persom_no = int(input('输入要乘车人信息的下标(默认第一个)：'))
        except:
            persom_no = 0
        person_dict = people_list[persom_no]

        # 选择坐席类型
        seat_type_in = input("请输入乘坐的类型(用拼音输入):")
        if seat_type_in in seat_type_dict.keys():
            self.seat_type = seat_type_dict[seat_type_in]
        else:
            self.seat_type = '1'

        # 构造下一个请求的参数
        self.passengerTicketStr = '{},0,1,{},{},{},{},N'.format(self.seat_type,
                                                                person_dict['name'],
                                                                person_dict['id_type_code'],
                                                                person_dict['id_no'],
                                                                person_dict['mobile_no'])
        self.oldPassengerStr = '{},{},{},1_'.format(person_dict['name'],
                                                    person_dict['id_type_code'],
                                                    person_dict['id_no'])

        # 检查乘车人信息
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
        data = {
            'cancel_flag': '2',  # 未知
            'bed_level_order_num': '000000000000000000000000000000',  # 未知
            'passengerTicketStr': self.passengerTicketStr.encode('utf-8'),
            # 1,0,1,曹嘉楠,1,320405199604292534,17714552601,N
            'oldPassengerStr': self.oldPassengerStr.encode('utf-8'),
            # 曹嘉楠,1,320405199604292534,1_
            'tour_flag': 'dc',  # 单程
            'randCode': '',
            'whatsSelect': '1',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.REPEAT_SUBMIT_TOKEN
        }
        resp = self.s.post(url, data=data)
        print(json.loads(resp.content.decode()))

    def buy_ticket(self):
        """买票"""
        # 获取排队人数
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'
        data = {
            'train_date': parseDate(self.train_date),  # Wed Feb 27 2019 00:00:00 GMT+0800 (中国标准时间)
            'train_no': self.train_dict['train_no'],  # 550000T20460
            'stationTrainCode': self.train_dict['stationTrainCode'],  # T204
            'seatType': self.seat_type,  # 席别
            'fromStationTelecode': self.train_dict['from_station'],  # one_train[6]
            'toStationTelecode': self.train_dict['to_station'],  # ? one_train[7]
            'leftTicket': self.train_dict['leftTicket'],  # one_train[12]
            'purpose_codes': '00',
            'train_location': self.train_dict['train_location'],  # one_train[15]
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.REPEAT_SUBMIT_TOKEN
        }
        resp = self.s.post(url, data=data)
        print(json.loads(resp.content.decode()))

        # 确认买票的请求
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue'
        data = {
            'passengerTicketStr': self.passengerTicketStr.encode('utf-8'),
            'oldPassengerStr': self.oldPassengerStr.encode('utf-8'),
            'randCode': '',
            'purpose_codes': '00',
            'key_check_isChange': self.key_check_isChange,
            'leftTicketStr': self.leftTicket,
            'train_location': self.train_location,  # one_train[15]
            'choose_seats': '',  # 选择坐席 ABCDEF 上中下铺 默认为空不选
            'seatDetailType': '000',
            'whatsSelect': '1',
            'roomType': '00',
            'dwAll': 'N',  # ?
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.REPEAT_SUBMIT_TOKEN
        }
        resp = self.s.post(url, data=data)
        print(json.loads(resp.content.decode()))

        # 排队等待获取订单号，根据获取的waitTime秒数之后再次重新发送本请求
        def func():
            url = 'https://kyfw.12306.cn/ot,n/confirmPassenger/queryOrderWaitTime?random={}&tourFlag=dc&_json_att=&REPEAT_SUBMIT_TOKEN={}'.format(
                int(time.time() * 1000),self.REPEAT_SUBMIT_TOKEN)
            resp = self.s.get(url)
            waitTime = json.loads(resp.content)['data']['waitTime']
            orderSequence_no = json.loads(resp.content)['data']['orderId']
            return orderSequence_no

        for i in range(3):
            try:
                orderSequence_no = func()
            except:
                if i == 2:
                    print('本次购票失败')
                    return
                time.sleep(5)
                continue

        # 获取最终结果
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForDcQueue'
        data = {
            'orderSequence_no': orderSequence_no,
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': self.REPEAT_SUBMIT_TOKEN
        }
        resp = self.s.post(url, data=data)
        print(json.loads(resp.content.decode()))

    def run(self):
        self.get_cookies()
        self.deal_img()
        self.login()
        self.get_trains_info()
        self.pre_submit()
        self.get_people_seat_info()
        self.buy_ticket()


if __name__ == '__main__':

    p1 = Get12306(17714552601,"****","2019-04-01","南京","常州")
    p1.run()




