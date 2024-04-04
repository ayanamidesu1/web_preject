from model.connect_sqlsever import connMysql
import pymysql
import json

class do_select_query:
    def conn(self):
        db_ipaddr = '127.0.0.1'
        db_name = 'web_user'
        db_username = 'root'
        db_password = 'root'

        conn = pymysql.connect(host=db_ipaddr, user=db_username, password=db_password,database='web_user', charset='utf8mb4')
        return conn

    def select_query(self, sql):
        conn = self.conn()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                data = [dict(zip([column[0] for column in cursor.description], row)) for row in result]
                # 将字典转换为 JSON 字符串
                json_data = json.dumps(data)
                return json_data
        finally:
            print("关闭数据库连接")
