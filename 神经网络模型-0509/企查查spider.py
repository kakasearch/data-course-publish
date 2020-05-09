import requests
import json
import re
import urllib.parse
import time
import random
import threading


def main(pkey):
	data = {}
	#pkey = '口罩'
	key = urllib.parse.quote(pkey)
	#
	provs = ["GD", "BJ", "JS", "SH", "ZJ", "SC", "SD", "HB", "HEN", "FJ", "HUB", "AH", "CQ", "SAX", "HUN", "LN", "TJ", "JX", "YN", "GX", "SX", "GZ", "JL", "HLJ", "NMG", "XJ", "GS", "HAIN", "NX", "QH", "XZ"]

	headers={
	'Accept':'text/html, */*; q=0.01',
	'Sec-Fetch-Dest':'empty',
	'X-Requested-With':'XMLHttpRequest',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
	'Sec-Fetch-Site':'same-origin',
	'Sec-Fetch-Mode':'cors',
	'Referer':'https://www.qcc.com/search_index?key='+key,
	'Accept-Encoding':'gzip, deflate, br',
	'Accept-Language':'zh-CN,zh;q=0.9',
	'Cookie':'zg_did=%7B%22did%22%3A%20%2217133ce487b265-0cdf3c100d3461-f313f6d-e1000-17133ce487c165%22%7D; _uab_collina=158571209389163149962586; QCCSESSID=ikm6qa3l1lriimn24ioaef77t0; acw_tc=3cddc21715886419160712016ed072002ea750e3c5750a5d19d3215bea; hasShow=1; acw_sc__v2=5eb3aab5898ab70197f6d83c035f760ed407afd9; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201588832952346%2C%22updated%22%3A%201588832953240%2C%22info%22%3A%201588641910772%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qcc.com%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%2C%22cuid%22%3A%20%2240dc4149bfd39af462662754027e1101%22%7D'	}
	for prov in provs:
		print(prov)
		url = 'https://www.qcc.com/search_getCityListHtml?province=%s&q_type=1'%prov
		r= requests.get(url,headers=headers)
		citys = re.findall(r'data-value="(\d+?)" data-append="(.*?)"',r.text)
		print(citys)
		if not citys:
			time.sleep(20)
			print('受限')
			url = 'https://www.qcc.com/search_getCityListHtml?province=%s&q_type=1'%prov
			r= requests.get(url,headers=headers)
			citys = re.findall(r'data-value="(\d+?)" data-append="(.*?)"',r.text)
			print(citys)
		for city in citys:
			code=city[0]
			city_name=city[1]
			#with open('./area.txt','a+',encoding='utf-8')as f:
			#	f.write(city_name+","+code+"\n")
			url = "https://www.qcc.com/search_index?key="+urllib.parse.quote(key)+"&ajaxflag=1&province=%s&city=%s&"%(prov,code)
			r= requests.get(url,headers=headers)
			#print(r.text)
			text = r.text.replace('\n','')
			#print(city_name)
			try:
				data['num']=re.findall(r'小查为您找到.*?(\d+).*?家符合条件的企业',text)[0]
				data['prov'] = re.findall(r"筛选项':'省份地区','筛选值':'(.*?)'",text)[0]
			except:
				continue
			print(city_name,data['num'])
			#print(data)
			with open('./'+pkey+'.txt','a+',encoding='utf-8')as f:
				f.write(data["prov"]+","+city_name+","+code+","+data['num']+"\n")
			time.sleep(3*random.random())

	#url = "https://www.qcc.com/search_index?key="+urllib.parse.quote(key)+"&ajaxflag=1&province=GD&city=440100&"


	# r= requests.get(url,headers=headers)
	# data['num']=re.findall(r'小查为您找到.*?(\d+).*?家符合条件的企业',r.text.replace('\n',''))[0]

	# print(data)
  
obj = []
keys = ['熔喷布',]			#'医疗器械','聚丙烯',！！'医疗'
for pkey in range(1):
	x = threading.Thread(target = main,args = (keys[pkey],))
	x.start()
	obj.append(x)
for i in obj:
	i.join()

