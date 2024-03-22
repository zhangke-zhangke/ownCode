import pandas as pd   #数据处理
from pylab import *   # 目前已知 numpy  和 matplotlib
from sklearn.preprocessing  import StandardScaler,MinMaxScaler,RobustScaler #特征缩放1,标准化2,最大最小归一化3,标量健壮性
from sklearn.decomposition import PCA
from sklearn.linear_model import SGDRegressor,SGDClassifier,Lasso,Ridge,LogisticRegression\
    ,LinearRegression,stochastic_gradient #随机梯度回归器，随机梯度分类器,套索回归，岭回归,逻辑回归，线性回归,随机梯度下降
from sklearn.preprocessing import PolynomialFeatures  #多项式回归
from sklearn.pipeline import Pipeline  #管道机制
from sklearn.model_selection import GridSearchCV   #网格搜索
from sklearn.model_selection import cross_val_predict,cross_val_score\
    ,cross_validate    #第一个是出现交叉验证的结果，第二个是出现交叉验证的分数，第三个是交叉验证的交互
from sklearn.preprocessing import OneHotEncoder,\
    LabelEncoder,MultiLabelBinarizer #第一个是独热编码 ，第二个是将字符转化为数字，第三个是多标签
from sklearn.neighbors import KNeighborsClassifier,KNeighborsRegressor  # KNN解决分类，KNN解决回归问题
from sklearn.naive_bayes import BernoulliNB,GaussianNB,MultinomialNB   #伯努利朴素贝叶斯，高斯朴素贝叶斯，多项式朴素贝叶斯
from sklearn.ensemble import AdaBoostRegressor,AdaBoostClassifier,\
    BaggingClassifier,BaggingRegressor,RandomForestClassifier,RandomForestRegressor,GradientBoostingClassifier\
    ,GradientBoostingRegressor   #串行1,2 Boosting 3Bagging,4,5随机森林 6 Bagging并行算法  #提升树分类， 提升树回归
from sklearn.tree import DecisionTreeClassifier,DecisionTreeRegressor   #分类树，回归树
from sklearn.cluster import KMeans,DBSCAN,MiniBatchKMeans,\
    mean_shift,AgglomerativeClustering   # 划分聚类的 密度聚类的  小数据划分聚类   均值平移聚类，   凝聚聚类（分层）
from sklearn.mixture import GaussianMixture,BayesianGaussianMixture    #混合高斯模型    混合贝叶斯高斯模型
from sklearn.neural_network import MLPClassifier,MLPRegressor   #神经网络分类，神经网络回归
from sklearn.svm import SVC   #支持向量机
import tensorflow.contrib as con
# con.seq2seq.sequence_loss()    代价函数
import tensorflow as tf
# tf.nn.rnn_cell.LSTMCell     #LSTM 算法模型
# tf.nn.rnn_cell.BasicRNNCell   RNN模型
from tensorflow.python.ops.rnn  import dynamic_rnn #动态RNN
import imageio
#img = imageio.imread(image_path)
from skimage.transform import resize
#scaled_temp = resize(cropped_temp,output_shape=(image_size, image_size))
#imsave 变为
import imageio
#imageio.imwrite(output_filename,scaled_temp)






