import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime


class Logger:
    def __init__(self, log_dir="H:/forum_log/log/", max_bytes=10 * 1024 * 1024, backup_count=5):
        # 检查 H 盘是否存在，不存在则使用 C 盘
        if not os.path.exists("H:/"):
            log_dir = "C:/forum_log/log/"
        self.log_dir = log_dir

        # 确保日志目录存在
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # 初始化 logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # 创建和添加处理器
        self._add_handler('info.log', logging.INFO, max_bytes, backup_count)
        self._add_handler('warning.log', logging.WARNING, max_bytes, backup_count)
        self._add_handler('error.log', logging.ERROR, max_bytes, backup_count)

    def _add_handler(self, filename, level, max_bytes, backup_count):
        file_path = os.path.join(self.log_dir, filename)
        handler = RotatingFileHandler(
            file_path,
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        handler.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def info(self, message):
        timestamped_message = self._add_timestamp(message)
        self.logger.info(timestamped_message)

    def warning(self, message):
        timestamped_message = self._add_timestamp(message)
        self.logger.warning(timestamped_message)

    def error(self, message, exc_info=False):
        timestamped_message = self._add_timestamp(message)
        self.logger.error(timestamped_message, exc_info=exc_info)

    def _add_timestamp(self, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return f"{message}\n{timestamp}"
