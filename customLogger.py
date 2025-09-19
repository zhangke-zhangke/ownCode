import logging
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime


class DailyRotatingLogger:
    def __init__(self, log_dir='logs', log_name='app', keep_days=30):
        self.log_dir = log_dir
        self.log_name = log_name
        self.keep_days = keep_days
        os.makedirs(log_dir, exist_ok=True)

        self.logger = logging.getLogger('DailyRotatingLogger')
        self.logger.setLevel(logging.INFO)

        # 设置按天轮转的handler
        log_file = os.path.join(log_dir, f'{log_name}.log')
        handler = TimedRotatingFileHandler(
            log_file,
            when='midnight',
            interval=1,
            backupCount=keep_days
        )

        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        # 添加控制台输出
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)


    def get_logger(self):
        return self.logger



logger = DailyRotatingLogger().get_logger()


if __name__ == "__main__":
    logger = DailyRotatingLogger().get_logger()
    logger.info("日志系统初始化完成")
    logger.warning("这是一个测试警告")
