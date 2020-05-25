
# -*- coding: utf-8 -*-
 
import requests
import js2py
import urllib3,time
 
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
    "Cookie": '''BAIDUID=3A81D0B48C49C694C499E2EDB3735465:FG=1; BIDUPSID=3A81D0B48C49C694C499E2EDB3735465; PSTM=1585910552; MCITY=-%3A; delPer=0; PSINO=2; jshunter-uuid=765acfdb-679b-4c72-b7ea-a8e8ab5efafc; BDUSS=F6bjZjRG5zalNhVzFFSjJmekh1REQ0TWhjRHZKZHk5ay1EMGlOLTJ6dHl2cnRlRVFBQUFBJCQAAAAAAAAAAAEAAAB9FP2cZGZzc2Z5dQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHIxlF5yMZReRj; CHKFORREG=42228c0c68b667b4b6574aea103a3322; bdindexid=qmnh9d0vv4qc93g1v3o3o9het6; H_PS_PSSID=1458_31169_21080_31186_30905_31271_31217_30823_31085_26350_31164_31195; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1586686783,1586770070,1586771509; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1586774349; RT="z=1&dm=baidu.com&si=og4vmh8w0fn&ss=k8y9xhbw&sl=16&tt=167n&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf"''',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/75.0.3770.142 Safari/537.36"
}
 
data_url = 'https://index.baidu.com/api/SearchApi/index?word={}&area={}&startDate={}&endDate={}'
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
        response = self.session.get(data_url.format(key_word,area,start,end)).json()
        print(response)
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
    bd = BDIndex()
    # start='2010-12-01'
    # end='2020-04-01'
    ran = [('2011-12-01', '2012-04-01'),
('2012-12-01', '2013-04-01'),
('2013-12-01', '2014-04-01'),
('2014-12-01', '2015-04-01'),
('2015-12-01', '2016-04-01'),
('2016-12-01', '2017-04-01'),
('2017-12-01', '2018-04-01'),
('2018-12-01', '2019-04-01'),
('2019-12-01', '2020-04-01'),
('2019-01-01', '2020-04-01'),
('2011-01-01', '2020-04-01')]
    for i in ran:#2011-2019
        start = i[0]
        end=i[1]
        key_word = 'n95'
        d = bd.get_bd_index(key_word,start,end)
        print(d)
        exit()
        with open('d:/desktop/百度指数/'+key_word+'/'+key_word+start+'_'+end+'.dict','w+',encoding='utf-8') as f:
            f.write(str(d))
        #time.sleep(5)
