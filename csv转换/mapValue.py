import pandas as pd
import sys



# 流水根据客户名称判断对公对私标识
def name2custInd(x):
    # 根据主体方名称长短判定，6个字以内为个人）     1：个人 ； 2：单位
    if len(str(x)) <= 6:
        return '个人'
    else:
        return '单位'

# 流水将交易时间格式更改为HH:MM:SS （原数据:20221208143027）
def tradeTime(x):
    x = str(x).replace('t', '0')
    if len(x) != 14:
        x = x.ljust(14,'0')

    # 取时间内容，然后处理为 HH:MM:SS
    retunTime = str(x)[8:]
    transformTime = ''
    for c,i in enumerate(retunTime):
        transformTime += i
        if (c + 1) % 2 == 0 and c != len(retunTime) -1:
            transformTime += ':'
    return transformTime

def returnCurrencyType(currencyName):
    if len(str(currencyName)) == 0:
        return ""
    elif str(currencyName).__contains__("人民币"):
        return "CNY"
    elif str(currencyName).__contains__("美元"):
        return "USD"
    elif str(currencyName).__contains__("欧元"):
        return "EUR"
    elif str(currencyName).__contains__("香港"):
        return "HKD"
    elif str(currencyName).__contains__("台湾"):
        return "TWD"
    elif str(currencyName).__contains__("澳门"):
        return "MOP"
    elif str(currencyName).__contains__("加拿大"):
        return "CAD"
    elif str(currencyName).__contains__("英镑"):
        return "GBP"
    elif str(currencyName).__contains__("日元"):
        return "JPY"
    elif str(currencyName).__contains__("卢比"):
        return "IDR"
    elif str(currencyName).__contains__("卢布"):
        return "RUB"
    elif str(currencyName).__contains__("铢"):
        return "THB"
    else:
        return ""


# 可疑交易主体及主要对手信息模板 表
def acc_process():
    # 主体基本信息
    base_info = pd.read_csv('result_身份信息列表.csv')
    base_info.replace('\s+','',regex=True,inplace=True)
    # 将家庭住址为空的填入值：暂无
    base_info['家庭住址'].fillna('暂无',inplace=True)

    # 对手账户信息
    acc_info = pd.read_csv('result_账户信息列表.csv')
    acc_info.replace('\s+','',regex=True,inplace=True)

    # 主体方账号字段需要从流水中获取
    mainBodyAccInfo = pd.read_csv('result_交易明细列表.csv')[['主体方账号','主体方名称','主体方证件号码']]
    mainBodyAccInfo.replace('\s+','',regex=True,inplace=True)


    # 循环主体身份信息表，从流水中寻找每一个主体的账号
    mainBodyResult = []
    for i in range(base_info.shape[0]):
        mainBody = mainBodyAccInfo.query(f" 主体方名称 == '{base_info['证件登记姓名'].iloc[i]}' & 主体方证件号码 == '{base_info['证件登记号码'].iloc[i]}' ")
        # 流水中的账号记录去重
        # mainBody.drop_duplicates(subset=['主体方账号'],inplace=True)   # 此种写法有警告
        mainBody = mainBody.drop_duplicates(subset=['主体方账号'])

        # 多张卡的情况，循环添加
        for num in range(mainBody.shape[0]):
            mainBodyResult.append(['主体',mainBody['主体方名称'].iloc[num],'身份证',mainBody['主体方证件号码'].iloc[num],'',base_info['家庭住址'].iloc[i],mainBody['主体方账号'].iloc[num],'',''])

    # 添加对手账户信息
    opponentResult = []
    for i in range(acc_info.shape[0]):
        opponentResult.append(['对手',acc_info['所有者姓名'].iloc[i],'身份证',acc_info['证件号码'].iloc[i],'','暂无',acc_info['账户号码'].iloc[i],'',''])

    # 合并主体及对手数据，输出csv
    result_col = ['*主体/对手','*客户名称/姓名','*证件种类','*证件号码','联系方式','*住所地或单位地址','*账号','开户网点名称','销户日期']
    finall_result = mainBodyResult + opponentResult
    result_df = pd.DataFrame(finall_result,columns=result_col)
    # 将索引做为列，重命名为序号
    result_df = result_df.reset_index(drop=False).rename(columns={'index':'序号'})
    # 序号加1
    result_df['序号'] = result_df['序号'].apply(lambda x:x+1)
    print(result_df)

    # 输出csv
    result_df.to_excel('可疑交易主体及主要对手信息模板.xls',index=False,encoding='utf-8')





