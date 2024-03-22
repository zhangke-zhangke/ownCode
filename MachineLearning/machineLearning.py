# 导入包
from sklearn.tree import DecisionTreeClassifier,export_graphviz
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,precision_score,recall_score
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
import graphviz
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error
from sklearn.metrics import plot_roc_curve
sns.set(style="whitegrid",  color_codes=True)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 在图中正确显示中文
plt.rcParams['axes.unicode_minus'] = False  # 默认是使用Unicode负号，设置正常显示字符，如正常显示负号
# import xgboost as xgb
# 基于scikit-learn接口
from xgboost import XGBClassifier
import warnings
warnings.filterwarnings("ignore")


# path = r"C:\Users\1\Desktop"+"\\"
fileName = "feature_data_poc.csv"
data = pd.read_csv(fileName, index_col=None)
X = data.drop(['target'], axis=1)
Y = data.target

##划分训练集，测试集，验证集=6:3:1
Xtrain, X_all, Ytrain, Y_all = train_test_split(X, Y, test_size=0.2,random_state=666,stratify=Y)
Xtest,Xval,Ytest,Yval = train_test_split(X_all,Y_all,test_size=0.25,random_state=666,stratify=Y_all)

print(Xtrain.shape,Xtest.shape,Xval.shape)
print(Ytrain.shape,Ytest.shape,Yval.shape)

# ##训练集
# data_train = pd.concat([Ytrain.to_frame(),Xtrain],axis=1)
# data_train.to_csv("train.csv",index=None)
#
# ##测试集
# data_test = pd.concat([Ytest.to_frame(),Xtest],axis=1)
# data_test.to_csv("test.csv",index=None)

# ##保存验证数据集
# data_val = Xval
# data_val.insert(0,"target", np.nan)
# data_val.to_csv("validation.csv",index=None)


def plot_learning_curve(algo,X_train,X_test,y_train,y_test):
    train_score = []
    test_score = []

    for i in range(1,len(X_train)+1):
        algo.fit(X_train[:i],y_train[:i])
        y_train_predict = algo.predict(X_train[:i])
        train_score.append(mean_squared_error(y_train[:i],y_train_predict ))

        y_test_predict = algo.predict(X_test)
        test_score.append(mean_squared_error(y_test,y_test_predict))

    plt.plot([i for i in range(1,len(X_train)+1)], np.sqrt(train_score),label = 'Train')
    plt.plot([i for i in range(1,len(X_train)+1)], np.sqrt(test_score),label = 'Test')
    plt.legend()
    plt.axis([0,len(X_train)+1,0,4])
    plt.show()



def DecisonTree(Xtrain, Xtest, Ytrain, Ytest):
    c = 0
    for i in range(1, 30, 3):
            c += 1
            print(c)
            dtc = DecisionTreeClassifier(class_weight="balanced",random_state=0,max_depth=i)
            dtc = dtc.fit(Xtrain,Ytrain)
            score_c = dtc.score(Xtest,Ytest)
            dtc_y_pred = dtc.predict(Xtest)

            ##决策树
            print(confusion_matrix(Ytest, dtc_y_pred, labels=[1, 0]))
            print("准确率: "+'{:.6f}'.format(score_c))
            print("精确率: "+'{:.6f}'.format(precision_score(Ytest,dtc_y_pred)))
            print("召回率: "+'{:.6f}'.format(recall_score(Ytest,dtc_y_pred)))

            # plot_learning_curve(dtc, Xtrain, Xtest, Ytrain, Ytest)

            plot_roc_curve(dtc, Xtest, Ytest)  # test_x：测试样本集；test_y：测试标签集
            plt.title(f'ROC_max_depth_{i}'+'\n'+
                      "准确率: " + '{:.6f}'.format(score_c) + ' ' +
                      "精确率: " + '{:.6f}'.format(precision_score(Ytest,dtc_y_pred))+ ' ' +
                      "召回率: " + '{:.6f}'.format(recall_score(Ytest, dtc_y_pred)))
            plt.axis = 'off'  # 关闭坐标 让图更美观
            plt.savefig(f'./imgs/max_depth_{i}.png')




    # dot_data = export_graphviz(dtc
    #                                 # , feature_names= Xtrain.columns
    #                                 , class_names=['是', '否', '贝尔摩德']
    #                                 ,out_file ='tree.pdf'
    #                                 ,rounded = True
    #                                 ,precision=1
    #                                 , filled=True
    #                                 )  # 圆角
    #
    # graph = graphviz.Source(dot_data)
    # from IPython.display import  display
    # display(graphviz.Source(dot_data))
    # graph.write_png("tree.png")

    # dot_data = tree.export_graphviz(dtc,
    #                                 class_names=['是', '否', '贝尔摩德'],
    #                                 rounded = True,
    #                                 precision=1,
    #                                 filled=True)
    # graph = graphviz.Source(dot_data)
    # graph.render("dt")


def RandomForestTree(Xtrain, Xtest, Ytrain, Ytest):
    rfc = RandomForestClassifier(n_estimators=100, criterion='entropy', max_depth=None, min_samples_split=2, min_samples_leaf=1,
                                             min_weight_fraction_leaf=0.0, max_features='sqrt',  min_impurity_decrease=0.0,
                                             class_weight = {0:1,1:500} , random_state=0, bootstrap=False, oob_score=False,
                                             n_jobs=-1, verbose=0, warm_start=False)
    rfc = rfc.fit(Xtrain, Ytrain)
    score_r = rfc.score(Xtest, Ytest)
    rfc_y_pred = rfc.predict(Xtest)
    ##随机森林
    print(confusion_matrix(Ytest, rfc_y_pred, labels=[1, 0]))
    print("准确率: "+'{:.6f}'.format(score_r))
    print("精确率: "+'{:.6f}'.format(precision_score(Ytest,rfc_y_pred)))
    print("召回率: "+'{:.6f}'.format(recall_score(Ytest,rfc_y_pred)))

