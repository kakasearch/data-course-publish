#coding=utf-8

from sklearn.neural_network import MLPClassifier
#from sklearn.datasets import fetch_mldata
import numpy as np
import pickle
import gzip
from sklearn.externals import joblib



# 加载数据
def getdata(name):
	with open(name,encoding='utf-8')as f:
		items=f.readlines()
	data=[x[:-1].split(',') for x in items]
	new=[]
	for item in data:
		temp=[]
		for t in item:
			temp.append(int(t))
		new.append(temp)
	return new
def getydata(name):
	with open(name,encoding='utf-8')as f:
		items=f.readlines()
	data=[int(x) for x in items]
	return data

xdata=getdata('训练数据集-3-x.txt')

ydata=getydata('训练数据集-3-y.txt')
xdata=np.array(xdata)
ydata=np.array(ydata)

tlength=int(len(xdata)*0.8)#训练长度
ylength=int(len(xdata)*0.64)#验证长度
x_training_data,y_training_data = (xdata[:ylength],ydata[:ylength])
x_valid_data,y_valid_data = (xdata[ylength:tlength],ydata[ylength:tlength])
x_test_data,y_test_data = (xdata[tlength:],ydata[tlength:])
classes = np.unique(y_test_data)

# 将验证集和训练集合并
x_training_data_final = np.vstack((x_training_data,x_valid_data))
y_training_data_final = np.append(y_training_data,y_valid_data)

# 设置神经网络模型参数
# mlp = MLPClassifier(solver='lbfgs', activation='relu',alpha=1e-4,hidden_layer_sizes=(50,50), random_state=1,max_iter=10,verbose=10,learning_rate_init=.1)
# 使用solver='lbfgs',准确率为79%，比较适合小(少于几千)数据集来说，且使用的是全训练集训练，比较消耗内存
# mlp = MLPClassifier(solver='adam', activation='relu',alpha=1e-4,hidden_layer_sizes=(50,50), random_state=1,max_iter=10,verbose=10,learning_rate_init=.1)
# 使用solver='adam'，准确率只有67%  logistic
mlp = MLPClassifier(solver='sgd', activation='tanh',alpha=1e-4,hidden_layer_sizes=(50,50,50,50,50,50,50,50,50,50), random_state=1,max_iter=1000,verbose=10,learning_rate_init=.1)
# 使用solver='sgd'，准确率为98%，且每次训练都会分batch，消耗更小的内存

#sgd-logistic:0.704
#adam-logistic:0.704
#sgd-tanh:0.989


# 训练模型
mlp.fit(x_training_data_final, y_training_data_final) 

# 查看模型结果
print('得分',mlp.score(x_test_data,y_test_data))
print('层数',mlp.n_layers_)
print('迭代次数',mlp.n_iter_)
print('当前损失值',mlp.loss_)
print('输出激活函数',mlp.out_activation_)
# 保存模型
joblib.dump(mlp, '通识课模型.pickle')

#载入模型
#model = joblib.load('model.pickle')


##############
'''Iteration 1, loss = 0.61678065
Iteration 2, loss = 0.61636947
Iteration 3, loss = 0.61710158
Iteration 4, loss = 0.61645258
Iteration 5, loss = 0.61699038
Iteration 6, loss = 0.61627478
Iteration 7, loss = 0.61643014
Iteration 8, loss = 0.61606600
Iteration 9, loss = 0.61622775
Iteration 10, loss = 0.61593197
Iteration 11, loss = 0.61589366
Iteration 12, loss = 0.61608920
Iteration 13, loss = 0.61608561
Iteration 14, loss = 0.61536850
Iteration 15, loss = 0.61557883
Iteration 16, loss = 0.61563028
Iteration 17, loss = 0.61601044
Iteration 18, loss = 0.61551028
Iteration 19, loss = 0.61548643
Iteration 20, loss = 0.61591975
Iteration 21, loss = 0.61606795
Iteration 22, loss = 0.61573592
Iteration 23, loss = 0.61589841
Iteration 24, loss = 0.61555684
Iteration 25, loss = 0.61577234
Training loss did not improve more than tol=0.000100 for 10 consecutive epochs. Stopping.
得分 0.7043346583380655
层数 12
迭代次数 25
当前损失值 0.6157723354633178
输出激活函数 logistic'''

########
'''Iteration 1, loss = 0.04715595
Iteration 2, loss = 0.00856519
Iteration 3, loss = 0.00377044
Iteration 4, loss = 0.00417834
Iteration 5, loss = 0.00542284
Iteration 6, loss = 0.00958706
Iteration 7, loss = 0.03267992
Iteration 8, loss = 0.06883568
Iteration 9, loss = 0.05342104
Iteration 10, loss = 0.05306404
Iteration 11, loss = 0.05310166
Iteration 12, loss = 0.05341405
Iteration 13, loss = 0.05303401
Iteration 14, loss = 0.05318676
Training loss did not improve more than tol=0.000100 for 10 consecutive epochs. Stopping.
得分 0.9892106757524134
层数 12
迭代次数 14
当前损失值 0.05318675969494809
输出激活函数 logistic'''
##########
'''Iteration 1, loss = 0.09705771
Iteration 2, loss = 0.05166508
Iteration 3, loss = 0.05594996
Iteration 4, loss = 0.06758247
Iteration 5, loss = 0.06496820
Iteration 6, loss = 0.06624483
Iteration 7, loss = 0.06631655
Iteration 8, loss = 0.06423630
Iteration 9, loss = 0.06511803
Iteration 10, loss = 0.06508184
Iteration 11, loss = 0.06439229
Iteration 12, loss = 0.06447269
Iteration 13, loss = 0.06500842
Training loss did not improve more than tol=0.000100 for 10 consecutive epochs. Stopping.
得分 0.9746634996041171
层数 12
迭代次数 13
当前损失值 0.06500841814405464
输出激活函数 logistic'''