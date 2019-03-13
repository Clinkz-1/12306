# THE WINTER IS COMING! the old driver will be driving who was a man of the world!
# -*- coding: utf-8 -*- python 3.6.7, create time is 18-12-26 下午12:25 GMT+8

import urllib.parse
from .telcode import telcode_dict

def parseTrainsInfo(trains_list):
    """
    解析列车信息列表, 返回列车信息列表
    """
    trains_infos_list = []

    if trains_list == []:
        return []

    for train_info in trains_list:
        train_info_list = train_info.split('|')
        train_info_dict = {}
        # 构造列车信息
        train_info_dict['secretStr'] = urllib.parse.unquote(train_info_list[0])  # secretStr ;为''时无法购买车票
        # train_info_list[1]  预定/列车停运
        train_info_dict['train_no'] = urllib.parse.unquote(train_info_list[2])  # train_no
        train_info_dict['stationTrainCode'] = urllib.parse.unquote(train_info_list[3])  # stationTrainCode 即车次 # 展示
        train_info_dict['start_station'] = urllib.parse.unquote(train_info_list[4])  # 始发站 # 展示
        train_info_dict['end_station'] = urllib.parse.unquote(train_info_list[5])  # 终点站 # 展示
        train_info_dict['from_station'] = urllib.parse.unquote(train_info_list[6])  # 出发站 # 展示
        train_info_dict['to_station'] = urllib.parse.unquote(train_info_list[7])  # 到达站 # 展示
        train_info_dict['from_time'] = urllib.parse.unquote(train_info_list[8])  # 出发时间 # 展示
        train_info_dict['to_time'] = urllib.parse.unquote(train_info_list[9])  # 到达时间 # 展示
        train_info_dict['use_time'] = urllib.parse.unquote(train_info_list[10])  # 时长 # 展示
        train_info_dict['buy_able'] = urllib.parse.unquote(train_info_list[11])  # 能否购买 Y 可以购买 N 不可以购买 IS_TIME_NOT_BUY 停运 # 展示
        train_info_dict['leftTicket'] = urllib.parse.unquote(train_info_list[12])  # leftTicket
        train_info_dict['start_time'] = urllib.parse.unquote(train_info_list[13])  # 车次始发日期 # 展示
        train_info_dict['train_location'] = urllib.parse.unquote(train_info_list[15])  # train_location ?
        train_info_dict['from_station_no'] = urllib.parse.unquote(train_info_list[16])  # 出发站编号
        train_info_dict['to_station_no'] = urllib.parse.unquote(train_info_list[17])  # 到达站编号
        # 14,18,19,20,27,34,35未知
        train_info_dict['gaojiruanwo'] = urllib.parse.unquote(train_info_list[21])  # 高级软卧 # 展示
        train_info_dict['qita'] = urllib.parse.unquote(train_info_list[22])  # 其他 # 展示
        train_info_dict['ruanwo'] = urllib.parse.unquote(train_info_list[23])  # 软卧 # 展示
        train_info_dict['ruanzuo'] = urllib.parse.unquote(train_info_list[24])  # 软座 # 展示
        train_info_dict['tedengzuo'] = urllib.parse.unquote(train_info_list[25])  # 特等座 # 展示
        train_info_dict['wuzuo'] = urllib.parse.unquote(train_info_list[26])  # 无座 # 展示
        train_info_dict['yingwo'] = urllib.parse.unquote(train_info_list[28])  # 硬卧 # 展示
        train_info_dict['yingzuo'] = urllib.parse.unquote(train_info_list[29])  # 硬座 # 展示
        train_info_dict['erdengzuo'] = urllib.parse.unquote(train_info_list[30])  # 二等座 # 展示
        train_info_dict['yidengzuo'] = urllib.parse.unquote(train_info_list[31])  # 一等座 # 展示
        train_info_dict['shangwuzuo'] = urllib.parse.unquote(train_info_list[32])  # 商务座 # 展示
        train_info_dict['dongwo'] = urllib.parse.unquote(train_info_list[33])  # 动卧 # 展示
        trains_infos_list.append(train_info_dict)
    return trains_infos_list

def print_style(value,length,type):
    if value =='':
        return '--'
    if value=='有'or value=='无':
        return value
    return value if len(value) == length else value+' '*type*(length - len(value))


def showTrainsInfo(trains_list):
    telcode_dict_re = {val:key for key,val in telcode_dict.items()}
    length = 113
    print('*' * length)
    print('   |车次 | 出发站 | 到达站 |出发时间|到达时间|历时 |特等座|一等座|二等座|高级软卧|一等软卧|动卧|硬卧|软座|硬座|无座|其他')
    print('=' * length)
    num = 0
    for train_dict in trains_list:
        print('{}|{}|{}|{}| {}  | {} |{}|  {}  |  {}  |  {}  |  {}   |  {}   | {} | {} | {} | {} | {} | {}'.format(
            print_style(str(num),3,1),
            print_style(train_dict['stationTrainCode'],5,1),
            print_style(telcode_dict_re[train_dict['from_station']],4,2),
            print_style(telcode_dict_re[train_dict['to_station']],4,2),
            print_style(train_dict['from_time'],5,1),
            print_style(train_dict['to_time'],5,1),
            print_style(train_dict['use_time'],5,1),
            print_style(train_dict['tedengzuo'],2,1),
            print_style(train_dict['yidengzuo'],2,1),
            print_style(train_dict['erdengzuo'],2,1),
            print_style(train_dict['gaojiruanwo'],2,1),
            print_style(train_dict['ruanwo'],2,1),
            print_style(train_dict['dongwo'],2,1),
            print_style(train_dict['yingwo'],2,1),
            print_style(train_dict['ruanzuo'],2,1),
            print_style(train_dict['yingzuo'],2,1),
            print_style(train_dict['wuzuo'],2,1),
            '--',
        ))
        num +=1
        print('-' * length)
    print('*' * length)
