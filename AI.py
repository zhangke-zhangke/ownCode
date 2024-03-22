import numpy as np
import pandas as pd
from sklearn.externals import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import f1_score
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from pyserver.common.action import base
import datetime
import os
from sklearn.model_selection import cross_val_score
from imblearn.over_sampling import RandomOverSampler    # 过采样
from sklearn.preprocessing import LabelEncoder
import datetime
import pymysql
from sqlalchemy import create_engine
from sklearn.preprocessing import StandardScaler,MinMaxScaler,MaxAbsScaler



class connectSql():
    def __init__(self,user,password,host,port,dbName):
        '''
            @p
        '''
        self.user = user
        self.passwrod = password
        self.host = host
        self.port = port
        self.dbName = dbName
        # self.engine = create_engine(f'mysql+pymysql://{self.user}:{self.passwrod}@{self.host}:{self.port}/{self.dbName}?charset=utf8')
        self.engine = f'mysql+pymysql://{self.user}:{self.passwrod}@{self.host}:{self.port}/{self.dbName}?charset=utf8'

    # 一般读取函数
    def querySql(self,sql):
        sqlDf = pd.read_sql(sql=sql,con=self.engine)
        return sqlDf

    # 取出甄别预处理生成的列式数据    (定制读取函数)
    def getFeatureData(self, sql):
        featureData = pd.read_sql(sql=sql,con=self.engine)
        new_df = featureData.set_index(['card_no', 'target_type'])['target_value']
        new_df = new_df.unstack().rename_axis(columns=None).reset_index().fillna(0)
        return new_df


class machineLearning():
    def __init__(self,cls):
        self.model = cls

    def modeFit(self,tranX,tranY):
        self.model.fit(tranX,tranY)

    def predict(self,testX):
        self.predict = self.model.predict(testX)
        return self.predict

    # def autoMlArgs(self,trainX,trainY):
    #     # import flaml
    #     from flaml import AutoML
    #     autoMl = AutoML()
    #     # autoMl.add_learner('lr',LogisticRegression())
    #     settings = {
    #         "metric": 'f1', # 候选可以是: 'r2', 'rmse', 'mae', 'mse', 'accuracy', 'roc_auc', 'roc_auc_ovr', 'roc_auc_ovo', 'log_loss', 'mape', 'f1', 'ap', 'ndcg', 'micro_f1', 'macro_f1'
    #         "task": 'classification',  # 任务类型
    #         # "estimator_list": ['rf','xgboost']
    #     }
    #     autoMl.fit(trainX,pd.Series(trainY),**settings)
    #     print(autoMl.best_config)
    #     print(autoMl.best_estimator)

    def args_adaption(self,x,y):
        # 使用网格搜索算法最优参数
        LR_params = {
            'C': [0.6,0.8,1.0,1.5,2.0],
            'max_iter' : [500,1000,2000,3000,4000]
        }
        gridsearchcv = GridSearchCV(estimator=self.model,param_grid=LR_params, cv=3,scoring='f1')
        gridsearchcv.fit(x, y)
        print("使用网格搜索得出最优参数为:", gridsearchcv.best_params_)

        return gridsearchcv.best_params_

    # 评估指标
    # def

    # 归一化   对特征进行归一化处理
    def featureStd(self,x):
        # StandardScaler,MinMaxScaler
        return StandardScaler().fit_transform(x)

    # 标签编码  处理离散值如：性别
    def featureLableEncoding(self,x):
        # LabelEncoder
        return LabelEncoder().fit_transform(x)


if __name__ == '__main__':
    sqlObject = connectSql('root','123456','172.30.6.205',3306,'zqyccserver_JR')
    sql = f'''
             select card_no,target_type,target_value 
             from et_target_info_202303
             where run_id = 'dcaf2e59-3566-4105-96af-bd9f2311ddc6'
             group by card_no,target_type
    '''
    # 取出特征数据
    queryDf = sqlObject.getFeatureData(sql)

    # 取出特征对应中文名称
    sql = '''
            select target_type,target_description
            from rs_target
    '''
    targetDesc = sqlObject.querySql(sql)
    descDict = {}
    for key,value in targetDesc.values:
        descDict[key] = value

    queryDf.rename(columns=descDict,inplace=True)
    print(queryDf)
    print(queryDf.columns)

    # 删除掉不需要的特征及卡号
    queryDf.drop(columns=['card_no','借贷账户比','借贷金额比', '客户名下账户数', '日均交易笔数', '入向对手账户数', '入向公司账户数',
       '入向个人账户数', '入向交易笔数', '日终余额小的天数', '日终余额小占比', '最大月交易总金额',
       '最大月交易笔数', '最大月交易天数', '交易集中在单月', '跨境交易笔数', '出向对手账户数', '出向公司账户数',
       '出向日均交易笔数', '出向个人账户数', '出向交易笔数', '出向交易天数', '总账户数', '总公司账户数',  '总个人账户数',
       '对手为个人交易金额', '总交易笔数', '交易天数', '交易月数'],inplace=True)
    print(queryDf.columns)
    # 测试自己造标签
    target = [1,1,0,1,0,0,0]



    '''
        模型调用
    '''
    # 机器学习模型
    model = machineLearning(LogisticRegression(class_weight='balanced', random_state=0))
    # 寻找模型最优参数
    best_params = model.args_adaption(queryDf,target)
    # 初始化最优参数的模型
    model.__init__(LogisticRegression(**best_params))

    model.modeFit(queryDf,target)
    print(model.predict(queryDf))



    # model.autoMlArgs(queryDf,target)





'''
    异常交易洗钱特征总结:
        沉默期+小额测试交易			交易金额
        分散转入、集中转出			    交易笔数
        集中转出、分散转入		
        跨行与跨平台交易			    交易对手本外行标志
        对公账户频繁转对私账户		    对公交易对手为对私，且交易频繁
        交易对手可疑判断	（判断对手是否为某银行已经上报过可疑或存在于可疑库中）
        交易时间判断（晚上及节假日）
        
        
        
        
    ['日均交易额', '入向公司总交易额','最大单笔交易金额','入向总交易额','出向总交易额','交易总金额']

    ['借贷金额比', '客户名下账户数', '日均交易笔数', '入向对手账户数', '入向公司账户数',
       '入向个人账户数', '入向交易笔数', '日终余额小的天数', '日终余额小占比', '最大月交易总金额',
       '最大月交易笔数', '最大月交易天数', '交易集中在单月', '跨境交易笔数', '出向对手账户数', '出向公司账户数',
       '出向日均交易笔数', '出向个人账户数', '出向交易笔数', '出向交易天数', '总账户数', '总公司账户数',  '总个人账户数', 
       '对手为个人交易金额', '总交易笔数', '交易天数', '交易月数'],
'''