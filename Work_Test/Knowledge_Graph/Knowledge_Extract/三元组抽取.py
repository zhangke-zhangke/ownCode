# coding=utf-8
import re, os
import jieba.posseg as pseg
import jieba
import time
from py2neo import Graph, Node, Relationship,NodeMatcher

class ExtractEvent:
    def __init__(self):
        self.map_dict = self.load_mapdict()
        self.minlen = 2
        self.maxlen = 30
        self.keywords_num = 20
        self.limit_score = 10
        self.IP = "(([NERMQ]*P*[ABDP]*)*([ABDV]{1,})*([NERMQ]*)*([VDAB]$)?([NERMQ]*)*([VDAB]$)?)*"
        self.IP = "([NER]*([PMBQADP]*[NER]*)*([VPDA]{1,}[NEBRVMQDA]*)*)"
        self.MQ = '[DP]*M{1,}[Q]*([VN]$)?'
        self.VNP = 'V*N{1,}'
        self.NP = '[NER]{1,}'
        self.REN = 'R{2,}'
        self.VP = 'P?(V|A$|D$){1,}'
        self.PP = 'P?[NERMQ]{1,}'
        self.SPO_n = "n{1,}"
        self.SPO_v = "v{1,}"
        self.stop_tags = {'u', 'wp', 'o', 'y', 'w', 'f', 'u', 'c', 'uj', 'nd', 't', 'x'}
        self.combine_words = {"首先", "然后", "之前", "之后", "其次", "接着"}

    """构建映射字典"""

    def load_mapdict(self):
        tag_dict = {
            'B': 'b'.split(),  # 时间词
            'A': 'a d'.split(),  # 时间词
            'D': "d".split(),  # 限定词
            'N': "n j s zg en l r".split(),  # 名词
            "E": "nt nz ns an ng".split(),  # 实体词
            "R": "nr".split(),  # 人物
            'G': "g".split(),  # 语素
            'V': "vd v va i vg vn g".split(),  # 动词
            'P': "p f".split(),  # 介词
            "M": "m t".split(),  # 数词
            "Q": "q".split(),  # 量词
            "v": "V".split(),  # 动词短语
            "n": "N".split(),  # 名词介宾短语
        }
        map_dict = {}
        for flag, tags in tag_dict.items():
            for tag in tags:
                map_dict[tag] = flag
        return map_dict

    """根据定义的标签,对词性进行标签化"""

    def transfer_tags(self, postags):
        # tags = [self.map_dict.get(tag[:2], 'W') for tag in postags]
        # 在自定义字典里查找postags里每个tag对应的标签，如果没查到则认为是W
        tags = [self.map_dict.get(tag, 'W') for tag in postags]

        return ''.join(tags)

    """抽取出指定长度的ngram"""

    def extract_ngram(self, pos_seq, regex):
        ss = self.transfer_tags(pos_seq)

        def gen():
            for s in range(len(ss)):
                for n in range(self.minlen, 1 + min(self.maxlen, len(ss) - s)):
                    e = s + n
                    substr = ss[s:e]
                    if re.match(regex + "$", substr):
                        yield (s, e)

        return list(gen())

    '''抽取ngram'''

    def extract_sentgram(self, pos_seq, regex):
        ss = self.transfer_tags(pos_seq)

        def gen():
            for m in re.finditer(regex, ss):
                yield (m.start(), m.end())

        return list(gen())

    """指示代词替换，消解处理"""
    #                          词      词性      人名
    def cite_resolution(self, words, postags, persons):
        #print(f"处理词为:{words},词性为:{postags},人名为:{persons}")
        if not persons and 'r' not in set(postags):
            #print("1")
            return words, postags
        elif persons and 'r' in set(postags):
            #print("2")
            cite_index = postags.index('r')
            if words[cite_index] in {"其", "他", "她", "我"}:
                words[cite_index] = persons[-1]
                postags[cite_index] = 'nr'
        elif 'r' in set(postags):
            #("3")
            cite_index = postags.index('r')
            if words[cite_index] in {"为何", "何", "如何"}:
                postags[cite_index] = 'w'
        # 判断首句既有人名又有代词噪声
        drop_r_index = []
        if 'r' and 'nr' in set(postags):
            #print("4")
            for i in range(len(words)):
                if postags[i] == 'r':
                    drop_r_index.append(i)
        for i in drop_r_index:
            del words[i]
            del postags[i]

        return words, postags

    """抽取量词性短语"""

    def extract_mqs(self, wds, postags):
        phrase_tokspans = self.extract_sentgram(postags, self.MQ)
        if not phrase_tokspans:
            return []
        phrases = [''.join(wds[i[0]:i[1]]) for i in phrase_tokspans]
        return phrases

    '''抽取动词性短语'''

    def get_ips(self, wds, postags):
        ips = []
        phrase_tokspans = self.extract_sentgram(postags, self.IP)
        #print(phrase_tokspans)
        if not phrase_tokspans:
            return []
        phrases = [''.join(wds[i[0]:i[1]]) for i in phrase_tokspans]
        phrase_postags = [''.join(postags[i[0]:i[1]]) for i in phrase_tokspans]
        for phrase, phrase_postag_ in zip(phrases, phrase_postags):
            if not phrase:
                continue
            #                                               数词              量词               形容词           时间
            phrase_postags = ''.join(phrase_postag_).replace('m', '').replace('q', '').replace('a', '').replace('t', '')
            #                       名词                              简称略语        startswith用来判断是否以指定字符串开头
            if phrase_postags.startswith('n') or phrase_postags.startswith('j'):
                has_subj = 1
            else:
                has_subj = 0
            ips.append((has_subj, phrase))
        return ips

    """分短句处理"""

    def split_short_sents(self, text):
        return [i for i in re.split(r'[,，]', text) if len(i) > 2]

    """分段落"""

    def split_paras(self, text):
        return [i for i in re.split(r'[\n\r]', text) if len(i) > 4]

    """分长句处理"""

    def split_long_sents(self, text):
        return [i for i in re.split(r'[;。:； ：？?!！【】▲丨|]', text) if len(i) > 4]

    """移出噪声数据"""

    def remove_punc(self, text):
        text = text.replace('\u3000', '').replace("'", '').replace('“', '').replace('”', '').replace('▲', '').replace(
            '” ', "”")
        tmps = re.findall('[\(|（][^\(（\)）]*[\)|）]', text)
        for tmp in tmps:
            text = text.replace(tmp, '')
        return text

    """保持专有名词"""

    def zhuanming(self, text):
        books = re.findall('[<《][^《》]*[》>]', text)
        return books

    """对人物类词语进行修正"""

    def modify_nr(self, wds, postags):
        phrase_tokspans = self.extract_sentgram(postags, self.REN)
        wds_seq = ' '.join(wds)
        pos_seq = ' '.join(postags)
        if not phrase_tokspans:
            return wds, postags
        else:
            wd_phrases = [' '.join(wds[i[0]:i[1]]) for i in phrase_tokspans]
            postag_phrases = [' '.join(postags[i[0]:i[1]]) for i in phrase_tokspans]
            for wd_phrase in wd_phrases:
                tmp = wd_phrase.replace(' ', '')
                wds_seq = wds_seq.replace(wd_phrase, tmp)
            for postag_phrase in postag_phrases:
                pos_seq = pos_seq.replace(postag_phrase, 'nr')
        words = [i for i in wds_seq.split(' ') if i]
        postags = [i for i in pos_seq.split(' ') if i]
        return words, postags

    """对人物类词语进行修正"""

    def modify_duplicate(self, wds, postags, regex, tag):
        phrase_tokspans = self.extract_sentgram(postags, regex)
        wds_seq = ' '.join(wds)
        pos_seq = ' '.join(postags)
        if not phrase_tokspans:
            return wds, postags
        else:
            wd_phrases = [' '.join(wds[i[0]:i[1]]) for i in phrase_tokspans]
            postag_phrases = [' '.join(postags[i[0]:i[1]]) for i in phrase_tokspans]
            for wd_phrase in wd_phrases:
                tmp = wd_phrase.replace(' ', '')
                wds_seq = wds_seq.replace(wd_phrase, tmp)
            for postag_phrase in postag_phrases:
                pos_seq = pos_seq.replace(postag_phrase, tag)
        words = [i for i in wds_seq.split(' ') if i]
        postags = [i for i in pos_seq.split(' ') if i]
        return words, postags

    '''对句子进行分词处理'''

    def cut_wds(self, sent):
        WordList = ["一星四射队", "中科院微电子所", "小聋瞎队", "打完就解散队", "女生1队", "2021年", "5月29日", "糊人不唬人队", "男子队伍", "女子队伍","动车","金融反洗钱"]
        for UserWord in WordList:
            jieba.add_word(UserWord)
        wds = list(pseg.cut(sent))
        postags = [w.flag for w in wds]
        words = [w.word for w in wds]
        return self.modify_nr(words, postags)

    """移除噪声词语"""

    def clean_wds(self, words, postags):
        wds = []
        poss = []
        # for wd, postag in zip(words, postags):
        #     print(postags[0].lower())
        #     if postag[0].lower() in self.stop_tags:
        #         continue
        #     wds.append(wd)
        #     poss.append(postag[:2])
        # return wds, poss
        for i in range(len(words)):
            if postags[i].lower() in self.stop_tags:
                continue
            else:
                wds.append(words[i])
                poss.append(postags[i])
        return wds, poss

    """检测是否成立, 肯定需要包括名词"""

    def check_flag(self, postags):
        if not {"v", 'a', 'i'}.intersection(postags):
            return 0
        return 1

    """识别出人名实体"""

    def detect_person(self, words, postags):
        persons = []
        for wd, postag in zip(words, postags):
            if postag == 'nr':
                persons.append(wd)
        return persons

    """识别出名词性短语"""

    def get_nps(self, wds, postags):
        phrase_tokspans = self.extract_sentgram(postags, self.NP)
        if not phrase_tokspans:
            return [], []
        phrases_np = [''.join(wds[i[0]:i[1]]) for i in phrase_tokspans]
        return phrase_tokspans, phrases_np

    """识别出介宾短语"""

    def get_pps(self, wds, postags):
        phrase_tokspans = self.extract_sentgram(postags, self.PP)
        if not phrase_tokspans:
            return [], []
        phrases_pp = [''.join(wds[i[0]:i[1]]) for i in phrase_tokspans]
        return phrase_tokspans, phrases_pp

    """识别出动词短语"""

    def get_vps(self, wds, postags):
        phrase_tokspans = self.extract_sentgram(postags, self.VP)
        if not phrase_tokspans:
            return [], []
        phrases_vp = [''.join(wds[i[0]:i[1]]) for i in phrase_tokspans]
        return phrase_tokspans, phrases_vp

    """抽取名动词性短语"""

    def get_vnps(self, s):
        wds, postags = self.cut_wds(s)
        if not postags:
            return [], []
        if not (postags[-1].endswith("n") or postags[-1].endswith("l") or postags[-1].endswith("i")):
            return [], []
        phrase_tokspans = self.extract_sentgram(postags, self.VNP)
        if not phrase_tokspans:
            return [], []
        phrases_vnp = [''.join(wds[i[0]:i[1]]) for i in phrase_tokspans]
        phrase_tokspans2 = self.extract_sentgram(postags, self.NP)
        if not phrase_tokspans2:
            return [], []
        phrases_np = [''.join(wds[i[0]:i[1]]) for i in phrase_tokspans2]
        return phrases_vnp, phrases_np

    """提取短语"""

    def phrase_ip(self, content):
        import sys
        #print("原句：\n",content)
        spos = []
        events = []
        # 移除噪声数据
        content = self.remove_punc(content)
        # 分段落
        paras = self.split_paras(content)
        # 遍历循环每个段落
        for para in paras:
            # 将每个段落分割成若干个句子
            long_sents = self.split_long_sents(para)
            # 遍历循环每个句子
            for long_sent in long_sents:
                persons = []
                # 将每个句子进行分割成若干个短句
                short_sents = self.split_short_sents(long_sent)
                # 遍历循环每个短句
                for sent in short_sents:
                    # 分词：words为词；postags为词性
                    words, postags = self.cut_wds(sent)
                    # 人名实体识别
                    person = self.detect_person(words, postags)
                    # 处理代词等指示词语
                    words, postags = self.cite_resolution(words, postags, persons)
                    # 移除停用词
                    words, postags = self.clean_wds(words, postags)
                    ips = self.get_ips(words, postags)
                    #print(ips)
                    persons += person
                    # ips [(n,'分词'),(n,'分词')]
                    for ip in ips:
                    #   ip[1]取(n,'分词')中的分词
                        events.append(ip[1])
                        wds_tmp = []
                        postags_tmp = []
                        # 第二次分词，去除掉噪声、消岐、代词替换后
                        words, postags = self.cut_wds(ip[1])
                        # 识别动词短语
                        verb_tokspans, verbs = self.get_vps(words, postags)
                        #print("识别动词短语：",verb_tokspans,verbs)
                        # 识别出介宾短语
                        pp_tokspans, pps = self.get_pps(words, postags)
                        #print("识别介宾短语：",pp_tokspans,pps)
                        tmp_dict = {str(verb[0]) + str(verb[1]): ['V', verbs[idx]] for idx, verb in
                                    enumerate(verb_tokspans)}
                        #print(tmp_dict)
                        pp_dict = {str(pp[0]) + str(pp[1]): ['N', pps[idx]] for idx, pp in enumerate(pp_tokspans)}
                        #print(pp_dict)
                        tmp_dict.update(pp_dict)
                        #print(tmp_dict)
                        # sys.exit()
                        sort_keys = sorted([int(i) for i in tmp_dict.keys()])
                        for i in sort_keys:
                            if i < 10:
                                i = '0' + str(i)
                            wds_tmp.append(tmp_dict[str(i)][-1])
                            postags_tmp.append(tmp_dict[str(i)][0])
                        wds_tmp, postags_tmp = self.modify_duplicate(wds_tmp, postags_tmp, self.SPO_v, 'V')
                        wds_tmp, postags_tmp = self.modify_duplicate(wds_tmp, postags_tmp, self.SPO_n, 'N')
                        if len(postags_tmp) < 2:
                            continue
                        seg_index = []
                        i = 0
                        for wd, postag in zip(wds_tmp, postags_tmp):
                            if postag == 'V':
                                seg_index.append(i)
                            i += 1
                        spo = []
                        for indx, seg_indx in enumerate(seg_index):
                            if indx == 0:
                                pre_indx = 0
                            else:
                                pre_indx = seg_index[indx - 1]
                            if pre_indx < 0:
                                pre_indx = 0
                            if seg_indx == 0:
                                spo.append(('', wds_tmp[seg_indx], ''.join(wds_tmp[seg_indx + 1:])))
                            elif seg_indx > 0 and indx < 1:
                                spo.append(
                                    (''.join(wds_tmp[:seg_indx]), wds_tmp[seg_indx], ''.join(wds_tmp[seg_indx + 1:])))
                            else:
                                spo.append((''.join(wds_tmp[pre_indx + 1:seg_indx]), wds_tmp[seg_indx],
                                            ''.join(wds_tmp[seg_indx + 1:])))
                        spos += spo

        return events, spos


