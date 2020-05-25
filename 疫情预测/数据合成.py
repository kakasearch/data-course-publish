#每天爬取数据一次
#百度指数（get）近30天
#每个城市的疫情情况(近30天)(get)
#为数据预测准备数据
#口罩相关厂商,熔喷布相关厂商,纺织机械相关厂商,无纺布相关厂商,医疗器械相关厂商,聚丙烯相关厂商,卫生相关厂商,人口密度,人口数,
#确诊,疑似,治愈,死亡,
#百度指数全部,百度指数pc,百度指数移动
#广东省,广州市,440100,131,3,39952,1062,75125,157,383636,3469,11346
import json
import re
def zipdata(area_name):
	code=get_area_code(area_name)
	parent_name=get_area_parent_name(area_name)
	fixed=get_fixed_by_code(code)

	with open('./19-ncov/'+area_name+'.csv',encoding='utf-8')as f:
		ncovs=f.readlines()
	ncov=[x.replace('\n','') for x in ncovs]

	with open('./baidu_index/'+parent_name+'.csv',encoding='utf-8')as f:
		indexs=f.readlines()
	index=[x.replace('\n','').replace(',,',',0,') for x in indexs][1:]
	print(area_name,'数据读取完毕，开始合成数据集')
	csv=[]
	for i in range(len(index)):
		csv_str= fixed+','+ncov[i]+","+index[i]
		csv.append(csv_str)
	csv='\n'.join(csv)
	print('正在写入',area_name)
	with open('./predict/'+area_name+'.csv','w+',encoding='utf-8')as f:
		f.write(csv)


def get_area_code(name):
 	with open('./19-ncov/163.com_area.json',encoding='utf-8')as f:
 		areas=json.loads(f.read())
 	for area in areas:
 		if name ==area['name'] or name in area['fullName']:
 			return area['code']
def get_area_parent_name(name):
 	with open('./19-ncov/163.com_area.json',encoding='utf-8')as f:
 		areas=json.loads(f.read())
 	for area in areas:
 		if name ==area['name'] or name in area['fullName']:
 			parent= area['parentCode']
 			break
 	for area in areas:
 		if area['code']==parent:
 			return area['name'] 

def get_fixed_by_code(code):
	with open('./data/固定数据集.txt',encoding='utf-8')as f:
		fixed=f.read()
	fix=re.findall(code+',(.*)',fixed)
	if not fix:
		print('无此城市数据')
		return False
	else:
		return fix[0]


if __name__ == '__main__':
	area_name='太原'
	zipdata(area_name)