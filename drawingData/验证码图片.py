from selenium import webdriver
import cv2
from paddleocr import PaddleOCR
import re
from PIL import Image
import requests
import sys
import scipy
import threading
from selenium.webdriver.chrome.options import Options
import time





if __name__ == '__main__':
    t = time.time()
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.page_load_strategy = 'eager'
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(3)
    # driver.get('https://www.qb50.com/login.php')
    # driver.find_element_by_id('username').send_keys('22222')
    # driver.find_element_by_id('password').send_keys('22222')
    # driver.find_element_by_class_name('iForm').find_element_by_class_name('btn').click()
    # print(driver.page_source)
    #
    # req = requests.get('https://www.qb50.com/login.php?do=submit')
    # print(req.text)



    driver.get('http://172.30.6.4/njfxq/login')
    driver.find_element_by_class_name('usernameInput').find_element_by_tag_name('input').send_keys('admin')
    driver.find_element_by_class_name('passwordInput').find_element_by_tag_name('input').send_keys('admin')
    driver.find_element_by_class_name('login-form-button').click()

    from selenium.webdriver import ActionChains
    from selenium.webdriver.common.keys import Keys

    # ActionChains(driver).key_down(Keys.CONTROL).send_keys('t').key_up(Keys.CONTROL).perform()
    # driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
    driver.execute_script('window.open("https://cn.bing.com/");')

    time.sleep(3)

    # data = {"force": "true", "username": "22222", "password": "22222"}
    # req = requests.post('http://172.30.6.4/finance/userService/api/v1/login')
    # print(req.text)

    driver.quit()
    print(time.time()-t)

    import pandas as pd

    pd.read_csv()

    # # 屏幕截图
    # driver.save_screenshot('code.png')
    #
    # # 找到验证码
    # photo = driver.find_element_by_tag_name('img')
    # x = photo.location['x']
    # y = photo.location['y']
    # width = photo.size['width']
    # height = photo.size['height']
    #
    # # 打开图片截取验证码 并保存
    # im = Image.open('code.png')
    # im = im.crop((x, y, x + width, y + height))
    # im.save('hehe.png')
    #
    #
    # raw = cv2.imread(r'hehe.png',0)
    # # 二值化图片
    # binary = cv2.adaptiveThreshold(~raw, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 35, -5)
    # # cv2.imshow('binary_picture', binary)
    # # if cv2.waitKey(0):
    # #     cv2.destroyWindow('binary_picture')
    #
    # ocr = PaddleOCR(use_angle_cls=True ,use_gpu=False)
    # img_info = ocr.ocr(binary, cls=False)
    # print(img_info)
    #
    # # 最终结果
    # img_result = ""
    # for line in img_info:
    #     # 得到图片中文字  循环加总，（多行文字的情况）
    #     img_result += line[-1][0]
    #     img_result += ' '
    #
    # print(img_result)
    #
    # # 去除特殊字符
    # text1 = re.findall(r'[^\*"/:?\\|<>″′‖ 〈\n]', img_result, re.S)
    # text1 = "".join(text1)
    # print('单元格图片信息：' + text1)
    #
    #
    # import time
    #
    # if driver.find_element_by_id('main').find_element_by_class_name('iForm').find_element_by_tag_name('img').is_enabled() == True:
    #     time.sleep(4)
    #     driver.find_element_by_id('main').find_element_by_class_name('iForm').find_element_by_tag_name('img').click()
    #
    #
    #
    # # while True:
    # #     try:
    # #         if driver.find_element_by_link_text(' 自动登录').is_displayed() == True:
    # #             print('1')
    # #             break
    # #     except:
    # #         continue
    #
    #
    #
    #
    #
    #
    #
