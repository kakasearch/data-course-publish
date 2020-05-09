import re,os
def format_(path,date):
	with open(path,encoding='utf-8')as f:
		a = eval(f.read())

	all_ =(a[0]['all'].split(','))
	pc =(a[1]['pc'].split(','))
	mob =(a[2]['wise'].split(','))
	try:
		with open(path.replace('dict','csv'),'w+',encoding='utf-8')as f:
			f.write('日期,全部,pc,移动\n')
			for x in range(len(all_)):
				f.write("{},{},{},{}\n".format(date[x],all_[x],pc[x],mob[x]))
	except Exception:
		print(path)
		print(Exception)

format_('d:/desktop/一组/消费端/百度指数/city_2019-12-01--2020-04-01/河南_周口.dict',)