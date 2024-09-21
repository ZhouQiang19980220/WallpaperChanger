# wallpaper/log_manager.py

import logging
import platform

class LogManager:
    def __init__(self, version: str):
        self.logger = logging.getLogger('WallpaperManager')
        self.logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler('wallpaper.log')
        fh.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s [OS: %(os)s, Version: %(version)s]'
        )
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        self.extra = {'os': platform.system(), 'version': version}

    def get_logger(self) -> logging.Logger:
        """获取日志记录器。"""
        return self.logger

    def get_extra(self) -> dict:
        """获取额外的日志信息。"""
        return self.extra
