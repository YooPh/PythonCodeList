import requests
import os
import json
import matplotlib.pyplot as plt
from prettytable import PrettyTable
import time
from colorama import init, Fore, Back, Style

headers = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36',
    'Accept': 'image/avif,image/webp,image/apng,image/*,*/*;q=0.8',
    'Referer': 'http://fund.eastmoney.com/',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

params = (
    ('v', '0.6514912493442406'),
    ('rt', '1605665314498'),
)

# init(autoreset=False)


class Colored(object):
    #  前景色:红色  背景色:默认
    def red(self, s):
        return Fore.LIGHTRED_EX + s + Fore.RESET

    #  前景色:绿色  背景色:默认
    def green(self, s):
        return Fore.LIGHTGREEN_EX + s + Fore.RESET

    def yellow(self, s):
        return Fore.LIGHTYELLOW_EX + s + Fore.RESET

    def white(self, s):
        return Fore.LIGHTWHITE_EX + s + Fore.RESET

    def blue(self, s):
        return Fore.LIGHTBLUE_EX + s + Fore.RESET



def find(code_list):
    dataTemp = []
    dataTemp1 = []
    title = [color.yellow("基金代码"), color.yellow("基金名称"), color.yellow("净值估算"), color.yellow("估算涨幅(%)"), color.yellow("更新时间")]
    t = PrettyTable(title)
    while True:
        dataTemp.clear()
        t.clear_rows()

        for code_item in code_list:
            try:
                url = "http://fundgz.1234567.com.cn/js/" + code_item + ".js"
                response1 = requests.get(url, headers=headers, params=params, verify=False)
                r = response1.content.decode(encoding='utf-8').replace("jsonpgz(", "")
                r = r.replace(");", "")
                r_dict = json.loads(r)
                gszzl = ""
                if float(r_dict.get("gszzl"))>0:
                    gszzl = color.red(r_dict.get("gszzl"))
                else:
                    gszzl = color.green(r_dict.get("gszzl"))
                row = [r_dict.get("fundcode"), r_dict.get("name"), r_dict.get("gsz"), gszzl,
                       r_dict.get("gztime")]
                dataTemp.append(r_dict.get("gztime"))
                response1.close()
                t.add_row(row)
            except:
                pass

        # if dataTemp1 != dataTemp:
        #     dataTemp1 = dataTemp.copy()
        #     os.system('cls')
        #     print(t)
        os.system('cls')
        print(t)
        time.sleep(5)


def main():
    if not os.path.exists("./code.txt"):
        open('./code.txt','w')
        print("未找到code.txt文件")
    else:
        with open("code.txt","r",encoding='utf-8') as fp:
            codes = fp.read()
            code_list = codes.split('\n')
            find(code_list)


if __name__ == "__main__":
    color = Colored()
    main()
