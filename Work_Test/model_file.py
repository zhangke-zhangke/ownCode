##code
# -*- coding:utf-8 -*-
# coding: unicode_escape
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.model_selection import train_test_split
# from sklearn.externals import joblib
import pickle, os
import sys, xlrd

path = os.getcwd()
sys_len = len(sys.argv)
if sys_len >= 3:
    black_data = sys.argv[0]  ##case_id_real.csv
    car_data = sys.argv[1]  ##car_data.csv
    car_info = sys.argv[2]  ##car_info.csv
    input_data = sys.argv[3]  ##输入的测试集
    test_data = path + "\\" + input_data
else:
    # black_data = "case_id_real.csv"
    car_data = "car_data.csv"
    # car_info = "car_info.csv"
    test_data = path + "/test_data.xlsx"
    # ori_result = path + "/seventy_person.xlsx"

car_address = r"C:\Users\1\Desktop\data\vechicle_ccic_clean.xlsx"
insurance_address = r"C:\Users\1\Desktop\data\concat_ccic_clean.xlsx"

model_file = "model.pkl"

pd.set_option('display.max_columns', 5000)
pd.set_option('display.max_rows', 5000)
pd.set_option('display.width', 1000)

###读取测试集数据 test_data_df
new_name = ["case_id", "case_person", "case_phone", "case_date", "car_num", "carriage_num", "driver_name",
            "driver_license", "third_car_num", "third_carriage_num", "third_driver_name",
            "third_driver_license", "car_owner", "insurant_name", "insurant_name_id", "money", "place", "date",
            "company", "pay_name", "pay_phone", "pay_id", "bank", "repair_shop", "third_repair_shop"]
old_name_pre = "报案号	报案人	报案电话	报案日期	标的车牌	标的车架号	标的驾驶员姓名	标的驾驶证号	三者车牌	三者车架号	三者驾驶员姓名	" \
               "三者驾驶证号	标的车主	标的被保险人姓名	标的被保险人证件号	赔付金额	出险地点	出险日期	保险公司	收款人姓名	收款人电话	收款人证件号码	银行账户	标的修理厂	三者修理厂"
# test_data_df = pd.read_excel(test_data, usecols=list(range(25)))  ##3500
# test_data_df = pd.read_csv(insurance_address)
test_data_df = pd.read_excel(insurance_address)

old_name = old_name_pre.split("\t")
dict_columns = dict(zip(old_name,new_name))
test_data_df.rename(columns=dict_columns,inplace= True)


test_data_df.drop_duplicates(subset=["case_id"],inplace = True)
# print(test_data_df.head(10))

##读取全量历史明细数据集  data
# data_df = pd.read_csv(path + f'\{car_data}', error_bad_lines=False, encoding='gb18030', dtype=str)  ##全量的线索明细数据669138条
# data_df.columns = new_name

# data_all = pd.concat([data_df,test_data_df],ignore_index=True)


# 汽车价格和使用年限处理   carriage_num：车架号
# car_info_df = pd.read_csv(path + f'\{car_data}', encoding='gb18030')  ###车架号，车龄，价格信息，35w条记录
car_info_df = pd.read_excel(car_address)  ###车架号，车龄，价格信息

new_name = ["carriage_num","usage_age", "car_price"]
old_name = ["车架号","使用年限","实际价值"]
dict_columns = dict(zip(old_name,new_name))
car_info_df = car_info_df.rename(columns=dict_columns)[new_name]
car_info_df.drop_duplicates(subset=["case_id"],inplace = True)
# print(car_info_df.head(5),car_info_df.columns,car_info_df.shape)

car_info_df = car_info_df[car_info_df["car_price"] > 0].groupby("carriage_num")[
    ["usage_age", "car_price"]].mean().reset_index()
car_price_median = car_info_df.car_price.median()  ##车辆价格中位数  115900
usage_age_median = car_info_df.usage_age.median()  ##车辆使用年限中位数  3.0

# print(car_info_df.head(50),car_info_df.columns,car_info_df.shape)
# print(test_data_df.head(5),test_data_df.columns,test_data_df.shape)
##定义test_data_agg
test_data_df["carriage_num"]=test_data_df.carriage_num.astype("object")
test_data_agg = pd.merge(test_data_df, car_info_df, how='left', on=["carriage_num"])
test_data_agg.car_price.fillna(car_price_median, inplace=True)  ##填充中位数
test_data_agg.usage_age.fillna(usage_age_median, inplace=True)  ##填充中位数

# 手机号和修理厂关联
iphone_repair_cols = ["case_phone", "repair_shop"]
phone_repair_shop = test_data_agg[iphone_repair_cols].dropna()
phone_repair_shop.insert(1, 'phone_repair_cnt', 1)
phone_repair_shop_agg = phone_repair_shop.groupby(iphone_repair_cols).count().reset_index()
phone_repair_cnt_median = phone_repair_shop_agg.phone_repair_cnt.median()  ##修理厂中位数：1

