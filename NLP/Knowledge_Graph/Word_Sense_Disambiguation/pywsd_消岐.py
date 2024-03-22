# import pywsd

from pywsd.lesk import simple_lesk   #引入pywsd库
sent = 'I went to the bank to deposit my money'  #设定包含具有多义的词的句子
ambiguous = 'bank'              #设定多义的词语
answer = simple_lesk(sent, ambiguous, pos='n')   #设置answer的参数，将句子与词进行判断
print (answer.definition())         #打印出答案
#
# import wn
# wn.download('own')




