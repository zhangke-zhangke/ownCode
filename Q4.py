
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MinMaxScaler,StandardScaler
import pandas as pd
from sklearn.metrics import ConfusionMatrixDisplay,classification_report,confusion_matrix
from sklearn.model_selection import GridSearchCV, KFold




if __name__ == '__main__':
    data = pd.read_excel(r'C:\Users\dell\Desktop\dataset.xlsx')
    print(data)

    # 1 2
    # 6 7
    # 3 4 5
    case = 3
    two_class_flag = True

    if case == 1:
        class_type = [6,7]
        new_data = data[data['Species_num'].isin(class_type)]
    elif case == 2:
        class_type = [1, 2]
        new_data = data[data['Species_num'].isin(class_type)]
    elif case == 3:
        class_type = [3,4,5]
        new_data = data[data['Species_num'].isin(class_type)]
        two_class_flag = False

    # 删除无用字段
    new_data.drop(columns=['Sex_num', 'Sex'], inplace=True)
    x = new_data.drop(columns=['Species_num'])

    # 特征归一化
    scaler = StandardScaler()
    x = scaler.fit_transform(x)
    y = new_data['Species_num']

    # 模型参数
    params = {
        'C' : [1.0,2.0,3.0],
        'max_iter' : [1000,3000,5000],
    }
    gradsearch = GridSearchCV(LogisticRegression(),params,cv=10)
    gradsearch.fit(x,y)
    print(f'经过网格搜索，得出相对较优参数为：{gradsearch.best_params_}')

    if two_class_flag == True:
        # 二分类
        lr = LogisticRegression(**gradsearch.best_params_)
        lr.fit(x,y)
        print(f'类群{case}准确率:{round(lr.score(x,y)*100,2)}%')
    else:
        # 多分类
        lr = LogisticRegression(multi_class="multinomial", solver="newton-cg",**gradsearch.best_params_)
        lr.fit(x,y)
        print(f'类群{case}准确率:{round(lr.score(x,y)*100,2)}%')

    print(lr.intercept_)
    print('\n')
    print(lr.coef_)

    '''
        回归方程：Y = a + b1x1 + b2x2 + ... + bnxn
        其中： a为截距，b1-bn为特征系数
        
        print(f'回归方程：Y = a + b1x1 + b2x2 + ... + bnxn'}
        a : [-0.10069485]
    
        b1-bn : [[-0.54658184 -0.42268772  0.02074616  0.35281991 -0.29337945 -0.41248868
                  -1.18784183  0.55454503 -0.06485619 -1.07456883 -1.44649662  1.24366274
                   0.12650769 -0.58330769  0.06246971 -0.66536402 -0.32281918 -0.05889998
                   0.28105975  0.11832771  0.29901413 -0.26263896 -1.11212844]]
    '''


