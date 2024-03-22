# 规则推荐


一、流程

    1）连接数据库，获得待优化特征及线索标签
    2）特征及标签拆分
    3）利用卡方分箱求最优区间（在分箱后样本占总样本的n%时，进行细分）
    4）接口返回分箱最优区间参数

二、接口

    http://172.30.4.81:9999/argsAdaption?host=172.30.6.184&user=root&password=zqykj123&database=finance&port=3306&stop_sample_pro=0.3    

三、返回

    [
      {
        "args_section": [
          43, 
          69.23
        ], 
        "term_id": "b6feaa09_3741_4c53_8a06_3e41dee12672"
      }, 
      {
        "args_section": [
          11, 
          22
        ], 
        "term_id": "b6feaa09_3741_4c53_8a06_3e41dee12673"
      }
    ]
    
    
    
    
    
    