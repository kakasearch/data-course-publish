#每天爬取数据一次
#百度指数（get）近30天
#每个城市的疫情情况(近30天)

##预测数据、
# -*- coding: utf-8 -*-
 
import requests
import js2py
import urllib3,time
import json
import re,os
# 禁用警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#按城市获取最近疫情数据 解析格式：累计数：确诊,疑似,治愈,死亡
#https://wp.m.163.com/163/page/news/virus_province/index.html?province=shanxi&spss=epidemic
 #https://c.m.163.com/ug/api/wuhan/app/data/list-total?t=1590294097609
 #https://c.m.163.com/ug/api/wuhan/app/data/list-by-area-code?areaCode=140000&t=1590300684265  #山西

class spider_baiduindex(object):
	provinces= {
			901: "山东",
			902: "贵州",
			903: "江西",
			904: "重庆",
			905: "内蒙古",
			906: "湖北",
			907: "辽宁",
			908: "湖南",
			909: "福建",
			910: "上海",
			911: "北京",
			912: "广西",
			913: "广东",
			914: "四川",
			915: "云南",
			916: "江苏",
			917: "浙江",
			918: "青海",
			919: "宁夏",
			920: "河北",
			921: "黑龙江",
			922: "吉林",
			923: "天津",
			924: "陕西",
			925: "甘肃",
			926: "新疆",
			927: "河南",
			928: "安徽",
			929: "山西",
			930: "海南",
			931: "台湾",
			932: "西藏",
			933: "香港",
			934: "澳门"
		}

	js_string = '''
	function decrypt(t, e) {
		for (var n = t.split(""), i = e.split(""), a = {}, r = [], o = 0; o < n.length / 2; o++)
			a[n[o]] = n[n.length / 2 + o];
		for (var s = 0; s < e.length; s++)
			r.push(a[i[s]]);
		return r.join("")
	}
	'''
	uniq_id_url = 'https://index.baidu.com/Interface/ptbk?uniqid={}'
	def __init__(self,cookie,area_name=None):
		self.headers = {
		"Cookie": cookie,
		"Referer": "http://index.baidu.com/v2/main/index.html",
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
	"X-Requested-With": "XMLHttpRequest",
	'Accept': "application/json, text/plain, */*",
	'Accept-Encoding': "gzip, deflate",
	'Accept-Language': "zh-CN,zh;q=0.9",
	}
		self.session = self.get_session()
		if area_name:#如果指定了爬哪个地区
			for pnum in self.provinces:#2011-2019
				if area_name == self.provinces[pnum]:
					province_name = self.provinces[pnum]
					area =str(pnum)
					key_word = '口罩'
					d = self.get_bd_index(key_word,area)
					print('index_baidu',province_name)
					print(d)
					time.sleep(4)
					#exit()
					self.format_(d,province_name,path='./baidu_index/')
		else:
			for pnum in self.provinces:#2011-2019
				province_name = self.provinces[pnum]
				area =str(pnum)
				key_word = '口罩'
				d = self.get_bd_index(key_word,area)
				print('index_baidu',province_name)
				print(d)
				time.sleep(4)
				#exit()
				self.format_(d,province_name,path='./baidu_index/')
	def format_(self,data,province_name,path):
		all_ =(data[0]['all'].split(','))
		pc =(data[1]['pc'].split(','))
		mob =(data[2]['wise'].split(','))
		try:
			with open(path+province_name+'.csv','w+',encoding='utf-8')as f:
				f.write('全部,pc,移动\n')
				for x in range(len(all_)):
					f.write("{},{},{}\n".format(all_[x],pc[x],mob[x]))
		except Exception:
			print(path)
			print(Exception)
	def get_session(self):
		"""
			初始化 session 会话
		:return:
		"""
		session = requests.session()
		session.headers = self.headers
		session.verify = False
		return session
	def decrypt(self,key, data):
		"""
			得到解密后的数据
		:param key:  key
		:param data: key 对应的 value
		:return:
		"""
		js_handler = js2py.eval_js(self.js_string)
		return js_handler(key, data)
 
	def get_bd_index(self,key_word,area=0):
		"""
			得到百度指数
		:param key_word:
		:return:
		"""
		#http://index.baidu.com/api/SearchApi/index?area=0&word=[[%7B%22name%22:%22%E5%8F%A3%E7%BD%A9%22,%22wordType%22:1%7D]]&days=30
		data_url = 'http://index.baidu.com/api/SearchApi/index?area='+area+'&word=[[{"name":"'+key_word+'","wordType":1}]]&days=30'
		response = self.session.get(data_url).json()
		try:
			uniq_id = self.session.get(
				self.uniq_id_url.format(response.get("data").get("uniqid"))
			).json().get("data")
		except:
			print(response)
			return('')
			#exit()
		result = []
		data_dict = response.get("data").get("userIndexes")[0]
		keys = ["all", "pc", "wise"]
		for key in keys:
			js_handler = js2py.eval_js(self.js_string)
			decrypt_data =js_handler(uniq_id, data_dict.get(key).get("data"))
			result.append({key: decrypt_data})
		return result
