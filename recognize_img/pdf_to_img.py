import PyPDF4
import pikepdf
import fitz
import os

def jiemi(pdfpath):
    new_pdfpath = pdfpath[:-4] + '_new' + pdfpath[-4:]

    with open(pdfpath,"rb") as fp:
        pdfFile = PyPDF4.pdf.PdfFileReader(fp)

        # pdf 解密
        if pdfFile.isEncrypted:
            pdf = pikepdf.open(pdfpath, password='123456')
            print("此文档加密")
        else:
            pdf = pikepdf.open(pdfpath,)
            print("此文档没有加密")
        pdf.save(new_pdfpath)

    fp.close()





def pdf_image(pdf_name):
    img_paths = []
    pdf = fitz.Document(pdf_name)
    for i,pg in enumerate(range(0, pdf.pageCount)):
        page = pdf[pg]  # 获得每一页的对象
        trans = fitz.Matrix(3.0, 3.0).preRotate(0)
        pm = page.getPixmap(matrix=trans, alpha=False)  # 获得每一页的流对象
        # pm.writePNG(dir_name + os.sep + base_name[:-4] + '_' + '{:0>3d}.png'.format(pg + 1))  # 保存图片
        # img_path = 'D:\\Gitlab\\my_world\\recognize_img\\parser_pdf\\' + '_' + str(pg+1) + '.png'
        img_path = rf'D:\Gitlab\my_world\recognize_img\img2pdf\{os.path.basename(pdf_name).split(".")[0]}_{i}.png'
        pm.writePNG(img_path)  # 保存图片
        img_paths.append(img_path)
    pdf.close()
    return img_paths



if __name__ == '__main__':
    # jiemi('D:\\Gitlab\\my_world\\recognize_img\\demo_img\\无框表格不可编辑.pdf')
    # pdf_image('C:\\Users\\dell\\Desktop\\202104147187110045_1.pdf')
    # pdf_image('C:\\Users\\dell\Desktop\\样例3.pdf')
    pdf_image(r'D:\Gitlab\my_world\recognize_img\demo_img\result.pdf')

