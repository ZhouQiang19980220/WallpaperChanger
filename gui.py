# gui.py

import sys
import os
from typing import Optional
from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QLabel,
    QFileDialog,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QSpinBox,
    QGroupBox,
    QVBoxLayout,
)

from PyQt5.QtCore import pyqtSignal

from wallpaper import WallpaperManager, VersionManager, LogManager
from time_input_widget import TimeInputWidget


class WallpaperApp(QWidget):
    close_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        # 初始化版本管理器和日志管理器
        self.version_manager = VersionManager()
        self.log_manager = LogManager(self.version_manager.get_version())

        # 初始化壁纸管理器
        self.manager = WallpaperManager(self.log_manager)

        self.init_ui()

    def init_ui(self) -> None:
        self.setWindowTitle(
            f"Wallpaper 壁纸管理器 v{self.version_manager.get_version()}"
        )
        self.setFixedSize(500, 350)  # 调整窗口大小

        # 状态面板
        self.status_group = QGroupBox("当前状态")
        self.mode_label = QLabel("模式：未开启定时更换")
        self.current_wallpaper_label = QLabel("当前壁纸：无")

        status_layout = QVBoxLayout()
        status_layout.addWidget(self.mode_label)
        status_layout.addWidget(self.current_wallpaper_label)
        self.status_group.setLayout(status_layout)

        # 时间输入控件
        self.time_input = TimeInputWidget()

        # 控件
        self.folder_label = QLabel(
            self.manager.folder_path if self.manager.folder_path else "未选择文件夹"
        )
        self.select_folder_btn = QPushButton("选择文件夹")
        self.set_wallpaper_btn = QPushButton("设置壁纸")
        self.prev_btn = QPushButton("上一张")
        self.next_btn = QPushButton("下一张")
        self.random_btn = QPushButton("随机")

        # 使用 QSpinBox 作为时间输入控件，以秒为单位
        self.interval_input = QSpinBox()
        self.interval_input.setRange(1, 3600)  # 设置范围为 1 秒到 1 小时
        self.interval_input.setValue(self.manager.interval // 1000)  # 将毫秒转换为秒
        self.interval_input.setSuffix(" 秒")
        self.start_slideshow_btn = QPushButton("开始定时更换")
        self.stop_slideshow_btn = QPushButton("停止定时更换")

        # 预留下载功能的按钮
        self.download_btn = QPushButton("下载壁纸（待实现）")

        # 布局
        folder_layout = QHBoxLayout()
        folder_layout.addWidget(self.folder_label)
        folder_layout.addWidget(self.select_folder_btn)

        control_layout = QHBoxLayout()
        control_layout.addWidget(self.set_wallpaper_btn)
        control_layout.addWidget(self.prev_btn)
        control_layout.addWidget(self.next_btn)
        control_layout.addWidget(self.random_btn)

        slideshow_layout = QHBoxLayout()
        slideshow_layout.addWidget(self.time_input)
        slideshow_layout.addWidget(self.start_slideshow_btn)
        slideshow_layout.addWidget(self.stop_slideshow_btn)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.status_group)

        # 将时间输入控件和开始/停止按钮放在一起
        slideshow_layout = QHBoxLayout()
        slideshow_layout.addWidget(self.time_input)
        slideshow_layout.addWidget(self.start_slideshow_btn)
        slideshow_layout.addWidget(self.stop_slideshow_btn)

        # 添加控件到主布局
        main_layout.addLayout(folder_layout)
        main_layout.addLayout(control_layout)
        main_layout.addLayout(slideshow_layout)
        main_layout.addWidget(self.download_btn)

        self.setLayout(main_layout)

        # 信号与槽
        self.select_folder_btn.clicked.connect(self.select_folder)
        self.set_wallpaper_btn.clicked.connect(self.set_wallpaper)
        self.prev_btn.clicked.connect(self.previous_wallpaper)
        self.next_btn.clicked.connect(self.next_wallpaper)
        self.random_btn.clicked.connect(self.random_wallpaper)
        self.start_slideshow_btn.clicked.connect(self.start_slideshow)
        self.stop_slideshow_btn.clicked.connect(self.stop_slideshow)
        self.download_btn.clicked.connect(self.download_wallpaper)
        self.close_signal.connect(self.on_close)

    def select_folder(self) -> None:
        try:
            initial_path = (
                self.manager.folder_path
                or os.path.expanduser("~/Pictures")
                or os.getcwd()
            )
            folder_path = QFileDialog.getExistingDirectory(
                self, "选择壁纸文件夹", initial_path
            )
            if folder_path:
                self.manager.set_folder(folder_path)
                self.folder_label.setText(folder_path)
        except Exception as e:
            self.manager.logger.error(
                f"选择文件夹时出错：{e}", extra=self.manager.extra
            )
            QMessageBox.critical(self, "错误", str(e))

    # 更新壁纸设置方法，添加更新当前壁纸路径的显示
    def set_wallpaper(self) -> None:
        try:
            initial_path = (
                self.manager.folder_path
                or os.path.expanduser("~/Pictures")
                or os.getcwd()
            )
            image_path, _ = QFileDialog.getOpenFileName(
                self, "选择壁纸图片", initial_path, "Images (*.png *.jpg *.jpeg *.bmp)"
            )
            if image_path:
                self.manager.set_wallpaper(image_path)
                self.current_wallpaper_label.setText(f"当前壁纸：{image_path}")
        except Exception as e:
            self.manager.logger.error(f"设置壁纸时出错：{e}", extra=self.manager.extra)
            QMessageBox.critical(self, "错误", str(e))

    def previous_wallpaper(self) -> None:
        try:
            self.manager.previous_wallpaper()
        except Exception as e:
            self.manager.logger.error(
                f"上一张壁纸时出错：{e}", extra=self.manager.extra
            )
            QMessageBox.critical(self, "错误", str(e))

    def next_wallpaper(self) -> None:
        try:
            self.manager.next_wallpaper()
        except Exception as e:
            self.manager.logger.error(
                f"下一张壁纸时出错：{e}", extra=self.manager.extra
            )
            QMessageBox.critical(self, "错误", str(e))

    def random_wallpaper(self) -> None:
        try:
            self.manager.random_wallpaper()
        except Exception as e:
            self.manager.logger.error(f"随机壁纸时出错：{e}", extra=self.manager.extra)
            QMessageBox.critical(self, "错误", str(e))

    def start_slideshow(self) -> None:
        try:
            interval_seconds = self.time_input.get_total_seconds()
            if interval_seconds <= 0:
                QMessageBox.warning(self, "输入错误", "请输入有效的时间间隔。")
                return
            interval_ms = interval_seconds * 1000  # 将秒转换为毫秒
            self.manager.start_slideshow(interval_ms)
            QMessageBox.information(self, "提示", "定时更换壁纸已启动。")
            self.mode_label.setText("模式：定时更换已开启")
        except Exception as e:
            self.manager.logger.error(
                f"开始定时更换时出错：{e}", extra=self.manager.extra
            )
            QMessageBox.critical(self, "错误", str(e))

    # 更新 stop_slideshow 方法
    def stop_slideshow(self) -> None:
        try:
            self.manager.stop_slideshow()
            QMessageBox.information(self, "提示", "定时更换壁纸已停止。")
            self.mode_label.setText("模式：定时更换已停止")
        except Exception as e:
            self.manager.logger.error(
                f"停止定时更换时出错：{e}", extra=self.manager.extra
            )
            QMessageBox.critical(self, "错误", str(e))

    def download_wallpaper(self) -> None:
        QMessageBox.information(self, "提示", "该功能尚未实现，敬请期待！")

    def closeEvent(self, event):
        self.close_signal.emit()
        super().closeEvent(event)

    def on_close(self):
        self.manager.logger.info("软件关闭", extra=self.manager.extra)
