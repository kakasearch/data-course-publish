
from sklearn.neural_network import MLPClassifier
#from sklearn.datasets import fetch_mldata
import numpy as np
import pickle
import gzip
from sklearn.externals import joblib
import time

def getdata(name,head=False,first_column=False):
	with open(name,encoding='utf-8')as f:
		items=f.readlines()
	if head:
		items=items[1:]
	if first_column:
		data=[x[:-1].split(',')[first_column:] for x in items]
	else:
		data=[x[:-1].split(',') for x in items]
	new=[]
	for item in data:
		temp=[]
		for t in item:
			try:
				temp.append(int(t))
			except:
				temp.append(t)
		new.append(temp)
	return new

def list2csv(data):
	new=[]
	for x in data:
		r=[]
		for k in x:
			r.append(str(k))
		new.append(r)
	new=[",".join(x) for x in new]
	return '\n'.join(new)


#载入模型
model = joblib.load('通识课模型.pickle')
found_city='成都市'
ydata=getdata("预测数据集-3-"+found_city+".txt",head=True)
data=getdata("预测数据集-3-"+found_city+".txt",head=True,first_column=4)

print('数据读取完毕，开始预测')

predict=model.predict(np.array(data))
print('预测结果',predict)
for x in range(len(ydata)):
	item=ydata[x]
	item.append(predict[x])

ydata=list2csv(ydata)
with open('./预测结果_'+found_city+'.txt','w+',encoding='utf-8') as f:
	head='日期,省,城市,城市代码,口罩相关厂商,熔喷布相关厂商,纺织机械相关厂商,无纺布相关厂商,医疗器械相关厂商,聚丙烯相关厂商,卫生相关厂商,人口密度,人口数,确诊,疑似,治愈,死亡,百度指数全部,百度指数pc,百度指数移动,是否缺口罩(0为不缺，1为缺)\n'
	f.write(head+ydata)



