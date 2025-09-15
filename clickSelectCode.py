# 点选验证码
import ddddocr

from PIL import Image, ImageDraw, ImageFont
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from io import BytesIO
from Clogs.log import SCLogger
from pageParser.yn.pageParser import *
from bs4 import BeautifulSoup
from utils.utils import getTime
import os
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class Ddddocr:

    def __init__(self):
        self.ocr = ddddocr.DdddOcr(show_ad=False)
        self.xy_ocr = ddddocr.DdddOcr(det=True, show_ad=False)

    def ddddocr_identify(self, captcha_bytes):
        return self.ocr.classification(captcha_bytes)

    def draw_img(self, content, xy_list):
        """画出图片"""
        # 填字字体
        # font_type = "./template/msyhl.ttc"
        # 加载字体
        font_type = resource_path("template/msyhl.ttc")
        # print(f"Loading font from: {font_type}")
        font_size = 20
        font = ImageFont.truetype(font_type, font_size)
        # 识别
        img = Image.open(BytesIO(content))
        draw = ImageDraw.Draw(img)
        words = []
        for row in xy_list:
            # 框字
            x1, y1, x2, y2 = row
            draw.line(([(x1, y1), (x1, y2), (x2, y2), (x2, y1), (x1, y1)]), width=1, fill="red")
            # 裁剪出单个字
            corp = img.crop(row)
            img_byte = BytesIO()
            corp.save(img_byte, 'png')
            # 识别出单个字
            word = self.ocr.classification(img_byte.getvalue())
            words.append(word)
            # 填字
            y = y1 - 30 if y2 > 300 else y2
            draw.text((int((x1 + x2)/2), y), word, font=font, fill="red")
        # img.show()
        return words

    def ddddocr_clcik_identify(self, content, crop_size=None):
        """目标检测识别"""
        img = Image.open(BytesIO(content))
        # print(img.size)
        if crop_size:
            img = img.crop(crop_size)
            img_byte = BytesIO()
            img.save(img_byte, 'png')
            content = img_byte.getvalue()
        xy_list = self.xy_ocr.detection(content)
        words = self.draw_img(content, xy_list)
        return dict(zip(words, xy_list))

    def case_demo(self, con):
        """点选识别结果"""
        click_identify_result = self.ddddocr_clcik_identify(con, (0, 0, 344, 344))
        img = Image.open(BytesIO(con))
        img = img.crop((0, 344, 344, 384))
        img_byte = BytesIO()
        img.save(img_byte, 'png')
        # identify_words = self.ocr.classification(img_byte.getvalue())
        # print(click_identify_result)
        # words_dict = {}
        # for word in identify_words:
        #     words_dict[word] = click_identify_result.get(word)
        # print(words_dict)
        img_xy = {}
        for key, xy in click_identify_result.items():
            img_xy[key] = (int((xy[0] + xy[2]) / 2), int((xy[1] + xy[3]) / 2))

        return img_xy


# 点选验证码，返回每个字在图片上的坐标位置
result = Ddddocr().case_demo('./xxx.png')

# 循环待点选的字，匹配result结果
# 按照待点选顺序，顺序进行