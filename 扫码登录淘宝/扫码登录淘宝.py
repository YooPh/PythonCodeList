from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import matplotlib.pyplot as plt # plt 用于显示图片
import _thread

class TaoBao:
    def __init__(self):
        self.url = 'https://login.taobao.com/member/login.jhtml'
        # 初始化浏览器选项
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        # 禁止加载图片
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        # 设置为开发者模式
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 加载浏览器选项
        self.browser = webdriver.Chrome(options=options)
        # 设置显式等待时间40s
        # self.wait = WebDriverWait(self.browser, 40)

    def login(self):
        self.browser.get(url=self.url)
        element = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, 'login')))
        self.browser.find_element_by_xpath('/html/body/div/div[2]/div[3]/div/div/div/div[1]/i').click()
        time.sleep(1)
        _thread.start_new_thread(self.showimage, ())
        element = WebDriverWait(self.browser, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "site-nav-login-info-nick")))
        time.sleep(1)
        plt.close()

    def getdata(self):
        self.browser.get('https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm?spm=a1z02.1.a2109.d1000368.jusr2o&nekot=1470211439694')
        element = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, 'list-bought-items')))
        time.sleep(1)
        # text = self.browser.page_source()
        items = self.browser.find_elements_by_class_name('index-mod__order-container___1ur4- js-order-container')
        print(len(items))
        print(items)
        # print(text)

    def showimage(self):
        self.browser.save_screenshot('login.png')
        im = plt.imread('login.png')
        plt.axis('off')
        plt.imshow(im)
        plt.show()


if __name__ == "__main__":
    tb=TaoBao()
    tb.login()
    tb.getdata()
