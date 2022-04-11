import pymysql
import pandas as pd
import sys
import pickle
import pymysql
from sklearn.externals import joblib
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split, cross_val_predict
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn import  metrics
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, roc_auc_score, plot_roc_curve, \
    SCORERS,recall_score,precision_score
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import MinMaxScaler, normalize
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from imblearn.over_sampling import RandomOverSampler, SMOTE  # 随机采样函数 和SMOTE过采样函数
from imblearn.under_sampling import RandomUnderSampler  # 随机采样函数 和SMOTE过采样函数
from imblearn.combine import SMOTETomek
from sklearn.neighbors import KNeighborsClassifier
import xgboost
from flaml import AutoML
import sys
from matplotlib import pyplot as plt
from sklearn.tree import DecisionTreeClassifier

plt.rcParams['font.sans-serif'] = ['SimHei']  # 在图中正确显示中文
plt.rcParams['axes.unicode_minus'] = False  # 默认是使用Unicode负号，设置正常显示字符，如正常显示负号


def get_enginen():
    engine = create_engine('mysql+pymysql://root:123456@172.30.6.5:3306/financeData?charset=utf8')
    return engine


def save_model_file(model, save_model_name):
    joblib.dump(model, save_model_name)


def use_model_file(model_name):
    model = joblib.load(model_name)
    return model


def train(data,target):
    # 随机采样
    f = RandomOverSampler(random_state=0)
    # f = SMOTETomek(sampling_strategy={1:500 },random_state=0)
    # f = RandomUnderSampler(sampling_strategy={1:1000},random_state=0)
    # f = SMOTE()

    data, target = f.fit_resample(data, target)
    print(target.to_frame().value_counts())

    test_x = data
    test_y = target
    m = MinMaxScaler()
    test_x = m.fit_transform(test_x)

    # # xgboost
    # xgb = xgboost.XGBRFClassifier(learning_rate=0.5, subsample=0.9)
    # xgb.fit(test_x, test_y)
    # # lr
    # lr = LogisticRegression(penalty='l1', solver='liblinear', C=6.0, max_iter=5000, class_weight='balanced',
    #                         random_state=0)
    # lr.fit(test_x, test_y)
    # # svm
    # svm = SVC(class_weight='balanced', probability=True)
    # svm.fit(test_x, test_y)
    # # tree
    # tree = DecisionTreeClassifier(max_depth=1, class_weight='balanced')
    # tree.fit(test_x, test_y)
    # # 集成学习lr
    # adaboost_lr = AdaBoostClassifier(LogisticRegression(C=0.1, max_iter=5000, class_weight='balanced', random_state=0))
    # adaboost_lr.fit(test_x, test_y)
    # # 集成学习tree
    # adaboost_tree = AdaBoostClassifier(DecisionTreeClassifier(max_depth=1))
    # adaboost_tree.fit(test_x, test_y)

    # # knn
    # knn_params = {
    #     'n_neighbors' : [1,3,5,7,9],
    #     'p' : [1,2],
    #     'weights': ['uniform', 'distance']
    # }
    # knn_params_search = GridSearchCV(KNeighborsClassifier(),param_grid=knn_params,cv=5,scoring='f1').fit(test_x,test_y)
    # print("knn最优参数:",knn_params_search.best_params_)
    # knn = KNeighborsClassifier(**knn_params_search.best_params_)
    # knn.fit(test_x, test_y)
    # print("knn训练",knn.score(test_x,test_y))

    # # 随机森林
    # random_t = RandomForestClassifier()
    # random_t.fit(test_x, test_y)


    # automl
    automl = AutoML()
    automl.fit(test_x,test_y)


    # save_model_file(svm, 'public\\svm.pkl')
    # save_model_file(tree, 'public\\tree.pkl')
    # save_model_file(lr, 'public\\lr.pkl')
    # save_model_file(xgb, 'public\\xgb.pkl')
    # save_model_file(adaboost_lr, 'public\\adaboost_lr.pkl')
    # save_model_file(adaboost_tree, 'public\\adaboost_tree.pkl')
    # save_model_file(knn, 'public\\knn.pkl')
    # save_model_file(knn, 'public\\knn.pkl')
    # save_model_file(random_t, 'public\\random_t.pkl')
    save_model_file(automl, 'FLAML\\automl.pkl')


