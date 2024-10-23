import sys
import time

from DrissionPage import ChromiumPage, ChromiumOptions
# from bs4 import BeautifulSoup
import lxml.html
# import xpath
from lxml import etree






# 遍历父级，寻找有display属性的父节点
def findElementDisplay(element):
    # 父级元素
    if element.tag == 'body':
        return True
    else:
        # 父节点有不可见属性，直接返回过滤，
        if not element.states.is_displayed or (element.style('height') == '0px' and element.style("overflow-y") == "hidden"):
            return False
        # 递归再找父级
    return findElementDisplay(element.parent())












co = ChromiumOptions()
# 1、设置无头模式：co.headless(True)
# 2、设置无痕模式：co.incognito(True)
# 3、设置访客模式：co.set_argument('--guest')
# 4、设置请求头user-agent：co.set_user_agent()
# 5、设置指定端口号：co.set_local_port(7890)
# 6、设置代理：co.set_proxy('http://localhost:1080')
co.set_browser_path('/opt/apps/cn.google.chrome/files/google/chrome/chrome')
page = ChromiumPage(co, timeout=5)




# # 1、elementui 2
# page.get('https://element.eleme.cn/#/zh-CN/component/select', retry=3, timeout=15, interval=2)
# selectEle = page.ele('x:/html/body/div[1]/div[2]/div/div[1]/div/div/div[2]/section/div[2]/div[1]/div/div/div/input')
# key = '黄金糕'


# # 2、elementui 3
# page.get('https://element-plus.org/zh-CN/component/select.html', retry=3, timeout=15, interval=2)
# selectEle = page.ele('x:/html/body/div[2]/div/main/div/div/div[1]/div/div[3]/div[1]/div/div[1]/div/div[1]/div[2]')
# key = 'Option1'


# # 3、ant-design 5
# page.get('https://ant-design.antgroup.com/components/select-cn', retry=3, timeout=30, interval=2)
# time.sleep(5)
# selectEle = page.ele('x:/html/body/div[1]/div/main/div[2]/article/div[4]/div[4]/div/section[1]/section[5]/section[1]/div/div/span[2]')
# key = 'Lucy'
# # selectEle = page.ele('x:/html/body/div[1]/div/main/div[2]/article/div[4]/div[4]/div/section[2]/section[3]/section[1]/div/div/div')
# # key = 'USA (美国)'


# # 4、ant-design 4
# page.get('https://4x-ant-design.antgroup.com/components/select-cn/', retry=3, timeout=30, interval=2)
# time.sleep(5)
# selectEle = page.ele('x:/html/body/div[1]/div/div/div[2]/section[1]/article/div[2]/div[2]/section[1]/section[1]/div/div/span[1]/input')
# key = 'Lucy'


# # 5、ant-design 3
# page.get('https://3x.ant.design/components/select-cn/', retry=3, timeout=30, interval=2)
# time.sleep(5)
# selectEle = page.ele('x:/html/body/div[1]/div/div/div/div[2]/section[1]/article/div[2]/div[1]/section[4]/section[1]/div/div/div')
# key = 'Jack'


# 6、ant-design 2
page.get('https://2x.ant.design/components/select-cn/', retry=3, timeout=30, interval=2)
time.sleep(5)
selectEle = page.ele('x:/html/body/div[1]/div/div/div[1]/div[2]/article/div[2]/div[1]/section[4]/section[1]/div/div/div')
key = 'Lucy'


# # 7、bootstrap 3
# page.get('https://v3.bootcss.com/components/#dropdowns', retry=3, timeout=30, interval=2)
# time.sleep(5)
# selectEle = page.ele('x:/html/body/div[2]/div/div[1]/div[2]/div[3]/div/button')
# key = 'Action'


# # 8、bootstrap 4
# page.get('https://v4.bootcss.com/docs/components/dropdowns/', retry=3, timeout=30, interval=2)
# # selectEle = page.ele('x:/html/body/div[2]/div/main/div[2]/div/button')
# selectEle = page.ele('x:/html/body/div[2]/div/main/div[66]/div/div[1]/button')
# key = 'Action'


# # 9、bootstrap 5
# page.get('https://v5.bootcss.com/docs/forms/select/', retry=3, timeout=30, interval=2)
# selectEle = page.ele('x:/html/body/div[2]/main/div[3]/div[1]/div[1]/select')
# key = 'Two'


# # 10、layui 2
# page.get('http://layui.xhcen.com/doc/form.html', retry=3, timeout=30, interval=2)
# selectEle = page.ele('x:/html/body/div[3]/div[2]/div[2]/form/div[3]/div/div/div/input')
# key = '广州'


# 11、jquery
# page.get('https://jqueryui.com/selectmenu/', retry=3, timeout=30, interval=2)
# selectEle = page.ele('x:/html/body/div[1]/form/fieldset/span[2]/span[2]')
# key = 'ui.jQuery.js'






# 如果是html原生select标签
if selectEle.tag == 'select':
    selectEle.select.by_text(key)
else:
    # 点击前后找到的元素
    beforeEle = [ele for ele in page.eles(f'text={key}')]
    beforeEleXpath = [ele.xpath for ele in beforeEle]
    beforeStatus = [findElementDisplay(ele) for ele in beforeEle]

    # 点击
    page.actions.scroll(on_ele=selectEle).click()
    time.sleep(3)

    # 点击后找到的元素
    afterEle = [ele for ele in page.eles(f'text={key}')]
    afterEleXpath = [ele.xpath for ele in afterEle]
    # afterStatus = [ele.states.is_displayed for ele in afterEle]



    # 1、判断点击前后的目标选项数量
    if len(afterEleXpath) > len(beforeEleXpath):
        print(1)
        findOptionXpath = list(set(afterEleXpath) - set(beforeEleXpath))
        # 点击后只多一个
        selectOption = page.ele(f'x:{findOptionXpath[0]}')
        if len(findOptionXpath) > 1:
            print(11)
            for xpath in list(set(afterEleXpath) - set(beforeEleXpath)):
                selectOption = page.ele(f'x:{xpath}')
                parentEle = findElementDisplay(selectOption)
                if parentEle:
                    break
        page.actions.move_to(selectOption).click()
        time.sleep(1)
        print(selectOption.states.is_displayed)
    # 2、数量相等，点击前后是否可见属性不同   bootstrap 3
    elif len(afterEleXpath) == len(beforeEleXpath):
        print(2)
        for index, ele in enumerate(afterEle):
            if beforeStatus[index] != findElementDisplay(ele):
                print(ele.xpath)
                page.actions.move_to(ele).click()
