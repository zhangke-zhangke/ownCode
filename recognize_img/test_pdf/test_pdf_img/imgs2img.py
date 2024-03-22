#!/usr/bin/env python
# -*- coding:utf-8 -*-
import PIL.Image as Image
import os

# IMAGES_PATH = r'D:\Gitlab\my_world\MachineLearning\imgs'+'\\'  # 图片集来源地址
IMAGES_PATH = r'C:\Users\dell\Desktop\邮储出差报销凭证\地铁\出行凭证'+'\\'  # 图片集来源地址
IMAGES_FORMAT = ['.jpg', '.JPG','.png']  # 图片格式
IMAGE_SIZE = 1500  # 每张小图片的大小
IMAGE_ROW = 3  # 图片间隔，也就是合并成一张图后，一共有几行
IMAGE_COLUMN = 7  # 图片间隔，也就是合并成一张图后，一共有几列
IMAGE_SAVE_PATH = r'C:\Users\dell\Desktop\concat.png'  # 图片转换后的地址

# 获取图片集地址下的所有图片名称
image_names = [name for name in os.listdir(IMAGES_PATH) for item in IMAGES_FORMAT if
               os.path.splitext(name)[1] == item]

# 简单的对于参数的设定和实际图片集的大小进行数量判断
if len(image_names) != IMAGE_ROW * IMAGE_COLUMN:
    raise ValueError("合成图片的参数和要求的数量不能匹配！")


# 定义图像拼接函数
def image_compose():
    to_image = Image.new('RGB', (IMAGE_COLUMN * IMAGE_SIZE, IMAGE_ROW * IMAGE_SIZE))  # 创建一个新图
    # 循环遍历，把每张图片按顺序粘贴到对应位置上
    for y in range(1, IMAGE_ROW + 1):
        for x in range(1, IMAGE_COLUMN + 1):
            from_image = Image.open(IMAGES_PATH + image_names[IMAGE_COLUMN * (y - 1) + x - 1]).resize(
                (IMAGE_SIZE, IMAGE_SIZE), Image.ANTIALIAS)
            to_image.paste(from_image, ((x - 1) * IMAGE_SIZE, (y - 1) * IMAGE_SIZE))
    return to_image.save(IMAGE_SAVE_PATH)  # 保存新图


image_compose()  # 调用函数这里插入代码片





# import numpy as np
#
# from PIL import Image
#
# paths = ['./1.png', './2.png', './3.png', './4.png']
# img_array = ''
# img = ''
# for i, v in enumerate(paths):
#     if i == 0:
#         img = Image.open(v)  # 打开图片
#         img_array = np.array(img)  # 转化为np array对象
#     if i > 0:
#         img_array2 = np.array(Image.open(v))
#
#         print(img_array.shape,img_array2.shape)
#         img_array = np.concatenate((img_array, img_array2), axis=1)  # 横向拼接
#         # img_array = np.concatenate((img_array, img_array2), axis=0)  # 纵向拼接
#         img = Image.fromarray(img_array)
#
# # 保存图片
# img.save('test.jpg')





# import os
# from PIL import Image
#
# UNIT_SIZE = 8900  # the size of image
# save_path = r'D:\Gitlab\my_world\recognize_img\test_pdf\test_pdf_img'
# path = r"D:\Gitlab\my_world\recognize_img\test_pdf\test_pdf_img"+'\\'
# images = []  # all pic name
#
#
# def pinjie():
#     if not os.path.exists(save_path):
#         os.makedirs(save_path)
#     for img in os.listdir(path):
#         images.append(img)
#     for i in range(int(len(images) / 6)):
#         imagefile = []
#         j = 0
#         for j in range(6):
#             print(Image.open(path + '/' + images[i * 6 + j]))
#             imagefile.append(Image.open(path + '/' + images[i * 6 + j]))
#         target = Image.new('RGB', (UNIT_SIZE, UNIT_SIZE * 6))  # width, height
#         left = 0
#         right = UNIT_SIZE
#         for image in imagefile:
#             target.paste(image, (0, left, UNIT_SIZE, right))
#             left += UNIT_SIZE
#             right += UNIT_SIZE
#             quality_value = 100
#         target.save(save_path + '/out_{}.jpg'.format(i), quality=quality_value)
#
#
#
#
#
# pinjie()
#
#
#
#
