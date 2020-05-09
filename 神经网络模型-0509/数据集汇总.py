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
			pass

	return data


#读取数据
index = getdatabypath("口罩2019-12-01_2020-04-01.csv")#日期,全部,pc,移动
#疫情数据处理代码
#日期,固定(城市代码),确诊,疑似,治愈,死亡(confirmed	,suspected	cured	dead)
fixed = getdatabypath('固定数据集.txt')#(省,城市,城市代码,口罩,熔喷布,纺织机械,无纺布,医疗器械,聚丙烯,卫生, 人口密度,人口数)
ncov = getdatabypath('每日疫情数据_官杂源_2019.12.01-2020.04.01.csv')#date,country,countryCode,province,provinceCode,city,cityCode,confirmed,suspected,cured,dead
print('数据读取完毕')
#处理格式
ncov19=[]#date,cityCode,confirmed,suspected,cured,dead
for item in ncov[1:]:
	if ('' not in item) and ('境外输入' not in item) and ('x' not in item[4]):
		temp=[item[0]]+item[-5:]#['2020-01-28', '130700', '1', '3', '0', '0']
		ncov19.append(temp)

#建立索引
getncov=list2dict(ncov19,0,1)
city_codes=set()#城市代码集合，共421个城市
for x in fixed:
	city_codes=city_codes|{x[2],}
data=[]#汇总
for day in index[1:]:
	for fix in fixed:
		try:
			yiqing= getncov[day[0]][fix[2]]
		except:
			if fix[2] in city_codes:
				yiqing=['0']*4
			else:
				continue
		exam=[day[0]]+fix+yiqing+day[1:]
		#print(exam)
		data.append(exam)
print('数据汇总完毕')

data = list2csv(data)

with open('./全部数据集-3.txt','w+',encoding='utf-8') as f:
	head='日期,省,城市,城市代码,口罩相关厂商,熔喷布相关厂商,纺织机械相关厂商,无纺布相关厂商,医疗器械相关厂商,聚丙烯相关厂商,卫生相关厂商,人口密度,人口数,确诊,疑似,治愈,死亡,百度指数全部,百度指数pc,百度指数移动\n'
	f.write(head+data)



