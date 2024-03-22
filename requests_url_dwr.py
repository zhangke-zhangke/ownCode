# -*- coding: utf-8 -*-

import requests
import re
import random, time, sys


def tokenify(number):
    tokenbuf = []
    charmap = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ*$"
    remainder = number
    while remainder > 0:
        tokenbuf.append(charmap[remainder & 0x3F])
        remainder = remainder // 64
    return ''.join(tokenbuf)


domain = "http://test2.maxblog.com:8080"


class Transaction(object):
    def __init__(self):
        self.custom_timers = {}  # restart timer
        self.ssrequest = requests.session()

        # get user
        url = 'http://192.168.149.84:5000/getuser'
        r = requests.get(url)
        res = eval(r.text)
        self.username = res[0]
        self.password = res[1]

        ##########################   Lgoin    ##########################
        # get dwr session
        url2 = domain + "/max_blog_rf/dwr/call/plaincall/__System.generateId.dwr"
        headers = {
            'content-type': 'text/plain',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36'
        }
        private = {
            'callCount': '1',
            'c0-scriptName': '__System',
            'c0-methodName': 'generateId',
            'c0-id': '0',
            'batchId': '0',
            'instanceId': '0',
            'page': '%2Fmax_blog_rf%2Flogin.jsp',
            'scriptSessionId': '',
            'windowName': ''
        }
        r = self.ssrequest.post(url2, data=private, headers=headers)
        # print r
        dwrsession = ""
        me = re.search(r'.*\"(\S{27})\"', r.text)
        if me:
            dwrsession = me.group(1)
        else:
            print('not match dwrsession')


        # scriptSessionId = dwrsession+"/O1tRakl-dPKysDfm5"
        t = long(time.time() * 1000)
        r = random.randint(1000000000000000, 9999999999999999)
        self.scriptSessionId = dwrsession + "/" + tokenify(t) + "-" + tokenify(r)
        requests.utils.add_dict_to_cookiejar(self.ssrequest.cookies, {'DWRSESSIONID': dwrsession})

        # login
        url = domain + "/max_blog_rf/dwr/call/plaincall/RfLoginService.login.dwr"
        headers = {
            'content-type': 'text/plain',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36'
        }
        private = {
            'callCount': '1',
            'windowName': '',
            'c0-scriptName': 'RfLoginService',
            'c0-methodName': 'login',
            'c0-id': '0',
            'c0-param0': 'string:4',
            'c0-param1': 'string:%s' % self.username,
            'c0-param2': 'string:%s' % self.password,
            'c0-param3': 'boolean:false',
            'batchId': '1',
            'instanceId': '0',
            'page': '%2Fmax_blog_rf%2Flogin.jsp',
            'scriptSessionId': self.scriptSessionId
        }
        r = self.ssrequest.post(url, data=private, headers=headers)
        # print r
        # print r.text
        # RF_SESSION_TAG=4%2Ctest100
        requests.utils.add_dict_to_cookiejar(self.ssrequest.cookies,
                                             {'RF_SESSION_TAG': '4%2C{user}'.format(user=self.username)})

        url = domain + "/max_blog_rf/pages/rf/pick/batchPicking.jsp"
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36'
        }
        r = self.ssrequest.get(url, headers=headers)
        # print r

        t = long(time.time() * 1000)
        r = random.randint(1000000000000000, 9999999999999999)
        self.scriptSessionId = dwrsession + "/" + tokenify(t) + "-" + tokenify(r)
        # /max_blog_rf/dwr/call/plaincall/__System.pageLoaded.dwr
        url3 = domain + "/max_blog_rf/dwr/call/plaincall/__System.pageLoaded.dwr"
        headers = {
            'content-type': 'text/plain',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36'
        }
        private = {
            'callCount': '1',
            'windowName': '',
            'c0-scriptName': '__System',
            'c0-methodName': 'pageLoaded',
            'c0-id': '0',
            'batchId': '1',
            'instanceId': '0',
            'page': '%2Fmax_blog_rf%2Fpages%2Frf%2Fpick%2FbatchPicking.jsp',
            'scriptSessionId': self.scriptSessionId
        }
        r = self.ssrequest.post(url3, data=private, headers=headers)
        # print r

    def run(self):
        # get box
        url = 'http://192.168.149.84:5000/getorder'
        r = requests.get(url)
        box = 'JH' + r.text

        # get pc info   ['16060100005096','ITEMTEST90023','TT01010102']
        url = 'http://192.168.149.84:5000/getupc/{user}'.format(user=self.username)
        r = requests.get(url)
        res = eval(r.text)
        pc_no = res[0]
        it_code = res[1]
        gd_loc = res[2]

        try:
            ##########################   Bussniess    ##########################
            url = domain + "/max_blog_rf/dwr/call/plaincall/BatchPickingService.txRequiredPick.dwr"
            headers = {
                'Content-Type': 'text/plain',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36'
            }
            private = {
                'callCount': '1',
                'windowName': '',
                'c0-scriptName': 'BatchPickingService',
                'c0-methodName': 'txRequiredPick',
                'c0-id': '0',
                'c0-param0': 'string:%s' % pc_no,
                'c0-param1': 'string:%s' % gd_loc,
                'c0-param2': 'string:%s' % box,
                'c0-param3': 'string:%s' % it_code,
                'c0-param4': 'number:1',
                'c0-param5': 'number:5',
                'batchId': '3',
                'instanceId': '0',
                'page': '%2Fmax_blog_rf%2Fpages%2Frf%2Fpick%2FbatchPicking.jsp',
                'scriptSessionId': self.scriptSessionId
            }
            start = time.time()
            r = self.ssrequest.post(url, data=private, headers=headers)
            response_time = time.time()
            self.custom_timers['response sent'] = response_time - start
            assert ('status:true' in r.text), 'Failed pick item:%s' % r.text.replace('\n', '')
            time.sleep(0.02)
            # print r
            # print r.text
        except Exception as e:
            # print str(e)
            # print str(sys.exc_info())
            raise Exception('Error: {0}--{1}'.format(str(e), str(sys.exc_info())))


if __name__ == '__main__':
    trans = Transaction()
    trans.run()

    # set a timer to calculate the interface response time.
    for timer in ('response sent',):
        print('%s: %.5f secs' % (timer, trans.custom_timers[timer])  )
