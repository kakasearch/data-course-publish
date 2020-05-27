#spider模块爬取百度、疫情
#数据预测模块预测数据
#网页渲染模块跟新网页
#后端持续运行
import json
import numpy
import time
#只做四川
citys=["成都","广安","内江","遂宁","南充","德阳","达州","攀枝花","自贡","泸州", "巴中", "眉山", "绵阳", "宜宾", "甘孜州", "资阳", "雅安", "广元", "乐山", "凉山州", "阿坝州"]

with open('./run_log.txt','a+',encoding='utf-8')as f:
	f.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'\t开始跟新数据\n')
################################
import 疫情数据爬取
##spider

try:
	cookie='''BAIDUID=6835BE052908F11DEF2B6764F9C6474C:FG=1; CHKFORREG=42228c0c68b667b4b6574aea103a3322; bdindexid=rifftm5cce3rc2im2e2p80n6f0; BIDUPSID=6835BE052908F11DEF2B6764F9C6474C; PSTM=1590288687; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1590287287,1590292944; BDUSS=5-amVIcn5IZDUyNWdTU3F5cmlxTlh6YW52U09mSkxqTGJIRzZxZG1GN2RmdkZlRVFBQUFBJCQAAAAAAAAAAAEAAAB9FP2cZGZzc2Z5dQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAN3xyV7d8clec3; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1590292960; RT="sl=e&ss=kakg2gr8&tt=glw&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&z=1&dm=baidu.com&si=fchspqmy9i6&ld=3atk7&ul=3azrt"'''
	print('百度指数爬取开始，一周更新一次cookie')
	疫情数据爬取.spider_baiduindex(cookie,'四川')
	print('疫情爬取开始')	
	for city in citys:
		疫情数据爬取.spider_ncov(city)
	疫情数据爬取.bi_data('web/')
	print('###########四川省数据全部爬取完毕###########')
except:
	with open('./run_log.txt','a+',encoding='utf-8')as f:
			f.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'\tERROR!!!请更新cookie!!!!\n')
	exit()

###########################
#数据合成，准备分析数据
import 数据合成
for city in citys:
	数据合成.zipdata(city)
print('###########四川省数据全部合成完毕###########')


############################
#过去30天+未来10天
import 疫情短期预测
future={
	'data':{},
	'date':[],
	'citys':citys,
}
for city in citys:
	result=疫情短期预测.predict_data(city,photo=False)
	future['data'][city]=result.tolist()
print('###########四川省口罩情况全部预测完毕###########')

#构建日期序列
import datetime
def get_day_list(b,n):
    days=[]
    for i in range(1, b)[::-1]:
       days.append(str(datetime.date.today() - datetime.timedelta(days=i)))
    days.append(str(datetime.date.today()))
    for i in range(1,n+1):
        days.append(str(datetime.date.today() + datetime.timedelta(days=i)))
    
    return days

future['date'] = get_day_list(30,10)

with open('./web/future.json','w+',encoding='utf-8')as f:
	f.write(str(json.dumps(future)).encode('utf-8').decode('unicode_escape'))
print('网站数据跟新完毕')
with open('./run_log.txt','a+',encoding='utf-8')as f:
	f.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'\t数据跟新成功\n')