import unittest
import requests
from ddt import ddt,data,unpack
import csv
import os
from db_fixture import test_data

parentdir=os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #os.path.abspath(__file__)返回当前文件路径
#sys.path.insert(0,parentdir)  # sys.path.insert(index,object)


def get_csv_data():
    filepath=parentdir+'/db_fixture/add_guest_testdata.csv'
    filename = open(filepath,'r+',newline='')
    csvData = csv.reader(filename)
    testData = []
    for data in csvData:
        testData.append(data)

    for d in testData[1:]:
        d[3]=int(d[3])

    return testData[1:]


@ddt
class AddGuestTest(unittest.TestCase):
    '''添加嘉宾'''
    def setUp(self):
        self.base_url="http://127.0.0.1:8000/api/add_guest/"

    @data(*get_csv_data())
    @unpack
    def test_add_guest(self,eid,realname,phone,expected_status,expected_message):
        payload={'eid':eid,'realname':realname,'phone':phone}
        r=requests.post(self.base_url,data=payload)
        self.result=r.json()
        self.assertEqual(self.result['status'],expected_status)
        self.assertEqual(self.result['message'],expected_message)

    def tearDown(self):
        print(self.result)

if __name__=='__main__':
    test_data.init_data() # 初始化测试数据
    unittest.main(verbosity=2)
