import logging
from logging.handlers import TimedRotatingFileHandler
import os
from flask import current_app
import sys




class applog():
    r'''
        日志模块
    '''
    def __init__(self):
        pass

    @staticmethod
    def get_handler(mainfile):
        r'''
        :param mainfile:  C:\Users\dell\Desktop\python-graph
        :return:
        '''
        app_log_path = f'{mainfile}/log/applog/'
        # 存放日志文件夹
        if not os.path.exists(app_log_path):
            try:
                os.makedirs(app_log_path)
            except Exception as e:
                print(f'创建日志文件夹失败：{e}')
                sys.exit(1)
        # 日志格式设置
        formatter = logging.Formatter(f"python-graph - %(asctime)s - %(filename)s:%(lineno)d - flask-thread-%(thread)d - %(levelname)s - %(message)s")
        handler = TimedRotatingFileHandler(f"{app_log_path}/flask.log", when="midnight", interval=1, backupCount=15,encoding="UTF-8")
        handler.setFormatter(formatter)
        handler.suffix = "%Y%m%d"
        # 解决第二天日志文件无法创建的问题
        handler.filename = f"{app_log_path}/flask.log"

        return handler

    @staticmethod
    def get_logger(app):
        r'''
        :param app: Flask app
        :return:
        '''
        logger = logging.getLogger("python-graph")
        logger.setLevel(logging.DEBUG)
        logger.addHandler(applog.get_handler(current_app.root_path))
        return logger

