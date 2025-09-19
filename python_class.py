



class T:

    _fit = None
    _ent = None

    def __init__(self, fit, ent):
        self._fit = fit
        self._ent = ent

    @property
    def fit(self):
        return self._fit

    @fit.setter
    def fit(self, value):
        self._fit = value


t = T(1, 2)
# 调用fit的setter方法
t.fit = 3
# 调用fit的getter方法（@property会隐式创建一个xxx的getter方法，使用效果同@xxx.getter等价）
print(t.fit)
