import numpy as np
import warnings
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']      #在图中正确显示中文
plt.rcParams['axes.unicode_minus']=False    # 默认是使用Unicode负号，设置正常显示字符，如正常显示负号
warnings.filterwarnings('ignore')



def h(X,theta):
    h=np.dot(X,theta)
    return h
def J(X,Y,theta,m):
    e=np.dot(X,theta)-Y
    Jold=(1.0/(2*m))*np.dot(e.T,e)
    return Jold
def tidu(X,Y,alpha=0.01,itears=20000):
    m,n=X.shape
    theta,Jold=np.zeros((n,1)),np.zeros((itears))
    for i in range(itears):
        H=h(X,theta)
        Jold[i]=J(X,Y,theta,m)
        if i%100==0:
            score3=score1(X,Y,theta)
            print(score3)
        grad=(1.0/m)*np.dot(X.T,(H-Y))
        theta-=alpha*grad
    return theta,Jold

def score1(test_X,test_Y,theta):
    h=np.dot(test_X,theta)
    y_mean=np.mean(test_Y,axis=0)  #真实值的平均数
    u=np.sum((h-test_Y)**2)      #预测值和真实值之间的方差
    v=np.sum((test_Y-y_mean)**2)   #真实值和真实值的平均值的方差
    score2= 1-u / v
    return score2

if __name__ == '__main__':
    train_data=np.loadtxt('数据.txt',delimiter=",")
    x=train_data[:,:-1]
    y=train_data[:,-1]

    #特征缩放
    # X=(x-np.mean(x,axis=0))/np.std(x,ddof=1,axis=0)

    # 数据处理
    X = np.c_[np.ones(len(x)), x]
    Y = np.c_[y]

    theta, Jold = tidu(X, Y)
    print(theta)
    print(Jold)

    #特征方程
    # print(f"特征方程为:\ny={theta[0]}+{theta[1]}*x1+{theta[2]}*x2+{theta[3]}*x3+{theta[4]}*x4")
    print(f"\n特征方程为:y={theta[0]}+{theta[1]}*x1+{theta[2]}*x2")


    #4.训练集画图
    plt.figure('数据关系图',figsize=(16,8))
    plt.subplot(131)
    plt.scatter(train_data[:,0],train_data[:,-1],c='r',label='X1')
    plt.plot(train_data[:,0],train_data[:,-1])
    plt.xlabel("自变量1")
    plt.ylabel("因变量")
    plt.legend(loc='upper right')


    plt.subplot(132)
    plt.scatter(train_data[:,1],train_data[:,-1],c='b',label='X2')
    plt.plot(train_data[:,1],train_data[:,-1])
    plt.xlabel("自变量2")
    plt.ylabel("因变量")
    plt.legend(loc='upper right')


    plt.subplot(133)
    plt.scatter(train_data[:, 0], train_data[:, -1], c='r', label='X1')
    plt.scatter(train_data[:, 1], train_data[:, -1], c='b', label='X2')
    plt.plot(train_data[:,0:-1],train_data[:,-1],c='y')

    plt.legend(loc='upper right')
    plt.show()
