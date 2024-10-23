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
        if not element.states.is_displayed or (
                element.style('height') == '0px' and element.style("overflow-y") == "hidden"):
            return False
        # 递归再找父级
    return findElementDisplay(element.parent())





def findParentEle(element, key, level=1):
    keyList = element.eles(f'text={key}')
    print(keyList)
    if len(keyList) > 0:
        # 单选找到一个
        if len(keyList) == 1:
            return keyList[0]
        # 找到多个
        else:
            # 查看父级是否有隐藏属性
            for ele in keyList:
                if findElementDisplay(ele):
                    return ele
    else:
        return findParentEle(element.parent(), key, level + 1)






co = ChromiumOptions()
# 1、设置无头模式：co.headless(True)
# 2、设置无痕模式：co.incognito(True)
# 3、设置访客模式：co.set_argument('--guest')
# 4、设置请求头user-agent：co.set_user_agent()
# 5、设置指定端口号：co.set_local_port(7890)
# 6、设置代理：co.set_proxy('http://localhost:1080')
co.set_browser_path('/opt/apps/cn.google.chrome/files/google/chrome/chrome')
page = ChromiumPage(co)

# # 1、elementui 2
# page.get('https://element.eleme.cn/#/zh-CN/component/radio', retry=3, timeout=15, interval=2)
# radioEle = page.ele(
#     'x:/html/body/div[1]/div[2]/div/div[1]/div/div/div[2]/section/div[5]/div[1]/div/div[2]/label[1]/span[2]')
# key = '备选项2'

# 2、elementui 3
page.get('https://element-plus.org/zh-CN/component/radio.html', retry=3, timeout=15, interval=2)
radioEle = page.ele('x:/html/body/div[2]/div/main/div/div/div[1]/div/div[5]/div[1]/div[2]/div/label[2]/span[2]')
key = 'Option 2'


# # 3、ant-design 5
# page.get('https://ant-design.antgroup.com/components/select-cn', retry=3, timeout=30, interval=2)
# time.sleep(5)
# radioEle = page.ele('x:/html/body/div[1]/div/main/div[2]/article/div[4]/div[4]/div/section[1]/section[5]/section[1]/div/div/span[2]')
# key = 'Lucy'
# # radioEle = page.ele('x:/html/body/div[1]/div/main/div[2]/article/div[4]/div[4]/div/section[2]/section[3]/section[1]/div/div/div')
# # key = 'USA (美国)'


# # 4、ant-design 4
# page.get('https://4x-ant-design.antgroup.com/components/select-cn/', retry=3, timeout=30, interval=2)
# time.sleep(5)
# radioEle = page.ele('x:/html/body/div[1]/div/div/div[2]/section[1]/article/div[2]/div[2]/section[1]/section[1]/div/div/span[1]/input')
# key = 'Lucy'


# # 5、ant-design 3
# page.get('https://3x.ant.design/components/select-cn/', retry=3, timeout=30, interval=2)
# time.sleep(5)
# radioEle = page.ele('x:/html/body/div[1]/div/div/div/div[2]/section[1]/article/div[2]/div[1]/section[4]/section[1]/div/div/div')
# key = 'Jack'


# # 6、ant-design 2
# page.get('https://2x.ant.design/components/select-cn/', retry=3, timeout=30, interval=2)
# time.sleep(5)
# radioEle = page.ele('x:/html/body/div[1]/div/div/div[1]/div[2]/article/div[2]/div[1]/section[4]/section[1]/div/div/div')
# key = 'Lucy'


# # 7、bootstrap 3
# page.get('https://v3.bootcss.com/components/#dropdowns', retry=3, timeout=30, interval=2)
# time.sleep(5)
# radioEle = page.ele('x:/html/body/div[2]/div/div[1]/div[2]/div[3]/div/button')
# key = 'Action'


# # 8、bootstrap 4
# page.get('https://v4.bootcss.com/docs/components/dropdowns/', retry=3, timeout=30, interval=2)
# # radioEle = page.ele('x:/html/body/div[2]/div/main/div[2]/div/button')
# radioEle = page.ele('x:/html/body/div[2]/div/main/div[66]/div/div[1]/button')
# key = 'Action'


# # 9、bootstrap 5
# page.get('https://v5.bootcss.com/docs/forms/select/', retry=3, timeout=30, interval=2)
# radioEle = page.ele('x:/html/body/div[2]/main/div[3]/div[1]/div[1]/select')
# key = 'Two'


# # 10、layui 2
# page.get('http://layui.xhcen.com/doc/form.html', retry=3, timeout=30, interval=2)
# radioEle = page.ele('x:/html/body/div[3]/div[2]/div[2]/form/div[3]/div/div/div/input')
# key = '广州'


# 11、jquery
# page.get('https://jqueryui.com/selectmenu/', retry=3, timeout=30, interval=2)
# radioEle = page.ele('x:/html/body/div[1]/form/fieldset/span[2]/span[2]')
# key = 'ui.jQuery.js'










radioOptionEle = findParentEle(radioEle, key)
radioOptionEle.click()







