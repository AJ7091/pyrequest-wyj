import sys
sys.path.append('../db_fixture') # 将/db_fixture目录添加到python解析器的搜索路径中，python会从sys.path中搜索相关路径
try:
    from mysql_db import DB
except ImportError:
    from .mysql_db import DB

if __name__=='__main__':
    print(sys.path)