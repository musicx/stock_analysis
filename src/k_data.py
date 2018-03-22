import logging
import pandas as pd
import tushare as ts
from functools import reduce
from datetime import date

conn = ts.get_apis()
basics = ts.get_stock_basics()
k_day_list = []
k_60m_list = []
for idx, code in enumerate(basics.index):
    print("getting {}, no. {}/{}".format(code, idx+1, basics.shape[0]))
    try:
        k_day = ts.bar(code, conn, adj='qfq', factors=['vr', 'tor'], start_date='2000-01-01')
        k_day_list.append(k_day)
    except Exception as e:
        print("getting day data for {} error!".format(code))
    try:
        k_60m = ts.bar(code, conn, adj='qfq', factors=['vr', 'tor'], freq='60min', start_date='2000-01-01')
        k_60m_list.append(k_60m)
    except Exception as e:
        print("getting 60min data for {} error!".format(code))

k_days = pd.concat(k_day_list, axis=0).reset_index()
k_60ms = pd.concat(k_60m_list, axis=0).reset_index()

k_days.to_hdf("../data/k_day_" + date.today().isoformat() + ".hd5", 'day')
k_60ms.to_hdf("../data/k_60m_" + date.today().isoformat() + ".hd5", '60m')
