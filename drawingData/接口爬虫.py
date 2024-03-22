import requests
import datetime
import time



# @classmethod
# def get_cookie_expires(cls, jar_cookies):
#     """
#     获取 jar_cookies 里面 sessionid 或 sessionid_ss 或 sid_tt 的有效期
#     """
#     result = None
#     for item in jar_cookies:
#         if item.name == "sessionid" or item.name == "sessionid_ss" or item.name == "sid_tt":
#             timestamp = item.expires
#             if timestamp:
#                 result = cls.timestamp_to_datetime(timestamp)
#     return result
#
#
# @staticmethod
# def timestamp_to_datetime(timestamp):
#     """
#     时间戳转datetime
#     :param timestamp:
#     :return: datetime
#     """
#     result = datetime.fromtimestamp(timestamp)
#     return result




headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Cookie':'SHIROJSESSIONID=f5a31062-0e38-413f-9583-1b690b80e418',
    'Referer':'http://172.30.6.205/content/taskManagement',
    'Content-Type': 'application/json;charset=UTF-8'
}
# res = requests.get('http://172.30.6.205/finance/task/queryList',headers=headers)
# print(res.content)



# session = requests.session()
# # # 添加cookies
# session.cookies = requests.utils.cookiejar_from_dict({'Cookies':'SHIROJSESSIONID=f5a31062-0e38-413f-9583-1b690b80e418'})

# # 获取初始化的session中的cookies
# cookie_dict = requests.utils.dict_from_cookiejar(session.cookies)
# print("======cookie_dict:", cookie_dict)


# get_cookie_expires(,'SHIROJSESSIONID=f5a31062-0e38-413f-9583-1b690b80e418')


# res = session.post('http://172.30.6.205/finance/task/queryList',data=headers)
# print(res.text)




data = {
    "user":'admin',
    "password":'password',
    "pageNum": 1,
    "pageSize": 15,
    "sort": 0,
    "sortType": 0
}
headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '49',
    'Content-Type': 'application/json;charset=UTF-8',
    'Cookie': 'SHIROJSESSIONID=4da84910-ca83-4f1e-8bd9-8fda733ea40f',
    'Host': '172.30.6.205',
    'Origin': 'http://172.30.6.205',
    'Referer': 'http://172.30.6.205/content/taskManagement',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }
req = requests.post('http://172.30.6.205/finance/task/queryList',json=data,headers=headers)
# req_return = req.json()


c = 0
while True:
    req = requests.post('http://172.30.6.205/finance/task/queryList',json=data,headers=headers)
    req_return = req.json()
    c += 1
    print(f'请求第{c}次，状态：{req_return.get("code")}，当前时间：{datetime.datetime.now()}')

    time.sleep(10)





'''
    请求第1次，状态：200，当前时间：2023-02-02 15:24:28.227830
    请求第288次，状态：200，当前时间：2023-02-02 16:12:36.519878
'''