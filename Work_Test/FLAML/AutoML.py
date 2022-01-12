from flaml import AutoML
from sklearn.datasets import load_iris
from flaml import ml
from sklearn.datasets import load_boston
import pandas as pd
from sklearn.metrics import classification_report,confusion_matrix,f1_score,accuracy_score,precision_score,recall_score
import sys


iris = load_iris()
iris_data = pd.concat([pd.DataFrame(iris.data),pd.Series(iris.target)],axis=1)
iris_data.columns = ["_".join(feature.split(" ")[:2]) for feature in iris.feature_names]+["target"]
iris_data = iris_data[(iris_data.target==0) |(iris_data.target==1)]


flaml_automl = AutoML()
flaml_automl.fit(pd.DataFrame(iris_data.iloc[:,:-1]),iris_data.iloc[:,-1],metric='f1',time_budget=2,estimator_list=['lgbm','xgboost'],log_training_metric =True,log_file_name='')


# iris = load_boston()
# iris_data = pd.concat([pd.DataFrame(iris.data),pd.Series(iris.target)],axis=1)
# iris_data.columns = ["_".join(feature.split(" ")[:2]) for feature in iris.feature_names]+["target"]
# iris_data = iris_data[(iris_data.target==0) |(iris_data.target==1)]

# flaml_automl = AutoML()
# flaml_automl.fit(pd.DataFrame(iris_data.iloc[:,:-1]),iris_data.iloc[:,-1],time_budget=10,estimator_list=['lgbm','xgboost'])

try:
    print(flaml_automl.best_model)
except:
    print("无best_model属性")
print(flaml_automl.estimator_list)
print("最优模型",flaml_automl.model)
print("最优参数",flaml_automl.best_config)
print("训练时间",flaml_automl.best_config_train_time)
print("分类器",flaml_automl.best_estimator)
print("误差",flaml_automl.best_loss)
print("模型精度:",(1-flaml_automl.best_loss))
print("每个分类器最优误差",flaml_automl.best_loss_per_estimator)

flaml_result = flaml_automl.predict(pd.DataFrame(iris_data.iloc[:,:-1]))

print("混淆矩阵:\n",confusion_matrix(iris_data.iloc[:,-1],flaml_result))
print("分类报告:\n",classification_report(iris_data.iloc[:,-1],flaml_result))
print("召回率:",recall_score(iris_data.iloc[:,-1],flaml_result))
print("准确率:",accuracy_score(iris_data.iloc[:,-1],flaml_result))
print("f1分值:",f1_score(iris_data.iloc[:,-1],flaml_result))
print("精确率:",precision_score(iris_data.iloc[:,-1],flaml_result))
# automl_f1 = ml.f1_score(iris_data.iloc[:,-1],flaml_result,average='weighted')
# print(automl_f1)

#



# automl = AutoML()
# automl_settings = {
#     "time_budget": 10,  # in seconds
#     "metric": 'accuracy',
#     "task": 'classification'
# }
#
#
# X_train, y_train = load_iris(return_X_y=True)
# print(X_train,y_train)
#
#
# # Train with labeled input data
# automl.fit(X_train=X_train, y_train=y_train,
#            **automl_settings)
# print(automl.predict_proba(X_train).shape)
# # Export the best model
# print(automl.model)
#
# print(automl.estimator_list)
# print('Best ML leaner:', automl.best_estimator)
# print('Best hyperparmeter config:', automl.best_config)
# print('Best accuracy on validation data: {0:.4g}'.format(1-automl.best_loss))
# print('Training duration of best run: {0:.4g} s'.format(automl.best_config_train_time))



