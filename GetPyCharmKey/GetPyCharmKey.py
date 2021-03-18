import requests
from lxml import etree
import pyperclip
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}

data={
    'key':'5263'
}

url1 = 'http://lookdiv.com/index/index/indexcode.html'
url2= 'http://lookdiv.com/index/index/indexcodeindex.html'
se = requests.session()
responses = se.post(url=url1,headers=headers,data=data)
responses = se.get(url2,headers=headers)
if responses.status_code==200:
    tree = etree.HTML(responses.text)
    txt = tree.xpath('//*[@id="subsModal"]/div/div/div/textarea/text()')
    if len(txt)!=0:
        pyperclip.copy(txt[0])
        print('复制成功')
        time.sleep(1)
