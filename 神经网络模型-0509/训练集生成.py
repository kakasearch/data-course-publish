#日期,(省,城市,城市代码,)口罩相关厂商,熔喷布相关厂商,纺织机械相关厂商,无纺布相关厂商,医疗器械相关厂商,聚丙烯相关厂商,卫生相关厂商,人口密度,人口数,确诊,疑似,治愈,死亡,百度指数全部,百度指数pc,百度指数移动 评价（1，0）1表示有，0表示缺乏
#2020.1.1-1.20--.>1
#1.21-2.14-->0
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

time_11=1577808000#1.1
time_21=1579536000#1.21
time_215=1581696000#2.15
train_x=[]
train_y=[]
for item in data[1:]:#取1.1--2.14并打标签
	if turntime(item[0])>=time_11 and turntime(item[0])<time_21:
		train_y.append('0')
		train_x.append(item[4:])
	elif turntime(item[0])>=time_21 and turntime(item[0])<time_215:
		train_y.append('1')
		train_x.append(item[4:])
	else:
		pass

data_x=list2csv(train_x)
data_y=list2csv(train_y)
with open('./训练数据集-3-x.txt','w+',encoding='utf-8') as f:
	f.write(data_x)
with open('./训练数据集-3-y.txt','w+',encoding='utf-8') as f:
	f.write(data_y)
