from selenium import webdriver
import time







if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.implicitly_wait(3)
    driver.maximize_window()
    driver.get('https://code.nhsa.gov.cn/search.html?sysflag=80')

    time.sleep(3)

    # 第一层ifram
    driver.switch_to.frame('dataInfo')
    li_list = driver.find_element_by_id('treeDemo1').find_element_by_id('treeDemo1_1').find_element_by_id('treeDemo1_1_ul').find_elements_by_tag_name('li')
    print(len(li_list))

    # 第二层
    driver.switch_to.frame('ICDMainframe')
    a = driver.find_elements_by_tag_name('script')
    print(len(a))

    driver.switch_to.parent_frame()
    print(len(driver.find_element_by_id('treeDemo1').find_element_by_id('treeDemo1_1').find_element_by_id('treeDemo1_1_ul').find_elements_by_tag_name('li')))



    # 直接返回到主页面
    driver.switch_to.default_content()