def bi_data(path):
	headers={
	'Accept': '*/*',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.9',
	'Referer': 'http://aiiyx.cn:81/',
	'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Mobile Safari/537.36',
	'X-Requested-With': 'XMLHttpRequest'
	}
	files=['c1','l1','l2','r1','r2']
	for file in files:
		url='http://aiiyx.cn:81/'+file
		r=requests.get(url,headers)
		with open(path+file+'.json','w+',encoding='utf-8')as f:
			f.write(r.text)
			print(r.text)

def spider_ncov(area_name='太原'):
	with open('./19-ncov/163.com_area.json',encoding='utf-8')as f:
		areas=json.loads(f.read())
	for area in areas:
		if area_name ==area['name']:
			code= area['code']
			url='https://c.m.163.com/ug/api/wuhan/app/data/list-by-area-code?areaCode='+code
			headers={
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
			}
			print('正在爬取'+area_name+"近30天疫情情况")
			r = requests.get(url,headers=headers)#按城市获取疫情数据
			data=r.json()['data']['list']
			csv=[]
			for item in data[-30:]:
				#date=item['date']#确诊,疑似,治愈,死亡
				confirm=item['total']['confirm']
				suspect=item['total']['suspect']
				heal=item['total']['heal']
				dead=item['total']['dead']
				csv_str=','.join([str(confirm),str(suspect),str(heal),str(dead)])
				csv.append(csv_str)
			csv='\n'.join(csv)
			with open('./19-ncov/'+area_name+".csv",'w+',encoding='utf-8')as f:
				f.write(csv)
def spider(cookie,area_name):
	print('疫情爬取开始')
	spider_ncov(area_name)
	print('百度指数爬取开始，一周更新一次cookie')
	spider_baiduindex(cookie)

if __name__ == '__main__':
	area_name='凉山州'
	print('疫情爬取开始')
	spider_ncov(area_name)
	print('百度指数爬取开始，一周更新一次cookie')
	cookie='''BAIDUID=6835BE052908F11DEF2B6764F9C6474C:FG=1; CHKFORREG=42228c0c68b667b4b6574aea103a3322; bdindexid=rifftm5cce3rc2im2e2p80n6f0; BIDUPSID=6835BE052908F11DEF2B6764F9C6474C; PSTM=1590288687; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1590287287,1590292944; BDUSS=5-amVIcn5IZDUyNWdTU3F5cmlxTlh6YW52U09mSkxqTGJIRzZxZG1GN2RmdkZlRVFBQUFBJCQAAAAAAAAAAAEAAAB9FP2cZGZzc2Z5dQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAN3xyV7d8clec3; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1590292960; RT="sl=e&ss=kakg2gr8&tt=glw&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&z=1&dm=baidu.com&si=fchspqmy9i6&ld=3atk7&ul=3azrt"'''
	spider_baiduindex(cookie)