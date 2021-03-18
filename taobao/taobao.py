from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions
import json
import os
import time

# 无头浏览器
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

# 规避被检测
options = ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])

bro = webdriver.Chrome(options=options)
login_url = 'https://login.taobao.com/member/login.jhtml?spm=a21bo.2017.754894437.1.5af911d97nmX7Z&f=top&redirectURL=https%3A%2F%2Fwww.taobao.com%2F'
bro.get(login_url)

user_name=bro.find_element_by_xpath('//*[@id="fm-login-id"]')
user_name.send_keys('wyf395897292')
user_pwd=bro.find_element_by_xpath('//*[@id="fm-login-password"]')
user_pwd.send_keys('ijliqnyqtd12....')
login_btn = bro.find_element_by_xpath('//*[@id="login-form"]/div[4]/button')
login_btn.click()
time.sleep(10)
sellerurl = 'https://myseller.taobao.com/home.htm'
bro.get(sellerurl)