def test(data,target):
    global auc
    test_x = data
    test_y = target
    m = MinMaxScaler()
    test_x = m.fit_transform(test_x)

    # # xgboost
    # print("=========================xgboost===================================")
    # xgb = use_model_file('public\\xgb.pkl')
    # test_pre = xgb.predict(test_x)
    # print("分数：", xgb.score(test_x, test_y))
    # print("混淆矩阵:\n", confusion_matrix(test_y, test_pre))
    # print("分类报告:\n", classification_report(test_y, test_pre))
    # pre_to_one = xgb.predict_proba(test_x)[:, 1]
    # fpr, tpr, thresholds = roc_curve(test_y, pre_to_one)
    # print("xgb_ks", max(tpr - fpr))
    # auc = metrics.auc(fpr, tpr)
    # print("xgb_auc: ", auc)
    #
    #
    #
    # # lr
    # print("=========================lr===================================")
    # lr = use_model_file('public\\lr.pkl')
    # test_pre = lr.predict(test_x)
    # print("分数：", lr.score(test_x, test_y))
    # print("混淆矩阵:\n", confusion_matrix(test_y, test_pre))
    # print("分类报告:\n", classification_report(test_y, test_pre))
    # pre_to_one = lr.predict_proba(test_x)[:, 1]
    # fpr, tpr, thresholds = roc_curve(test_y, pre_to_one)
    # print("lr_ks", max(tpr - fpr))
    # auc = metrics.auc(fpr, tpr)
    # print("lr_auc: ", auc)
    #
    #
    # # svm
    # print("=========================svm===================================")
    # svm = use_model_file('public\\svm.pkl')
    # test_pre = svm.predict(test_x)
    # print("分数：", svm.score(test_x, test_y))
    # print("混淆矩阵:\n", confusion_matrix(test_y, test_pre))
    # print("分类报告:\n", classification_report(test_y, test_pre))
    # pre_to_one = svm.predict_proba(test_x)[:, 1]
    # fpr, tpr, thresholds = roc_curve(test_y, pre_to_one)
    # print("svm_ks", max(tpr - fpr))
    # auc = metrics.auc(fpr, tpr)
    # print("svm_auc: ", auc)
    #
    #
    # # tree
    # print("=========================tree===================================")
    # tree = use_model_file('public\\tree.pkl')
    # test_pre = tree.predict(test_x)
    # print("分数：", tree.score(test_x, test_y))
    # print("混淆矩阵:\n", confusion_matrix(test_y, test_pre))
    # print("分类报告:\n", classification_report(test_y, test_pre))
    # pre_to_one = tree.predict_proba(test_x)[:, 1]
    # fpr, tpr, thresholds = roc_curve(test_y, pre_to_one)
    # print("tree_ks", max(tpr - fpr))
    # auc = metrics.auc(fpr, tpr)
    # print("tree_auc: ", auc)
    #
    #
    #
    # # 集成学习lr
    # print("=========================集成学习lr===================================")
    # adaboost_lr = use_model_file('public\\adaboost_lr.pkl')
    # test_pre = adaboost_lr.predict(test_x)
    # print("分数：", adaboost_lr.score(test_x, test_y))
    # print("混淆矩阵:\n", confusion_matrix(test_y, test_pre))
    # print("分类报告:\n", classification_report(test_y, test_pre))
    # pre_to_one = adaboost_lr.predict_proba(test_x)[:, 1]
    # fpr, tpr, thresholds = roc_curve(test_y, pre_to_one)
    # print("adaboost_lr_ks", max(tpr - fpr))
    # auc = metrics.auc(fpr, tpr)
    # print("adaboost_lr_auc: ", auc)
    #
    #
    # # 集成学习tree
    # print("=========================集成学习tree===================================")
    # adaboost_tree = use_model_file('public\\adaboost_tree.pkl')
    # test_pre = adaboost_tree.predict(test_x)
    # print("分数：", adaboost_tree.score(test_x, test_y))
    # print("混淆矩阵:\n", confusion_matrix(test_y, test_pre))
    # print("分类报告:\n", classification_report(test_y, test_pre))
    # pre_to_one = adaboost_tree.predict_proba(test_x)[:, 1]
    # fpr, tpr, thresholds = roc_curve(test_y, pre_to_one)
    # print("adaboost_tree_ks", max(tpr - fpr))
    # auc = metrics.auc(fpr, tpr)
    # print("adaboost_tree_auc: ", auc)


    # # knn
    # print("=========================knn===================================")
    # knn = use_model_file('public\\knn.pkl')
    # print(test_x.shape)
    # test_pre = knn.predict(test_x)
    # print("分数：", knn.score(test_x, test_y))
    # print("混淆矩阵:\n", confusion_matrix(test_y, test_pre))
    # print("分类报告:\n", classification_report(test_y, test_pre))
    #
    # pre_to_one = knn.predict_proba(test_x)[:, 1]
    # fpr, tpr, thresholds = roc_curve(test_y, pre_to_one)
    # print("knn_ks", max(tpr - fpr))
    # auc = metrics.auc(fpr, tpr)
    # print("knn_auc: ", auc)


    # # 随机森林
    # print("=========================随机森林===================================")
    # random_t = use_model_file('public\\random_t.pkl')
    # test_pre = random_t.predict(test_x)
    # print("分数：", random_t.score(test_x, test_y))
    # print("混淆矩阵:\n", confusion_matrix(test_y, test_pre))
    # print("分类报告:\n", classification_report(test_y, test_pre))
    # pre_to_one = random_t.predict_proba(test_x)[:, 1]
    # fpr, tpr, thresholds = roc_curve(test_y, pre_to_one)
    # print("random_t_ks", max(tpr - fpr))
    # auc = metrics.auc(fpr, tpr)
    # print("random_t_auc: ", auc)


    # flaml自动化建模
    print("=========================随机森林===================================")
    automl = use_model_file('FLAML\\automl.pkl')
    test_pre = automl.predict(test_x)
    print("混淆矩阵:\n", confusion_matrix(test_y, test_pre))
    print("分类报告:\n", classification_report(test_y, test_pre))
    pre_to_one = automl.predict_proba(test_x)[:, 1]
    fpr, tpr, thresholds = roc_curve(test_y, pre_to_one)
    print("automl_ks", max(tpr - fpr))
    auc = metrics.auc(fpr, tpr)
    print("automl_auc: ", auc)

