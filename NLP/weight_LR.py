
import pymysql
import pandas as pd
import sys
import pickle
import pymysql
from sklearn.externals import joblib
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split ,cross_val_predict
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, roc_auc_score, plot_roc_curve, auc \
    , SCORERS
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import MinMaxScaler ,normalize
from sklearn.svm import SVC

#from mlxtend.plotting import plot_decision_regions, plot_confusion_matrix



import sys
from matplotlib import pyplot as plt
from sklearn.tree import DecisionTreeClassifier

plt.rcParams['font.sans-serif' ] =['SimHei']  # 在图中正确显示中文
plt.rcParams['axes.unicode_minus' ] =False    # 默认是使用Unicode负号，设置正常显示字符，如正常显示负号



def get_enginen():
    engine = create_engine('mysql+pymysql://root:123456@172.30.6.5:3306/financeData?charset=utf8')
    return engine



def save_model_file(model ,save_model_name):
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
                FROM `tb_finance_ML_20210924`
            '''
            cursor.execute(sql)
            res = cursor.fetchall()
            col = [item[0] for item in cursor.description]
            result_data = pd.DataFrame(res ,columns=col)
            result_data.fillna(0 ,inplace=True)
            result_data = result_data.apply(pd.to_numeric, errors='ignore')
    finally:
        cursor.close()



    target = result_data['标签']
    data = result_data.iloc[: ,3:-1]
    data = data.fillna(0)


    train_x ,test_x ,train_y ,test_y = train_test_split(data ,target ,train_size=0.8 ,test_size=0.2 ,random_state=0)


    m = MinMaxScaler()
    train_x = m.fit_transform(train_x)
    test_x = m.fit_transform(test_x)



    weights = np.linspace(0.01, 0.99, 20)

    gsc = GridSearchCV(
        estimator=LogisticRegression(),
        param_grid={
            'class_weight': [{0: x, 1: 1.0 - x} for x in weights]
        },
        scoring='recall',
        cv=5
    )
    grid_result = gsc.fit(train_x, train_y)

    print("Best parameters : %s" % grid_result.best_params_)

    lr = LogisticRegression(**grid_result.best_params_)
    lr.fit(train_x, train_y)

    y_pred = lr.predict(test_x)

    print(lr.score(test_x,test_y))
    print(classification_report(test_y, y_pred))
    print(confusion_matrix(test_y, y_pred))
    plt.show()

    sys.exit()

    # lr = LogisticRegression(C=0.1,max_iter=1000,class_weight='balanced',random_state=0)
    # lr.fit(train_x,train_y)
    # test_pre = lr.predict(test_x)




    print("预测标签:\n" ,test_pre ,len(test_pre))
    print("真实标签:\n" ,test_y)
    print("分数：" ,lr.score(test_x ,test_y))

    print("混淆矩阵:\n" ,confusion_matrix(test_y ,test_pre))
    print("分类报告:\n" ,classification_report(test_y ,test_pre))

    # sys.exit()
    plot_roc_curve(lr, test_x, test_y)
    plt.title("ROC曲线")
    plt.show()


    pre_to_one = lr.predict_proba(test_x)[:, :-1]
    fpr, tpr, thresholds = roc_curve(test_y, pre_to_one)
    # print(fpr)
    # print(tpr)

    auc = auc(fpr ,tpr)
    print(auc)

    auc = roc_auc_score(test_y ,pre_to_one)
    print(auc)







