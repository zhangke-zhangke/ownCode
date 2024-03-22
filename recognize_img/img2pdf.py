





import os
from fpdf import FPDF

pdf = FPDF()
pdf.set_auto_page_break(0)         # 自动分页设为False

path = r"D:\Gitlab\my_world\recognize_img\img2pdf"
imagelist = [i for i in os.listdir(path)]


for image in sorted(imagelist):
    pdf.add_page()
    pdf.image(os.path.join(path, image), w=200, h=300)      # 指定宽高

pdf.output(os.path.join(path, "佩奇.pdf"), "F")










