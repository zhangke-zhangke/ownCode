import pandas as pd
import numpy as np
import scipy.stats
import pymysql
import sys
import re
import flask


def reverse_df(crash_result):
    # 纵向表转横向
    new_df = crash_result.set_index(['card_no', 'term_id'])['param_value']
    new_df = new_df.unstack().rename_axis(columns=None).reset_index().fillna(0)

    # 封装成dataframe返回
    df = new_df.iloc[:, -1]
    df_col = new_df.columns[-1]

    return pd.DataFrame(df, columns=[f'{df_col}'])


result_args_section = {}
def calculate_parser(by,all_data,all_sample_num,stop_sample_pro=0.1, t=0):
    global result_args_section

    # 求一些值
    target_info = dict(all_data['target'].value_counts())
    black_sample = target_info.get(1)   # 黑样本个数
    max_x = max(all_data[f'{all_data.columns[0]}'])
    min_x = min(all_data[f'{all_data.columns[0]}'])

    # 分段排序
    result, sentence = ChiMerge3(all_data, 100, [0, 1], pvalue_edge=0.1)
    result['sample_info'] = result[1] + result[0]
    result['recall_pro'] = result[1].apply(lambda x: x / black_sample)
    result['precision_pro'] = result[1] / result['sample_info']
    result.sort_values(by='recall_pro', ascending=False, inplace=True)

    # 取出排名第一的数据，并取出区间条件
    top_one = result.iloc[t]
    condition = top_one['interval']
    is_and = False
    is_condition = False

    # 区间存储
    args_section = []
    # 运算符
    operation = ''
    # 解析排名第一的区间情况
    if 'and' in condition:
        # 直接解析区间
        is_and = True
        for i in condition.split('and'):
            args_section.append(round(float(float(i.strip().replace('x>', '').replace('x<=', ''))),2))
    elif '<=' in condition or '<' in condition:
        # 解析小于
        operation = re.search(r'([<>]=?|==)', condition).group()
        args_section.append(min_x)
        args_section.append(round(float(float(condition.replace('x<=', '').replace('x<', ''))),2))
    elif '>=' in condition or '>' in condition:
        # 解析大于
        operation = re.search(r'([<>]=?|==)', condition).group()
        args_section.append(round(float(float(condition.replace('x>=', '').replace('x>', ''))),2))
        args_section.append(max_x)

    # 如果设置了样本占比则进行判断排名第一的区间是否满足样本阈值占比
    if stop_sample_pro != 0:
        # 查看排名第一的样本占比是否满足阈值  小于总样本的30%则停止继续细分
        if (top_one['sample_info'] / all_sample_num) > stop_sample_pro:
            is_condition = True
        else:
            is_condition = False

    is_continue = True
    print(is_and, is_condition, is_continue)
    print("参数调优区间：",args_section)

    # 递归循环调用直至满足条件
    if is_and == False and is_condition == True and is_continue == True:
        print("满足条件，开始细分！")
        a = str(all_data.columns[0]).replace('-','_')
        again_data = all_data.query(f'{a} >= {args_section[0]} & {a} <= {args_section[-1]}').reset_index(drop=True)
        if len(set(again_data['target'].tolist())) == 1:
            print('细分失败。原因：此次细分数据标签为0或全为1！')
            result_args_section[by] = args_section
        else:
            # 满足条件，并且标签不是一维，继续递归细分！
            calculate_parser(by,again_data, stop_sample_pro, 0)
    else:
        result_args_section[by] = args_section


def tagcount(series, tags):
    """
    统计该series中不同标签的数量，可以针对多分类
    series:只含有标签的series
    tags:为标签的列表，以实际为准，比如[0,1],[1,2,3]
    """
    result = []
    countseries = series.value_counts()
    for tag in tags:
        try:
            result.append(countseries[tag])
        except:
            result.append(0)
    return result