# 下载交易明细模板 表
def trade_process():
    # 读取交易明细数据
    tradeInfo = pd.read_csv('result_交易明细列表.csv')[['交易日期','交易时间','主体方金融机构名称','主体方账号','主体方证件号码',
                                                  '主体方银行卡号','主体方名称','资金收付标志','货币名称','原币金额','用途',
                                                  '对手方账号','对手方名称','对手方金融机构名称']]
    tradeInfo.replace('\s+','',regex=True,inplace=True)

    # 交易时间格式更改
    tradeInfo['交易时间'] = tradeInfo['交易时间'].apply(lambda x:tradeTime(x))
    # 对公对私标识
    tradeInfo['公私标识'] = tradeInfo['主体方名称'].apply(lambda x:name2custInd(x))
    # 客户号及账号都取主体方账号
    tradeInfo['客户号'] = tradeInfo['主体方账号']
    # 货币名称换算为代码值
    tradeInfo['货币名称'] = tradeInfo['货币名称'].apply(lambda x:returnCurrencyType(x))
    # 默认值
    tradeInfo['现金、转账标识'] = '转账'
    tradeInfo['账户余额'] = '0'
    tradeInfo['交易方式标识'] = '其他'
    # 将字段重命名为标准字段
    tradeInfo.rename(columns={'交易日期':'*交易日期','交易时间':'*交易时间','主体方金融机构名称':'*交易行名称','公私标识':'*公私标识',
                              '主体方银行卡号':'卡号','客户号':'*客户号','主体方证件号码':'*证件号码','主体方账号':'*账号',
                              '主体方名称':'*账户名称','资金收付标志':'*资金收付标识','现金、转账标识':'*现金、转账标识',
                              '货币名称':'*币种','原币金额':'*原币种交易金额','账户余额':'*账户余额','交易方式标识':'*交易方式标识',
                              '用途':'摘要说明','对手方账号':'交易对方账号（卡号）','对手方名称':'交易对方户名',
                              '对手方金融机构名称':'交易对方行名称'},inplace=True)

    # 定义输出的总列名
    result_frame_col = ['*交易日期', '*交易时间', '*交易行名称', '*公私标识', '*客户号', '*证件号码', '*账号', '卡号','*账户名称',
                  '账户类型', '账户类别','交易对手方账户类别', '交易对方行代码', '交易对方行名称', '交易对方账号（卡号）','交易对方户名',
                  '*资金收付标识', '*现金、转账标识', '*币种', '*原币种交易金额','原币种交易金额（万元）','折美元交易金额',
                  '折美元交易金额（万元）','折人民币交易金额','折人民币交易金额（万元）','*账户余额','账户余额（万元）',
                  '代理交易标识', '代理人姓名','代理人联系方式','代理人身份证件种类', '代理人身份证件号码', '业务流水号', '柜员号',
                  '业务名称', '冲账标识','摘要说明', '跨境交易标识','交易对方所在国家或地区', '*交易方式标识', 'IP地址', 'ATM机具编号',
                  'ATM机具所属行行号','MAC或IMEI地址']
    result_frame_df = pd.DataFrame(columns=result_frame_col)
    # 将数据放到最终输出的列表里
    result_df = pd.concat([result_frame_df,tradeInfo],sort=False)
    result_df = result_df.reset_index(drop=False).rename(columns={'index':'序号'})
    result_df['序号'] = result_df['序号'].apply(lambda x:x+1)
    print(result_df)

    result_df.to_excel('下载交易明细模板.xls',index=False,encoding='utf-8')








if __name__ == '__main__':

    # 账户信息
    acc_process()


    # 交易流水
    trade_process()











