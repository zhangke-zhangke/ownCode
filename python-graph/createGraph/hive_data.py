
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Enum,
    DECIMAL,
    DateTime,
    Boolean,
    UniqueConstraint,
    Index,
    text,
    literal_column,
    ColumnDefault,
)
from sqlalchemy.ext.declarative import declarative_base





# 基础类
# hive数据来源
Base = declarative_base()
class hivedata(Base):
    """ 必须继承Base """
    # 数据库中存储的表名
    __tablename__ = "zqy_transflow_info"


    # hive columns
    cust_name = Column(String(32),comment='客户名称')
    # cust_cert = Column(String(32),default='',comment='客户证件号码')
    # 当表中无此字段，但业务逻辑需要使用时候。添加空列逻辑，还需要在query中对应列名使用label方法重命名
    cust_cert = literal_column('""',String)
    card_no = Column('card_no',String,comment='查询卡号')
    cnter_cust_name = Column(String(32),comment='交易对方名称')
    cnter_cert_no = Column(String(32),comment='交易对方证件号码')
    cnter_card_no = Column(String(32),comment='交易对方卡号')
    tx_type = Column(String(32),comment='交易类型')
    credit_debit_ind = Column(String(32),comment='借贷标志')
    currency_code = Column(String(32),comment='币种')
    tx_amt_rmb = Column(DECIMAL(16,2),comment='交易金额')
    acct_bal = Column(DECIMAL(16,2),comment='交易余额')
    tx_time = Column(DateTime,comment='交易时间')
    tx_abstract = Column(String(32),comment='交易摘要')
    ip_addr = Column(String(32),comment='IP地址')
    cross_tx_ind = Column(String(32),comment='境内外标识')
    comment = Column(String(32),comment='备注')

    __mapper_args__ = {
        'primary_key':[cust_name]
    }


    def __str__(self):
        return f"object : <emp_id:{self.cust_name} cust_id:{self.cust_name} date:{self.cust_name}>"
        # return f"object : <id:{self.id} name:{self.name}>"






'''
    select 
    	cust_name as `客户名称`
    	,'' as `客户证件号码`
    	,card_no as `查询卡号`
    	,cnter_cust_name as `交易对方名称`
    	,cnter_cert_no as `交易对方证件号码`
    	,cnter_card_no as `交易对方卡号`
    	,tx_type as `交易类型`
    	,credit_debit_ind as `借贷标志`
    	,currency_code as `币种`
    	,tx_amt_rmb as `交易金额`
    	,acct_bal as `交易余额`
    	,tx_time as `交易时间`
    	,tx_abstract as `交易摘要`
    	,ip_addr as `IP地址`
    	,cross_tx_ind as `境内外标识`
    	,comment as `备注`
    from bojs_dm.zqy_transflow_info
    where card_no is not null and card_no != ''
    and cnter_card_no is not null and cnter_card_no != ''
	and cust_name not regexp '公司|有限'
    and cnter_cust_name not regexp '财付通|支付宝|淘宝|钱袋宝|钱宝科技|宝付网络科技|通行宝|合众易宝|支付|备付金|天翼|银联|网联|网银在线|平安付|易智付|京东商城|特约|内部户|待清算|清算款|资金清算|清算资金|清算回款|清算户|清算过账|清算专户|清算专用|结算|代收|代付|代发|代扣|批量|汇款|收入|收款|付款|过渡|专用|暂收|暂挂|暂存|挂账|账号|服务费|赎回账户|清盘账户|终止账户|发放账户|BGL账户|往来账户|他行账户|企业贷账户|中间账户|内部账户|放款账户|发放账户|垫款账户|账户黄金户|账户白银户|账户管理|商户|专户|专项|款项|在途资金|资金归集|结算资金|资金管理|交易资金|划转资金|资金监管|信用卡|还款|银行|人寿保险|财产保险|健康保险|社会保险|医疗保险|证券|基金|理财产品|产品实时|产品本金|产品收益|产品开通|政企账户|法院|诉讼|税务|财政|公积金|江苏苏电|国网|高速通行费|美团'
    
'''