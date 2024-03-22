import time
import requests
from bs4 import BeautifulSoup
import os
import re
from urllib.request import urljoin
from PIL import Image

webp_file = 'girlfriends_webp'
png_file = 'girlfriends_png'

print(os.getcwd())

# 创建图片保存路径
if not os.path.exists(webp_file):
    os.makedirs(webp_file, exist_ok=True)
if not os.path.exists(png_file):
    os.makedirs(png_file, exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0',
    # 'Cookie':''
    'Connection': 'keep-alive'
}
url_pattern = "https://www.huashi6.com/tags/161?p={}"

domain = 'https://img2.huashi6.com'


# 图片地址获取函数
def analysis(item, results):
    pattern = re.compile(item, re.I | re.M)
    result_list = pattern.findall(results)
    return result_list


# 图片格式转换函数
def change_webp2png(name_webp, name_png, img_url):
    try:
        image_wepb = Image.open(name_webp)
        image_wepb.save(name_png)
    except:
        download_image(name_webp, name_png, img_url)


# 图片下载函数
def download_image(name_webp, name_png, img_url):
    if not os.path.exists(name_png):
        if os.path.exists(name_webp):
            os.remove(name_webp)
        print(img_url)
        r = requests.get(img_url, headers=headers)
        # print(r.content)
        time.sleep(5)
        if r.status_code == 200:
            with open(name_webp, 'wb') as f:
                f.write(r.content)
        change_webp2png(name_webp, name_png, img_url)


for i in range(1, 20):
    time.sleep(5)
    url = url_pattern.format(i)
    response = requests.get(url=url, headers=headers)
    # 解码
    # response.encoding = 'utf-8'
    response.encoding = 'unicode-escape'
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    results = soup.find_all('script')

    image_dirty = str(results[1])

    urls = analysis(r'"path":"(.*?)"', image_dirty)[:20]

    for img in urls:
        img_url = urljoin(domain, img)

        # 获取文件名
        name = img.split('/')[-1]
        name = name.split('.')[0]
        name_webp = name + '.webp'
        name_webp = os.path.join(webp_file, name_webp)
        name_png = name + '.png'
        name_png = os.path.join(png_file, name_png)
        download_image(name_webp, name_png, img_url)
