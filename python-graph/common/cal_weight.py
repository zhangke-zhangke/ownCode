import sys
from common import *
import re




'''
    初步想法
    计算十个可疑指标，每个指标0.1的权重。每条交易流水满足几个指标就加总权重。
    最终每条流水点边为0-1之间的权重。
    指标针对单条流水
        
    指标清单:
        1、 （20） 夜间大额交易： 交易时间在 22 点到 6 点之间，交易金额>=50000
        2、 （20） 境外交易： 交易 IP 在境外
        3、 （10） 年龄不符： 年龄起止 1930-1950或 2001-2020，交易金额>=100000
        4、 （5）  规避监管： 交易金额 48000-49999
        5、 （10） 向境外汇款或收到境外汇款： 交易来源或去向是境外
        6、 （20） 交易发生地位高风险地区： 交易发生地 CHN65|CHN54|CHN53
        7、 （5）  金额尾数包含特征：交易金额尾数特征为 999|9999
        8、 （20） IP地址为境内高风险地区
        9、 （20） IP地址为境外高风险国家及地区
        10、（20） 交易备注精准匹配：交易备注、摘要精准匹配包含 神仙水|胶囊|聪明药|巧克力
        11、（5）  入向交易金额尾数特征：入向交易金额尾数特征包含 888|8888|880|8800|0000
        12、（15） 收到诉讼执行款： 存在入向交易对手名称包含 人民法院，交易备注中包含 *执*号|案件款|执行款
        13、（15） 代缴律师诉讼费：交易备注中包含 律师费|诉讼费
        14、（20） 存在代理人交易行为，交易代理人不为空
        15、（15） 交易币种非人民币
        16、（20） 交易对手为特殊人员对手名称非中文
        17、（15） 账户余额清零：大额交易(>=5000)后不留余额(<=10)
        18、（20） 交易备注异常：交易备注包含非中文（纯字母、纯数字、特殊符号、组合），备注字符数小于20
        
        
        
        
        -- 第一步
        insert overwrite table bojs_dm.zqy_transflow_info_python
        select 
            *
        from bojs_dm.zqy_transflow_info
        -- 过滤三方及其他无用交易
        where cust_acct_num != cnter_cust_acct_num and cust_name != cnter_cust_name
        and cust_name not regexp ''
        and cnter_cust_name not regexp ''
        
        
        
        
        -- 第二步
        insert overwrite table xxx.zqy_python_graph_edge_weight
        select 
            cust_no
            ,card_no cust_acct_num
            ,cnter_cust_no
            ,cnter_card_no cnter_cust_acct_num
            ,case when tx_time between 60000 and 220000 and tx_amt_rmb >= 50000 then 20 else 0 end -- f1
--                +case when ip_addr in (select ip from xxx) then 20 else 0 end -- f2
--                +case when (age between xxx and xxx or age between xxx and xxx) and tx_amt_rmb >= 100000 then 10 else 0 end -- f3
            +case when tx_amt_rmb between 48000 and 49999 then 5 else 0 end -- f4
            +case when cross_tx_ind = '1' then 10 else 0 end -- f5
            +case when tx_area_code in ('CHN65','CHN54','CHN53') then 20 else 0 end -- f6
            +case when tx_amt_rmb like '%999' or tx_amt_rmb like '%9999' then 5 else 0 end -- f7
--                +case when ip_addr in (select ip from xxx) then 20 else 0 end -- f8
--                +case when ip_addr in (select ip from xxx) then 20 else 0 end -- f9
            +case when concat(comment,tx_abstract) regexp '神仙水|胶囊|聪明药|巧克力' then 20 else 0 end -- f10
            +case when credit_debit_ind = 'D' and (tx_amt_rmb like '%888' or tx_amt_rmb like '%8888' or tx_amt_rmb like '%880' or tx_amt_rmb like '%8800' or tx_amt_rmb like '%0000') then 5 else 0 end -- f11
            +case when credit_debit_ind = 'C' and cnter_cust_name regexp '人民法院' and comment regexp '/*执*号|案件款|执行款' then 15 else 0 end -- f12
            +case when comment regexp '律师费|诉讼费' then 15 else 0 end -- f13
            +case when agent_name is not null and agent_cert_num is not null then 20 else 0 end -- f14
            +case when currency_code not in ('CNY','156') then 15 else 0 end -- f15
            +case when regexp_extract(cnter_cust_name,'[\u4e00-\u9fa5]',0) = '' then 20 else 0 end -- f16 
            +case when tx_amt_rmb >= 5000 and acct_bal <= 10 then 15 else 0 end -- f17
            +case when regexp_extract(comment,'[\u4e00-\u9fa5]',0) = '' and length(comment) < 20 then 20 else 0 end -- f18
                sum_score
        from bojs_dm.zqy_transflow_info_python


'''
# 实现指标计算
class graphWeightCal():
    # 构造函数
    def __init__(self, default_feature_value=0):
        # self.df = df
        self.default_feature_value = default_feature_value

    # 最大最小标准化
    # 负向指标
    def maxmin_n(self,x):
        new_x = (max(x) - x) / (max(x) - min(x))
        return new_x

    # 正向指标
    def maxmin_a(self,x):
        new_x = (x - min(x)) / (max(x) - min(x))
        return new_x

    # 熵权法计算权重
    def ent_w(self,fdf):
        '''
        :param fdf: 特征df
        :return:
        '''
        print(fdf)
        fdf_std = fdf.apply(self.maxmin_a, axis=0)

        print(fdf_std)


    # 模糊匹配多值
    def search_all(self, data, keyword):
        for key in keyword:
            if re.search(key, data):
                return True


    # ==============================================================================================================
    # ==============================================================================================================
    # ==============================================================================================================
    # 特征1
    # （20） 夜间大额交易： 交易时间在 22 点到 6 点之间，交易金额>=50000
    def cal_feature1(self, df):
        int_time = int(str(df['tx_time'])[11:].replace(':', ''))
        if int_time >= 0 and int_time <= r1_trade_start_time and df['tx_amt_rmb'] >= r1_trade_end_time:
            return r1_weight
        else:
            return self.default_feature_value

    # 特征2
    # （20） 境外交易： 交易 IP 在境外
    def cal_feature2(self, df):
        return self.default_feature_value

    # 特征3
    # （10） 年龄不符： 年龄起止 1930-1950或 2001-2020，交易金额>=100000
    def cal_feature3(self, df):
        return self.default_feature_value

    # 特征4
    # （5）  规避监管： 交易金额 48000-49999
    def cal_feature4(self, df):
        if df['tx_amt_rmb'] >= r4_trade_start_money and df['tx_amt_rmb'] <= r4_trade_end_money:
            return r4_weight
        else:
            return self.default_feature_value

    # 特征5
    # （10） 向境外汇款或收到境外汇款： 交易来源或去向是境外
    def cal_feature5(self, df):
        if df['cross_tx_ind'] == 1:
            return r5_weight
        else:
            return self.default_feature_value

    # 特征6
    # （20） 交易发生地位高风险地区： 交易发生地 CHN65|CHN54|CHN53
    def cal_feature6(self, df):
        '''
        :param df: dataframe
        :param r6_trade_area_keyword: list
        :return:  int value
        '''
        if df['tx_area'] in r6_trade_area_keyword:
            return r6_weight
        else:
            return self.default_feature_value

    # 特征7
    # （5）  金额尾数包含特征：交易金额尾数特征为 999|9999
    def cal_feature7(self, df):
        '''
        :param df:
        :param r7_trade_include: list type keyword
        :return:
        '''
        r7_trade_include_new = tuple(r7_trade_include)
        if str(df['tx_amt_rmb']).split('.')[0].endswith(r7_trade_include_new):
            return r7_weight
        else:
            return self.default_feature_value

    # 特征8
    # （20） IP地址为境内高风险地区
    def cal_feature8(self, df):
        return self.default_feature_value

    # 特征9
    # （20） IP地址为境外高风险国家及地区
    def cal_feature9(self, df):
        return self.default_feature_value

    # 特征10
    # （20） 交易备注精准匹配：交易备注、摘要精准匹配包含 神仙水|胶囊|聪明药|巧克力
    def cal_feature10(self, df):
        '''
        :param df:
        :param r10_comment_or_abstract_keyword: list type keywrod
        :return:
        '''
        # if re.search('聪明药|神仙水|巧克力',df['comment']):
        if df['comment'] in r10_comment_or_abstract_keyword \
                or df['tx_abstract'] in r10_comment_or_abstract_keyword:
            return r10_weight
        else:
            return self.default_feature_value

    # 特征11
    # （5）  入向交易金额尾数特征：入向交易金额尾数特征包含 888|8888|880|8800|0000
    def cal_feature11(self, df):
        '''
        :param df:
        :return:
        '''
        r11_in_money_include_new = tuple(r11_in_money_include)
        if df['credit_debit_ind'] == '入' \
                and df['tx_amt_rmb'].split('.')[0].endswith(r11_in_money_include_new):
            return r11_weight
        else:
            return self.default_feature_value

    # 特征12
    # （15） 收到诉讼执行款： 存在入向交易对手名称包含 人民法院，交易备注中包含 *执*号|案件款|执行款
    def cal_feature12(self, df):
        '''
        :param df:
        :return:
        '''
        r12_in_cnter_include_cnter_name_keyword_new = '|'.join(r12_in_cnter_include_cnter_name_keyword[i] for i in
                                                               range(r12_in_cnter_include_cnter_name_keyword.__len__()))
        r12_in_cnter_include_comment_keyword_new = '|'.join(
            r12_in_cnter_include_comment_keyword[i] for i in range(r12_in_cnter_include_comment_keyword.__len__()))
        if df['credit_debit_ind'] == '入' \
                and re.search(r12_in_cnter_include_cnter_name_keyword_new, df['cnter_cust_name']) \
                and re.search(r12_in_cnter_include_comment_keyword_new, df['comment']):
            return r12_weight
        else:
            return self.default_feature_value

    # 特征13
    # （15） 代缴律师诉讼费：交易备注中包含 律师费|诉讼费
    def cal_feature13(self, df):
        r13_include_comment_keyword_new = '|'.join(
            r13_include_comment_keyword[i] for i in range(r13_include_comment_keyword.__len__()))
        if re.search(r13_include_comment_keyword_new, str(df['comment'])):
            return r13_weight
        else:
            return self.default_feature_value

    # 特征14
    # （20） 存在代理人交易行为，交易代理人不为空
    def cal_feature14(self, df):
        if len(df['agent_name'].strip()) != 0:
            return r14_weight
        else:
            return self.default_feature_value

    # 特征15
    # （15） 交易币种非人民币
    def cal_feature15(self, df):
        if df['currency_code'] not in r15_currency_code:
            return r15_weight
        else:
            return self.default_feature_value

    # 特征16
    # （20） 交易对手为特殊人员对手名称非中文
    def cal_feature16(self, df):
        # 匹配中文，取反
        if len(re.sub(r'[^\u4e00-\u9fa5]', '', df['cnter_cust_name'])) == 0:
            return r16_weight
        else:
            return self.default_feature_value

    # 特征17
    # （15） 账户余额清零：大额交易(>=5000)后不留余额(<=10)
    def cal_feature17(self, df):
        if df['tx_amt_rmb'] >= r17_tx_amt_rmb and df['acct_bal'] <= t17_acct_bal:
            return r17_weight
        else:
            return self.default_feature_value

    # 特征18
    # （20） 交易备注异常：交易备注包含非中文（纯字母、纯数字、特殊符号、组合），备注字符数小于20
    def cal_feature18(self, df):
        return self.default_feature_value











