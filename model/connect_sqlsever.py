import pymysql

class connMysql:
    def __init__(self):
        print("数据库连接初始化")

    def connect(self, db_ipaddress, db_name, username, password):
        try:
            conn = pymysql.connect(host=db_ipaddress, user=username, passwd=password, database=db_name)
            print("数据库连接成功")
            return conn
        except pymysql.Error as e:
            print(e)
            raise

