from pymysql import connect,cursors
from pymysql.err import OperationalError
import os
import configparser as cparser # 使用配置文件（.ini）生效

# ===========读取db_config.ini文件设置=============
base_dir = str(os.path.dirname(os.path.dirname(__file__))) # os.path.dirname(__file__)获取当前文件运行的目录，两次嵌套获取到根目录下
base_dir = base_dir.replace('\\','/')
file_path = base_dir+"/db_config.ini"
#print(os.path.dirname(__file__))
#print(base_dir)

cf = cparser.ConfigParser() # 实例化对象
cf.read(file_path) # 读取db_config.ini文件

host = cf.get('mysqlconf','host')
port = cf.get('mysqlconf','port')
db = cf.get('mysqlconf','db_name')
user = cf.get('mysqlconf','user')
password = cf.get('mysqlconf','password')


# ==============封装Mysql基本操作===============
class DB():
    def __init__(self):
        try:
            # 连接数据库
            self.conn=connect(host=host,
                              user=user,
                              password=password,
                              db=db,
                              charset='utf8mb4',
                              cursorclass=cursors.DictCursor) # 查询结果以dic(字典)形式返回
        except OperationalError as e:
            print("Mysql Error %d: %s"%(e.args[0],e.args[1]))


    # 清除表数据
    def clear(self,table_name):
        #real_sql="truncate table"+table_name+";"
        real_sql="delete from "+table_name+";"
        with self.conn.cursor() as cursor:   # 游标指针，获得当前指向数据库的指针赋值给cursor，也可写成：cursor=self.conn.cursor
            # execute(query, args):执行单条sql语句。query为sql语句本身，args为参数值的列表。执行后返回值为受影响的行数
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")  # 取消外键约束，才好删除表数据
            cursor.execute(real_sql)
        self.conn.commit() # 提交数据库sql操作

    # 插入表数据
    def inser(self,table_name,table_data):
        for key in table_data:
            table_data[key] = "'"+str(table_data[key])+"'"  # 改变value的值
        key   = ','.join(table_data.keys())  # join()方法用于将序列中的元素以指定的字符连接生成一个新的字符串
        value = ','.join(table_data.values())

        real_sql = "INSERT INTO " + table_name + " (" + key + ") VALUES (" + value + ")"

        with self.conn.cursor() as cursor:
            cursor.execute(real_sql)
        self.conn.commit()

    # 关闭数据库连接
    def close(self):
        self.conn.close()

    # 初始化测试数据
    def init_data(self,datas):
        for table,data in datas.items(): #items()以元组形式返回[(table1,data1),(table2,data2)]
            self.clear(table)
            for d in data:
                self.inser(table,d)
        self.close()



if __name__=='__main__':
    db = DB()
    table_name = 'sign_event'
    data = {'id':1,'name':'红米','`limit`':2000,'status':1,'address':'北京会展中心','start_time':'2016-08-20 00:25:42','create_time':'2000-01-01 00:00:00'}
    db.clear(table_name)
    db.inser(table_name,data)
    db.close()