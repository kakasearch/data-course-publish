import json
import requests
import time
import re

session = requests.session()
headers = {
'Accept': 'application/json, text/javascript, */*; q=0.01',
'Sec-Fetch-Dest': 'empty',
'X-Requested-With': 'XMLHttpRequest',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
'Sec-Fetch-Site': 'same-origin',
'Sec-Fetch-Mode': 'cors',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9'
}
def get_info(maskid):
	now_time = str(int(time.time()*1000))
	url = 'https://xin.baidu.com/antivirus/maskDetailAjax?maskid=%s&_=%s'%(maskid,now_time)
	#url = 'https://xin.baidu.com/antivirus/maskDetailAjax?maskid=ac90571cf91a7b5ccaac4793f8656177&_=1585910266909'
	res = session.get(url,headers=headers)
	return res.text
def get_money(bdcode):
	url= 'https://xin.baidu.com/detail/compinfo?pid='+bdcode
	headers={
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
'Sec-Fetch-Dest':'document',
'Sec-Fetch-Site':'same-origin',
'Sec-Fetch-Mode':'navigate',
'Sec-Fetch-User':'?1',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.9',
	}
	r = session.get(url,headers=headers)
	#print(r.text)
	money = re.findall(r'class="table-regCapital-lable">(.*?)</td>',r.text)
	if money:
		return money[0]
	else:
		print('获取注册资本错误',maskid)
		print(r.text)
		exit()
		return '-'	



with open('口罩厂家_百度.json',encoding='utf-8')as f:
	data = f.read()
data = json.loads(data)
# with open('口罩厂家信息_百度源.csv','a+',encoding='utf-8')as f:
# 	f.write(','.join(['厂名','注册资本','地址','产品','批准编号'])+'\n')

for item in data['data']['list'][804:]:
	name = item["regName"]
	maskid = item['encryptRegNo']
	pid = item['pid']
	info = json.loads(get_info(maskid))
	try:
		info  = info['data']["maskInfo"]
	except:
		time.sleep(10)
		print('sleeping')
		info = json.loads(get_info(maskid))
		info  = info['data']["maskInfo"]
	finally:
		addr = info["produceAddr"]
		productName = info["productName"]
		regNo = info['regNo']#许可证
		bdcode = info["bdCode"]
		money = get_money(bdcode)
		with open('口罩厂家信息_百度源.csv','a+',encoding='utf-8')as f:
			f.write(','.join([name,money,addr,productName,regNo])+'\n')
		print('已爬取',name)
