# 现有一个循环发电场样本数据集，其中包括训练集（ccpp_train.txt文件）和测试集（ccpp_test.txt文件）。
# 数据集格式如下：

# AT（温度）	V（压力）	AP（湿度）	RH（压强）	PE（输出电力）
# 8.34	40.77	1010.84	90.01	480.48
# 23.64	58.49	1011.4	74.2	445.75
# 29.74	56.9	1007.15	41.91	438.76
#
# 请通过Python实现线性回归模型，并用此模型预测输出电力，具体要求如下：
# 完成数据集的读取
# 实现代价函数
# 实现梯度下降函数
# 要求输出迭代过程中的代价函数值
# 完成测试集的数据预测，并计算在测试集上的代价函数值
# 以横轴为真实值，纵轴为预测值，画出散点图mei
''''''


# 每100次输出一次训练集迭代过程中的代价值输出测试集精度，
# 计算测试集上的代价


import numpy as np
from numpy import *
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression

# from pylab import *                             #显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']  #显示中文

#加载数据
train_data=np.loadtxt('数据.txt',delimiter=',')


#特征缩放
# X=train_data[:,:-1]
# mu=np.mean(X,0)               #求X的平均值mu
# sigma=np.std(X,0,ddof=1)    #求标准差
# X-=mu                        #利用广播机制,X-平均值
# X/=sigma                     #利用广播机制，X/sigma=标准差
#
# #数据标准化
# m,f=train_data.shape        #样本个数m,特征数f
# X=np.c_[np.ones(m),X]

X = np.c_[train_data[:,:-1]]
y=np.c_[train_data[:,-1]]

print(X,y)


# 1. 定义计算代价函数
def costFunction(X,y,theta,lamda=1.0):
    m=y.size
    # J = (1.0/(2*m))*np.sum(np.square(X.dot(theta)-y))
    J = (1.0/(2*m))*((X.dot(theta)-y).T.dot(X.dot(theta)-y))
    return J

# 2.定义计算梯度下降的函数
def gradDes(X,y,theta=[[0],[0]],alpha=0.001,num_iters=15000):
    m,f=X.shape
    theta=np.zeros((f,1))
    J_histories=np.zeros(num_iters)
    for i in range(num_iters):
        J_histories[i]=costFunction(X,y,theta)
        deltatheta = (1.0/m)*(X.T.dot(X.dot(theta)-y))
        theta = theta - alpha*deltatheta
    return J_histories,theta

#3.调用代价函数取得代价函数和theta值
J_history,theta=gradDes(X,y)
print(theta)
print(f"特征方程：{theta[0]}+{theta[1]}*x1+{theta[2]}*x2")

# plt.figure('代价函数')
# plt.xlabel('迭代步数')
# plt.ylabel('代价')
# plt.plot(J_history)
# plt.show()


print("=="*100)
# print(train_data[:,0:-1])
# print(train_data[:,-1])

print(train_data[:,0])
print(train_data[:,1])
print(train_data[:,-1])


#4.训练集画图
plt.figure('数据关系图')
plt.scatter(train_data[:,0],train_data[:,-1],c='r',label='1')
plt.scatter(train_data[:,1],train_data[:,-1],c='b',label='2')
# plt.plot(train_data[:,0],train_data[:,-1],c='r',label = '1')
# plt.plot(train_data[:,1],train_data[:,-1],c='b',label = '2')
plt.plot(train_data[:,0:-1],train_data[:,-1],c='y',label = '2')
plt.xlabel("自变量")
plt.ylabel("因变量")

plt.legend(loc='upper right')
plt.show()






sys.exit()






#5.加载测试集并缩放和标准化
test_data=np.loadtxt('ccpp_test.txt',delimiter=',')
m,f=test_data.shape
# #测试集特征缩放
test_X=test_data[:,0:4]
mu=np.mean(test_X,0)               #求X的平均值mu
sigma=np.std(test_X,0,ddof=1)    #求标准差
test_X-=mu                        #利用广播机制,X-平均值
test_X/=sigma     #利用广播机制，X/sigma=标准差
#
# # ddofValue=0 表示样本标准差分母是n
# #
# # ddofValue=1 表示样本标准差分母是n-1
# #
# # ddofValue=2 表示样本标准差分母是n-2
#
# #测试集的预处理
test_X=np.c_[np.ones(m),test_X]
test_y=np.c_[test_data[:,-1]]
#
#
# #测试集预测值
predict_y=test_X.dot(theta)

# #测试集画图
plt.figure('测试集实际值和预测值')
plt.scatter(test_y,predict_y,c='r',label='预测值')
plt.scatter(test_y,test_y,label='真实值')
plt.legend(loc='upper left')
plt.show()

def score(X,y,theta):
     h=np.dot(X,theta)
     y_mean=np.mean(y)
     u = np.sum((h-y)**2)   # 计算预测值与真实值的方差
     v = np.sum((y - y_mean)**2) # 计算真实值方差
     score = 1- u/v
     return score