'''
                交易天数,
                交易对手总账户数,
                交易总笔数,
                交易总金额,
                交易月数,
                借贷账户比,
                借贷金额比,
                入向交易对手账户数,
                入向交易笔数,
                出向交易对手账户数,
                出向交易笔数,
                对公对私标志,
                对手为个人交易金额,
                对手为个人账户数,

                最大单笔交易金额,
                最大月交易天数,
                最大月交易总金额,
                最大月交易笔数,
'''
'''
                交易天数,
                交易总金额,
                交易月数,
                最大月交易总金额,
                最大月交易总金额 / 交易总金额 as '交易集中在单月',
				日终余额小的天数 / 交易天数 as '日终余额小的占比',
				日终余额小的天数,

'''


if __name__ == '__main__':
    connection = pymysql.connect(host='172.30.6.204', user='root', password='123456', database='financeML',
                                 port=int(3306))
    try:
        with connection.cursor() as cursor:
            # sql = '''
            #     SELECT
            #     客户名称,
            #     客户编号,
            #     客户账号,
            #
            #     交易天数,
            #     交易对手总账户数,
            #     交易总笔数,
            #     交易总金额,
            #     交易月数,
            #     借贷账户比,
            #     借贷金额比,
            #     入向交易对手账户数,
            #     入向交易笔数,
            #     出向交易对手账户数,
            #     出向交易笔数,
            #     对公对私标志,
            #     对手为个人交易金额,
            #     对手为个人账户数,
            #
            #     最大单笔交易金额,
            #     最大月交易天数,
            #     最大月交易总金额,
            #     最大月交易笔数,
            #
            #     CASE WHEN 3号令 = '06' or 3号令 = '6' THEN 1 ELSE 0 END '标签'
            #
            #     FROM financeML.`tb_finance_ML_20210923`
            #     where  对公对私标志 = '0'
            #
            #     order by 3号令
            #
            #
            #
            #
            # '''
            # cursor.execute(sql)
            # res = cursor.fetchall()
            # col = [item[0] for item in cursor.description]
            # result_data = pd.DataFrame(res, columns=col)
            # result_data.fillna(0, inplace=True)
            # result_data.drop_duplicates(subset=['客户编号','客户账号'],inplace=True,keep='first')
            # result_data = result_data.apply(pd.to_numeric, errors='ignore')
            # result_data = result_data.iloc[:]

            sql = '''
                SELECT id,tx_id,tx_dt,biz_type,biz_line,tx_amt_rmb,abstract_cd,detail_num
                FROM P20210257_JS_FXQ_TRAN_20210425_0001
            
            '''
            cursor.execute(sql)
            res = cursor.fetchall()
            col = [item[0] for item in cursor.description]
            result_data1 = pd.DataFrame(res, columns=col)
            result_data1.fillna(0, inplace=True)

            sql = '''
                SELECT id,CARDNO,txn_dt,acdn_cd
                FROM P20210257_JS_FXQ_ACCT_ACDN_20210425_0001
            
            '''
            cursor.execute(sql)
            res = cursor.fetchall()
            col = [item[0] for item in cursor.description]
            result_data2 = pd.DataFrame(res, columns=col)
            result_data2.fillna(0, inplace=True)


    finally:
        cursor.close()

    # # target = result_data['标签']
    # data = result_data
    # data = data.fillna(0)
    # # print(target.to_frame().value_counts())

    print(result_data1.info())
    print(result_data2.info())

    import featuretools as ft




    result_data1 = result_data1.apply(pd.to_numeric, errors='ignore')
    result_data2 = result_data2.apply(pd.to_numeric, errors='ignore')

    es = ft.EntitySet(id='test')
    es = es.entity_from_dataframe(entity_id='result_data1', dataframe=result_data1,index='tx_id',time_index='tx_dt')
                              # ,variable_types={'FRZ_AFFR_SN': ft.variable_types.Categorical,
                              #                 'DEP_FRZ_TPCD':ft.variable_types.Categorical})
    es = es.entity_from_dataframe(entity_id='result_data2', dataframe=result_data2,index='id',time_index='txn_dt')
                              # ,variable_types={'FRZ_AFFR_SN': ft.variable_types.Categorical,
                              #                 'DEP_FRZ_TPCD':ft.variable_types.Categorical})


    # 表关联
    r_client_previous = ft.Relationship(es['result_data1']['tx_id'], es['result_data2']['CARDNO'])
    # 将关系添加到实体集
    es = es.add_relationship(r_client_previous)

    features, feature_names = ft.dfs(entityset=es, target_entity='result_data1',max_depth=1)
    # features, feature_names = ft.dfs(entityset=es, target_entity='data',agg_primitives=['mean', 'max', 'percent_true', 'last'],
    #                              trans_primitives=[ 'month'])
    print(len(feature_names))
    print(np.c_[feature_names])


    # # 0
    # # 5312
    # # 1
    # # 1265
    #
    # # 训练，并保存模型
    # train(data,target)
    #
    # # 测试，并输出效果指标
    # test(data,target)







    sys.exit()

    lr = use_model_file('xgb.pkl')
    test_pre = lr.predict(test_x)

    # sys.exit()
    #
    print("预测标签:\n", test_pre, len(test_pre))
    print("真实标签:\n", test_y)
    print("分数：", lr.score(test_x, test_y))
    # print("分数：",tree.score(test_x,test_y))

    print("混淆矩阵:\n", confusion_matrix(test_y, test_pre))
    print("分类报告:\n", classification_report(test_y, test_pre))

    # sys.exit()
    # plot_roc_curve(lr, test_x, test_y)
    # plot_roc_curve(tree, test_x, test_y)
    # plt.title("ROC曲线")

    # pre_to_one = lr.predict_proba(test_x)[:, :-1]
    pre_to_one = lr.predict_proba(test_x)[:, 1]
    # pre_to_one = tree.predict_proba(test_x)[:, :-1]
    fpr, tpr, thresholds = roc_curve(test_y, pre_to_one)
    print("ks", max(tpr - fpr))



    auc = auc(fpr, tpr)
    print("auc: ", auc)


