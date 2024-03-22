from sklearn.feature_extraction.text import TfidfTransformer,CountVectorizer

corpus=["我 来到 北京 清华大学",
    "他 来到 了 网易 杭研 大厦",
    "小明 硕士 毕业 与 中国 科学院",
    "我 爱 北京 天安门"]
vectorizer=CountVectorizer()         #该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
transformer=TfidfTransformer()       #该类会统计每个词语的tf-idf权值
X=vectorizer.fit_transform(corpus)   #将文本转为词频矩阵
print(X)
tfidf=transformer.fit_transform(X)   #计算tf-idf，
word=vectorizer.get_feature_names()  #获取词袋模型中的所有词语
weight=tfidf.toarray()               #将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重

for i in range(len(weight)):         #打印每类文本的tf-idf词语权重
    print(list(zip(word,weight[i])))
    # print(list([word, weight[i]]))





# ================================================================================================








from sklearn.feature_extraction.text import TfidfTransformer,CountVectorizer

text = [
        "TF-IDF的主要思想是：如果某个词或短语在一篇文章中出现的频率TF高，并且在其他文章中很少出现，则认为此词或者短语具有很好的类别区分能力，适合用来分类。"
        ]

# 词向量模型
vector_model = CountVectorizer()
# tf-idf算法
tfidf_model = TfidfTransformer()

#　文本转向量
text_vector = vector_model.fit_transform(text)

# 提取文本中的词语
word = vector_model.get_feature_names()

# 计算ti-idf值
tfidf_count = tfidf_model.fit_transform(text_vector)
# 对应的ti-idf权重
tfidf_weight = tfidf_count.toarray()

for i in range(len(tfidf_weight)):         #每本的tf-idf词权重
    print(list(zip(word,tfidf_weight[i])))
    # print(list([word, weight[i]]))







# ===============================================================================================




# 利用搜狐新闻语料库计算每个词语的idf值，
# -*-coding:utf-8-*-
import numpy as np
import math
from collections import defaultdict

doc_num = 0
doc_frequency = defaultdict(int)
with open('sohu_train.txt', encoding='utf-8') as trainText:
    for line in trainText:
        id, catgre, body = line.split('^_^')
        # if doc_num>100000:break
        doc_num += 1
        for word in set(body.split('    ')):
            word = word.replace('\n', '').strip()
            # if word in stopword :continue
            if word == '' or word == '': continue
            doc_frequency[word] += 1

fw = open('idf-1.txt', 'w', encoding='utf-8')
for word in doc_frequency:
    idf = math.log(doc_num / (doc_frequency[word] + 1))
    fw.write(word + ' ' + str(idf) + '\n')
    print(word, doc_frequency[word])
fw.close()
print('procesing completed')

# 加载已经训练好的idf值，计算部分文章的tfidf，返回相应关键词
idf_dict = defaultdict(int)
with open('idf-1.txt', encoding='utf-8') as idf_dict_text:
    for line in idf_dict_text:
        word, value = line.split(' ')
        idf_dict[word] = float(value)

doc_num = 0
with open('sohu_train.txt', encoding='utf-8') as trainText:
    for line in trainText:
        id, catgre, body = line.split('^_^')
        # 仅抽取前5篇文档的关键词
        if doc_num > 5:
            break
        else:
            doc_num += 1
        word_num = 0
        word_frequency = defaultdict(int)
        for word in body.split('    '):  # 每篇文档中词频统计
            word = word.replace('\n', '').strip()
            if word == '' or word == '': continue
            word_frequency[word] += 1
            word_num += 1

        for word in word_frequency:  # 计算当前文章中每个词的tfidf值
            # print(idf_dict[word],type(idf_dict[word]))
            tfidf = idf_dict[word] * word_frequency[word] / word_num
            word_frequency[word] = tfidf
        word_sorted = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)
        print('document:', body.strip().replace('    ', ''))
        print('keywords:', word_sorted[:5])