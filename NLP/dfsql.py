import pandasql
import pandas as pd



df1 = pd.DataFrame([[1,2,3,4],[5,6,7,8],[9,10,11,12]])
print(df1)


sql = '''
    select 0
    from df1
'''

aa = pandasql.sqldf(sql)
print(aa)

