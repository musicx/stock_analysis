import tushare as ts
from datetime import date

# 机构交易明细
inst_detail = ts.inst_detail()

# 机构席位追踪
inst_days_5 = ts.inst_tops(days=5)
inst_days_10 = ts.inst_tops(days=10)
inst_days_30 = ts.inst_tops(days=30)
inst_days_60 = ts.inst_tops(days=60)

inst_detail.to_hdf("../data/inst_detail_{}.hd5".format(date.today().isoformat()), "inst")
inst_days_5.to_hdf("../data/inst_days_{}.hd5".format(date.today().isoformat()), "day5")
inst_days_10.to_hdf("../data/inst_days_{}.hd5".format(date.today().isoformat()), "day10")
inst_days_30.to_hdf("../data/inst_days_{}.hd5".format(date.today().isoformat()), "day30")
inst_days_60.to_hdf("../data/inst_days_{}.hd5".format(date.today().isoformat()), "day60")
