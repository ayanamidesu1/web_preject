# 将当前脚本目录切换到 H: 盘
Set-Location H:\

# 路径定义
$webPath = "H:\web_project\web"
$serverPath = "H:\web_project\server"
$tornadoPath = "H:\web_project\server\tornado_server"

# 启动前端 (npm run dev)
Start-Process powershell -ArgumentList "cd `"$webPath`"; npm run dev"

# 启动 Django 后端 (python manage.py runserver 2233)
Start-Process powershell -ArgumentList "cd `"$serverPath`"; python ./manage.py runserver 2233"

# 启动 Tornado 服务 (python main.py)
Start-Process powershell -ArgumentList "cd `"$tornadoPath`"; python main.py"
