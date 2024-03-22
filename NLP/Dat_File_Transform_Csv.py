input_path = 'F:\\KINGSTON\\金融历史训练数据\\反洗钱图谱历史训练数据0428-0430\\'
output_path = 'K:\\0428场景二数据清洗\\'

import os
str1 = ''
file_list = []
os.chdir(input_path)
for path_name, dir, files_name in os.walk(os.getcwd()):
    for file in files_name:
        if '$' not in file:
            file_list.append(os.path.join(path_name, file))
print(len(file_list))
print('\n'.join(file_list))

if not os.path.exists(output_path):
    os.mkdir(output_path)

import pandas as pd
df_流水汇总 = pd.DataFrame()
for path_name, dir, files_name in os.walk(os.getcwd()):
    for file in files_name:
        if '_AML_SSPCS_RPT_' in file:
            with open(os.path.join(path_name, file), encoding = 'utf-8') as f:
                lines = f.readlines()
            df = pd.DataFrame(lines)
            df_3号令 = df[0].str.split('\|\@\|',expand = True).iloc[:,:-1]
            df_3号令.columns = ['客户编号','反洗钱报告编号','反洗钱可疑交易笔数','金融机构网点名称','金融机构网点所在地区行政区划代码','反洗钱报告对公对私代码','可疑交易特征描述','反洗钱业务规则名称','反洗钱报告最大交易日期','反洗钱报告最小交易日期','反洗钱报告涉及人民币交易金额','反洗钱报告涉及人民币交易笔数','反洗钱传统渠道人民币交易金额','反洗钱电子银行渠道人民币交易金额','反洗钱新兴电子渠道人民币交易金额','反洗钱其他渠道人民币交易金额','反洗钱传统渠道交易笔数','反洗钱电子银行渠道交易笔数','反洗钱新兴电子渠道交易笔数','反洗钱其他渠道交易笔数','可疑交易措施描述','可疑交易报告报送方向代码','反洗钱可疑行为描述','#报告报送状态代码','报送日期','可疑交易报送标志','#批量导入日期','反洗钱交易主体账户个数','反洗钱中心机构编号','反洗钱中心机构中文名称','#备注二(洗钱类型)','报送次数','接续报告参考标志(0-否 1-是)','非可疑行为描述','可疑交易报告疑点分析说明','可疑交易报告疑点分析及排除理由','反洗钱可疑行为描述2','可疑交易报告疑点分析说明2','风险等级']
            df_3号令.to_csv(output_path + file.split('.')[0]+'.csv', encoding = 'utf-8',index = None)
            print('3号令Done！')
        elif '_IDV_BASE_IMG_' in file:
            with open(os.path.join(path_name, file), encoding = 'utf-8') as f:
                lines = f.readlines()
            df = pd.DataFrame(lines)
            df_对私基本 = df[0].str.split('\|\@\|',expand = True).iloc[:,:-1]
            df_对私基本.columns = ['客户编号','类罪','反洗钱报告编号','场景类型','客户姓名','证件类型','证件号码','性别','出生日期','年龄','民族','职业','职务','最佳联系电话','主地址','工作地址','国家地区代码','单位名称','个人住房贷款客户标志','非保本理财客户标志','保本理财客户标志','电话银行签约标志','短信金融签约标志','网上银行签约标志','手机银行签约标志','客户月均AUM值','单位客户编号','公司名称','四部委规模','客户所属行业','组织机构代码','营业执照号码','注册资本币种','注册资本','注册地址','经营地址','办公地址','员工人数','组织实收资本金额','经营状态代码','组织成立日期','机构经营范围说明','公司联系电话','法定代表人证件类型','法定代表人证件号码','法定代表人','授权代表人证件类型','授权代表人证件号码','授权代表人','业务联系人证件类型','业务联系人证件号码','业务联系人','实际控制人证件类型','实际控制人证件号码','实际控制人','受益所有人证件类型','受益所有人证件号码','受益所有人','风险等级','商户标志']
            df_对私基本.to_csv(output_path + file.split('.')[0]+'.csv', encoding = 'utf-8',index = None)
            print('对私基本Done！')
        elif '_CORP_BASE_IMG_' in file:
            with open(os.path.join(path_name, file), encoding = 'utf-8') as f:
                lines = f.readlines()
            df = pd.DataFrame(lines)
            df_对公基本 = df[0].str.split('\|\@\|',expand = True).iloc[:,:-1]
            df_对公基本.columns = ['客户编号','类罪','反洗钱报告编号','场景类型','客户名称','所属机构','四部委规模','客户所属行业','组织机构代码','营业执照号码','注册资本币种','注册资本','组织实收资本金额','信贷客户标识','联系电话','注册地址','经营地址','办公地址','对公客户类型','员工人数','经营状态代码','组织成立日期','主营业务描述','机构经营范围说明','企业网银签约标识','企业手机银行签约标志','企业网银高级版签约标志','企业手机银行高级版签约标志','企业网银简版签约标志','企业手机银行简版签约标志','法定代表人证件类型','法定代表人证件号码','法定代表人','授权代表人证件类型','授权代表人证件号码','授权代表人','业务联系人证件类型','业务联系人证件号码','业务联系人','实际控制人证件类型','实际控制人证件号码','实际控制人','受益所有人证件类型','受益所有人证件号码','受益所有人','风险等级','商户标志']
            df_对公基本.to_csv(output_path + file.split('.')[0]+'.csv', encoding = 'utf-8',index = None)
            print('对公基本Done！')
        elif '_IDV_OPN_ACCT_' in file:
            with open(os.path.join(path_name, file), encoding = 'utf-8') as f:
                lines = f.readlines()
            df = pd.DataFrame(lines)
            df_对私开户 = df[0].str.split('\|\@\|',expand = True).iloc[:,:-1]
            df_对私开户.columns = ['客户编号','类罪','反洗钱报告编号','场景类型','对公对私标志','账户开户名称','开户证件号码','客户账号','开户日期','存款账户余额','可用余额','币种代码','钞汇代码','开户机构编号','开户机构名称','开户二级分行名称','账户状态代码描述','销户日期','销户机构编号','联系电话','通讯地址','邮政编码','电子邮件地址','营业执照编号','国税登记号','地税登记号','企业法人姓名','企业法人证件类型','企业法人证件号码','授权代理人名称','授权代理人证件类型代码','授权代理人证件号码','最后交易营业日期','账户收付控制状态代码']
            df_对私开户.to_csv(output_path + file.split('.')[0]+'.csv', encoding = 'utf-8',index = None)
            print('对私开户Done！')
        elif '_CORP_OPN_ACCT_' in file:
            with open(os.path.join(path_name, file), encoding = 'utf-8') as f:
                lines = f.readlines()
            df = pd.DataFrame(lines)
            df_对公开户 = df[0].str.split('\|\@\|',expand = True).iloc[:,:-1]
            df_对公开户.columns = ['客户编号','类罪','反洗钱报告编号','场景类型','对公对私标志','账户开户名称','开户证件号码','客户账号','开户日期','存款账户余额','可用余额','币种代码','钞汇代码','开户机构编号','开户机构名称','开户二级分行名称','账户状态代码描述','销户日期','销户机构编号','联系电话','通讯地址','邮政编码','电子邮件地址','营业执照编号','国税登记号','地税登记号','企业法人姓名','企业法人证件类型','企业法人证件号码','授权代理人名称','授权代理人证件类型代码','授权代理人证件号码','最后交易营业日期','账户收付控制状态代码']
            df_对公开户.to_csv(output_path + file.split('.')[0]+'.csv', encoding = 'utf-8',index = None)
            print('对公开户Done！')
        elif '_REL_' in file:
            with open(os.path.join(path_name, file), encoding = 'utf-8') as f:
                lines = f.readlines()
            df = pd.DataFrame(lines)
            df_关联 = df[0].str.split('\|\@\|',expand = True).iloc[:,:-1]
            df_关联.columns = ['客户编号','类罪','反洗钱报告编号','场景','客户名称','关联类型','关系类型详细描述','对公对私标志','证件类型','证件号码','关联人名称','关联人客户编号']
            df_关联.to_csv(output_path + file.split('.')[0]+'.csv', encoding = 'utf-8',index = None)
            print('关联Done！')
        elif '_TRAN_' in file:
            with open(os.path.join(path_name, file), encoding = 'utf-8') as f:
                lines = f.readlines()
            df = pd.DataFrame(lines)
            df_流水 = df[0].str.split('\|\@\|',expand = True).iloc[:,:-1]
            df_流水.columns = ['类罪类型','反洗钱报告编号','场景类型','交易ID','客户编号','交易日期','明细来源','业务种类','业务条线','报送业务条线','明细序号','定活存标志','账卡标志','客户账号','客户名称','对公对私标志','客户年龄','国际卡卡币种','币种代码','存款种类','可售产品编号','资金用途代码','客户类型代码','交易时间','交易金额','折人民币金额','折美元金额','借贷标志','收付标志','交易种类','交易方式','汇款种类','交易渠道种类','交易流水号','全局事件跟踪号','交易柜员号','交易代码','交易机构','交易机构名称','交易发生地','交易所在国家地区代码','交易方向','凭证号码','凭证种类','摘要代码','摘要描述','账户性质','账户类型','资金用途','开户机构','开户机构名称','开户机构行政区划','反洗钱机构','反洗钱机构名称','开户日期','销户日期','上次明细交易日','产品种类','交易对手系统账号','交易对手账号修饰符','交易对手账户类型','交易对手账户性质','交易对手对公对私标志','交易对手客户账号','交易对手客户编号','交易对手客户名称','交易对手本外行标识','交易对手证件号码','交易对手证件类型','交易对手证件类型说明','交易对手商户编号','交易对手商户种类','交易对手开户机构','交易对手开户机构行政区划','交易对手定活存标志','交易对手金融机构代码','交易对手金融机构名称','交易对手金融机构行政区划','交易对手金融机构代码网点类型','交易对手国籍地区','终端信息','大额豁免标志','老可疑豁免标志','新可疑豁免标志','代理人姓名','代理人证件类型','代理人证件类型说明','代理人证件号码','代理人电话','代理人国籍地区','是否被代办','是否跨境交易','结算类型现金转账消费','是否跨行交易','是否异地交易','补录机构','账户余额','备注1','备注2']
            df_流水.to_csv(output_path +file.split('.')[0]+'.csv', encoding = 'utf-8',index = None)
            print('流水Done！')
            df_流水汇总 = df_流水汇总.append(df_流水)


