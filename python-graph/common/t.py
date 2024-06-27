import re


a = '江苏省南*执*号xxx文件'
b = r'\*执\*号|法院'

t = re.search(b,a)
print(t)


c = '啊啊啊zz'
print(re.sub(r'[^\u4e00-\u9fa5]','',c))




print('2888.0'.split('.')[0].endswith(('888','2')))


print(tuple(['888,11']))


a = ['888','11']


print('|'.join(a[i] for i in range(len(a))))

