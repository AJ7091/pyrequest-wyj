import time,sys
sys.path.append('./interface_Case')
sys.path.append('./db_fixture')
from HTMLTestRunner import HTMLTestRunner
import unittest
from db_fixture import test_data

# 指定测试用例为当前文件夹下的interface_Case目录
test_dir="./interface_Case"
test_list=unittest.defaultTestLoader.discover(test_dir,pattern='add_guest_test_ddt.py')

if __name__=='__main__':
    test_data.init_data() # 初始化接口测试数据

    now = time.strftime("%Y-%m-%d %H_%M_%S")
    filename = './report/' + now + '_result.html'
    fp = open(filename,'wb')
    runner=HTMLTestRunner(stream=fp,
                          title='Guest Manage System Interface Test Report',
                          description='Implementation Example with:',
                          verbosity=2) # 在窗口打印用例执行结果的详细程度设置
    runner.run(test_list)
    fp.close()
