import requests
from urllib3 import encode_multipart_formdata



header = {
    # 'Accept': 'application/json, text/plain, */*',
    'Authorization':'1677034306556',

    'Connection': 'keep-alive',
    'Content-Length': '47715',
    # 'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryFXTT4S1LKA1LUDBd',
    'Cookie': 'SHIROJSESSIONID=29d3d835-396e-4abe-9802-c51ef44ec14f',
    'Host': '172.30.6.183:8088',
    'Origin': 'http://172.30.6.183:8088',
    'Referer': 'http://172.30.6.183:8088/njfxq/clue/clueDetail?id=1574316828061339650&Paramspage=&caseId=',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}
#
# # with open('上传文件.xlsx','r',encoding='ISO-8859-1') as f:
# if 1==1:
#     files = {
#         'file': open('上传文件.xlsx','rb')
#     }
#     # file_data = encode_multipart_formdata(files)
#     print(files)
#
#     req = requests.post('http://172.30.6.183:8088/njfxq/finance/suspiciousClueFile/uploadCustomerTradeInfoExcel',files=files,headers=header)
#     print(req.text)



# # 下载文件
# parasms = {
#     'fileId': '1582565645638455298'
# }
# downloadHeader = {
#     'Content-Type': 'application/json'
# }
# req = requests.get('http://172.30.6.183:8088/njfxq/finance/suspiciousClueFile/getFilePath?fileId=1582565645638455298',headers=header,params=parasms)
# with open('tttt.xls','wb') as f:
#     f.write(req.content)



'''
Accept: application/json, text/plain, */*
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Authorization: 1677034306556
Connection: keep-alive
Cookie: SHIROJSESSIONID=29d3d835-396e-4abe-9802-c51ef44ec14f
Host: 172.30.6.183:8088
Referer: http://172.30.6.183:8088/njfxq/clue/clueDetail?id=1574316828061339650&Paramspage=&caseId=
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36
'''







# X-Requested-With: XMLHttpRequest



header = {
    'Authorization': '1677034306556',
    'Connection': 'keep-alive',
    # 'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryFXTT4S1LKA1LUDBd',
    'Cookie': 'SHIROJSESSIONID=75ace860-0f00-4db0-9440-6c6d53cdf101',
    'Host': '172.30.6.183:8088',
    'Origin': 'http://172.30.6.183:8088',
    'Referer': 'http://172.30.6.183:8088/njfxq/search/clue/clueFeedBackDetailAll?id=1574192996457648130&Paramspage=clue&caseId=1567439544410976257',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}
# 请求体Payload
'''
    这里有必要解释下：
    如果请求体按照页面显示的配置如下：
        fileObject = {
            'type':'6',
            'orgType': 'B',
            'file': open('上传文件.xlsx','rb')
        }
    是错误的（第一次花费半天才调通）
    //////////////////////////////////////////////////////////
    正确的格式应该是传入一个元组，格式为：(<fileName>,<fileObject>,<Content-Type>) ，这里的fileObject是指具体的值。
    正确的请求体应为：
        fileObject = {
            'type':(None,'6',None),
            'orgType': (None,'B',None),
            'file': ('上传文件.xlsx',open('上传文件.xlsx','rb'),'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        }
'''
# fileObject = {
#     'type':(None,'6',None),
#     'orgType': (None,'B',None),
#     'file': ('上传文件.xlsx',open('上传文件.xlsx','rb'),'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
# }
# req = requests.post('http://172.30.6.183:8088/njfxq/finance/investigatefeedback/uploadFile',headers=header,files=fileObject)
# print(req.text)


from selenium import webdriver

chrome = webdriver.Chrome()
chrome.get('http://tpi.zhonju.cn/')
print(chrome.get_cookies())


cookie = [item["name"] + "=" + item["value"] for item in chrome.get_cookies()]
print(';'.join(it for it in cookie))


import sys
sys.exit()
chrome.quit()

req = requests.get('http://tpi.zhonju.cn/')
print(req.text)


from requestium import Session,Keys

session = Session()


# ww # 问我

'''
awdw
   

'''
