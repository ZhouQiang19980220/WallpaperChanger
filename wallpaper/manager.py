# wallpaper/manager.py

import sys
import os
import random
import json
from typing import List, Optional
from PyQt5.QtCore import QTimer

from .log_manager import LogManager

class WallpaperManager:
    def __init__(self, logger_manager: LogManager):
        self.folder_path: Optional[str] = None
        self.image_list: List[str] = []
        self.current_index: int = -1
        self.timer: Optional[QTimer] = None
        self.interval: int = 60000  # 默认间隔为 60 秒

        self.logger = logger_manager.get_logger()
        self.extra = logger_manager.get_extra()

        self.logger.info('软件启动', extra=self.extra)

        # 加载上次的配置
        self.config_file = os.path.expanduser('~/.wallpaper_config.json')
        self.load_config()

    def load_config(self) -> None:
        """加载配置文件。"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.folder_path = config.get('folder_path')
                    if self.folder_path and os.path.isdir(self.folder_path):
                        self.set_folder(self.folder_path)
            except Exception as e:
                self.logger.error(f'加载配置文件时出错：{e}', extra=self.extra)
        else:
            # 如果是初次启动，尝试设置为 ~/Pictures
            default_folder = os.path.expanduser('~/Pictures')
            if os.path.isdir(default_folder):
                try:
                    self.set_folder(default_folder)
                    self.logger.info(f'初次启动，设置默认文件夹为 {default_folder}', extra=self.extra)
                except Exception as e:
                    self.logger.error(f'设置默认文件夹时出错：{e}', extra=self.extra)

    def save_config(self) -> None:
        """保存配置文件。"""
        config = {'folder_path': self.folder_path}
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f)
            self.logger.info('配置已保存', extra=self.extra)
        except Exception as e:
            self.logger.error(f'保存配置文件时出错：{e}', extra=self.extra)

    def set_folder(self, folder_path: str) -> None:
        """设定壁纸文件夹。"""
        if os.path.isdir(folder_path):
            self.folder_path = folder_path
            self.image_list = [
                os.path.join(self.folder_path, f)
                for f in os.listdir(self.folder_path)
                if os.path.isfile(os.path.join(self.folder_path, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))
            ]
            self.current_index = 0 if self.image_list else -1
            self.logger.info(f'设置壁纸文件夹为：{folder_path}', extra=self.extra)
            self.save_config()
        else:
            raise FileNotFoundError(f"未找到文件夹：{folder_path}")

    def set_wallpaper(self, image_path: str) -> None:
        """设置壁纸。"""
        try:
            if sys.platform == 'darwin':  # macOS
                from appscript import app, mactypes
                app('Finder').desktop_picture.set(mactypes.File(image_path))
            elif sys.platform.startswith('win'):  # Windows
                import ctypes
                ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 0)
            else:
                # Linux 系统，使用 GNOME 桌面环境
                os.system(f"gsettings set org.gnome.desktop.background picture-uri file://{image_path}")
            self.logger.info(f'设置壁纸为：{image_path}', extra=self.extra)
        except Exception as e:
            self.logger.error(f'设置壁纸时出错：{e}', extra=self.extra)
            raise e

    def next_wallpaper(self) -> None:
        """设置下一张壁纸。"""
        if self.image_list:
            self.current_index = (self.current_index + 1) % len(self.image_list)
            self.set_wallpaper(self.image_list[self.current_index])

    def previous_wallpaper(self) -> None:
        """设置上一张壁纸。"""
        if self.image_list:
            self.current_index = (self.current_index - 1) % len(self.image_list)
            self.set_wallpaper(self.image_list[self.current_index])

    def random_wallpaper(self) -> None:
        """随机设置壁纸。"""
        if self.image_list:
            self.current_index = random.randint(0, len(self.image_list) - 1)
            self.set_wallpaper(self.image_list[self.current_index])

    def start_slideshow(self, interval: int) -> None:
        """开始定时更换壁纸。"""
        self.interval = interval
        if self.timer is None:
            self.timer = QTimer()
            self.timer.timeout.connect(self.next_wallpaper)
            self.timer.start(self.interval)
            self.logger.info(f'开始定时更换壁纸，间隔：{self.interval} 毫秒', extra=self.extra)

    def stop_slideshow(self) -> None:
        """停止定时更换壁纸。"""
        if self.timer:
            self.timer.stop()
            self.timer = None
            self.logger.info('停止定时更换壁纸', extra=self.extra)
