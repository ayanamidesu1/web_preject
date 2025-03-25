import os
import io
from datetime import datetime


class Logger:
    def __init__(self, log_dir="H:/web_project_log/", max_bytes=10 * 1024 * 1024, backup_count=5):
        # 检查 H 盘是否存在，不存在则使用 C 盘
        if not os.path.exists("H:/"):
            log_dir = "C:/web_project_log/"
        self.log_dir = log_dir
        self.max_bytes = max_bytes
        self.backup_count = backup_count

        # 确保日志目录存在
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def info(self, message):
        self._write_to_log('info.log', message)

    def warning(self, message):
        self._write_to_log('warning.log', message)

    def error(self, message):
        self._write_to_log('error.log', message)

    def _write_to_log(self, filename, message):
        file_path = os.path.join(self.log_dir, filename)

        # 检查文件大小是否超过限制
        if os.path.exists(file_path) and os.path.getsize(file_path) >= self.max_bytes:
            self._rotate_log(filename)

        # 写入日志
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"{timestamp} - {message}\n"

        with io.open(file_path, 'a', encoding='utf-8') as file:
            file.write(log_message)

    def _rotate_log(self, filename):
        file_path = os.path.join(self.log_dir, filename)

        # 重命名超过上限的日志文件
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        new_name = f"{timestamp}_{filename}"
        os.rename(file_path, os.path.join(self.log_dir, new_name))

        # 删除最老的日志文件
        self._delete_oldest_log(filename)

    def _delete_oldest_log(self, filename):
        log_files = sorted(os.listdir(self.log_dir))
        log_files = [f for f in log_files if f.startswith(filename.split('.')[0])]

        if len(log_files) > self.backup_count:
            oldest_file = log_files[0]
            os.remove(os.path.join(self.log_dir, oldest_file))
