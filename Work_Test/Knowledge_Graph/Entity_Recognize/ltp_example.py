# from ltp import LTltp = LTP() # 默认加载 Small 模型
from ltp import LTP
ltp = LTP()
seg, hidden = ltp.seg(["杨超越在1998年7月31日出生于江苏省盐城市大丰区。"])
ner = ltp.ner(hidden)
print(ner)
tag, start, end = ner[0][0]
print(tag,":", "".join(seg[0][start:end + 1]))