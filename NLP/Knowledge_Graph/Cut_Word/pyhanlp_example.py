#coding=utf-8



import pyhanlp
from pyhanlp import *


text = '张科是来自河北邯郸。周杰伦是一位明星。赵露思是张科喜欢的明星之一。中国是世界强国。我南京智器云科技有限公司工作。南京智器云科技有限公司的ceo是王海波。'
sentence = text.split('。')

for i in range(len(sentence)):

    print("pyhanlp:",HanLP.segment(sentence[i]))


