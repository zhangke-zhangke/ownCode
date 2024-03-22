import flask
from flask import request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import numpy as np
import re
from PIL import Image
from paddleocr import PaddleOCR
import os

'''
    账号密码登录
'''
def login_system(driver,account,password):
    # 输入用户名和密码
    driver.find_element_by_id('ouserId').send_keys(account)
    driver.find_element_by_id('userPwd').send_keys(password)
    # 点击登录
    while True:
        try:
            if driver.find_element_by_tag_name('img').is_enabled() == True:
                # 点击登录
                driver.find_element_by_tag_name('img').click()
                time.sleep(3)
                break
        except:
            continue

    return driver


'''
    账密校验服务
'''
server = flask.Flask(__name__)
@server.route('/passwordCheck', methods=['get', 'post'])
def psbc_check_password():
    # web启动
    chrome_opt = Options()
    chrome_opt.add_argument('--headless')
    chrome_opt.add_argument('--disable-gpu')
    chrome_opt.add_argument('--no-sandbox')
    driver = webdriver.Chrome(chrome_options=chrome_opt)
    driver.get('http://22.246.53.134:8080/')

    # 账号信息字典
    acc_info = eval(request.values.get('accInfo'))
    return_acc_login_info = {}
    if len(acc_info) >= 1:
        # 批次多帐号验证
        for account, password in acc_info.items():
            print(account, password)
            # 系统登录
            driver = login_system(driver, account, password)
            # 判断输入的密码是否正确
            # if driver.find_element_by_id('userPwdTap').text == '密码不正确!(密码格式为大小写字母、数字、特殊字符组成)!':
            if driver.find_element_by_id('userPwdTap').text != '':
                print(f'当前账号：{account}密码错误，请更新密码到/usr/local/zqykj/Network_Robots_Project_linux/account_set.py中!\n')
                return_acc_login_info[account] = 0
            else:
                print(f'当前账号：{account}密码正确!\n')
                return_acc_login_info[account] = 1
    elif len(acc_info) == 0:
        # 无账号
        print('无账号密码')

    print(return_acc_login_info)
    driver.quit()
    return flask.jsonify(return_acc_login_info)


'''
    OCR识别验证码服务
'''


@server.route('/ocrServer', methods=['get', 'post'])
def run():
    file = request.files['file']
    file.save('api_save.png')

    binary = np.array(Image.open(r'api_save.png').convert('L'), 'f')

    # ocr 识别验证码
    ocr = PaddleOCR(use_angle_cls=True, lang='ch')
    img_info = ocr.ocr(binary, cls=False)

    # 最终结果
    img_result = ""
    for line in img_info:
        # 得到图片中文字  循环加总，（多行文字的情况）
        img_result += line[-1][0]
        img_result += ' '
    # 去除特殊字符
    code_value = re.findall(r'[^\*"/:?\\|<>″′‖ 〈\n]', img_result, re.S)
    code_value = "".join(code_value)

    print('识别验证码信息：', code_value)
    # 及时删除
    os.remove('api_save.png')

    return code_value


if __name__ == '__main__':
    # 账密校验   https://localhost:8888/passwordCheck?accInfo={'1','2'}
    # ocr识别   https://localhost:8888/ocrServer? & photoFile
    server.run(debug=True, port='8888', host='0.0.0.0')
