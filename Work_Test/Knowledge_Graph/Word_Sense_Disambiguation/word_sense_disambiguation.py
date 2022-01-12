import os
import jieba
from math import log2

# 读取每个义项的语料
def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = [_.strip() for _ in f.readlines()]
        return lines

# 去掉停用词
def stopwords(wsd_word,sent_words):
    stopwords = [wsd_word, '我', '你', '它', '他', '她', '了', '是', '的', '啊', '谁', '什么','都',\
                 '很', '个', '之', '人', '在', '上', '下', '左', '右', '。', '，', '！', '？']

    sent_cut = []
    for word in sent_words:
        if word not in stopwords:
            sent_cut.append(word)

    return sent_cut


# 抽取语料库中的语料
def extract_word_repository(wsd_words):
    wsd_dict = {}
    # 将语料库中关于火箭的预料全部取出来
    for file in os.listdir('.'):
        for wsd_word in wsd_words:
            if wsd_word in file:
                # 字典格式，键为文件名；值为文件里面的语句
                wsd_dict[file.replace('.txt', '')] = read_file(file)
    return wsd_dict



# 统计每个词语在语料中的TF-IDF以及频数
#                   去停用词后   词库
def count_everyword(sent_cut,wsd_dict):
    # print(sent_cut)
    # print(wsd_dict)
    # tf
    tf_dict = {}
    #   类别     每类句子
    for meaning, sents in wsd_dict.items():
        tf_dict[meaning] = []
        #  每个词
        for word in sent_cut:
            word_count = 0
            # 每个句子
            for sent in sents:
                # 给句子分词
                example = list(jieba.cut(sent, cut_all=False))
                # 计算每个词在句子中出现的频率
                word_count += example.count(word)

            if word_count:
                tf_dict[meaning].append((word, word_count))
    # idf
    idf_dict = {}
    #  每个词
    for word in sent_cut:
        document_count = 0
        #    类别    每类句子
        for meaning, sents in wsd_dict.items():
            #  每个句子   每类句子
            for sent in sents:
                #  每个词   句子
                if word in sent:
                    document_count += 1

        idf_dict[word] = document_count
    return tf_dict,idf_dict


# 总文档数
def total_docx_count(wsd_dict):
    total_document = 0
    for meaning, sents in wsd_dict.items():
        total_document += len(sents)

    return total_document


# 计算tf_idf值
#                  每个类别词频数  总频数      总文档数
def calculate_tf_idf(tf_dict,idf_dict,total_document):
    mean_tf_idf = []
    #  类别  在此类的所有词和词频
    for k, v in tf_dict.items():
        print(k+':')
        tf_idf_sum = 0
        #  元组（词，频）
        for item in v:
            # item[0]为词
            word = item[0]
            # item[1]为词频
            tf = item[1]
            # tf-idf = tf*log(总文档数/(1+词的频数))
            tf_idf = item[1]*log2(total_document/(1+idf_dict[word]))
            tf_idf_sum += tf_idf
            print('%s, 频数为: %s, TF-IDF值为: %s'% (word, tf, tf_idf))

        mean_tf_idf.append((k, tf_idf_sum))

    # 以频率降序排序
    sort_array = sorted(mean_tf_idf, key=lambda x:x[1], reverse=True)
    true_meaning = sort_array[0][0].split('_')[1]
    print('\n经过词义消岐，%s在该句子中的意思为 %s .' % (wsd_word, true_meaning))





if __name__ == '__main__':
    # 对示例句子分词
    sent = '赛季初的时候，火箭是众望所归的西部决赛球队。'
    # sent = '周杰伦发明了火箭'
    wsd_word = '火箭'

    jieba.add_word(wsd_word)
    sent_words = list(jieba.cut(sent, cut_all=False))
    # print("原句经jieba分词后：",sent_words)

    # 去停用词后
    stopwords_after = stopwords(sent_words,sent_words)
    # print("原句去停用词后：", stopwords_after)

    # 获得语料库
    word_repository = extract_word_repository(sent_words)
    # print("不同词义对应的语料库为：",word_repository)

    # 统计去停用词后剩余词的词频
    tf_count,idf_count = count_everyword(stopwords_after,word_repository)
    # print(tf_count)
    # print(idf_count)

    # 总文档数
    total_document = total_docx_count(word_repository)
    # print(total_document)

    # 计算tf-idf以确定最终词义
    calculate_tf_idf(tf_count,idf_count,total_document)