# 以下对流水拆分一人一表
if not os.path.exists(output_path + '拆分'):
    os.mkdir(output_path + '拆分')
df_分编号 = df_流水汇总.groupby(['客户编号'],as_index = False).size()
print(len(df_分编号))

for i in df_分编号.index:
    df_every = df_流水汇总.groupby(['客户编号'],as_index = False).get_group(df_分编号['客户编号'][i]).sort_values(by = ['客户账号','交易日期','交易时间'],ascending=[True,True,True])
    if len(df_every)<655360:
        df_every.to_excel(output_path +'拆分\\'+ str(df_every['客户名称'].iloc[0])+str(df_every['客户编号'].iloc[0])+'.xlsx',index = None)
        print(i,end = ' ')
    else:
        size = df_every.index.size
        limit = 500000
        sheets = int(size / limit)+1

        with pd.ExcelWriter(output_path +'拆分\\'+ str(df_every['客户名称'].iloc[0])+str(df_every['客户编号'].iloc[0])+'.xlsx') as writer:
            for j in range(sheets):
                start = limit * j
                stop = limit * (j+1)
                print(str(i)+'-'+str(j),end = ' ')
                data = df_every.iloc[start:stop].astype(str).replace('nan','')
                data.to_excel(writer, sheet_name='sheet'+str(j),index = False)
print('Done!')
