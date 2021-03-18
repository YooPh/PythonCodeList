import requests
from lxml import etree
import os

url = 'https://www.iqiyi.com/dianying_new/i_list_paihangbang.html' # 爱奇艺电影排行

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}

responses = requests.get(url = url , headers = headers)
tree = etree.HTML(responses.text)
moviesdics=[]


moviesurls = tree.xpath('/html/body/div[3]/div/div[2]/div/div[1]/ul/li')
print(len(moviesurls))
for moviesurl in moviesurls:
    # print(moviesurl.xpath('./div[1]/a/@title')[0],moviesurl.xpath('./div[1]/a/@href')[0])
    moviesdic = {}
    moviesdic['name'] = moviesurl.xpath('./div[1]/a/@title')[0]
    moviesdic['url']=moviesurl.xpath('./div[1]/a/@href')[0]
    moviesdics.append(moviesdic)

for movie in moviesdics:
    url = 'https://jx.618g.com/?url='+movie['url']
    responses = requests.get(url=url,headers=headers)
    tree = etree.HTML(responses.text)
    m3u8url = tree.xpath('/html/body/div[1]/iframe/@src')[0]
    a = '/m3u8-dp.php?url='
    if a in m3u8url:
        cmd = 'ffmpeg -i '+ m3u8url.replace(a,'') +' -vcodec copy -acodec copy '+movie['name']+'.mp4'
        os.system(cmd)
