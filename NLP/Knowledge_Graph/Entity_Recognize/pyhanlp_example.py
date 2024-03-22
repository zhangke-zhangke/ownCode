# HanLP1.7.7版本
from pyhanlp import *
from collections import Counter

with open("doc.txt", "r", encoding="utf-8") as f:
    txt = f.read()

    # 中国人名识别
    # nlp = HanLP.newSegment().enableNameRecognize(True)
    # [张科/nr, 是/vshi, 来自/v, 河北/ns, 邯郸/ns, 。/w, 周杰伦/nr, 是/vshi, 一/m, 位/q, 明星/nnd, 。/w, 赵露思/nr, 是/vshi, 张科/nr, 喜欢/vi, 的/ude1, 明星/nnd, 之一/rz, 。/w, 中国/ns, 是/vshi, 世界/n, 强国/n, 。/w]

    # 地名识别
    # nlp = HanLP.newSegment().enablePlaceRecognize(True)
    # [张科/nr, 是/vshi, 来自/v, 河北/ns, 邯郸/ns, 。/w, 周杰伦/nr, 是/vshi, 一/m, 位/q, 明星/nnd, 。/w, 赵露思/nr, 是/vshi, 张科/nr, 喜欢/vi, 的/ude1, 明星/nnd, 之一/rz, 。/w, 中国/ns, 是/vshi, 世界/n, 强国/n, 。/w]

    # 机构名识别
    nlp = HanLP.newSegment().enableOrganizationRecognize(True)
    #[张科/nr, 是/vshi, 来自/v, 河北/ns, 邯郸/ns, 。/w, 周杰伦/nr, 是/vshi, 一/m, 位/q, 明星/nnd, 。/w, 赵露思/nr, 是/vshi, 张科/nr, 喜欢/vi, 的/ude1, 明星/nnd, 之一/rz, 。/w, 中国/ns, 是/vshi, 世界/n, 强国/n, 。/w]

    doc = nlp.seg(txt)
    # doc = postag(txt)
    print("原句分词：",doc)
    c = Counter()

    entity = []
    for w in doc:
        if w.toString().find("nt") >= 0:
            ww = w.toString()
            entity.append(ww.split('/')[0])
    for w in doc:
        if w.toString().find("nr") >= 0:
            ww = w.toString()
            entity.append(ww.split('/')[0])
    for w in doc:
        if w.toString().find("ntc") >= 0:
            ww = w.toString()
            entity.append(ww.split('/')[0])
    print("识别实体：",entity)
    # for i in entity:
    #     name = i.split("/")[0]
    #     c[name] += 1
    # print(c.most_common(50))



# import pyhanlp
# text = '杨超越在1998年7月31日出生于江苏省盐城市大丰区。'
# NLPTokenizer = pyhanlp.JClass('com.hankcs.hanlp.tokenizer.NLPTokenizer')
# NER = NLPTokenizer.segment(text)
# print(NER)
#








