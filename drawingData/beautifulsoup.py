from bs4 import BeautifulSoup
import requests
import sys
from lxml import etree



def requests_url(url,headers):
    p4 = requests.get(url, headers=headers)
    soup = BeautifulSoup(p4.content, 'html.parser')


    print(type(soup.prettify()))  # <class 'str'>
    '''
        相当于把html解析成一个数据对象，可以通过.的方式访问html的标签
    '''
    print(soup.div.ul)
    print(soup.div.ul.find(href="/vod-type-id-3-pg-1.html"))
    print(soup.div.ul.li.a['title'])
    print(type(soup.div))  # <class 'bs4.element.Tag'>
    # 一次查找所有标签带a的
    print(soup.find_all('a'))



if __name__ == '__main__':

    url_list = ['https://4480.tv/vod-play-id-63360-src-3-num-{}.html'.format(i) for i in range(9, 16)]
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62',
        'cookies': 'PHPSESSID=g65ipam1c0kgj8sctkcbfmkq35; __51vcke__JSfg3PPYsm2jAeAF=59365898-12ee-5c79-aee8-c07a733dec1f; __51vuft__JSfg3PPYsm2jAeAF=1649736012578; __51uvsct__JSfg3PPYsm2jAeAF=2; __vtins__JSfg3PPYsm2jAeAF=%7B%22sid%22%3A%20%22475e118d-15a5-55ef-8abd-75e4e54116f2%22%2C%20%22vd%22%3A%2020%2C%20%22stt%22%3A%202315702%2C%20%22dr%22%3A%20678768%2C%20%22expires%22%3A%201649765561094%2C%20%22ct%22%3A%201649763761094%7D'
    }

    for url in url_list:
        requests_url(url, headers)

        sys.exit()

