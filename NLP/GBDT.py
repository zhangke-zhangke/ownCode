from sklearn.ensemble import GradientBoostingClassifier
import pandas as pd
import sys
from sklearn.metrics import classification_report



if __name__ == '__main__':
    data_ds = pd.read_excel('C:\\Users\\dell\\Desktop\\GBDT模型数据.xlsx',sheet_name='对私')
    data_dg = pd.read_excel('C:\\Users\\dell\\Desktop\\GBDT模型数据.xlsx',sheet_name='对公')
    # print(data)

    ds_train = data_ds.iloc[:,5:]
    ds_train_target = data_ds['rpt_sbmsn_stcd']

    dg_train = data_dg.iloc[:,5:]
    dg_train_target = data_dg['rpt_sbmsn_stcd']

    print("对私特征个数：",ds_train.shape[1])
    print("对公特征个数：",dg_train.shape[1])

    ds = GradientBoostingClassifier(n_estimators=150)
    ds.fit(ds_train,ds_train_target)
    print("对私特征重要程度分别为：",ds.feature_importances_.tolist())
    print("对私分类报告：",classification_report(ds_train_target,ds.predict(ds_train)))

    dg = GradientBoostingClassifier(n_estimators=150)
    dg.fit(dg_train,dg_train_target)
    print("对公特征重要程度分别为：",dg.feature_importances_.tolist())
    print("对公分类报告：", classification_report(dg_train_target, dg.predict(dg_train)))







