# 安装指令：pip install pypdf2
from PyPDF2.pdf import PdfFileReader
import re
import urllib.request
import urllib.parse
import json
import sys
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams
# import StringIO
from io import StringIO
from PyPDF2.pdf import PdfFileReader
import sys



# 有道翻译方法
def youdao_translate(content):
    '''实现有道翻译的接口'''
    youdao_url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
    data = {}

    data['i'] = content
    data['from'] = 'AUTO'
    data['to'] = 'AUTO'
    data['smartresult'] = 'dict'
    data['client'] = 'fanyideskweb'
    data['salt'] = '1525141473246'
    data['sign'] = '47ee728a4465ef98ac06510bf67f3023'
    data['doctype'] = 'json'
    data['version'] = '2.1'
    data['keyfrom'] = 'fanyi.web'
    data['action'] = 'FY_BY_CLICKBUTTION'
    data['typoResult'] = 'false'
    data = urllib.parse.urlencode(data).encode('utf-8')

    youdao_response = urllib.request.urlopen(youdao_url, data)
    youdao_html = youdao_response.read().decode('utf-8')
    target = json.loads(youdao_html)

    trans = target['translateResult']
    ret = ''
    for i in range(len(trans)):
        # line = ''
        # for j in range(len(trans[i])):
        #     line = trans[i][j]['tgt']
        # ret += line + '\n'

        for j in range(len(trans[i])):
            line = trans[i][j]['tgt']
            ret += line
        ret += '\n'
    return ret



class PDFUtils():
    def __init__(self):
        pass

    def pdf2txt(self, path):
        with open(path, 'rb') as f:
            # # 创建pdfreader，判断是否文档加密
            # pdf = PdfFileReader(f)
            # if pdf.isEncrypted == True:
            #     print("加密")
            # else:
            #     pass
            #
            # sys.exit()
            praser = PDFParser(f)


            doc = PDFDocument(praser)

            if not doc.is_extractable:
                raise PDFTextExtractionNotAllowed

            pdfrm = PDFResourceManager()
            laparams = LAParams()

            device = PDFPageAggregator(pdfrm, laparams=laparams)
            interpreter = PDFPageInterpreter(pdfrm, device)

            pdf_infomation = []
            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)
                layout = device.get_result()
                for x in layout:
                    if hasattr(x, "get_text"):
                        content = x.get_text().replace('\n','')
                        pdf_infomation.append(content)
        f.close()
        return pdf_infomation




# 一句一句返回
def translate():
    '''读取pdf，并且翻译'''

    filepath = u'C:\\Users\\dell\\Desktop\\Nokia_N958GB_UG_zh-CN.pdf'
    pdf_utils = PDFUtils()
    pdf_info = pdf_utils.pdf2txt(filepath)
    # print(pdf_info,type(pdf_info))
    for i in pdf_info:
        print(i)
        trans = youdao_translate(i)
        print(trans)

        # print(i)
        # if len(i) < 1:
        #     continue
        # else:
        #     trans = youdao_translate(i)
        #     print(trans)





if __name__ == '__main__':

    translate()
