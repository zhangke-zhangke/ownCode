#coding:utf-8
'''
@File    :   setup.py    
@Author :   zhangke@zqykj.com
@Modify Time 2022/3/11 14:27
@Function :
'''

import io
#python setup.py bdist_wheel
from setuptools import find_packages,setup

setup(
 name = "node2vecter",    # 包名
 version = "0.1",    # 版本信息
 author="zhangke",
 author_email='zhangke@zqykj.com',
 packages = find_packages(),   # 要打包的项目文件夹
 include_package_data=True, # 自动打包文件夹内所有数据
 zip_safe=True,    # 设定项目包为安全，不用每次都检测其安全性
 install_requires = [   # 安装依赖的其他包 Hello.py, zqykj.py 依赖
 'pandas>=0.23.0',
 'pymysql>=0.9.3',
 'sqlalchemy>=1.2.7',
 ],
 python_requires='>=3.6'
)