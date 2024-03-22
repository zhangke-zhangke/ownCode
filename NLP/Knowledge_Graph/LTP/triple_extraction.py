#!/usr/bin/env python3
# coding: utf-8
# File: triple_extraction.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-3-12
from NLP.LTP.sentence_parser import *
import re


class TripleExtractor:
    def __init__(self):
        self.parser = LtpParser()

    '''文章分句处理, 切分长句，冒号，分号，感叹号等做切分标识'''

    def split_sents(self, content):
        return [sentence for sentence in re.split(r'[？?！!。；;：:\n\r]', content) if sentence]

    '''利用语义角色标注,直接获取主谓宾三元组,基于A0,A1,A2'''

    def ruler1(self, words, postags, roles_dict, role_index):
        v = words[role_index]
        role_info = roles_dict[role_index]
        if 'A0' in role_info.keys() and 'A1' in role_info.keys():
            s = ''.join([words[word_index] for word_index in range(role_info['A0'][1], role_info['A0'][2] + 1) if
                         postags[word_index][0] not in ['w', 'u', 'x'] and words[word_index]])
            o = ''.join([words[word_index] for word_index in range(role_info['A1'][1], role_info['A1'][2] + 1) if
                         postags[word_index][0] not in ['w', 'u', 'x'] and words[word_index]])
            if s and o:
                return '1', [s, v, o]
        # elif 'A0' in role_info:
        #     s = ''.join([words[word_index] for word_index in range(role_info['A0'][1], role_info['A0'][2] + 1) if
        #                  postags[word_index][0] not in ['w', 'u', 'x']])
        #     if s:
        #         return '2', [s, v]
        # elif 'A1' in role_info:
        #     o = ''.join([words[word_index] for word_index in range(role_info['A1'][1], role_info['A1'][2]+1) if
        #                  postags[word_index][0] not in ['w', 'u', 'x']])
        #     return '3', [v, o]
        return '4', []

    '''三元组抽取主函数'''

    def ruler2(self, words, postags, child_dict_list, arcs, roles_dict):
        svos = []
        for index in range(len(postags)):
            tmp = 1
            # 先借助语义角色标注的结果，进行三元组抽取
            if index in roles_dict:
                flag, triple = self.ruler1(words, postags, roles_dict, index)
                if flag == '1':
                    svos.append(triple)
                    tmp = 0
            if tmp == 1:
                # 如果语义角色标记为空，则使用依存句法进行抽取
                # if postags[index] == 'v':
                if postags[index]:
                    # 抽取以谓词为中心的事实三元组
                    child_dict = child_dict_list[index]
                    # 主谓宾
                    if 'SBV' in child_dict and 'VOB' in child_dict:
                        r = words[index]
                        e1 = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0])
                        e2 = self.complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
                        svos.append([e1, r, e2])

                    # 定语后置，动宾关系
                    relation = arcs[index][0]
                    head = arcs[index][2]
                    if relation == 'ATT':
                        if 'VOB' in child_dict:
                            e1 = self.complete_e(words, postags, child_dict_list, head - 1)
                            r = words[index]
                            e2 = self.complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
                            temp_string = r + e2
                            if temp_string == e1[:len(temp_string)]:
                                e1 = e1[len(temp_string):]
                            if temp_string not in e1:
                                svos.append([e1, r, e2])
                    # 含有介宾关系的主谓动补关系
                    if 'SBV' in child_dict and 'CMP' in child_dict:
                        e1 = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0])
                        cmp_index = child_dict['CMP'][0]
                        r = words[index] + words[cmp_index]
                        if 'POB' in child_dict_list[cmp_index]:
                            e2 = self.complete_e(words, postags, child_dict_list, child_dict_list[cmp_index]['POB'][0])
                            svos.append([e1, r, e2])
        return svos

    '''对找出的主语或者宾语进行扩展'''

    def complete_e(self, words, postags, child_dict_list, word_index):
        child_dict = child_dict_list[word_index]
        prefix = ''
        if 'ATT' in child_dict:
            for i in range(len(child_dict['ATT'])):
                prefix += self.complete_e(words, postags, child_dict_list, child_dict['ATT'][i])
        postfix = ''
        if postags[word_index] == 'v':
            if 'VOB' in child_dict:
                postfix += self.complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
            if 'SBV' in child_dict:
                prefix = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0]) + prefix

        return prefix + words[word_index] + postfix

    '''程序主控函数'''

    def triples_main(self, content):
        sentences = self.split_sents(content)
        svos = []
        for sentence in sentences:
            words, postags, child_dict_list, roles_dict, arcs = self.parser.parser_main(sentence)
            svo = self.ruler2(words, postags, child_dict_list, arcs, roles_dict)
            svos += svo

        return svos


'''测试'''


def test():
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
    extractor = TripleExtractor()
    svos = extractor.triples_main(content2)
    print('svos', svos)


if __name__ == '__main__':
    test()

