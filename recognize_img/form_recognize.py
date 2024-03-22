import cv2
import imutils
import sys
import numpy as np
import re
import pytesseract
from paddleocr import PaddleOCR
import matplotlib.pyplot as plt
import pandas as pd
import time
import os

plt.rcParams['font.sans-serif'] = ['SimHei']  # 在图中正确显示中文
plt.rcParams['axes.unicode_minus'] = False  # 默认是使用Unicode负号，设置正常显示字符，如正常显示负号




# 将字段转为str,防止数字位数高的写入csv会变成科学计数法
def num_out(data):
    data = str(data) + '\t'
    return data





# src = 'IMG_0016.jpg'
# src = 'money.jpg'
# src = 'img_recognize.png'
# src = 'D:\\Gitlab\\my_world\\recognize_img\\demo_img\\_1.png'
src = r'D:\Gitlab\my_world\recognize_img\img2pdf\222_0.png'  # 扫描有边框
#  1 ： 彩色，  0 ： 灰色，  -1 ： 保持原有色素
raw = cv2.imread(src, 0)



# 二值化图片
binary = cv2.adaptiveThreshold(~raw, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 35, -5)
# print(binary)
# # 膨胀操作
# kernel_dilate = cv2.getStructuringElement(cv2.MORPH_RECT,(1,1))
# binary = cv2.dilate(binary, kernel_dilate)
# cv2.imshow("膨胀后图片", binary)


# # 腐蚀操作
# kernel_erode = cv2.getStructuringElement(cv2.MORPH_RECT,(1,1))
# binary = cv2.erode(binary, kernel_erode)
# cv2.imshow("腐蚀后图片", binary)


# 展示图片，并使用 imutils.resize 重置图片大小
cv2.imshow('binary_picture',imutils.resize(binary,600))
# if cv2.waitKey(0):
#     cv2.destroyWindow('binary_picture')



