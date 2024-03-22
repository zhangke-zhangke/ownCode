from selenium import webdriver
from selenium.webdriver.common.by import By
from pyquery import PyQuery as pq
import time
from selenium.webdriver.support.select import Select







if __name__ == '__main__':

    url = 'http://172.30.6.71:81/zentao/user-login.html'

    # # 无头浏览器
    # opt = webdriver.ChromeOptions()
    # opt.set_headless()
    # driver = webdriver.Chrome(options=opt)


    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(3)

    # 输入账号密码
    driver.find_element_by_name('account').send_keys('zhangke')
    driver.find_element_by_name('password').send_keys('zqykj123')

    # 点击登陆
    driver.find_element_by_id('submit').click()

    # 找到迭代任务爬取
    # time.sleep(2)
    driver.find_element_by_link_text('迭代').click()
    driver.find_element_by_link_text('任务').click()


    # # 下拉选择邮储项目
    # select = Select(driver.find_element_by_id('currentItem'))
    # select.deselect_by_visible_text('江苏邮储-Iterate01-0829-0903 ')

    # 任务列表4
    driver.find_element_by_id('currentItem').click()
    driver.find_element_by_link_text('江苏邮储-Iterate01-0829-0903').click()


    # 循环进入所以任务详情页
    all_task = driver.find_elements_by_class_name('c-name.text-left')
    print(len(all_task))

    for c,task in enumerate(all_task):
        task.click()

        find_tr_list = driver.find_element_by_id('legendBasic').find_element_by_class_name('table.table-data').find_elements_by_tag_name('tr')
        data_dict = {}
        for tr in find_tr_list:
            # key = tr.find_element_by_tag_name('th').text()
            value = tr.text.split(' ')
            # data_dict[key] = value

            # print(key)
            print(value)

        print("==============================================")

        # print(data_dict)

        # 返回上一个页面
        driver.back()


