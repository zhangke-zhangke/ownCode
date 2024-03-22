# pip install you-get

import sys
import you_get

def download(url, path):
    sys.argv = ['you-get', '-o', path, '-i', url]
    you_get.main()



if __name__ == '__main__':
    # 视频网站的地址
    url = 'https://www.bilibili.com/bangumi/play/ep118488?from=search&seid=5050973611974373611'
    # url = 'https://xlntidea.com.cn/index.php/vplay/55911-2-1.html'
    # 视频输出的位置
    path = 'D:/test'
    download(url, path)
    # mp4的xpath是/html/body/div[4]/div[1]/script[3]/text() 可能需要用re.split分割一下 还有什么不会的问我

