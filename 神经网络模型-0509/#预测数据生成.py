#预测数据生成
#输入城市和日期，输出对应数据文件

import time

def getdata(name):
	with open('./'+name+'.txt',encoding='utf-8')as f:
		items=f.readlines()
	data=[x[:-1].split(',') for x in items]
	return data
def turntime(a1):#2019-12-01
	# 先转换为时间数组
	timeArray = time.strptime(a1, "%Y-%m-%d")
	# 转换为时间戳
	timeStamp = int(time.mktime(timeArray))
	return(timeStamp)
def list2csv(data):
	new=[",".join(x) for x in data]
	return '\n'.join(new)

 

data=getdata("全部数据集-3")

#输入时间
start_time=turntime('2019-12-01')
end_time=turntime('2020-04-01')
#输入城市
found_city='成都市'

predict=[]
for item in data[1:]:#取data
	if turntime(item[0])>=start_time and turntime(item[0])<end_time and (found_city in item[2]):
		predict.append(item)

predict=list2csv(predict)
with open('./预测数据集-3-'+found_city+'.txt','w+',encoding='utf-8') as f:
	head='日期,省,城市,城市代码,口罩相关厂商,熔喷布相关厂商,纺织机械相关厂商,无纺布相关厂商,医疗器械相关厂商,聚丙烯相关厂商,卫生相关厂商,人口密度,人口数,确诊,疑似,治愈,死亡,百度指数全部,百度指数pc,百度指数移动\n'
	f.write(head+predict)


