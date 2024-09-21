# time_input_widget.py

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSpinBox


class TimeInputWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 创建控件
        self.days_spinbox = QSpinBox()
        self.days_spinbox.setRange(0, 365)
        self.days_spinbox.setSuffix(" 天")

        self.hours_spinbox = QSpinBox()
        self.hours_spinbox.setRange(0, 23)
        self.hours_spinbox.setSuffix(" 时")

        self.minutes_spinbox = QSpinBox()
        self.minutes_spinbox.setRange(0, 59)
        self.minutes_spinbox.setSuffix(" 分")

        self.seconds_spinbox = QSpinBox()
        self.seconds_spinbox.setRange(0, 59)
        self.seconds_spinbox.setSuffix(" 秒")

        # 布局
        layout = QHBoxLayout()
        layout.addWidget(self.days_spinbox)
        layout.addWidget(self.hours_spinbox)
        layout.addWidget(self.minutes_spinbox)
        layout.addWidget(self.seconds_spinbox)

        self.setLayout(layout)

    def get_total_seconds(self) -> int:
        """获取总的秒数。"""
        days = self.days_spinbox.value()
        hours = self.hours_spinbox.value()
        minutes = self.minutes_spinbox.value()
        seconds = self.seconds_spinbox.value()
        total_seconds = days * 86400 + hours * 3600 + minutes * 60 + seconds
        return total_seconds