# 识别横线与竖线
rows, cols = binary.shape
scale = 40
# 自适应获取核值
# 识别横线:
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (cols // scale, 1))
eroded = cv2.erode(binary, kernel, iterations=1)
dilated_col = cv2.dilate(eroded, kernel, iterations=1)
cv2.imshow("excel_horizontal_line", dilated_col)




# 识别竖线：
scale = 20
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, rows // scale))
eroded = cv2.erode(binary, kernel, iterations=1)
dilated_row = cv2.dilate(eroded, kernel, iterations=1)
cv2.imshow("excel_vertical_line", dilated_row)
# if cv2.waitKey(0):
#     cv2.destroyWindow('excel_vertical_line')




# 将识别出来的横竖线合起来，求出交点
bitwise_and = cv2.bitwise_and(dilated_col, dilated_row)

cv2.imshow("excel_bitwise_and", bitwise_and)
# if cv2.waitKey(0):
#     cv2.destroyWindow('excel_bitwise_and')



# 标识表格轮廓
merge = cv2.add(dilated_col, dilated_row)
cv2.imshow("entire_excel_contour", merge)
# if cv2.waitKey(0):
#     cv2.destroyWindow('entire_excel_contour')



# 两张图片进行减法运算，去掉表格框线
merge2 = cv2.subtract(binary, merge)
cv2.imshow("binary_sub_excel_rect", merge2)
# if cv2.waitKey(0):
#     cv2.destroyWindow('binary_sub_excel_rect')


new_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
erode_image = cv2.morphologyEx(merge2, cv2.MORPH_OPEN, new_kernel)
cv2.imshow('erode_image2', erode_image)
# if cv2.waitKey(0):
#     cv2.destroyWindow('erode_image2')



merge3 = cv2.add(erode_image, bitwise_and)
cv2.imshow('merge3', merge3)




# 将焦点标识取出来
ys, xs = np.where(bitwise_and > 0)


# 横纵坐标数组
y_point_arr = []
x_point_arr = []
# 通过排序，排除掉相近的像素点，只取相近值的最后一点
# 这个10就是两个像素点的距离，不是固定的，根据不同的图片会有调整，基本上为单元格表格的高度（y坐标跳变）和长度（x坐标跳变）
i = 0
sort_x_point = np.sort(xs)
for i in range(len(sort_x_point) - 1):
    if sort_x_point[i + 1] - sort_x_point[i] > 10:
        x_point_arr.append(sort_x_point[i])
    i = i + 1
# 要将最后一个点加入
x_point_arr.append(sort_x_point[i])

i = 0
sort_y_point = np.sort(ys)
# print(np.sort(ys))
for i in range(len(sort_y_point) - 1):
    if (sort_y_point[i + 1] - sort_y_point[i] > 10):
        y_point_arr.append(sort_y_point[i])
    i = i + 1
y_point_arr.append(sort_y_point[i])



# 按esc关闭图片， 单位 ms
if cv2.waitKey(0):
    cv2.destroyAllWindows()



# 循环y坐标，x坐标分割表格
data = [[] for i in range(len(y_point_arr))]
for i in range(len(y_point_arr) - 1):
    for j in range(len(x_point_arr) - 1):
        # 在分割时，第一个参数为y坐标，第二个参数为x坐标
        cell = cv2.imread(src)[y_point_arr[i]:y_point_arr[i + 1], x_point_arr[j]:x_point_arr[j + 1]]
        # cell = binary[y_point_arr[i]:y_point_arr[i + 1], x_point_arr[j]:x_point_arr[j + 1]]

        # cv2.imshow('cell',cell)
        # # 按esc关闭图片， 单位 ms
        # if cv2.waitKey(0):
        #     cv2.destroyAllWindows()

        '''
            easyocr 库识别图片文字   ps:此库不可用，与cv2.imshow()函数有冲突  冲突原因未知
        '''
        # # 导入easyocr
        # import easyocr
        # # 创建reader对象
        # reader = easyocr.Reader(['ch_sim', 'en'])
        # # 读取图像
        # result = reader.readtext('test.jpg')
        # # 结果
        # print(result)



        '''
            PaddleOCR 库识别图片文字
        '''
        # 得到的图片信息    PaddleOCR识别不出来换行，所以遇到单元格有多行文字时，要做处理
        ocr = PaddleOCR(use_angle_cls=True, lang="ch")
        img_info = ocr.ocr(cell,cls=False)
        # 最终结果
        img_result = ""
        for line in img_info:
            # 得到图片中文字  循环加总，（多行文字的情况）
            img_result += line[-1][0]
            img_result += ' '

        # 去除特殊字符
        text1 = re.findall(r'[^\*"/:?\\|<>″′‖ 〈\n]', img_result, re.S)
        text1 = "".join(text1)
        print('单元格图片信息：' + text1)
        print("\n")
        data[i].append(text1)
        j = j + 1



        '''
            pytesseract 库识别图片文字
        '''
        # # 读取文字，此为默认英文
        # # pytesseract.pytesseract.tesseract_cmd = 'E:/Tesseract-OCR/tesseract.exe'
        # text1 = pytesseract.image_to_string(cell, lang="chi_sim+eng")
        #
        # # 去除特殊字符
        # text1 = re.findall(r'[^\*"/:?\\|<>″′‖ 〈\n]', text1, re.S)
        # text1 = "".join(text1)
        # print('单元格图片信息：' + text1)
        # data[i].append(text1)
        # j = j + 1

        # import os
        # os.remove(f'{j-1}.png')

    i = i + 1


data = pd.DataFrame(data).replace('None',np.nan).dropna()

for i in range(data.shape[1]):
    data[i] = data[i].map(num_out)



data.to_csv(f'{os.path.dirname(src)}\\{os.path.basename(src).split(".")[0]}.csv',index=False,encoding='utf-8',header=False)

