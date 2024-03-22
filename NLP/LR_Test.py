import pymysql
import pandas as pd
import sys
import pickle
import pymysql
from sklearn.externals import joblib
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split,cross_val_predict
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.metrics import classification_report,confusion_matrix,roc_curve,roc_auc_score,plot_roc_curve,auc,SCORERS
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import MinMaxScaler,normalize
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier,AdaBoostClassifier
from imblearn.over_sampling import RandomOverSampler, SMOTE  # 随机采样函数 和SMOTE过采样函数
from imblearn.under_sampling import RandomUnderSampler  # 随机采样函数 和SMOTE过采样函数
from imblearn.combine import SMOTETomek
from sklearn.neighbors import KNeighborsClassifier
import xgboost as xgb

import sys
from matplotlib import pyplot as plt
from sklearn.tree import DecisionTreeClassifier

plt.rcParams['font.sans-serif']=['SimHei']      #在图中正确显示中文
plt.rcParams['axes.unicode_minus']=False    # 默认是使用Unicode负号，设置正常显示字符，如正常显示负号



def get_enginen():
    engine = create_engine('mysql+pymysql://root:123456@172.30.6.5:3306/financeData?charset=utf8')
    return engine



def save_model_file(model,save_model_name):
    joblib.dump(model, save_model_name)


def use_model_file(model_name):
    model = joblib.load(model_name)
    return model










