from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import sys
from lxml import etree
import time
from selenium.webdriver.common.by import By
import os


def parser_url(url):
    driver.get(url)
    driver.implicitly_wait(3)

    # # \
    pwd = os.path.split(os.path.realpath(__file__))[0]
    # # 保存快照
    # driver.save_screenshot(pwd+'\快照.png')

    try:

        # aa = driver.find_element_by_class_name("subHeader").find_element_by_tag_name('h1').get_attribute("id")
        # aa = driver.find_elements_by_id("Player")
        # for i in aa:
        #     url = i.get_attribute("src")
        #     print(url)
            # url_mp4 = requests.get(url)
            # with open(pwd+'/9.mp4',"wb") as fp:
            #     # fp.write(url_mp4.content)
            #     for chunk in url_mp4.iter_content(chunk_size=4096):
            #         if chunk:
            #             fp.write(chunk)

        aa = driver.find_elements_by_tag_name("iframe")  # 查找html标签为iframe的数据
        for i in aa:
            print(i.get_attribute("src"))

             # print(i.get_attribute("src"))


        # aa = driver.find_element(by=By.LINK_TEXT,value='电影').get_property("herf")
        # aa = driver.title

        # for i in aa:
        #     print(i.text)

    except Exception as e:
        print("出错",e)

    finally:
        driver.close()
        sys.exit()


if __name__ == '__main__':
    driver = webdriver.Chrome()

    url_list = ['https://4480.tv/vod-play-id-63360-src-3-num-{}.html'.format(i) for i in range(9,16)]
    print(url_list)

    for url in url_list:
        # headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62',
        #            'cooker':'PHPSESSID=g65ipam1c0kgj8sctkcbfmkq35; __51vcke__JSfg3PPYsm2jAeAF=59365898-12ee-5c79-aee8-c07a733dec1f; __51vuft__JSfg3PPYsm2jAeAF=1649736012578; __51uvsct__JSfg3PPYsm2jAeAF=2; __vtins__JSfg3PPYsm2jAeAF=%7B%22sid%22%3A%20%22475e118d-15a5-55ef-8abd-75e4e54116f2%22%2C%20%22vd%22%3A%2020%2C%20%22stt%22%3A%202315702%2C%20%22dr%22%3A%20678768%2C%20%22expires%22%3A%201649765561094%2C%20%22ct%22%3A%201649763761094%7D'}

        parser_url(url)
















# # selenium demo
#
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
#
# driver = webdriver.Chrome()
# driver.get("http://www.python.org")
# assert "Python" in driver.title
# elem = driver.find_element_by_name("q")
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# driver.close()
#
#
#
