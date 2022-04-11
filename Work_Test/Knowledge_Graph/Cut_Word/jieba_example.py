#coding=utf-8

import spacy
import jiagu
import jieba
import jieba.posseg as pseg

def postag(text):
    words = pseg.cut(text)
    return words



text = '张科是来自河北邯郸。周杰伦是一位明星。赵露思是张科喜欢的明星之一。中国是世界强国。我南京智器云科技有限公司工作。南京智器云科技有限公司的ceo是王海波。'
text = '关羽的别名叫什么'

sentence = text.split('。')
jieba.add_word("别名",freq='999999',tag='r')

for i in range(len(sentence)):

    word = postag(sentence[i])
    print("jieba:")
    jieba_list = []
    for w in word:
        jieba_list.append([w.flag,w.word])
        # print(w.flag,w.word)
    print(jieba_list)

