'''
python装饰器
通过@xxx语法糖方式，附加到函数头上，调用函数时，会将函数作为参数调用装饰器函数。支持带参数的装饰器，内部逻辑分为构建时、执行时。装饰器在函数构建时完成
其中在函数执行前后一些操作，如：日志记录、参数校验等。常用于以下场景。
    1、业务功能扩展
    2、日志记录、参数校验

使用方法
    装饰器函数每层必须返回，最终返回原函数结果
    1、简单装饰器
        两层结构，最外层为装饰器函数（入参为原函数），里层定义wrapper函数（入参为原函数的入参*args, **kwargs）,
        wrapper函数中，最终返回原函数执行（return fun(*args, **kwargs)）
    2、传参装饰器
        三层结构，最外层为装饰器函数（入参为装饰函数时接收的参数），里面两层同上面逻辑一致  。
'''
from functools import reduce
from typing import Callable

class DefineDecorator:
    @staticmethod
    def recordLog(level: str):
        print(level)
        def decorator(fun: Callable):
            def wrapper(*args, **kwargs):
                print('recordLog记录开始')
                print(f'recordLog在xxx时间xxx秒，调用了{fun.__name__}函数')
                result = fun(*args, **kwargs)
                print('recordLog记录结束')
                return result
            return wrapper
        return decorator

    @staticmethod
    def checkType(tp):
        print(tp)
        def decorator(fun):
            def wrapper(*args, **kwargs):
                for arg in args:
                    if not isinstance(arg, tp):
                        raise TypeError(f'{arg}类型错误')
                else:
                    print('类型校验通过')
                print(f'checkType在xxx时间xxx秒，调用了{fun.__name__}函数')
                return fun(*args, **kwargs)
            return wrapper
        return decorator


# checkType(recordLog(calc))
@DefineDecorator.checkType(int)
@DefineDecorator.recordLog(level='info')
def calc(a: int, b: int) -> int:
    '''
    计算函数
    :param a:
    :param b:
    :return: 返回相加结果
    '''
    print('开始计算')
    return a + b

print('-----------------')
r = calc(3, 4)
print(r)


import math

def printV(v):
    return math.pow(v, 2)


lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
powLista = list(map(lambda x: printV(x), lista))
f50Lista = list(filter(lambda v: v >= 50, powLista))
reduceLista = reduce(lambda x, y: x + y, f50Lista)
# print(reduceLista)

# # py >= 3.8 特有语法
# if (l:= reduceLista) > 244:
#     print('reduceLista大于144')
















