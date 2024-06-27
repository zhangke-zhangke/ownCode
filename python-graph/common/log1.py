# log sys
# dev at 2022-09-20
# dever : zhangke

import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler



def log_object():
    log = logging.getLogger(__name__)
    current_path = os.path.realpath(__file__)
    parent_current_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
    parent_current_path = os.path.abspath(os.path.dirname(parent_current_path) + os.path.sep + ".")

    # 存放日志文件夹
    log_info_path = parent_current_path + '/log/app'
    if not os.path.exists(log_info_path):
        try:
            os.makedirs(log_info_path)
        except Exception:
            exc_type,exc_value,exc_traceback = sys.exc_info()
            print(exc_type,exc_value,exc_traceback)
    formatter = logging.Formatter('flask-flaskStudy - %(asctime)s - %(levelname)s - %(name)s - %(threadName)s - %(message)s')
    # 存放日志文件，设置一天一分表，保存近31天日志文件
    fileTimeHandler = TimedRotatingFileHandler(log_info_path + '/flask.log',"D",1,31)
    # 初始化日志结构
    fileTimeHandler.suffix = "%Y%m%d"
    fileTimeHandler.setFormatter(formatter)
    logging.basicConfig(level=logging.INFO)
    log.addHandler(fileTimeHandler)

    # return log

    return fileTimeHandler



'''
    %(name)s            Name of the logger (logging channel)
    %(levelno)s         Numeric logging level for the message (DEBUG, INFO,WARNING, ERROR, CRITICAL)
    %(levelname)s       Text logging level for the message ("DEBUG", "INFO","WARNING", "ERROR", "CRITICAL")
    %(pathname)s        Full pathname of the source file where the logging call was issued (if available)
    %(filename)s        Filename portion of pathname
    %(module)s          Module (name portion of filename)
    %(lineno)d          Source line number where the logging call was issued (if available)
    %(funcName)s        Function name
    %(created)f         Time when the LogRecord was created (time.time() return value)
    %(asctime)s         Textual time when the LogRecord was created
    %(msecs)d           Millisecond portion of the creation time
    %(relativeCreated)d Time in milliseconds when the LogRecord was created,relative to the time the logging module was loaded (typically at application startup time)
    %(thread)d          Thread ID (if available)
    %(threadName)s      Thread name (if available)
    %(process)d         Process ID (if available)
    %(message)s         The result of record.getMessage(), computed just as the record is emitted
'''