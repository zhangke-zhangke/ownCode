'''

'''


# 存在直接交易
'''
    select cust_acct_num,cnter_cust_acct_num
    from zqy_transflow_info
    where cust_acct_num in (select cust_acct_num from zqy_clue_warning)
        and cnter_cust_acct_num in (select cust_acct_num from zqy_clue_warning)
    group by cust_acct_num,cnter_cust_acct_num
'''

# 存在共同对手
'''
    select cnter_cust_no,string_agg(cust_no,',')
    from zqy_transflow_info
    where cust_acct_num in (select cust_acct_num from zqy_clue_warning)
    group by cnter_cust_no
    having count(distinct cust_no) > n


    select t.cnter_cust_no,string_agg(t.cust_no,',')
    from(
        select cust_no,cnter_cust_no
        from zqy_transflow_info
        where cust_acct_num in (select cust_acct_num from zqy_clue_warning)
        group by cust_no,cnter_cust_no
    ) t
    group by t.cnter_cust_no
    having count(1) > n
'''

# a 6221 11.0.1
# b 6222 11.1.1
# b 6223 11.1.0

# 存在共同IP
'''
    select t.ip,string_agg(t.cust_no,',')
    from(
        select cust_no,ip
        from zqy_transflow_info
        where cust_acct_num in (select cust_acct_num from zqy_clue_warning)
        group by cust_no,ip
    ) t
    group by t.ip
    having count(1) > n
'''



# 存在开户行相同
'''
    select t.open_org,string_agg(t.cust_no,',')
    from(
        select cust_no,open_org
        from zqy_account_info
        where card_no in (select cust_acct_num from zqy_clue_warning)
        group by cust_no,open_org
    ) t
    group by t.open_org
    having count(1) > n
'''




# 存在开户时间相近
'''
    select cust_no,card_no,open_org_time
    from zqy_account_info
    where card_no in (select cust_acct_num from zqy_clue_warning)
    group by cust_no,card_no,open_org_time
'''
df = exec_sql()
all_group = []
for i in range(df.shape[0]):
    group = []
    flag = False
    i_time = df['open_org_time'].iloc[i]
    i_cust_no = df['cust_no'].iloc[i]
    for j in range(i+1,df.shape[0]):
        j_time = df['open_org_time'].iloc[j]
        j_cust_no = df['cust_no'].iloc[j]
        if abs(j_time-i_time) <= 10 * 60:
            flag = True
            group.append(j_cust_no)
    if flag == True:
        group.append(i_cust_no)
    all_group.append(group)

print(all_group)