if __name__ == '__main__':
    connection = pymysql.connect(host='172.30.6.204', user='root', password='123456', database='financeML', port=int(3306))
    try:
        with connection.cursor() as cursor:
            sql = '''
                SELECT 
                客户名称,
                客户编号,
                客户账号,
                
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

                CASE WHEN 3号令 = '06' or 3号令 = '6' THEN 1 ELSE 0 END '标签'
                FROM `tb_finance_ML_20210923`
                where  对公对私标志 = '0'
                
                order by 3号令 desc
                
                
                
            '''
            cursor.execute(sql)
            res = cursor.fetchall()
            col = [item[0] for item in cursor.description]
            result_data = pd.DataFrame(res,columns=col)
            result_data.fillna(0,inplace=True)
            result_data = result_data.apply(pd.to_numeric, errors='ignore')
    finally:
        cursor.close()



    target = result_data['标签']
    data = result_data.iloc[:,3:-1]
    data = data.fillna(0)
    print(target.to_frame().value_counts())

    # # 随机采样
    # f = RandomOverSampler(random_state=0)
    # # f = SMOTETomek(sampling_strategy={1:500 },random_state=0)
    # # f = RandomUnderSampler(sampling_strategy={1:1000},random_state=0)
    # # f = SMOTE()
    #
    #
    # data,target = f.fit_resample(data,target)
    # print(target.to_frame().value_counts())


    #
    # train_x = data
    # train_y = target
    # m = MinMaxScaler()
    # train_x = m.fit_transform(train_x)
    # print(data)

    # train_x,test_x,train_y,test_y = train_test_split(data,target,train_size=0.8,test_size=0.2,stratify=target,random_state=0)


    #交叉验证
    # cross = cross_val_score(LogisticRegression(C=0.1,max_iter=1000,class_weight='balanced'),train_x,train_y,scoring='f1',cv=10)
    # print(max(cross))

    # sys.exit()
    # train_y = np.c_[train_y]    #pd.DataFrame(train_y)
    # test_y = np.c_[test_y]      #pd.DataFrame(test_y)

    # train_x = normalize(train_x)
    # test_x = normalize(test_x)

    # m = MinMaxScaler()
    # train_x = m.fit_transform(train_x)
    # test_x = m.fit_transform(test_x)

    # data = m.fit_transform(data)



    #
    #
    # # sys.exit()
    # lr = LogisticRegression(penalty='l1',solver='liblinear',C=6.0,max_iter=5000,class_weight='balanced',random_state=0)
    #网格搜索
    # lr_params = {
    #     'C':[0.2,0.4,0.6,0.8,1]
    # }
    # gridsearchcv = GridSearchCV(estimator=SVC(class_weight='balanced'),param_grid=lr_params,cv=5,scoring='f1')
    # gridsearchcv.fit(train_x,train_y)
    # lr = LogisticRegression(C=0.1,max_iter=1000,class_weight='balanced',random_state=0)
    #

    #网格搜索
    # lr_params = {
    #     'max_depth':[2,4,6,8,10,12,14,16]
    # }
    # gridsearchcv = GridSearchCV(estimator=DecisionTreeClassifier(class_weight='balanced'),param_grid=lr_params,cv=5,scoring='recall')
    # gridsearchcv.fit(train_x,train_y)
    # print(gridsearchcv.best_params_)
    # #
    # # sys.exit()
    # lr = DecisionTreeClassifier(max_depth=1,class_weight='balanced')
    # lr = SVC(class_weight='balanced',probability=True)
    # lr = RandomForestClassifier(class_weight='balanced')

    lr = xgb.XGBRFClassifier(learning_rate=0.5,subsample=0.9)
    # lr.fit(train_x,train_y)
    # test_pre = lr.predict(test_x)

    # tree = DecisionTreeClassifier(**gridsearchcv.best_params_)
    # tree.fit(train_x,train_y)
    # test_pre=tree.predict(test_x)

    # save_model_file(lr,'over_svm.pkl')
    # save_model_file(tree,'tree.pkl')
    # save_model_file(lr,'svm.pkl')
    # save_model_file(lr,'xgb.pkl')


    test_x = data
    test_y = target
    m = MinMaxScaler()
    test_x = m.fit_transform(test_x)

    # adaboost = AdaBoostClassifier(LogisticRegression(C=0.1,max_iter=5000,class_weight='balanced',random_state=0))
    # adaboost = AdaBoostClassifier(DecisionTreeClassifier(max_depth=1))
    # adaboost.fit(train_x,train_y)
    # test_pre = adaboost.predict(test_x)


    lr = use_model_file('xgb.pkl')
    test_pre = lr.predict(test_x)

    # sys.exit()
    #
    print("预测标签:\n",test_pre,len(test_pre))
    print("真实标签:\n",test_y)
    print("分数：",lr.score(test_x,test_y))
    # print("分数：",tree.score(test_x,test_y))

    print("混淆矩阵:\n",confusion_matrix(test_y,test_pre))
    print("分类报告:\n",classification_report(test_y,test_pre))

    # sys.exit()
    # plot_roc_curve(lr, test_x, test_y)
    # plot_roc_curve(tree, test_x, test_y)
    # plt.title("ROC曲线")



    # pre_to_one = lr.predict_proba(test_x)[:, :-1]
    pre_to_one = lr.predict_proba(test_x)[:, 1]
    # pre_to_one = tree.predict_proba(test_x)[:, :-1]
    fpr, tpr, thresholds = roc_curve(test_y, pre_to_one)
    print("ks",max(tpr-fpr))

    # KS_max=0
    # best_thr=0
    # for i in range(len(fpr)):
    #     if(i==0):
    #         KS_max=tpr[i]-fpr[i]
    #         best_thr=thresholds[i]
    #     elif (tpr[i]-fpr[i]>KS_max):
    #         KS_max = tpr[i] - fpr[i]
    #         best_thr = thresholds[i]
    # print("ks值： ",KS_max)

    auc = auc(fpr,tpr)
    print("auc: ",auc)

    # auc = roc_auc_score(test_y,pre_to_one)
    # print(auc)


    plt.show()


    # y_pre = model.predict_proba(x_test)
    # fpr,tpr,thresholds=roc_curve(y_test,y_0)  #计算fpr,tpr,thresholds
    # auc=roc_auc_score(y_test,y_0) #计算auc
    #
    # #画曲线图
    # plt.figure()
    # plt.plot(fpr,tpr)
    # plt.title('$ROC curve$')
    # plt.show()
    #
    #
    # #计算ks
    # KS_max=0
    # best_thr=0
    # for i in range(len(fpr)):
    #     if(i==0):
    #         KS_max=tpr[i]-fpr[i]
    #         best_thr=thresholds[i]
    #     elif (tpr[i]-fpr[i]>KS_max):
    #         KS_max = tpr[i] - fpr[i]
    #         best_thr = thresholds[i]
    #
    # print('最大KS为：',KS_max)
    # print('最佳阈值为：',best_thr)


