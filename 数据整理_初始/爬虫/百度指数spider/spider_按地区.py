
# -*- coding: utf-8 -*-
 
import requests
import js2py
import urllib3,time
import json
# 禁用警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
 
js_string = '''
function decrypt(t, e) {
    for (var n = t.split(""), i = e.split(""), a = {}, r = [], o = 0; o < n.length / 2; o++)
        a[n[o]] = n[n.length / 2 + o];
    for (var s = 0; s < e.length; s++)
        r.push(a[i[s]]);
    return r.join("")
}
'''
 
headers = {
    "Cookie": '''BAIDUID=7102680246C70691B861E9BD616EE2C8:FG=1; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1590287287; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1590287290; BDUSS=lRTQld-ZFJBY2g5RWIzRUt0emdUd0dvaHlWUHo3cnNrQi12cDV-M3FGekFhUEZlRVFBQUFBJCQAAAAAAAAAAAEAAAB9FP2cZGZzc2Z5dQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMDbyV7A28led; RT="sl=2&ss=kakfz5zw&tt=4o1&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&z=1&dm=baidu.com&si=qw888bh8zaj&ld=mit&ul=sfg''',
    "Referer": "http://index.baidu.com/v2/main/index.html",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
"X-Requested-With": "XMLHttpRequest",
'Accept': "application/json, text/plain, */*",
'Accept-Encoding': "gzip, deflate",
'Accept-Language': "zh-CN,zh;q=0.9",
}
 
data_url = 'http://index.baidu.com/api/SearchApi/index?area={}&word={}&startDate={}&endDate={}'
uniq_id_url = 'https://index.baidu.com/Interface/ptbk?uniqid={}'
keys = ["all", "pc", "wise"]
 
 
class BDIndex(object):
 
    def __init__(self):
        self.session = self.get_session()
        pass
 
    @staticmethod
    def get_session():
        """
            初始化 session 会话
        :return:
        """
        session = requests.session()
        session.headers = headers
        session.verify = False
        return session
 
    @staticmethod
    def decrypt(key, data):
        """
            得到解密后的数据
        :param key:  key
        :param data: key 对应的 value
        :return:
        """
        js_handler = js2py.eval_js(js_string)
        return js_handler(key, data)
 
    def get_bd_index(self,key_word,start,end,area=0):
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
                uniq_id_url.format(response.get("data").get("uniqid"))
            ).json().get("data")
        except:
            print(response)
            return('')
            #exit()
        result = []
        data_dict = response.get("data").get("userIndexes")[0]
        for key in keys:
            decrypt_data = self.decrypt(uniq_id, data_dict.get(key).get("data"))
            result.append({key: decrypt_data})
        return result
 

if __name__ == '__main__':
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

    bd = BDIndex()
    # start='2010-12-01'
    # end='2020-04-01'
 #    ran = [
#('20-11-12-01', '20-12-04-01'),
# ('20-12-12-01', '20-13-04-01'),
# ('20-13-12-01', '20-14-04-01'),
# ('20-14-12-01', '20-15-04-01'),
# ('20-15-12-01', '20-16-04-01'),
# ('20-16-12-01', '20-17-04-01'),
# ('20-17-12-01', '20-18-04-01'),
# ('20-18-12-01', '20-19-04-01'),
#('20-19-12-01', '20-20-04-01'),
# ('20-19-01-01', '20-20-04-01'),
# ('20-11-01-01', '20-20-04-01')
#]
    for pnum in provinces:#2011-2019
        province_name = provinces[pnum]
        # with open('./area.txt',encoding='utf-8')as f:
        #     citys=eval(f.read())
        # #citys = citys[pnum]
        # citys = []
        #for city in citys:
        #city_name = city['label']
        #area = city['value']
        area =str(pnum)
        start = '2019-05-01'#i[0]
        end='2020-05-24'#i[1]
        key_word = '口罩'
        d = bd.get_bd_index(key_word,start,end,area)
        print(province_name)
        print(d)
        #with open('d:/desktop/百度指数/口罩/city_19-12-01--20-04-01/'+province_name+'.dict','w+',encoding='utf-8') as f:
        #    f.write(str(d))
        # time.sleep()
