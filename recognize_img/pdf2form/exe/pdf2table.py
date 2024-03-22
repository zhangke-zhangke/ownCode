#-*- coding : utf-8-*-
# coding:unicode_escape
import pdfplumber
import pandas as pd
import sys
import os
import argparse




parser = argparse.ArgumentParser()
parser.add_argument('--input_filepath', type=str , help = 'Select the PDF you want to analyze')
parser.add_argument('--output_file_style', type=str, help='output_style：csv，xlsx')  # 1 for dn and jpeg car
parser.add_argument('--output_filepath', type=str,  help='Select the output path')
args = parser.parse_args()



# 解析参数
in_filepath = args.input_filepath
out_style = args.output_file_style
out_filepath = args.output_filepath



# # 解析参数
# in_filepath = sys.argv[1]
# out_style = sys.argv[2]
# out_filepath = sys.argv[3]


print("--input_filepath:",in_filepath)
print("--output_file_style",out_style)
print("--output_filepath",out_filepath)



# 解析pdf
pdf = pdfplumber.open(in_filepath)

# 获取pdf页数对象
print("pdf_page_num:",len(pdf.pages))

count = 0
for page in pdf.pages:
    count += 1
    #  page.extract_text()可以抓取当前页的全部信息，因为内容较多就先注释。
    # print(page.extract_text())
    page_list = []
    page_header = []
    for table in page.extract_tables():
        for i,row in enumerate(table):
            # 标头
            if i == 0:
                page_header.append(row)
            # 内容
            else:
                page_list.append(row)

    page_df = pd.DataFrame(page_list,columns=page_header)
    print(f'============ End of parsing on page {count} ============')

    # 输出路径
    if out_style == 'csv':
        out_path = out_filepath + f'\\{os.path.basename(in_filepath).split(".")[0]}_{count}.csv'
        print("Generate a CSV file in the following path:",out_path)
        page_df.to_csv(out_path,sep=',',index=False)
    elif out_style == 'xlsx':
        out_path = out_filepath + f'\\{os.path.basename(in_filepath).split(".")[0]}_{count}.xlsx'
        print("Generate a XLSX file in the following path:",out_path)
        page_df.to_excel(out_path,index=False)

pdf.close()



