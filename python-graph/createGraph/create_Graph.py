import networkx as nx
from sqlalchemy import and_,or_,text
from createGraph import orm_session as orm
from createGraph import hive_data
import pandas as pd
from flask import request,Blueprint,jsonify,redirect,url_for,current_app
from flask import after_this_request
from common.cal_weight import graphWeightCal
import json



# 蓝图
creat_graph = Blueprint('creat_graph',__name__)
'''
    to do : create nx.graph
    step:
        1、get_data
        2、add_weight
        3、creat_nx_graph
'''



@creat_graph.route('/getData',methods=['get','post'])
def get_data():
    # orm query result ——> type list
    result = orm.session.query(
        hive_data.hivedata.cust_name.label('cust_name'),
        hive_data.hivedata.cust_cert.label('cert_no'),
        hive_data.hivedata.card_no.label('card_no'),
        hive_data.hivedata.cnter_cust_name.label('cnter_cust_name'),
        hive_data.hivedata.cnter_cert_no.label('cnter_cert_no'),
        hive_data.hivedata.cnter_card_no.label('cnter_card_no'),
        hive_data.hivedata.tx_type.label('tx_type'),
        hive_data.hivedata.credit_debit_ind.label('credit_debit_ind'),
        hive_data.hivedata.currency_code.label('currency_code'),
        hive_data.hivedata.tx_amt_rmb.label('tx_amt_rmb'),
        hive_data.hivedata.acct_bal.label('acct_bal'),
        hive_data.hivedata.tx_time.label('tx_time'),
        hive_data.hivedata.tx_abstract.label('tx_abstract'),
        hive_data.hivedata.ip_addr.label('ip_addr'),
        hive_data.hivedata.cross_tx_ind.label('cross_tx_ind'),
        hive_data.hivedata.comment.label('comment'),
    ).filter(
        and_(
            hive_data.hivedata.card_no.isnot(None),
            hive_data.hivedata.card_no != '',
            hive_data.hivedata.cnter_card_no != None,
            hive_data.hivedata.cnter_card_no != '',
            text("cust_name not regexp '公司|有限'"),
            text(
                "cnter_cust_name not regexp '财付通|支付宝|淘宝|钱袋宝|钱宝科技|宝付网络科技|通行宝|合众易宝|支付|备付金|天翼|银联|网联|网银在线|平安付|易智付|京东商城|特约|内部户|待清算|清算款|资金清算|清算资金|清算回款|清算户|清算过账|清算专户|清算专用|结算|代收|代付|代发|代扣|批量|汇款|收入|收款|付款|过渡|专用|暂收|暂挂|暂存|挂账|账号|服务费|赎回账户|清盘账户|终止账户|发放账户|BGL账户|往来账户|他行账户|企业贷账户|中间账户|内部账户|放款账户|发放账户|垫款账户|账户黄金户|账户白银户|账户管理|商户|专户|专项|款项|在途资金|资金归集|结算资金|资金管理|交易资金|划转资金|资金监管|信用卡|还款|银行|人寿保险|财产保险|健康保险|社会保险|医疗保险|证券|基金|理财产品|产品实时|产品本金|产品收益|产品开通|政企账户|法院|诉讼|税务|财政|公积金|江苏苏电|国网|高速通行费|美团'")
        )
    ).limit(100000)
    result_df = pd.DataFrame(result)
    result_df = result_df.apply(pd.to_numeric,errors='ignore')


    @after_this_request
    def orm_session(response):
        current_app.logger.info('销毁数据库连接！')
        # 查询也可以不commit，会自动rollback
        orm.session.commit()
        # 关闭链接，亦可使用session.remove()，它将回收该链接
        orm.session.close()

        return response



    current_app.logger.info('get_data执行完成')

    return jsonify(result_df.to_dict())





@creat_graph.route('/addWeight',methods=['get','post'])
def add_weight(sqlDf):
    '''
    :param df: 待计算指标
    :return: add feature columns to df
    '''

    # 实例化计算指标类
    cal = graphWeightCal()

    sqlDf['feature1'] = sqlDf.apply(cal.cal_feature1,axis=1)
    sqlDf['feature2'] = sqlDf.apply(cal.cal_feature2,axis=1)
    sqlDf['feature3'] = sqlDf.apply(cal.cal_feature3,axis=1)
    sqlDf['feature4'] = sqlDf.apply(cal.cal_feature4,axis=1)
    sqlDf['feature5'] = sqlDf.apply(cal.cal_feature5,axis=1)
    # sqlDf['feature6'] = sqlDf.apply(cal.cal_feature6,axis=1)
    sqlDf['feature7'] = sqlDf.apply(cal.cal_feature7,axis=1)
    sqlDf['feature8'] = sqlDf.apply(cal.cal_feature8,axis=1)
    sqlDf['feature9'] = sqlDf.apply(cal.cal_feature9,axis=1)
    sqlDf['feature10'] = sqlDf.apply(cal.cal_feature10,axis=1)
    sqlDf['feature11'] = sqlDf.apply(cal.cal_feature11,axis=1)
    sqlDf['feature12'] = sqlDf.apply(cal.cal_feature12,axis=1)
    sqlDf['feature13'] = sqlDf.apply(cal.cal_feature13,axis=1)
    # sqlDf['feature14'] = sqlDf.apply(cal.cal_feature14,axis=1)
    sqlDf['feature15'] = sqlDf.apply(cal.cal_feature15,axis=1)
    sqlDf['feature16'] = sqlDf.apply(cal.cal_feature16,axis=1)
    sqlDf['feature17'] = sqlDf.apply(cal.cal_feature17,axis=1)
    sqlDf['feature18'] = sqlDf.apply(cal.cal_feature18,axis=1)

    # 将所有特征类的字段拿出来加总为权重
    feature_columns = [column for column in sqlDf.columns if column.startswith('feature')]
    sqlDf['weight'] = cal.maxmin_a(sqlDf[feature_columns].values.sum(axis=1))
    weight_count_info = sqlDf['weight'].value_counts()
    current_app.logger.info(f'权重结果信息展示：\n{weight_count_info}')

    # 删除权重小于 xxx 的数据
    sqlDf.drop(sqlDf[sqlDf['weight'] <= 0.3].index,inplace=True)

    # # 调用熵权法计算权重
    # sqlDf['weight'] = ent_w(sqlDf[feature_columns])


    current_app.logger.info('add_weight执行完成')


    return jsonify(sqlDf.to_dict())




@creat_graph.route('/creatNxGraph',methods=['get','post'])
def creat_nx_graph(df):
    '''
    :param df:
    :return:
    '''


    # dataframe to graph         nx.MultiDiGraph
    G = nx.from_pandas_edgelist(df, source='card_no', target='cnter_card_no', edge_attr='weight', create_using=nx.MultiDiGraph())
    current_app.logger.info(f'入图成功，图对象信息：{G}')


    # 过滤度小于2的点，减小数据量
    # remove = [node for node, degree in dict(G.degree()).items() if degree < 5]
    # G.remove_nodes_from(remove)
    # print(G)


    # 设置边属性
    node_attributes = {}
    for node,attributes in df.iterrows():
        df_dict = dict(attributes)
        node_attributes[df_dict.get('查询卡号')] = {key:df_dict.get(key) for key in ['客户名称']}
        node_attributes[df_dict.get('交易对方卡号')] = {key:df_dict.get(key) for key in ['交易对方名称']}
    nx.set_node_attributes(G,node_attributes)
    current_app.logger.info('create_nx_graph执行完成')



    return G