def del_all_graph(graph):
    #删除节点
    # 图中所有节点及关系都删除
    y = input("请确认是否要删除图库中所有节点及关系（y/n）：")
    if y == 'y':
        graph.delete_all()
        print("已确认删除图库所有节点和关系\n")
    elif y == 'n':
        print("已确认不删除图库所有节点和关系\n")
        pass
    else:
        print("=========请输入正确的提示引导=========\n")
        del_all_graph(graph)



if __name__ == '__main__':
    print("非结构化文本提取可视化程序开始")
    start_time = time.time()

    handler = ExtractEvent()
    start = time.time()
    content1 = """环境很好，位置独立性很强，比较安静很切合店名，半闲居，偷得半日闲。点了比较经典的菜品，味道果然不错！烤乳鸽，超级赞赞赞，脆皮焦香，肉质细嫩，超好吃。艇仔粥料很足，香葱自己添加，很贴心。金钱肚味道不错，不过没有在广州吃的烂，牙口不好的慎点。凤爪很火候很好，推荐。最惊艳的是长寿菜，菜料十足，很新鲜，清淡又不乏味道，而且没有添加调料的味道，搭配的非常不错！"""
    content2 = """近日，一条男子高铁吃泡面被女乘客怒怼的视频引发热议。女子情绪激动，言辞激烈，大声斥责该乘客，称高铁上有规定不能吃泡面，质问其“有公德心吗”“没素质”。视频曝光后，该女子回应称，因自己的孩子对泡面过敏，曾跟这名男子沟通过，但对方执意不听，她才发泄不满，并称男子拍视频上传已侵犯了她的隐私权和名誉权，将采取法律手段。12306客服人员表示，高铁、动车上一般不卖泡面，但没有规定高铁、动车上不能吃泡面。
    高铁属于密封性较强的空间，每名乘客都有维护高铁内秩序，不破坏该空间内空气质量的义务。这也是乘客作为公民应当具备的基本品质。但是，在高铁没有明确禁止食用泡面等食物的背景下，以影响自己或孩子为由阻挠他人食用某种食品并厉声斥责，恐怕也超出了权利边界。当人们在公共场所活动时，不宜过分干涉他人权利，这样才能构建和谐美好的公共秩序。
    一般来说，个人的权利便是他人的义务，任何人不得随意侵犯他人权利，这是每个公民得以正常工作、生活的基本条件。如果权利可以被肆意侵犯而得不到救济，社会将无法运转，人们也没有幸福可言。如西谚所说，“你的权利止于我的鼻尖”，“你可以唱歌，但不能在午夜破坏我的美梦”。无论何种权利，其能够得以行使的前提是不影响他人正常生活，不违反公共利益和公序良俗。超越了这个边界，权利便不再为权利，也就不再受到保护。
    在“男子高铁吃泡面被怒怼”事件中，初一看，吃泡面男子可能侵犯公共场所秩序，被怒怼乃咎由自取，其实不尽然。虽然高铁属于封闭空间，但与禁止食用刺激性食品的地铁不同，高铁运营方虽然不建议食用泡面等刺激性食品，但并未作出禁止性规定。由此可见，即使食用泡面、榴莲、麻辣烫等食物可能产生刺激性味道，让他人不适，但是否食用该食品，依然取决于个人喜好，他人无权随意干涉乃至横加斥责。这也是此事件披露后，很多网友并未一边倒地批评食用泡面的男子，反而认为女乘客不该高声喧哗。
    现代社会，公民的义务一般分为法律义务和道德义务。如果某个行为被确定为法律义务，行为人必须遵守，一旦违反，无论是受害人抑或旁观群众，均有权制止、投诉、举报。违法者既会受到应有惩戒，也会受到道德谴责，积极制止者则属于应受鼓励的见义勇为。如果有人违反道德义务，则应受到道德和舆论谴责，并有可能被追究法律责任。如在公共场所随地吐痰、乱扔垃圾、脱掉鞋子、随意插队等。此时，如果行为人对他人的劝阻置之不理甚至行凶报复，无疑要受到严厉惩戒。
    当然，随着社会的发展，某些道德义务可能上升为法律义务。如之前，很多人对公共场所吸烟不以为然，烟民可以旁若无人地吞云吐雾。现在，要是还有人不识时务地在公共场所吸烟，必然将成为众矢之的。
    再回到“高铁吃泡面”事件，要是随着人们观念的更新，在高铁上不得吃泡面等可能产生刺激性气味的食物逐渐成为共识，或者上升到道德义务或法律义务。斥责、制止他人吃泡面将理直气壮，否则很难摆脱“矫情”，“将自我权利凌驾于他人权利之上”的嫌疑。
    在相关部门并未禁止在高铁上吃泡面的背景下，吃不吃泡面系个人权利或者个人私德，是不违反公共利益的个人正常生活的一部分。如果认为他人吃泡面让自己不适，最好是请求他人配合并加以感谢，而非站在道德制高点强制干预。只有每个人行使权利时不逾越边界，与他人沟通时好好说话，不过分自我地将幸福和舒适凌驾于他人之上，人与人之间才更趋于平等，公共生活才更趋向美好有序。"""

    content7 = """2021年5月29日至6月5日，由中国科学院大学学生会主办，果壳篮球协会协办的中国科学院大学篮球3v3挑战赛圆满落幕，共有来自各个校区的15支男子队伍及4支女子队伍报名参赛。比赛分为两个男子组和女子组两个组别，分小组赛和淘汰赛两个赛段。2021年5月29日，经过一天的紧张较量，女子组所有比赛落下帷幕。随着选手们在场上的一次次精准投篮、巧妙传球，场下喝彩声阵阵。值得一提的是，四支女子队伍中有两支队伍均为校队成员，她们也顺利进入决赛，进行最后的对决，比赛气氛被推向高潮。最终女子组比赛结果如下：“小聋瞎队”获第一名，“打完就解散队”获第二名，“女生1队”获第三名；凭借出色的个人表现，“小聋瞎队”来自中科院微电子所的张雨萌获得MVP（最有价值球员）。2021年6月5日，男子组八强赛在玉泉路校区篮球场拉开帷幕。相较于小组赛，八强赛的比赛更加精彩刺激。参赛队员们在场上积极进攻，全面防守，时而强打内线，时而高举高打，给大家带来了一场场精彩的对决，场下观众喝彩阵阵。经过近2小时的激烈角逐，最终，“一星四射队”和“糊人不唬人队”进入决赛，将进行冠亚军的争夺。中场休息时，来自中国科学院大学WINGS舞社的同学带来了精彩的表演。随着裁判员一声令下，本次3v3篮球赛决赛一触即发。双方球员迅速进入状态。他们默契配合、巧妙进攻，完成了一次又一次精彩的投篮。场外的观众也不甘示弱，一声声喝彩与鼓励响彻球场。最终经过一番激烈的角逐，“一星四射队”以21：15获取本届篮球3v3比赛的冠军。"""
    content8 = '智器云研究院促进员工成长为技术骨干。智器云研究院隶属智器云'
    content5 = '周杰伦其是一位歌手'
    content6 = '''智器云南京信息科技有限公司，大数据时代的福尔摩斯，中国领先的大数据可视化认知分析专家，提供功能强大的数据处理及情报分析工具及平台，并提供高效专业的情报分析服务及培训。
    公司具有多年行业实战经验，拥有资深的情报分析产品专家和分析服务团队，并始终保持与国内外顶尖大学和领先公司的交流合作，自主研发符合中国市场需求和安全态势的大数据分析产品。
    智器云正凭借深厚的技术积累、持续的技术创新、领先的技术优势、以及先进的服务理念，昂首引领整个数据分析行业的高速增长，推动可视化认知分析技术的繁荣发展'''
    content9 = '''反洗钱的制定和实施，对未来中国经济社会的健康有序发展具有重大意义。这主要体现在以下几个方面：一是有利于及时发现和监控洗钱活动，追查并没收犯罪所得，遏制洗钱犯罪及其上游犯罪，维护经济安全和社会稳定；二是有利于消除洗钱行为给金融机构带来的潜在金融风险和法律风险，维护金融安全；三是有利于发现和切断资助犯罪行为的资金来源和渠道，防范新的犯罪行为；四是有利于保护上游犯罪受害人的财产权，维护法律尊严和社会正义；五是有利于参与反洗钱国际合作，维护我国良好的国际形象。'''
    events, spos = handler.phrase_ip(content6)
    spos = [i for i in spos if i[0] and i[2]]

    # 输出提取的所有三元组关系
    print(spos)

    # 初始化图库
    graph = Graph('http://localhost:7474', auth=('neo4j', '123456789'))
    # 确认是否删除图库所有节点
    del_all_graph(graph)

    for word_list in spos:
        # 三元组输出
        print("准备写入图库当前三元组：",word_list)
        # 词性列表
        word_flag = []
        for i in range(len(word_list)):
            # 添加三元组中每项到词典
            jieba.add_word(word_list[i],freq='9999')
            # 对三元组中每个词进行分词
            word = jieba.posseg.cut(word_list[i])
            for i in word:
                # 添加词性
                word_flag.append(i.flag)



        # # 创建节点输出图库

        head = Node(f"{word_flag[0]}", name=f'{word_list[0]}')
        tail = Node(f"{word_flag[2]}", name=f'{word_list[2]}')

        # 匹配查找图库中节点
        matcher = NodeMatcher(graph)
        nodelist = list(matcher.match(f"{word_flag[0]}",name=f'{word_list[0]}'))
        if len(nodelist) > 0:
            # 表示节点存在，不需创建新的节点
            already_header = nodelist[0]  #
            # 可以直接添加关系
            entity = Relationship(already_header, f"{word_list[1]}", tail)
            graph.create(entity)
        else:
            # 表示图库中没有存在当前要写入的节点
            entity = Relationship(head, f"{word_list[1]}", tail)
            # 创建关系
            graph.create(entity)
        print("当前三元组写入结束\n")

    end_time = time.time()
    print(f"非结构化文本提取可视化程序结束，总耗时（秒）：{end_time-start_time}，写入图库节点数据量：{len(spos)}")




