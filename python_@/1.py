import time




def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        print(f'{func.__name__} executed in {end_time - start_time} seconds')
        return result
    return wrapper




@timer
def my_function(*args,**kwargs):
    print('Function executed')
    time.sleep(2)
    print(args)
    for arg in args:
        print(arg)
    print(kwargs)
    for key,value in kwargs.items():
        print(key,value)

import numpy
my_function(2,1,0,name='aaa')