phone_data = test_data_agg[["case_phone"]].dropna()
phone_data.insert(1, 'phone_cnt', 1)
phone_data_agg = phone_data.groupby("case_phone").count().reset_index()
phone_cnt_median = phone_data_agg.phone_cnt.median()  ##手机号中位数：1

test_data_agg = pd.merge(test_data_agg, phone_repair_shop_agg, how='left', on=["case_phone", "repair_shop"])

test_data_agg = pd.merge(test_data_agg, phone_data_agg, how='left', on=["case_phone"])
test_data_agg.phone_cnt.fillna(phone_cnt_median, inplace=True)
test_data_agg.phone_repair_cnt.fillna(phone_repair_cnt_median, inplace=True)
# test_data_df.loc[((test_data_df['phone_cnt']==1) & (test_data_df['label'] !=1)),'label'] = 0         ###报警电话出现1次且没有标记为黑名单的用0补

# 驾驶证、车辆、修理厂关联
driver_license_repair_cols = ["driver_license", "repair_shop"]
driver_license_repair_shop = test_data_agg[driver_license_repair_cols].dropna()
driver_license_repair_shop.insert(1, 'driver_license_repair_cnt', 1)
driver_license_repair_shop_agg = driver_license_repair_shop.groupby(driver_license_repair_cols).count().reset_index()
driver_license_repair_cnt_median = driver_license_repair_shop_agg.driver_license_repair_cnt.median()  ##驾驶证关联到的修理厂次数 中位数：2

driver_license_car_cols = ["driver_license", "carriage_num"]
driver_license_carriage_num = test_data_agg[driver_license_car_cols].dropna()
driver_license_carriage_num.insert(1, 'driver_license_car_cnt', 1)
driver_license_carriage_num_agg = driver_license_carriage_num.groupby(driver_license_car_cols).count().reset_index()
driver_license_car_cnt_median = driver_license_carriage_num_agg.driver_license_car_cnt.median()  ##驾驶证与关联到的车辆次数 中位数：2

driver_license_data = test_data_agg[["driver_license"]].dropna()
driver_license_data.insert(1, 'driver_license_cnt', 1)
driver_license_data_agg = driver_license_data.groupby("driver_license").count().reset_index()
driver_license_cnt_median = driver_license_data_agg.driver_license_cnt.median()  ###驾驶证出现的次数 中位数：1

test_data_agg = pd.merge(test_data_agg, driver_license_repair_shop_agg, how='left',
                         on=["driver_license", "repair_shop"])
test_data_agg = pd.merge(test_data_agg, driver_license_carriage_num_agg, how='left',
                         on=["driver_license", "carriage_num"])
test_data_agg = pd.merge(test_data_agg, driver_license_data_agg, how='left', on=["driver_license"])

test_data_agg.driver_license_repair_cnt.fillna(driver_license_repair_cnt_median, inplace=True)
test_data_agg.driver_license_car_cnt.fillna(driver_license_car_cnt_median, inplace=True)
test_data_agg.driver_license_cnt.fillna(driver_license_cnt_median, inplace=True)
# print(test_data_agg.head(100))
# 标的三者车辆和标的三者修理厂、不同保险公司关联
third_car_repair_cols = ["third_carriage_num", "third_repair_shop"]
third_car_repair_shop = test_data_agg[third_car_repair_cols].dropna()
third_car_repair_shop.insert(1, 'third_car_repair_cnt', 1)
third_car_repair_shop_agg = third_car_repair_shop.groupby(third_car_repair_cols).count().reset_index()
third_car_repair_cnt_median = third_car_repair_shop_agg.third_car_repair_cnt.median()  ##标的三者车辆和标的三者修理厂 关联次数中位数：1.0

third_car_data = test_data_agg[["third_carriage_num"]].dropna()
third_car_data.insert(1, 'third_car_cnt', 1)
third_car_data_agg = third_car_data.groupby("third_carriage_num").count().reset_index()
third_car_cnt_median = third_car_data_agg.third_car_cnt.median()

third_car_company_cols = ["third_carriage_num", "company"]
third_car_company = test_data_agg[third_car_company_cols].dropna()
third_car_company_agg = third_car_company.groupby('third_carriage_num')["company"].apply(set).reset_index()
third_car_company_agg["third_car_company_cnt"] = third_car_company_agg["company"].map(len)
third_car_company_agg = third_car_company_agg[["third_carriage_num", "third_car_company_cnt"]]
third_car_company_cnt_median = third_car_company_agg.third_car_company_cnt.median()

test_data_agg = pd.merge(test_data_agg, third_car_repair_shop_agg, how='left',
                         on=["third_carriage_num", "third_repair_shop"])
