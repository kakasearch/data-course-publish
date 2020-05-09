#数据生成1-固定数据
#省,城市，城市代码，口罩,熔喷布，纺织机械，无纺布，医疗器械，聚丙烯，卫生, 人口密度,人口数


def getdata(name):
	with open('./'+name+'.txt',encoding='utf-8')as f:
		items=f.readlines()
	data=[x[:-1].split(',') for x in items]
	return data
def dict2csv(data):
	new=[]
	for x in data:
		new.append(",".join(data[x]))
	return '\n'.join(new)
def getdatabypath(path):
	with open(path,encoding='utf-8')as f:
		items=f.readlines()
	data=[x[:-1].split(',') for x in items]
	return data
def list2csv(data):
	new=[",".join(x) for x in data]
	return '\n'.join(new)
def list2dict(list_,first,second):#[[date,cityCode,confirmed,suspected,cured,dead
	data={}
	first_index=set()
	for x in list_:
		first_index=first_index|{x[first]}
	for f in first_index:
		data[f]={}
	
	for x in list_:
		try:
			data[x[first]][x[second]]=x[-4:]
		except:
			

	return data

#读取数据
口罩 = getdata("口罩")
熔喷布 = getdata("熔喷布")
纺织机械 = getdata('纺织机械')
无纺布=getdata('无纺布')
医疗器械=getdata('医疗器械')
聚丙烯=getdata('聚丙烯')
卫生=getdata('卫生')
area = getdata('area')
人口密度=getdata('人口密度')
人口数量=getdata('人口数量')

print('数据读取完毕')

data={}#汇总于此
for item in area:#[广州市,440100]#####init
	data[item[0]]=["0"]*12

items = [口罩,熔喷布,纺织机械,无纺布,医疗器械,聚丙烯,卫生]
for i in range(3,10):
	items_=items[i-3]#取数据集
	for item in items_:#[广东,广州市,440100,157]
		data[item[1]][0]=item[0]#prov
		data[item[1]][1]=item[1]#citty
		data[item[1]][2]=item[2]#city_code
		data[item[1]][i]=item[3]#other

for k in range(len(人口密度)):#[江苏省,2176]
	item=人口密度[k]
	item2 = 人口数量[k]
	for x in data:
		if data[x][0] in item[0]:
			data[x][0] = item[0]#更新省份为全名
			data[x][10]=item[1]#person p
			data[x][11]=item2[1]#person num

print('数据汇总完毕')
data = dict2csv(data)
with open('./固定数据集.txt','w+',encoding='utf-8') as f:
	f.write(data)

# 变动数据：12.1--4.1
# 日期,(省,城市,城市代码,口罩,熔喷布,纺织机械,无纺布,医疗器械,聚丙烯,卫生, 人口密度,人口数),确诊,疑似,治愈,死亡,百度指数全部,百度指数pc,百度指数移动
