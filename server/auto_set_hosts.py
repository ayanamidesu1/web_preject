import os
import sys
import ctypes
import shutil

def is_admin():
    """
    检查当前用户是否具有管理员权限
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def modify_hosts(ip_address, domain_name):
    """
    修改 hosts 文件，添加新的 IP 和域名映射
    """
    # 定义 hosts 文件路径
    hosts_path = r'C:\Windows\System32\drivers\etc\hosts'
    backup_path = r'C:\Windows\System32\drivers\etc\hosts_backup'

    # 检查是否有备份，没有则创建一个
    if not os.path.exists(backup_path):
        shutil.copy(hosts_path, backup_path)
        print("备份已创建")

    def add_host_entry(ip, domain):
        # 以utf-8编码打开文件
        with open(hosts_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # 检查是否已经存在该条记录
        for line in lines:
            if domain in line:
                print(f"记录 {domain} 已存在")
                return

        # 如果不存在，则追加
        with open(hosts_path, 'a', encoding='utf-8') as file:
            file.write(f"{ip} {domain}\n")
            print(f"已添加 {domain} 到 hosts 文件")

    # 添加新的 host 条目
    add_host_entry(ip_address, domain_name)

def request_admin():
    """
    重新启动程序并申请管理员权限
    """
    print("尝试以管理员权限重新运行脚本...")
    # 通过 UAC 提升权限
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

if __name__ == "__main__":
    # 检查是否为管理员权限
    if is_admin():
        # 有管理员权限，执行修改 hosts 的操作
        ip_address = "127.0.0.1"
        domain_name = "www.sunyuanling.com"
        modify_hosts(ip_address, domain_name)
        print("hosts 文件修改完成")

        # 添加此行以防程序立即退出
        input("操作完成，按 Enter 键退出...")
    else:
        # 没有管理员权限，请求提升权限
        request_admin()
        # 程序退出
        sys.exit(0)
