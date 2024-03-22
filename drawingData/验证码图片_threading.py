from threading import Thread
import threading
from selenium import webdriver
from time import ctime, sleep
import sys
import re
import pandas as pd

lock = threading.Lock()
def test_baidu(a,acc,pas):

    """测试用例"""
    print('start:%s' % ctime())

    print(f"============当前运行线程名称：{threading.current_thread().getName()}。登陆账号：{acc}")
    driver = webdriver.Chrome()
    driver.get('http://172.30.6.71:81/zentao/user-login.html')

    lock.acquire()
    driver.find_elements_by_class_name('form-control')[0].send_keys(acc)
    driver.find_elements_by_class_name('form-control')[-1].send_keys(pas)
    driver.find_element_by_id('submit').click()
    lock.release()

    sleep(2)

    driver.find_element_by_id('subNavbar').find_element_by_link_text('任务').click()

    task_tr_list = driver.find_element_by_id('tasktable').find_elements_by_tag_name('tr')
    line = []
    header = []
    for c,tr in enumerate(task_tr_list):
        if c == 0:
            col = re.split(' ',tr.text)[:-1]
            header.append(col)
        else:
            cell = re.split(' ',tr.text.replace('\n',' '))
            line.append(cell)

    task_data = pd.DataFrame(line,columns=header)
    print(task_data)
    task_data.to_csv(f'task_{acc}.csv',index=False)



    driver.quit()



if __name__ == '__main__':
    # lists = ['threading','threading1']

    # threads = []
    # files = range(len(lists))
    # print(files)

    # # 创建线程
    # for i in range(len(lists)):
    #     t = Thread(target=test_baidu, args=(1,key,value))
    #     threads.append(t)
    #
    # # 启动线程
    # for t in files:
    #     threads[t].start()
    #
    # for c,t in enumerate(files):
    #         threads[t].join()



    acc_dict = {
        'zhangke':'zqykj123',
        'zhangli':'zqykj123',
    }

    threads_list = []
    for key,value in acc_dict.items():
        t = Thread(target=test_baidu, args=(1, key, value))
        threads_list.append(t)

    for thread in threads_list:
        thread.start()

    for thread in threads_list:
        thread.join()

    print('end:%s' % ctime())