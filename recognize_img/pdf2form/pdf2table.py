# -*- coding: utf-8 -*-
import pdfplumber
import pandas as pd
import sys
import os
import argparse

import csv







in_filepath = r'D:\Gitlab\my_world\recognize_img\test_pdf\3.pdf'
out_file_style = 'csv'
out_filepath = r'C:\\Users\\dell\\Desktop'




# 解析pdf
pdf = pdfplumber.open(in_filepath)


# 获取pdf页数对象
print("pdf_page_num:",len(pdf.pages))

count = 0
for page in pdf.pages:
    count += 1
    #  page.extract_text()可以抓取当前页的全部信息，因为内容较多就先注释。
    # print(page.extract_text())

    # 判断是否有识别表格
    if len(page.extract_tables()) < 1:
        insert_list = []
        for i in range(len(page.extract_text().split('\n'))):
            row = page.extract_text().split('\n')[i].split(' ')
            insert_list.append(row)
        print(insert_list)
        with open(f'{out_filepath}\\{os.path.basename(in_filepath).split(".")[0]}.csv', 'w',encoding='utf-8') as f:
            # 创建CSV写入器
            writer = csv.writer(f)
            # 遍历，插入
            for row in insert_list:
                # 向CSV文件写入一行
                writer.writerow(row)

    else:
        # 以写模式打开文件
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
        if out_file_style == 'csv':
            out_path = out_filepath + f'\\{os.path.basename(in_filepath).split(".")[0]}_{count}.csv'
            print("Generate a CSV file in the following path:",out_path)
            page_df.to_csv(out_path,sep=',',index=False)
        elif out_file_style == 'xlsx':
            out_path = out_filepath + f'\\{os.path.basename(in_filepath).split(".")[0]}_{count}.xlsx'
            print("Generate a XLSX file in the following path:",out_path)
            page_df.to_excel(out_path,index=False)

    pdf.close()



