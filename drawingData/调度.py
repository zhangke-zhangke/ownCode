import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import os



# 初始化调度器
sched = BlockingScheduler()

# 具体任务函数
def task():
    print(f'function start at {datetime.datetime.now()}')
    os.system('python xxx.py')


#            任务函数  触发间隔    触发事件     最大并行任务数
sched.add_job(task,'interval',minutes=5,max_instances=10)
sched.start()













