def parsePeople(people_temp_list):
    people_infos_list = people_temp_list['data']['normal_passengers']
    people_list = []
    for person_info in people_infos_list:
        person_info_dict = {}
        person_info_dict['name'] = person_info.get('passenger_name', '')
        person_info_dict['gender'] = person_info.get('sex_name', '')
        person_info_dict['id_type_code'] = person_info.get('passenger_id_type_code', '')
        person_info_dict['id_no'] = person_info.get('passenger_id_no', '')
        person_info_dict['mobile_no'] = person_info.get('mobile_no', '')
        person_info_dict['email'] = person_info.get('email','')
        people_list.append(person_info_dict)
    return people_list

def print_style(value,length,type):
    """value:值, length:指定长度, type:补全类型(1:英文 2:中文)"""
    return value if len(value) == length else value+' '*type*(length - len(value))

def showPeople(people_list):
    length = 64
    print('*' * length)
    print(" 姓名   | 性别 |      身份证      |   手机号  | 邮箱 ")
    print('=' * length)
    for person_dict in people_list:
        print("{}|  {}  |{}|{}|{}".format(
            print_style(person_dict['name'],4,2),
            person_dict['gender'],
            person_dict['id_no'],
            person_dict['mobile_no'],
            person_dict['email'],
        ))
        print('-' * length)
    print('*' * length)


if __name__ == '__main__':
    showPeople([1])


