# -*- coding:utf-8 -*-#
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions
import time
import pymssql
from PIL import  Image
import matplotlib.pyplot as plt
import _thread

class TaoBao:
    def __init__(self):
        self.login_url = 'https://login.taobao.com/member/login.jhtml'
        self.order_url = 'https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm?action=itemlist/BoughtQueryAction&event_submit_do_query=1&tabCode=waitConfirm'

        # 无头浏览器
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')  # 为Chrome配置无头模式
        chrome_options.add_argument('--disable-dev-shm-u|sage')

        # 规避被检测
        # options = ChromeOptions()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.browser = webdriver.Chrome(options=chrome_options)

    def login(self):
        self.browser.get(url=self.login_url)
        element = WebDriverWait(self.browser,60).until(EC.presence_of_element_located((By.ID, 'login')))

        self.browser.find_element_by_xpath('/html/body/div/div[2]/div[3]/div/div/div/div[1]/i').click()
        element = WebDriverWait(self.browser, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'qrcode-img')))
        time.sleep(0.5)
        _thread.start_new_thread(self.showImage(), (1,))
        element = WebDriverWait(self.browser, 6).until(EC.presence_of_element_located((By.CLASS_NAME, 'site-nav site-nav-status-login')))
        plt.close()


    def getdata(self):
        print('获取淘宝订单数据...')
        self.browser.get(self.order_url)
        element = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, 'list-bought-items')))
        items1 = self.browser.find_elements_by_class_name('index-mod__order-container___1ur4-.js-order-container')
        infos = []
        htmls = []
        for item in items1:
            info = []
            s = item.find_element_by_tag_name('div')
            str = s.get_attribute('data-id')
            print("获取%s订单信息..." %str)
            info.append(str)

            s = item.find_element_by_link_text('查看物流')
            htmls.append(s.get_attribute('href'))
            info.append(s.get_attribute('href'))

            s = item.find_elements_by_tag_name('a')
            info.append(s[3].get_attribute('href'))

            infos.append(info)
            print("获取%s订单信息完成" % str)

        for info in infos:
                info[1] = self.getTaadeInfo(info[1])
        print('获取淘宝订单数据完成')

        print('信息写入数据库...')
        db.delete('delete from dbo.淘宝订单表', conn)
        db.add(infos, conn)
        print('信息写入数据库完成')

        for info in infos:
            print("订单号:%s  物流号:%s  链接:%s" %(info[0],info[1],info[2]))


    def getTaadeInfo(self, url):
        time.sleep(0.5)
        self.browser.get(url)
        element = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, 'tb-beacon-aplus')))
        s = self.browser.find_element_by_class_name('order-row')
        s = s.find_elements_by_class_name('em')[0].text
        return s

    def showImage(self):
        img = self.browser.find_element_by_xpath('//*[@id="login"]/div[2]/div/div[1]/div[1]/undefined/canvas')
        img.screenshot('qrcode.png')
        img = Image.open('qrcode.png')
        plt.imshow(img)
        plt.axis('off')
        plt.show()


    def isElementPresent(self, by, value):
        # 从selenium.common.exceptions 模块导入 NoSuchElementException类
        from selenium.common.exceptions import NoSuchElementException
        try:
            element = self.browser.find_element(by=by, value=value)
        except NoSuchElementException as e:
            # 打印异常信息
            print(e)
            # 发生了NoSuchElementException异常，说明页面中未找到该元素，返回False
            return False
        else:
            # 没有发生异常，表示在页面中找到了该元素，返回True
            return True

class DataBase:
    def connectToSqlServer():
        conn = pymssql.connect('127.0.0.1', 'sa', 'XMMSW20150625', '11')
        return conn


    def queryTable(sql,conn):
        cu = conn.cursor()
        cu.execute(sql)
        res = cu.fetchall()
        return res

    def add(infos, conn):
        cu = conn.cursor()
        for info in infos:
            sql = "insert into dbo.淘宝订单表 (订单号,物流号,链接) values ('%s','%s','%s')" %(info[0], info[1], info[2])
            cu.execute(sql)
            conn.commit()
        cu.close()

    def delete(sql,conn):
        cu = conn.cursor()
        cu.execute(sql)
        conn.commit()
        cu.close()


db = DataBase
if __name__ == "__main__":
    tb = TaoBao()
    tb.login()
    conn = db.connectToSqlServer()
    while True:
        temp = input("请输入代码(1:执行  q:退出):")
        if temp != 'q':
            if temp !="":
                res = tb.isElementPresent('id', 'login')
                print(res)
                if res is False:
                    if temp == '1':
                        tb.getdata()
                else:
                    tb.login()
        else:
            break
    tb.browser.quit()
    conn.close()






