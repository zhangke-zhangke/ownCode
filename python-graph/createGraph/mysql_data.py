
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
    Index
)
from sqlalchemy.ext.declarative import declarative_base





# 基础类
Base = declarative_base()
class UserInfo(Base):
    """ 必须继承Base """
    # 数据库中存储的表名
    __tablename__ = "tmp_tradeFlow_0_0c1675ec_9a51_48c0_9320_1cd602d61e02"

    # columns
    cust_name = Column(name='客户名称',type_=String)
    cert_no = Column(name='客户证件号码',type_=String)
    card_no = Column(name='查询卡号',type_=String)
    cnter_cust_name = Column(name='交易对方名称',type_=String)
    cnter_cert_no = Column(name='交易对方证件号码',type_=String)
    cnter_card_no = Column(name='交易对方卡号',type_=String)
    tx_type = Column(name='交易类型',type_=String)
    credit_debit_ind = Column(name='借贷标志',type_=String)
    currency_code = Column(name='币种',type_=String)
    tx_amt_rmb = Column(name='交易金额',type_=String)
    acct_bal = Column(name='交易余额',type_=String)
    tx_time = Column(name='交易时间',type_=String)
    tx_abstract = Column(name='交易摘要',type_=String)
    ip_addrd = Column(name='IP地址',type_=String)
    cross_tx_ind = Column(name='境内外标识',type_=String)
    comment = Column(name='备注',type_=String)


    __mapper_args__ = {
        'primary_key': [cust_name]
    }

    # __table__args__ = (
    #     UniqueConstraint("name", "age", "phone"),  # 联合唯一约束
    #     Index("name", "addr", unique=True),       # 联合唯一索引
    # )

    # def __str__(self):
    #     return f"object : <emp_id:{self.emp_id} cust_id:{self.cust_id} date:{self.date}>"
    #     # return f"object : <id:{self.id} name:{self.name}>"







'''
    select
        客户名称
        ,客户证件号码
        ,查询卡号
        ,交易对方名称
        ,交易对方证件号码
        ,交易对方卡号
        ,交易类型
        ,借贷标志
        ,币种
        ,交易金额
        ,交易余额
        ,交易时间
        ,交易摘要
        ,IP地址
        ,境内外标识
        ,备注
    from zqyccserver_JR.tmp_tradeFlow_0_0c1675ec_9a51_48c0_9320_1cd602d61e02
    where 查询卡号 is not null and 查询卡号 != ''
    and 交易对方卡号 is not null and 交易对方卡号 != ''
	and 客户名称 not regexp '公司|有限' and 交易是否成功 = 1
    and 交易对方名称 not regexp '财付通|支付宝|淘宝|钱袋宝|钱宝科技|宝付网络科技|通行宝|合众易宝|支付|
        备付金|天翼|银联|网联|网银在线|平安付|易智付|京东商城|特约|内部户|待清算
        |清算款|资金清算|清算资金|清算回款|清算户|清算过账|清算专户|清算专用|结算|代收|代付|代发|代扣|批量|汇款|收入|收款|付款|过渡|专用|暂收|暂挂|暂存|挂账|账号|服务费|赎回账户|清盘账户 |终止账户|发放账户|BGL账户|往来账户|他行账户|企业贷账户|中间账户|内部账户|放款账户|发放账户|垫款账户|账户黄金户|账户白银户|账户管理|商户|专户|专项|款项|在途资金|资金归集|结算资金|资金管理|交易资金|划转资金|资金监管|信用卡|还款|银行|人寿保险|财产保险|健康保险|社会保险|医疗保险|证券|基金|理财产品|产品实时|产品本金|产品收益|产品开通|政企账户|法院|诉讼|税务|财政|公积金|江苏苏电|国网|高速通行费|美团'

'''





