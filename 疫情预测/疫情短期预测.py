import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier
#from sklearn.datasets import fetch_mldata
import numpy as np
import pickle
import gzip
from sklearn.externals import joblib
import time


def predict(item,photo=True):
	x_data=range(len(item))
	y_data=item
	if [item[-1]]*5==item[-5:]:
		n_order = 1          #阶数
		x_data=x_data[-5:]
		y_data=item[-5:]
	else:
		n_order = 5          #阶数
	

	p = np.poly1d(np.polyfit(x_data,y_data,n_order))            #拟合并构造出一个n次多项式
	#print(p.coeffs)                               #输出拟合的系数，顺序从高阶低阶

	#画出拟合出来的多项式所表达的曲线以及原始的点
	t = range(len(item)+10)#未来10个点
	#plt.figure(figsize=(12, 6), dpi=300)
	if photo:
		plt.plot(range(len(item)),item,'ro',t,p(t),'-')
		plt.savefig(r"./predict/photo/"+str(item[1])+str(time.time())+'.png')
		plt.close()
	return p(t)

def trans(l):
    l = zip(*l)
    l = [list(i) for i in l]
    return l
def predict_data(area_name,photo=True):
	with open('./predict/'+area_name+'.csv',encoding='utf-8')as f:
		datas=f.readlines()
	data=[x.replace('\n','').split(',') for x in datas]
	data=trans(data)#叉开
	for i in range(len(data)):
		for j in range(len(data[i])):
			data[i][j]=int(data[i][j])
	#print(data)
	#数据预测未来10个
	print('预测未来10天数据',area_name)
	newdata=[]
	for item in data[:-7]:#固定的数据，沿袭前面
		item=item+[item[-1]]*10
		newdata.append(item)
	for item in data[-7:]:
		item=predict(item,photo)
		newdata.append(item)
	data=trans(newdata)
	print(area_name,'数据预测完毕，开始预判口罩情况')

	#载入模型
	model = joblib.load('通识课模型.pickle')

	result=model.predict(np.array(data))
	print(area_name,'预测结果',result)
	return result
##################################
if __name__ == '__main__':

	area_name='太原'
	predict_data(area_name)