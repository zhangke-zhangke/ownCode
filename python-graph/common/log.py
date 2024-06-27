import logging
from logging.handlers import TimedRotatingFileHandler
import os
from flask import current_app
import sys




class applog():

    def __int__(self):
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
            except Exception:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                print(exc_type, exc_value, exc_traceback)

        formatter = logging.Formatter(f"[python-graph] - [%(asctime)s] - [%(filename)s:%(lineno)d] - [flask-thread-%(thread)d] - [%(levelname)s] - %(message)s")
        handler = TimedRotatingFileHandler(f"{app_log_path}/flask.log", when="midnight", interval=1, backupCount=15,encoding="UTF-8", delay=False, utc=True)
        handler.setFormatter(formatter)

        return handler

