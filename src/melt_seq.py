import numpy as np
import pandas as pd

FUTURE_DAYS = 3

day = pd.read_hdf("d:/Work/Python/MyCode/Stock/data/k_day_2018-04-06.hd5", "day")
day.sort_values(["code", "datetime"], inplace=True)

date_rank = day.loc[:, ['code', 'datetime', 'open', 'close']]
date_rank.loc[:, 'rank'] = day.groupby('code').rank().loc[:, 'datetime']
date_rank.loc[:, 'future'] = date_rank.loc[:, 'rank'] - FUTURE_DAYS

date_tag = pd.merge(date_rank, date_rank.loc[:, ['code', 'future', 'open', 'close']],
                    left_on=['code', 'rank'], right_on=['code', 'future'], how='left',
                    suffixes=['', '_f'])

date_tag.loc[:, 'pos'] = date_tag.open_f / date_tag.close > 1.1
date_tag.loc[:, 'neg'] = date_tag.open_f / date_tag.close < 0.9


def melt_feature(data, num):
    queue = []
    new_data = []
    for line in data:
        if len(queue) >= num:
            queue.pop()
        if len(queue) > 0 and queue[0][1] != line[1]:
            queue.clear()
        new_line = np.r_[line[:2], line[2:6] / line[3], line[7] / line[7]]
        for x in range(num-1):
            if len(queue) > x:
                new_line = np.r_[new_line, queue[x][2:6] / line[3], queue[x][7] / line[7]]
            else:
                new_line = np.r_[new_line, np.zeros(5)]
        new_data.append(new_line)
        queue.insert(0, line)
    return pd.DataFrame(new_data)


melt_data = melt_feature(np.array(day), 7).rename(columns={0: 'date', 1: 'code'})
merged = pd.merge(date_tag, melt_data, "left", left_on=['datetime', 'code'],
                  right_on=['date', 'code'])

merged.to_csv("../data/merged.csv", index=False)
