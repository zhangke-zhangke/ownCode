import retrying
from selenium.webdriver import Chrome
import datetime


def form1(driver):
    @retrying.retry(stop_max_attempt_number=4,wait_fixed=3000)
    def test(driver):

        driver.find_element_by_class_name('ant-input')

        print('重试')
    test(driver)

    print('爬取流水')





if __name__ == '__main__':

    driver = Chrome()
    driver.get('http://172.30.6.4/njfxq/login')

    print(datetime.datetime.now())
    form1(driver)
    datetime.datetime.now()








