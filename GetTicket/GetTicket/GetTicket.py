# -*- coding: UTF-8 -*-
import requests
import json
import re
import os
from prettytable import PrettyTable

def get_station():
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.916'
    response = requests.get(url).text
    name = re.findall(r'.*?\|(.*?)\|.*?\|.*?\|.*?\|.*?', response)
    referred = re.findall(r'.*?\|.*?\|(.*?)\|.*?\|.*?\|.*?', response)
    station = dict(zip(name, referred))
    return station


def decrypt(string):
    reg = re.compile(
        '.*?\|预订\|.*?\|(.*?)\|(.*?)\|(.*?)\|.*?\|.*?\|(.*?)\|(.*?)\|(.*?)\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|.*?\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|.*?\|.*?\|.*?\|.*')
    result = re.findall(reg, string)[0]
    return result


def query(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36",
        "Cookie": "_uab_collina=160532058677272595790286; JSESSIONID=58AC231A54617B4369B17CB09854FF00; RAIL_EXPIRATION=1605658794908; RAIL_DEVICEID=IKRFKexsQH7-tXX-o6Ul8hp0843D5tVDwfjfdmIe4B_s_FYxPPobk2Zjmn_k8dgkVj2PxrCXbVKvknwufAoYyn8sepo0UVfkSRarrCggjvMKwaswdEnDKmFUdLUR6vQe0haG1vXV83z4YsMMlzAMHxjAwUsBgCHx; _jc_save_wfdc_flag=dc; _jc_save_fromStation=%u53A6%u95E8%2CXMS; _jc_save_toStation=%u5E7F%u5DDE%2CGZQ; BIGipServerpool_passport=82051594.50215.0000; route=c5c62a339e7744272a54643b3be5bf64; BIGipServerotn=250610186.24610.0000; _jc_save_fromDate=2020-11-15; _jc_save_toDate=2020-11-15"
    }
    f = requests.get(url, headers=headers)
    response = json.loads(f.content.decode(encoding='utf-8-sig'))
    dataList1 = []
    data = ["车次", "出发站", "到达站", "出发时间", "到达时间", "历时", "其他", "无座", "硬座", "软座", "硬卧二等", "动卧", "软卧一等", "高级软卧",
            "二等座",
            "一等座",
            "商务/特等"]
    t = PrettyTable(data)
    dataList1.append(data)
    result = response['data']['result']
    dict_new = {value: key for key, value in get_station().items()}
    dataList2 = []
    for item in result:
        dataList2.append(decrypt(item))

    for item in dataList2:
        dataTemp = list(item)
        dataTemp[1] = dict_new.get(dataTemp[1])
        dataTemp[2] = dict_new.get(dataTemp[2])
        t.add_row(dataTemp)
    print(t)


def main():
    while True:
        fun = input("输入功能码(查询：f 退出：q 刷新上次查询：r)：")
        if fun == "f":
            datetime = input("请输入查询日期(yyyy-mm-dd)：")
            from_station = input("请输入出发站名：")
            to_station = input("请输入到达站名：")
            try:
                os.system('cls')
                from_station = get_station().get(from_station)
                to_station = get_station().get(to_station)
                input_url = "https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=" + datetime + "&leftTicketDTO.from_station=" + from_station + "&leftTicketDTO.to_station=" + to_station + "&purpose_codes=ADULT"
                query(input_url)
            except:
                print("查询出错")
        elif fun=="r":
            try:
                os.system('cls')
                query(input_url)
            except:
                print("查询出错")
        elif fun == "q":
            break


if __name__ == "__main__":
    main()
