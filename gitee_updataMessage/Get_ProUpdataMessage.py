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

bro = webdriver.Chrome(chrome_options = chrome_options ,options=options)

login_url = 'https://gitee.com/login'
bro.get(login_url)

user_name = bro.find_element_by_class_name('login-password__account-input')
user_name.send_keys('395897292@qq.com')
user_pwd = bro.find_element_by_id('user_password')
user_pwd.send_keys('wyf395897292')
login_btn = bro.find_element_by_xpath('//*[@id="new_user"]/div[2]/div/div/div[4]/input')
login_btn.click()
time.sleep(1)
graph_url = 'https://gitee.com/mswRD/on_line_machine__bus/graph/master.json'
bro.get(graph_url)
page_text = bro.page_source
data_text = bro.find_element_by_xpath('/html/body/pre')
data_json = json.loads(data_text.text)
data_commits = data_json['commits']
alldatas = []
for data in data_commits:
    text = data['message']
    alldatas.append(text)
    print(text)

# for data in alldatas:
with open('./versionInformation.txt','w',encoding='utf-8') as fp:
    fp.writelines(alldatas)
bro.quit()

input('<回车退出>:')



