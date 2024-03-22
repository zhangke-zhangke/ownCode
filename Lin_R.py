# -*- coding: utf-8 -*-
import numpy as np
import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler,StandardScaler


data = []
header_col = []
with open("data.txt", "r", encoding='utf-8') as fp:
    f = fp.readlines()
    for i,line in enumerate(f):
        data_line = line.replace('\n',' ').split(" ")
        # if i == 0:
        #     header_col.append(data_line)
        # else:
        data.append(data_line)

data = pd.DataFrame(data).iloc[:,:-1]
print(data)

# data=data.apply(pd.to_numeric,errors='ignore')


x = data.iloc[:,0:-1]
y = data.iloc[:,-1]



scaler = StandardScaler()
x = scaler.fit_transform(x)

lr = LinearRegression()
lr.fit(x,y)
y = lr.predict(x)

print("theta",lr.coef_)
print("theta0",lr.intercept_)

print(y)





# plt.scatter(data[0:,0:2],data[-1],c='b', marker='.')
#
# plt.show()
#
#