def LogisticRegressionClassifier(Xtrain, Xtest, Ytrain, Ytest):
    lr = LogisticRegression()
    lr = lr.fit(Xtrain, Ytrain)
    score_r = lr.score(Xtest, Ytest)
    lr_y_pred = lr.predict(Xtest)
    ##逻辑回归
    print(confusion_matrix(Ytest, lr_y_pred, labels=[1, 0]))
    print("准确率: "+'{:.6f}'.format(score_r))
    print("精确率: "+'{:.6f}'.format(precision_score(Ytest,lr_y_pred)))
    print("召回率: "+'{:.6f}'.format(recall_score(Ytest,lr_y_pred)))

def SVMclassifier(Xtrain, Xtest, Ytrain, Ytest):
    svc = LinearSVC(C=1e5)
    svc = svc.fit(Xtrain, Ytrain)
    score_r = svc.score(Xtest, Ytest)
    svc_y_pred = svc.predict(Xtest)
    ##SVM
    print(confusion_matrix(Ytest, svc_y_pred, labels=[1, 0]))
    print("准确率: "+'{:.6f}'.format(score_r))
    print("精确率: "+'{:.6f}'.format(precision_score(Ytest,svc_y_pred)))
    print("召回率: "+'{:.6f}'.format(recall_score(Ytest,svc_y_pred)))

def KNN(Xtrain, Xtest, Ytrain, Ytest):
    KNN = KNeighborsClassifier()
    KNN = KNN.fit(Xtrain, Ytrain)
    score_r = KNN.score(Xtest, Ytest)
    KNN_y_pred = KNN.predict(Xtest)
    ##knn
    print(confusion_matrix(Ytest, KNN_y_pred, labels=[1, 0]))
    print("准确率: "+'{:.6f}'.format(score_r))
    print("精确率: "+'{:.6f}'.format(precision_score(Ytest,KNN_y_pred)))
    print("召回率: "+'{:.6f}'.format(recall_score(Ytest,KNN_y_pred)))

def xgboost(Xtrain, Xtest, Ytrain, Ytest):
    xgb = XGBClassifier(eval_metric=['logloss','auc','error'])
    xgb = xgb.fit(Xtrain,Ytrain)
    score_c = xgb.score(Xtest,Ytest)
    xgb_y_pred = xgb.predict(Xtest)

    ##xgboost
    print(confusion_matrix(Ytest, xgb_y_pred, labels=[1, 0]))
    print("准确率: "+'{:.6f}'.format(score_c))
    print("精确率: "+'{:.6f}'.format(precision_score(Ytest,xgb_y_pred)))
    print("召回率: "+'{:.6f}'.format(recall_score(Ytest,xgb_y_pred)))

def polt():
    #
    # #目的是带大家复习一下交叉验证
    # #交叉验证：是数据集划分为n分，依次取每一份做测试集，每n-1份做训练集，多次训练模型以观测模型稳定性的方法
    # from sklearn.model_selection import cross_val_score
    # import matplotlib.pyplot as plt
    # rfc = RandomForestClassifier(n_estimators=25)
    # rfc_s = cross_val_score(rfc,wine.data,wine.target,cv=10)
    # clf = DecisionTreeClassifier()
    # clf_s = cross_val_score(clf,wine.data,wine.target,cv=10)
    # plt.plot(range(1,11),rfc_s,label = "RandomForest")
    # plt.plot(range(1,11),clf_s,label = "Decision Tree")
    # plt.legend()
    # plt.show()
    # #====================一种更加有趣也更简单的写法===================#
    # """
    # label = "RandomForest"
    # for model in [RandomForestClassifier(n_estimators=250),DecisionTreeClassifier()]:
    #    score = cross_val_score(model,wine.data,wine.target,cv=10)
    #    print("{}:".format(label)),print(score.mean())
    #    plt.plot(range(1,11),score,label = label)
    #    plt.legend()
    #    label = "DecisionTree"
    # """
    # superpa =[]
    # for i in range(200):
    #     rfc = RandomForestClassifier(n_estimators=i+1,n_jobs=-1)
    #     rfc_s = cross_val_score(rfc,wine.data,wine.target,cv=10).mean()
    #     superpa.append(rfc_s)
    # plt.figure()
    # plt.plot(range(1,201),superpa)
    # plt.show()
    return 0





if __name__ == "__main__":
    cust_info = ['cst_no', 'cst_name']
    Xtrain = Xtrain.drop(cust_info,axis=1)
    Xtest = Xtest.drop(cust_info,axis=1)
    print("决策树:")
    DecisonTree(Xtrain, Xtest, Ytrain, Ytest)

    import sys
    sys.exit()

    print("\n"+"随机森林:")
    RandomForestTree(Xtrain, Xtest, Ytrain, Ytest)
    print("\n"+"逻辑回归:")
    LogisticRegressionClassifier(Xtrain, Xtest, Ytrain, Ytest)
    print("\n"+"svm:")
    SVMclassifier(Xtrain, Xtest, Ytrain, Ytest)
    # print("\n"+"knn:")
    # KNN(path)
    print("\n"+"xgboost:")
    xgboost(Xtrain, Xtest, Ytrain, Ytest)
