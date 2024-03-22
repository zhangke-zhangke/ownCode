import jieba.posseg as pseg


text = '反洗钱职能部门是国家职能部门'
# text = '张科生于河北邯郸'

def postag(text):
    words = pseg.cut(text)
    return words

# 将句子以句号分割
sentence = text.split('。')
print(sentence)

# 对每个句子进行解析
for i in range(len(sentence)):
    print("处理第{}个句子".format(i+1))
    word = postag(sentence[i])

    # 定义词性列表
    nr = []     #
    v = []
    m = []
    p = []
    ns = []

    # 定义用来记录词性个数
    word_speech_count = {}
    # 三元组关系提取表
    relation = []
    for k in word:
        print("词性和词语：",k.flag,k.word)
        word_speech_count[k.flag] = k.word
        if k.flag == 'nr':
            nr.append(k.word)
        elif k.flag == 'v':
            v.append(k.word)
        elif k.flag == 'm':
            m.append(k.word)
        elif k.flag == 'p':
            v.append(k.word)
        elif k.flag == 'ns':
            m.append(k.word)

    nr_str = ''.join(nr)
    v_str = ''.join(v)
    m_str = ''.join(m)
    p_str = ''.join(p)
    ns_str = ''.join(ns)

    relation.append([nr_str, v_str, m_str])
    relation.append([nr_str, v_str, m_str])
    relation.append([nr_str, v_str, m_str])

    # 按照人为主观组成三元组
    # if len(word_speech_count) == 3:
    #     relation.append([nr_str,v_str,m_str])
    # else:
    #     relation.append([nr_str,v_str,m_str])c


    print("经处理，关系三元组如下所示：",relation)


    # # 调用第三方库从百度百科知识图谱查找
    # knowledge = jiagu.knowledge(text)
    # print(knowledge)


#    常用词性及词性表示字母
'''
    动词          v
    形容词         a
    副词          d
    名词          n
    数词          m
    人名          nr
    地名          ns
    介词          p
    时间词         t
'''








