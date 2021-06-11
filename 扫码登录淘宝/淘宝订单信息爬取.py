# -*- coding:utf-8 -*-#
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pymssql
import pymssql._mssql
import uuid
import decimal
from PIL import Image
from prettytable import PrettyTable
import configparser
import psutil


class TaoBao:
    def __init__(self):
        self.login_url = cf.get('Url', 'login_url')
        self.order_url = cf.get('Url', 'order_url')
        self.userName = cf.get('Login', 'userName')
        self.userPws = cf.get('Login', 'userPws')
        self.userqr = cf.get('Login', 'use_qr')

        # 无头浏览器
        chrome_options = Options()
        item = cf.get('Chrome_option', 'headless')
        if item == '1':  # 配置文件开启无头模式
            chrome_options.add_argument('--headless')  # 为Chrome配置无头模式
            chrome_options.add_argument('--disable-gpu')

        # 规避被检测
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')

        chrome_options.add_argument('log-level=3')

        self.browser = webdriver.Chrome(options=chrome_options)

    def login(self):
        self.browser.get(url=self.login_url)
        element = WebDriverWait(self.browser, 60).until(EC.presence_of_element_located((By.ID, 'login')))
        if self.userqr=='1':
            self.browser.find_element_by_xpath('/html/body/div/div[2]/div[3]/div/div/div/div[1]/i').click()
            element = WebDriverWait(self.browser, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'qrcode-img')))
            time.sleep(0.5)
            item = cf.get('Chrome_option', 'headless')
            if item == '1':  # 配置文件开启无头模式
                self.showImage()
                time.sleep(0.5)
        elif self.userqr == '0':
            self.browser.find_element_by_xpath('//*[@id="fm-login-id"]').send_keys(self.userName)
            self.browser.find_element_by_xpath('//*[@id="fm-login-password"]').send_keys(self.userPws)
            try:
                iframe = self.browser.find_element_by_xpath('//div[@class="bokmXvaDlH"]//iframe')
                self.browser.switch_to.frame(iframe)
                # 获取滑块的大小
                span_background = self.browser.find_element_by_xpath('//*[@id="nc_1__scale_text"]/span')
                span_background_size = span_background.size
                print(span_background_size)

                # 获取滑块的位置
                button = self.browser.find_element_by_xpath('//*[@id="nc_1_n1z"]')
                button_location = button.location
                print(button_location)

                # 拖动操作：drag_and_drop_by_offset
                # 将滑块的位置由初始位置，右移一个滑动条长度（即为x坐标在滑块位置基础上，加上滑动条的长度，y坐标保持滑块的坐标位置）
                x_location = span_background_size["width"]
                y_location = button_location["y"]
                print(x_location, y_location)
                action = ActionChains(self.browser)
                source = self.browser.find_element_by_xpath('//*[@id="nc_1_n1z"]')
                action.click_and_hold(source).perform()
                action.move_by_offset(300, 0)
                action.release().perform()
            except:
                None
            time.sleep(1)
            self.browser.find_element_by_xpath('//*[@id="login-form"]/div[4]/button').click()

        element = WebDriverWait(self.browser, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'site-nav.site-nav-status-login')))
        print('登录成功')

    def getdata(self):
        print('获取淘宝订单数据...\n')
        self.browser.get(self.order_url)
        infos = []
        pgnum=1
        order_lis=[]
        try:
            while True:
                element = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, 'list-bought-items')))
                items1 = self.browser.find_elements_by_class_name('index-mod__order-container___1ur4-.js-order-container')
                itemCount = len(items1)
                if itemCount > 0:
                    print('*' * 80)
                    for item in items1:
                        info = []
                        s = item.find_element_by_tag_name('div')
                        str = s.get_attribute('data-id')

                        if str not in order_lis:
                            print("获取%s订单信息..." % str)
                            info.append(str)
                            order_lis.append(str)

                            try:
                                s = item.find_element_by_link_text('查看物流')
                                info.append(s.get_attribute('href'))
                            except:
                                info.append('无')

                            try:
                                s = item.find_element_by_link_text('[交易快照]')
                                info.append(s.get_attribute('href'))
                            except:
                                try:
                                    s = item.find_element_by_xpath('./div//a[1]')
                                    info.append(s.get_attribute('href'))
                                except:
                                    info.append('无')

                            infos.append(info)
                            print("获取%s订单信息完成" % str)

                    print('[当前第%d页]' % pgnum)
                    print('*'*80)
                    element = self.browser.find_element_by_xpath('//*[@id="tp-bought-root"]/div[3]/div[2]/div/button[2]')
                    if element.get_attribute('disabled') == 'true':
                        break
                    time.sleep(0.5)
                    element.click()
                    time.sleep(1)
                    res = input('<请查看网页是否有滑块验证，验证正确后按回车键继续下一页订单查询，按q结束订单查询>')
                    if res == 'q':
                        break
                    time.sleep(1)

                    pgnum += 1

                else:
                    print('无相关订单信息\n')
                    break
        except:
            print('获取订单出错')

        for info in infos:
            if info[1] != "无":
                info[1] = self.getTaadeInfo(info[1])
        print('\n获取淘宝订单数据完成\n')
        

        title = ["订单号", "物流号", "链接"]
        t = PrettyTable(title)
        for info in infos:
            t.add_row(info)
        print(t)
        print(' ')

        if useDatabaseFlag == '1':
            print('信息写入数据库...\n')
            db.delete('delete from dbo.淘宝订单表', conn)
            db.add(infos, conn)
            print('信息写入数据库完成\n')
                

    def getTaadeInfo(self, url):
        try:
            self.browser.get(url)
            element = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, 'tb-beacon-aplus')))
            s = self.browser.find_element_by_class_name('order-row')
            s = s.find_elements_by_class_name('em')[0].text
            return s
        except:
            return '无'

    def showImage(self):
        img = self.browser.find_element_by_xpath('//*[@id="login"]/div[2]/div/div[1]/div[1]/undefined/canvas')
        img.screenshot('qrcode.png')
        img = Image.open('qrcode.png')
        img.show()



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
        try:
            host = cf.get('Database', 'host')
            user = cf.get('Database', 'user')
            password = cf.get('Database', 'password')
            db = cf.get('Database', 'db')
            conn = pymssql.connect(host, user, password, db)
            return True, conn
        except:
            print('连接数据库出错,请检查配置文件！')
            return False, None

    def queryTable(sql, conn):
        try:
            cu = conn.cursor()
            cu.execute(sql)
            res = cu.fetchall()
            return res
        except:
            print('查询数据库出错！')

    def add(infos, conn):
        try:
            cu = conn.cursor()
            for info in infos:
                sql = "insert into dbo.淘宝订单表 (订单号,物流号,链接) values ('%s','%s','%s')" % (info[0], info[1], info[2])
                cu.execute(sql)
                conn.commit()
            cu.close()
        except:
            print('添加数据至数据库出错！')

    def delete(sql, conn):
        try:
            cu = conn.cursor()
            cu.execute(sql)
            conn.commit()
            cu.close()
        except:
            print('删除连接数据库数据出错！')


