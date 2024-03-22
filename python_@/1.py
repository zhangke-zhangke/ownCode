import time




def count_time(func):
    def wrapper():
        t1 = time.time()
        func()
        print("执行时间为：", time.time() - t1)

    return wrapper

@count_time
def baiyu() -> None:
    print("我是攻城狮白玉")
    time.sleep(2)


if __name__ == '__main__':
    # baiyu = count_time(baiyu)  # 因为装饰器 count_time(baiyu) 返回的时函数对象 wrapper，这条语句相当于  baiyu = wrapper
    # baiyu()  # 执行baiyu()就相当于执行wrapper()


    baiyu()

