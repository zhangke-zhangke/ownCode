

# mysql connection engine
user = 'root'
password = '123456'
host = '172.30.6.204'
port = 3306
database = 'zqyccserver_JR'


# hive connection engine
# 设置连接参数
hive_host = '172.30.6.5'  # Hive服务器地址
hive_port = 10000  # Hive服务器端口号
hive_username = 'hive'  # Hive用户名
hive_password = 'hive'  # Hive密码
hive_database = 'bojs_dm'  # Hive数据库名
hive_auth = 'LDAP'
hive_limit_date = 4





# feature args
r1_trade_start_time = 0
r1_trade_end_time = 60000
r1_trade_money = 5000
r1_weight = 20

r2_weight = 20

r3_age_start_num = [1930,2001]
r3_age_end_num = [1950,2020]
r3_trade_money = 100000
r3_weight = 10

r4_trade_start_money = 48000
r4_trade_end_money = 49999
r4_weight = 5

r5_weight = 10


r6_trade_area_keyword = ['CHN65','CHN54','CHN53']
r6_weight = 20

r7_trade_include = ['999','9999']
r7_weight = 5

# r8、r9可以在sql中计算
# r8、r9_weight

r10_comment_or_abstract_keyword = ['神仙水','胶囊','聪明药','巧克力']
r10_weight = 20

r11_in_money_include = ['888','8888','880','8800','0000']
r11_weight = 5

r12_in_cnter_include_cnter_name_keyword = ['人民法院']
# 关键字有字符内容需要定义字符为非转义字符
r12_in_cnter_include_comment_keyword = ['\*执\*号','案件款','执行款']
r12_weight = 15

r13_include_comment_keyword = ['律师费','诉讼费']
r13_weight = 15

r14_weight = 20

r15_currency_code = ['CNY', 'cny', '156', '人民币']
r15_weight = 15

r16_weight = 20

r17_tx_amt_rmb = 5000
t17_acct_bal = 10
r17_weight = 15

r18_weight = 20










