# 规则推荐


一、流程

    1）连接数据库，获得衍生特征及线索标签
    2）特征及标签拆分
    3）训练决策树模型
    4）对树模型的可视化进行解析
    5）组合解析出来的树分支。并计算组合后的召回、精准指标
    6）接口返回


二、接口

    http://172.30.4.81:8888/newRule?host=172.30.6.184&user=root&password=zqykj123&database=finance&port=3306
    

三、返回

    [
        {"index": [
            {"index_name": "AMT_ALL_NCB_AVG", "index_value": "29967.6201171875", "index_operation": "<="}, 
            {"index_name": "TXC_820H_CB_AVG", "index_value": "1.656149983406067", "index_operation": "<="}, 
            {"index_name": "AMT_918H_OD_MIN", "index_value": "0.5149999996647239", "index_operation": ">"}], 
            "RECALL": 0.3142857142857143, 
            "PRECISION": 0.6875}, 
        {"index": [
            {"index_name": "AMT_ALL_NCB_AVG", "index_value": "29967.6201171875", "index_operation": ">"},
            {"index_name": "TXD_024M_ID_COUNT", "index_value": "237.5", "index_operation": "<="},
            {"index_name": "AMT_820H_NCS_MIN", "index_value": "1.5200000405311584", "index_operation": ">"}],
            "RECALL": 0.17142857142857143, 
            "PRECISION": 0.6}, 
        {"index": [
            {"index_name": "AMT_ALL_NCB_AVG", "index_value": "29967.6201171875", "index_operation": "<="},
            {"index_name": "TXC_820H_CB_AVG", "index_value": "1.656149983406067", "index_operation": "<="}, 
            {"index_name": "AMT_918H_OD_MIN", "index_value": "0.5149999996647239", "index_operation": "<="}], 
            "RECALL": 0.11428571428571428, 
            "PRECISION": 0.16666666666666666}
    ]
    
    
    
    
    
    