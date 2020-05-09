
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
    "Cookie": '''BAIDUID=3A81D0B48C49C694C499E2EDB3735465:FG=1; BIDUPSID=3A81D0B48C49C694C499E2EDB3735465; PSTM=1585910552; MCITY=-%3A; BDUSS=F6bjZjRG5zalNhVzFFSjJmekh1REQ0TWhjRHZKZHk5ay1EMGlOLTJ6dHl2cnRlRVFBQUFBJCQAAAAAAAAAAAEAAAB9FP2cZGZzc2Z5dQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHIxlF5yMZReRj; CHKFORREG=42228c0c68b667b4b6574aea103a3322; bdindexid=qmnh9d0vv4qc93g1v3o3o9het6; H_PS_PSSID=1458_31169_21080_31186_30905_31271_31217_30823_31085_26350_31164_31195; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1586686783,1586770070,1586771509; delPer=0; PSINO=2; RT="sl=a&ss=k8ycsmb9&tt=b3i&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&z=1&dm=baidu.com&si=4c4zew9pf9z"; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1586779798''',
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
        data_url = 'http://index.baidu.com/api/SearchApi/index?area='+area+'&word='+key_word+'&startDate='+start+'&endDate='+end
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
        start = '2019-12-01'#i[0]
        end='2020-04-01'#i[1]
        key_word = '口罩'
        d = bd.get_bd_index(key_word,start,end,area)
        print(province_name)
        with open('d:/desktop/百度指数/口罩/city_19-12-01--20-04-01/'+province_name+'.dict','w+',encoding='utf-8') as f:
            f.write(str(d))
        # time.sleep()