test_data_agg = pd.merge(test_data_agg, third_car_data_agg, how='left', on=["third_carriage_num"])
test_data_agg = pd.merge(test_data_agg, third_car_company_agg, how='left', on=["third_carriage_num"])

test_data_agg.third_car_repair_cnt.fillna(third_car_repair_cnt_median, inplace=True)
test_data_agg.third_car_cnt.fillna(third_car_cnt_median, inplace=True)
test_data_agg.third_car_company_cnt.fillna(third_car_company_cnt_median, inplace=True)

# 车牌是否曾经既为标的也为三者
car_num = set(test_data_agg["car_num"].dropna().values.tolist())
third_car_num = set(test_data_agg["third_car_num"].dropna().values.tolist())
car_common = car_num.intersection(third_car_num)
car_commmon_df = pd.DataFrame({"car_num": list(car_common)})
car_commmon_df["is_car_third"] = 1
test_data_agg = pd.merge(test_data_agg, car_commmon_df, how='left', on=["car_num"])
test_data_agg.is_car_third.fillna(0, inplace=True)

# 报案电话的平均时间间隔
phone_date_cols = ["case_phone", "case_date"]
phone_date = test_data_agg[phone_date_cols].dropna()
print(phone_date.head(5))

phone_date.case_date = pd.to_datetime(phone_date.case_date,format = "%Y-%m-%d")

t1 = [t.value // (10 ** 9 * 86400) for t in phone_date.case_date]
phone_date["time_pre"] = pd.DataFrame(t1)
phone_date_agg = phone_date.dropna().groupby('case_phone')["time_pre"].apply(set).reset_index()

phone_date_agg["time_gap"] = phone_date_agg["time_pre"].apply(lambda x: (max(x) - min(x)) / len(x))
phone_date_agg.loc[phone_date_agg["time_gap"] == 0.0, "time_gap"] = 500
phone_date_gap_median = phone_date_agg.time_gap.median()
test_data_agg = pd.merge(test_data_agg, phone_date_agg, how='left', on=["case_phone"])
test_data_agg.time_gap.fillna(phone_date_gap_median, inplace=True)

# print(test_data_agg.head(100))
# data_need = data[(data["label"]==1) | (data["label"]==0)].reset_index(drop=True)
sample_data = test_data_agg[
    ["car_price", "usage_age", "phone_repair_cnt", "phone_cnt", "driver_license_repair_cnt", "driver_license_car_cnt",
     "driver_license_cnt", "third_car_repair_cnt", "third_car_cnt", "third_car_company_cnt", "is_car_third",
     "time_gap"]].copy()

###归一化
def dataNormalization(train):
    #     max_min_scaler = lambda x:(x-np.min(x)/(np.max(x)-np.min(x)))
    featureCols = ["car_price", "usage_age", "phone_repair_cnt", "phone_cnt", "driver_license_repair_cnt",
                   "driver_license_car_cnt",
                   "driver_license_cnt", "third_car_repair_cnt", "third_car_cnt", "third_car_company_cnt",
                   "is_car_third", "time_gap"]
    for name in featureCols:
        mean_value = train.loc[:, name].mean()
        std_value = train.loc[:, name].std()
        if std_value>0:
            train.loc[:, name] = (train.loc[:,name] - mean_value)/std_value
            # (train[name]-mean_value)/(train[name].max()-train[name].min())#train[[name]].apply(max_min_scaler)
        else:
            train.loc[:, name]= 0

    return train


sample_data = dataNormalization(sample_data)



# sample_data = sample_data.iloc[:,:]
def savemodel(model, filedir):
    f = open(filedir, "wb")
    pickle.dump(model, f)
    f.close()


def loadmodel(filedir):
    f = open(filedir, "rb")
    model = pickle.load(f)
    f.close()
    return model


##读取模型文件
gbdt = loadmodel(path + "//" + model_file)

# #print("4"*100)
test_pred = gbdt.predict(sample_data)  ###测试集预测分类结果
test_pred_df = pd.DataFrame({"pred": test_pred.tolist()})
test_predprob = gbdt.predict_proba(sample_data)[:, 1]
test_predprob_df = pd.DataFrame({"predprob": test_predprob.tolist()})  ###测试集预测概率值
case_id_df = test_data_df["case_id"].to_frame("case_id")
# predict_1 = pd.concat([test_data_df,test_pred_df,test_predprob_df],axis=1)    ###测试集数据+预测分类结果
predict_2 = pd.concat([case_id_df, sample_data, test_pred_df, test_predprob_df], axis=1)

print(case_id_df.head(5),case_id_df.shape)
print(predict_2.head(5),predict_2.shape)
print(test_pred_df.head(5),test_pred_df.shape)
print(test_predprob_df.head(5),test_predprob_df.shape)

result_col = ["case_id", "pred", "predprob"]
result = predict_2[result_col]

# result.to_csv("test_result.csv")

print(result.groupby("pred").size())