def ChiMerge3(df, num_split, tags=[1,2,3], pvalue_edge=0.1, biggest=10, smallest=3, sample=None):
    """
    df:只包含要分箱的参数列和标签两列
    num_split:初始化时划分的区间个数,适合数据量特别大的时候。
    tags：标签列表，二分类一般为[0,1]。以实际为准。
    pvalue_edge：pvalue的置信度值
    bin：最多箱的数目
    smallest:最少箱的数目
    sample:抽样的数目，适合数据量超级大的情况。可以使用抽样的数据进行分箱。百万以下不需要
    """

    variable = df.columns[0]
    flag = df.columns[1]
    # 进行是否抽样操作
    if sample != None:
        df = df.sample(n=sample)
    else:
        df

    # 将原始序列初始化为num_split个区间，计算每个区间中每类别的数量，放置在一个矩阵中。方便后面计算pvalue值。
    percent = df[variable].quantile([1.0 * i / num_split for i in range(num_split + 1)],
                                    interpolation="lower").drop_duplicates(keep="last").tolist()
    percent = percent[1:]
    np_regroup = []
    for i in range(len(percent)):
        if i == 0:
            tempdata = tagcount(df[df[variable] <= percent[i]][flag], tags)
            tempdata.insert(0, percent[i])
        elif i == len(percent) - 1:
            tempdata = tagcount(df[df[variable] > percent[i - 1]][flag], tags)
            tempdata.insert(0, percent[i])
        else:
            tempdata = tagcount(df[(df[variable] > percent[i - 1]) & (df[variable] <= percent[i])][flag], tags)
            tempdata.insert(0, percent[i])
        np_regroup.append(tempdata)
    np_regroup = pd.DataFrame(np_regroup)
    np_regroup = np.array(np_regroup)

    # 如果两个区间某一类的值都为0，就会报错。先将这类的区间合并，当做预处理吧
    i = 0
    while (i <= np_regroup.shape[0] - 2):
        check = 0
        for j in range(len(tags)):
            if np_regroup[i, j + 1] == 0 and np_regroup[i + 1, j + 1] == 0:
                check += 1
        """
        这个for循环是为了检查是否有某一个或多个标签在两个区间内都是0，如果是的话，就进行下面的合并。
        """
        if check > 0:
            np_regroup[i, 1:] = np_regroup[i, 1:] + np_regroup[i + 1, 1:]
            np_regroup[i, 0] = np_regroup[i + 1, 0]
            np_regroup = np.delete(np_regroup, i + 1, 0)
            i = i - 1
        i = i + 1

    # 对相邻两个区间进行置信度计算
    chi_table = np.array([])
    for i in np.arange(np_regroup.shape[0] - 1):
        temparray = np_regroup[i:i + 2, 1:]
        pvalue = scipy.stats.chi2_contingency(temparray, correction=False)[1]
        chi_table = np.append(chi_table, pvalue)
    temp = max(chi_table)

    # 把pvalue最大的两个区间进行合并。注意的是，这里并没有合并一次就重新循环计算相邻区间的pvalue，而是只更新影响到的区间。
    while (1):
        # 终止条件，可以根据自己的期望定制化
        if (len(chi_table) <= (biggest - 1) and temp <= pvalue_edge):
            break
        if len(chi_table) < smallest:
            break

        num = np.argwhere(chi_table == temp)
        for i in range(num.shape[0] - 1, -1, -1):
            chi_min_index = num[i][0]
            np_regroup[chi_min_index, 1:] = np_regroup[chi_min_index, 1:] + np_regroup[chi_min_index + 1, 1:]
            np_regroup[chi_min_index, 0] = np_regroup[chi_min_index + 1, 0]
            np_regroup = np.delete(np_regroup, chi_min_index + 1, 0)

            # 最大pvalue在最后两个区间的时候，只需要更新一个，删除最后一个。大家可以画图，很容易明白
            if (chi_min_index == np_regroup.shape[0] - 1):
                temparray = np_regroup[chi_min_index - 1:chi_min_index + 1, 1:]
                chi_table[chi_min_index - 1] = scipy.stats.chi2_contingency(temparray, correction=False)[1]
                chi_table = np.delete(chi_table, chi_min_index, axis=0)

            # 最大pvalue是最先两个区间的时候，只需要更新一个，删除第一个。
            elif (chi_min_index == 0):
                temparray = np_regroup[chi_min_index:chi_min_index + 2, 1:]
                chi_table[chi_min_index] = scipy.stats.chi2_contingency(temparray, correction=False)[1]
                chi_table = np.delete(chi_table, chi_min_index + 1, axis=0)

            # 最大pvalue在中间的时候，影响和前后区间的pvalue，需要更新两个值。
            else:
                # 计算合并后当前区间与前一个区间的pvalue替换
                temparray = np_regroup[chi_min_index - 1:chi_min_index + 1, 1:]
                chi_table[chi_min_index - 1] = scipy.stats.chi2_contingency(temparray, correction=False)[1]
                # 计算合并后当前与后一个区间的pvalue替换
                temparray = np_regroup[chi_min_index:chi_min_index + 2, 1:]
                chi_table[chi_min_index] = scipy.stats.chi2_contingency(temparray, correction=False)[1]
                # 删除替换前的pvalue
                chi_table = np.delete(chi_table, chi_min_index + 1, axis=0)

        # 更新当前最大的相邻区间的pvalue
        temp = max(chi_table)

    print("*" * 30)
    print("最终相邻区间的pvalue值为：\n",chi_table)
    print("*" * 30)

    # 把结果保存成一个数据框。
    """
    可以根据自己的需求定制化。我保留两个结果。
    1. 显示分割区间，和该区间内不同标签的数量的表
    2. 为了方便pandas对该参数处理，把apply的具体命令打印出来。方便直接对数据集处理。
        serise.apply(lambda x:XXX)中XXX的位置
    """
    # 将结果整合到一个表中，即上述中的第一个
    interval = []
    interval_num = np_regroup.shape[0]
    for i in range(interval_num):
        if i == 0:
            interval.append('x<=%f' % (np_regroup[i, 0]))
        elif i == interval_num - 1:
            interval.append('x>%f' % (np_regroup[i - 1, 0]))
        else:
            interval.append('x>%f and x<=%f' % (np_regroup[i - 1, 0], np_regroup[i, 0]))

    result = pd.DataFrame(np_regroup)
    result[0] = interval
    result.columns = ['interval'] + tags

    # 整理series的命令，即上述中的第二个
    premise = "str(0) if "
    length_interval = len(interval)
    for i in range(length_interval):
        if i == length_interval - 1:
            premise = premise[:-4]
            break
        premise = premise + interval[i] + " else " + 'str(%d+1)' % i + " if "

    return result, premise