class Tools:
    # 杀进程
    def killPrc(self, prcname):
        for proc in psutil.process_iter():
            if proc.name() == prcname:
                proc.kill()


db = DataBase
conSta = True
exit_flag = False
if __name__ == "__main__":
    cf = configparser.ConfigParser()  # 读取配置文件
    cf.read('./config.ini')
    print('登录淘宝！')
    tools = Tools()
    tools.killPrc('chromedriver.exe')
    tools.killPrc('chrome.exe')
    tb = TaoBao()
    try:
        useDatabaseFlag = cf.get('Database', 'useDatabase')  # 配置文件是否使用数据库
        if useDatabaseFlag == '1':
            conSta, conn = db.connectToSqlServer()

        if conSta:
            tb.login()  # 扫码登录淘宝
            while True:
                temp = input("请输入代码< 1:执行  q:退出 >:")
                if temp != 'q':
                    if temp != "":
                        if temp == '1':
                            tb.getdata()
                else:
                    break
            exit_flag = True
            print('正在退出，请稍等...')
            tb.browser.quit()
            if useDatabaseFlag == '1':
                conn.close()
    finally:
        if not exit_flag:
            print('正在退出，请稍等...')
            tb.browser.quit()
            if useDatabaseFlag == '1' and conSta:
                conn.close()
            tools.killPrc('chromedriver.exe')
            tools.killPrc('chrome.exe')
