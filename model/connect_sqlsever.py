import pyodbc

class connectsql:
    def __init__(self):
        print("连接数据库")
    def connect(server,database,name,password):
        conn=pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+name+';PWD='+password)

# 连接到数据库
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=your_server;DATABASE=your_database;UID=your_username;PWD=your_password')

# 创建游标
cursor = conn.cursor()

# 执行查询
cursor.execute("SELECT * FROM your_table")

# 获取结果集
for row in cursor.fetchall():
    print(row)

# 关闭连接
conn.close()