def get_data(host,user,password,port,database):
    # connection = pymysql.connect(host='172.30.6.184', user='root', password='zqykj123', database='finance',port=int(3306))
    connection = pymysql.connect(host=host, user=user, password=password, database=database,port=int(port))
    try:
        with connection.cursor() as cursor:
            sql = '''
                select model_id,group_id,rule_id,term_id,param_value,card_no,target
                from et_rule_term_value
                where create_time > date_add(now(),interval -3 month)
            '''
            cursor.execute(sql)
            res = cursor.fetchall()
            col = [item[0] for item in cursor.description]
            result_data = pd.DataFrame(res, columns=col)
    #         result_data = result_data.apply(pd.to_numeric, errors='ignore')
    except Exception as e:
        print(e)
    finally:
        cursor.close()

    return result_data


def reverse_col(result_data,stop_sample_pro):
    # 行转列
    df_by = result_data.groupby(by=['model_id', 'group_id', 'rule_id'])
    for by, all_frame in df_by:
        # 将多特征frame转成多个单特征frame
        every_frame = all_frame.groupby(by=['term_id'])
        for by, frame in every_frame:
            print(f'======================================{by}开始参数调优======================================')
            try:
                if len(set(frame['target'].tolist())) == 1:
                    print(f'{by}只有一维度标签\n')
                    continue
                else:
                    data_x = reverse_df(frame)
                    data_x = data_x.apply(pd.to_numeric, errors='ignore')
                    data_y = frame['target'].reset_index(drop=True)
                    # x 和 y 拼接
                    all_data = data_x.copy()
                    all_data.insert(1, 'target', data_y.astype(np.int))

                    all_sample_num = all_data.shape[0]  # 总样本个数
                    calculate_parser(by,all_data,all_sample_num,stop_sample_pro)
            except:
                print(f'{by}数据异常，不做调优推荐！\n')
            else:
                print(f'======================================{by}参数调优成功======================================\n')

    return result_args_section


server = flask.Flask(__name__)
@server.route('/argsAdaption',methods=['get','post'])
def run():
    # 接收API参数
    host = flask.request.values.get('host')
    user = flask.request.values.get('user')
    password = flask.request.values.get('password')
    port = flask.request.values.get('port')
    database = flask.request.values.get('database')
    stop_sample_pro = float(flask.request.values.get('stop_sample_pro'))

    result_data = get_data(host,user,password,port,database)
    # Python会将字符串中的-解析成减号，为后续处理，先替换成_。
    result_data['term_id'] =  result_data['term_id'].apply(lambda x:str(x).replace('-','_'))
    result = reverse_col(result_data,stop_sample_pro)
    print("\n参数调优结果：",result)


    return_result = []
    for key,value in result.items():
        info = {}
        info['term_id'] = key.replace('_','-')
        info['args_section'] = value
        return_result.append(info)
    print(return_result)


    return flask.jsonify(return_result)




if __name__ == '__main__':
    server.run(host='0.0.0.0',port='9999',debug=True)

    # run()

    # http://172.30.4.81:9999/argsAdaption?host=172.30.6.184&user=root&password=zqykj123&database=finance&port=3306&stop_sample_pro=0.3
