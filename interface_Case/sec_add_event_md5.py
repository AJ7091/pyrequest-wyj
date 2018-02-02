import unittest
import requests
import hashlib
import os,sys
parentdir=os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #os.path.abspath(__file__)返回当前文件路径
sys.path.insert(0,parentdir)  # sys.path.insert(index,object)
from db_fixture import test_data
from time import time

class AddEventTest(unittest.TestCase):
    '''添加发布会'''

    def setUp(self):
        self.base_url = "http://127.0.0.1:8000/api/sec_add_event/"
        #api_key
        self.api_key="&Guest-Bugmaster"
        #当前时间
        now_time=time()
        self.client_time = str(now_time).split('.')[0]
        #sign
        md5 = hashlib.md5()
        sign_str = self.client_time + self.api_key
        sign_bytes_utf8 = sign_str.encode(encoding="utf-8")
        md5.update(sign_bytes_utf8)
        self.sign_md5 = md5.hexdigest()

    def test_add_event_request_error(self):
        '''请求方法错误'''
        r = requests.get(self.base_url)
        self.result = r.json()
        self.assertEqual(self.result['status'],10011)
        self.assertEqual(self.result['message'],'request error')

    def test_add_event_sign_null(self):
        '''签名参数为空'''
        payload = {'eid': '', '': '', 'limit': '', 'address': '', 'start_time': '','time':'','sign':''}
        r = requests.post(self.base_url , data=payload)
        self.result=r.json()
        self.assertEqual(self.result['status'], 10012)
        self.assertEqual(self.result['message'],'user sign null')

    def test_add_event_time_out(self):
        '''请求超时'''
        now_time = str(int(self.client_time)-61)
        payload = {'eid': 1, '': '', 'limit': '', 'address': '', 'start_time': '', 'time': now_time, 'sign': 'adc'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10013)
        self.assertEqual(self.result['message'],'user sign timeout')

    def test_add_event_sign_fail(self):
        '''签名错误'''
        payload = {'eid': 1, '': '', 'limit': '', 'address': '', 'start_time': '', 'time': self.client_time, 'sign': 'adc'}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 10014)
        self.assertEqual(self.result['message'],'user sign fail')

    def test_add_event_success(self):
        '''添加成功'''
        payload = {'eid': 21, 'name': '一加5发布会', 'limit': 2000, 'address': '深圳',
                   'start_time': '2018-02-02 16:00:00', 'time': self.client_time, 'sign': self.sign_md5}
        r = requests.post(self.base_url, data=payload)
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertEqual(self.result['message'],'add event success')

    def tearDown(self):
        print(self.result)

if __name__=='__main__':
    test_data.init_data()
    unittest.main(verbosity=2)