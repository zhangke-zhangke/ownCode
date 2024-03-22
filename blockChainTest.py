import flask
import os
import requests
import pandas as pd


uploadFilePath = '/usr/local/zqykj/finance/blockchainCollide/upload/'
downloadFilePath = '/usr/local/zqykj/finance/blockchainCollide/download/'
blockChainHost = ''
blockChainPort = ''
financeHost = '172.30.6.205'
financePort = '8083'



# 判断待上传文件是否存在    true 存在 ； False 不存在
def fileExists(taskId):
    if not os.path.exists(uploadFilePath + taskId + '/blockchainCollide.xlsx'):
        return False
    else:
        return True


# Python向java同步信息
def SyncInfoApi(returnInfo):
    try:
        req = requests.post(f'http://{financeHost}:{financePort}/finance/mainService/dataPython/pythonTaskInfoSync',json=returnInfo)
    except Exception as e:
        print(f'python同步信息出错，错误信息：{e}')
    else:
        print('python同步信息完成')



'''
    python 服务主入口
'''
server = flask.Flask(__name__)
@server.route('/uploadFile',methods=['get','post'])
def run():
    userName = flask.request.values.get('userName')
    password = flask.request.values.get('password')
    taskId = flask.request.values.get('taskId')
    print(f'python拿到以下参数: userName = {userName},password = {password},taskId = {taskId}')

    # 初始化参数
    area = ''   # 失败返回原因
    successfulCount = 0 # 成功的话返回数量
    runFlag = 0    # 程序成功与失败    成功 0 ； 失败 1


    # 验证文件是否存在
    if fileExists(taskId) == False:
        area = '文件不存在，无法上传！'
        runFlag = 1
        print(area)
        returnErrorInfo = {"taskId":taskId,"status":runFlag,"result":area,"blockchainCollideDetails":None}
        print(returnErrorInfo)
        # 调用接口同步成功信息
        SyncInfoApi(returnErrorInfo)

        return '1'

    # 存在即继续
    # 请求区块链上传文件接口
    # req = requests.post(f'http://{blockChainHost}:{blockChainPort}/upload/xx/xxxx/xxx/',data=data,headers=headers)
    # print(req.json())


    df = pd.read_excel(uploadFilePath + taskId + '/blockchainCollide.xlsx')
    allDetails = []
    for i in range(df.shape[0]):
        details = {}
        details['name'] = df['姓名或者企业名'].iloc[i]
        details['type'] = df['证件类型'].iloc[i]
        details['idCard'] = df['证件号码'].iloc[i]
        details['status'] = 1   # 碰撞状态
        allDetails.append(details)

    # 封装结果返回
    returnSuccessfulInfo = {}
    returnSuccessfulInfo['taskId'] = taskId
    returnSuccessfulInfo['status'] = runFlag
    returnSuccessfulInfo['result'] = df.shape[0]
    returnSuccessfulInfo['blockchainCollideDetails'] = allDetails
    print(returnSuccessfulInfo)

    # 调用接口同步成功信息
    SyncInfoApi(returnSuccessfulInfo)


    # 保存数据文件
    if not os.path.exists(downloadFilePath + taskId):
        os.mkdir(downloadFilePath + taskId)
    df.to_excel(downloadFilePath + taskId + f'/{taskId}.xlsx',encoding='utf-8',index=False)



    return '0'





if __name__ == '__main__':
    from waitress import serve

    serve(server,host='0.0.0.0',port='8888')
    # # 启动服务
    # server.run('0.0.0.0',port='8888',debug=True)













