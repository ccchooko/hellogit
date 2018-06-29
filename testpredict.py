# 我们都有一个家名字叫中欧

import pandas as pd

pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 5000)

df_test = pd.read_csv('toBePredict.csv', index_col=False)

df_train = pd.read_csv('traindata/new_train1-24.csv')

test_terminalno_list = df_test['O_TERMINALNO'].unique().tolist()

terminalno = {}
for no in test_terminalno_list:
    temp = df_train[df_train['O_TERMINALNO']==int(no)]
    terminalno[no] = temp.groupby(['stationno']).median()['sub_time_stamp'].to_dict()

print(len(terminalno))

df_test['pred_timeStamps'] = ""
for i in df_test.index:
	no = df_test.iloc[i, 2]
	start = df_test.iloc[i, 4]
	stop = df_test.iloc[i, 5]
	# print(df_test.loc[i])
	try:
		df_test.iloc[i, 6] = str(list(terminalno[no][x] for x in range(start, stop+1))).replace(', ',';').replace('[','').replace(']','')
	except:
		df_test.iloc[i, 6] = str(list(terminalno[no][x] if terminalno.get(no).get(x) else 100 for x in range(start, stop+1) )).replace(', ',';').replace('[','').replace(']','')
df_test.to_csv('test.csv', index=None)
