from pyspark.sql import SparkSession
from pyspark.sql import functions


spark = SparkSession.builder.appName('my_spark_demo').getOrCreate()


print(spark)
print(type(spark))


# connection = pymysql.connect(host='172.30.6.204', user='root', password='123456', database='financeML', port=int(3306))

sql = '(select * from financeML.tb_finance_ML_20210922 limit 10) t'
df = spark.read.format('jdbc').options(
    url = 'jdbc:mysql://172.30.6.204',
    dbtable = sql,
    user = 'root',
    password = '123456'
).load()

df.printSchema()

df.select(['客户名称','对手为个人交易金额','年龄']).show()



