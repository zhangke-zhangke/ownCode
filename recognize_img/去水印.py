from itertools import product
from PIL import Image

img = Image.open('D:\\Gitlab\\my_world\\recognize_img\\test_pdf\\3.pdf')
width, height = img.size
for pos in product(range(width), range(height)):
    if sum(img.getpixel(pos)[:3]) > 600:
        img.putpixel(pos, (255,255,255))
img.save('D:\\Gitlab\\my_world\\recognize_img\\test_pdf\\3_去水印.pdf')





