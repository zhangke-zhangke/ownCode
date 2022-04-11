import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver



if __name__ == '__main__':

    r = requests.get('https://v.qq.com/')

    # print(r.status_code)
    # print(r.encoding)
    print(r.content)
    # print(r.headers)
    # print(r.cookies)

    pattern = re.compile(r'https://[^\s]+.html')
    url = re.findall(pattern,r.content)
    print(url)

