from pypdf import PdfMerger
import os
import re
import argparse



# pyinstaller  -F run.py --collect-all pypdf,os,re,argparse


parser = argparse.ArgumentParser()
parser.add_argument('--outfile_name', type=str, help='out concat pdf name',default='concat')
args = parser.parse_args()

# 解析参数
outfile_name = args.outfile_name




# 合并后的文件名
mergeFileName = f'{outfile_name}.pdf'

# 获取当前目录下所有PDF文件，并按照文件名自然排序(要排除合并后的文件，避免多次合并造成内容重复)
pdf_files = sorted([f for f in os.listdir('.') if f.endswith('.pdf') and f != mergeFileName], key=lambda x: [int(c) if c.isdigit() else c for c in re.split('(\d+)', x)])




# 创建PDF文件写入器
merger = PdfMerger()

# 将所有PDF文件添加到写入器中
for pdf in pdf_files:
    merger.append(pdf)


# 将合并后的PDF文件保存到磁盘上
# "wb" 以二进制写方式打开，只能写文件。如果文件不存在，创建该文件；如果文件已存在，先清空，再打开文件。
with open(mergeFileName, 'wb') as output:
    # 写入合并后的PDF文件
    merger.write(output)
    merger.close()

