# -*- coding: utf-8 -*-
"""
@author: liuyw
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep


class TrainTicket(object):
    def __init__(self, headless):
        self.login_url = 'https://kyfw.12306.cn/otn/resources/login.html'
        self.main_url = 'https://kyfw.12306.cn/otn/view/index.html'
        # 浏览器设置
        chrome_options = Options()
        # 取消浏览器日志
        chrome_options.add_argument('log-level=3')
        # 规避被检测
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        # 是否使用无头模式
        if headless:
            chrome_options.add_argument('--headless')  # 为Chrome配置无头模式
            chrome_options.add_argument('--disable-gpu')
        # 创建浏览器
        self.bro = webdriver.Chrome(options=chrome_options)

    def login(self):
        self.bro.get(self.login_url)
        print('请登录账号!')
        while True:
            if self.bro.current_url == self.main_url:
                print('登录成功!')
                break



if __name__ == '__main__':
    tt = TrainTicket(False)
    tt.login()