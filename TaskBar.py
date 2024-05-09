from PySide6.QtWidgets import (
    QHBoxLayout,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)

from PySide6.QtCore import QSize, Signal

from qfluentwidgets import (
    CaptionLabel,
    CardWidget,
    ProgressRing,
    TitleLabel,
    TransparentToolButton,
    color,
    MessageBox,
    ToolTipFilter,
)

from qfluentwidgets import FluentIcon as FIF

import datetime
from PyQt5.QtCore import QTimer


class TaskBar(QWidget):

    topmost_signal = Signal()
    remove_signal = Signal(type)
    selected_signal = Signal(type)
    set_attribute_signal = Signal(type)

    def __init__(
        self,
        parent=None,
        title="ERROR",
        start_date="2024-04-27 00:00:00",
        end_date="2024-04-28 00:00:02",
        topmost=False,
        progress=0,
    ):
        super().__init__(parent=parent)
        self.init_widgets()

        # 时间设置
        self.start_date = datetime.datetime.fromisoformat(start_date)
        self.end_date = datetime.datetime.fromisoformat(end_date)
        self.current_date = datetime.datetime.now()

        self.time_left = 0
        self.ring_color = color.QColor(0, 255, 0)
        self.topmost = topmost
        self.task_progress = progress

        # 初始化基础信息
        self.title = title
        self.TitleLabel.setText(title)
        self.update_ring()
        self.update_topmost_icon()

    def init_widgets(self):
        self.CardWidget = CardWidget(self)
        self.CardWidget.setBorderRadius(50)
        self.horizontalLayout2 = QHBoxLayout(self.CardWidget)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(5)
        self.ProgressRing = ProgressRing(self.CardWidget)
        self.ProgressRing.setMaximum(0)
        self.ProgressRing.setMinimum(-100)
        self.ProgressRing.setFixedSize(80, 80)
        self.ProgressRing.setStrokeWidth(10)

        self.CardWidget.setFixedSize(400, 100)
        self.setFixedSize(400, 100)

        self.horizontalLayout.addWidget(self.ProgressRing)

        self.verticalLayout = QVBoxLayout()
        self.TitleLabel = TitleLabel(self.CardWidget)

        self.verticalLayout.addWidget(self.TitleLabel)

        self.horizontalLayout3 = QHBoxLayout()
        self.horizontalLayout3.setSpacing(0)
        self.CaptionLabel = CaptionLabel(self.CardWidget)

        self.horizontalLayout3.addWidget(self.CaptionLabel)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.horizontalLayout3.addItem(self.horizontalSpacer)

        self.TransparentToolButton = TransparentToolButton(self.CardWidget)
        self.TransparentToolButton.setFixedSize(35, 35)
        self.TransparentToolButton.setIcon(FIF.UP)
        self.TransparentToolButton.setIconSize(QSize(20, 20))
        self.TransparentToolButton.setToolTip("置顶任务")
        self.TransparentToolButton.installEventFilter(
            ToolTipFilter(self.TransparentToolButton)
        )
        self.TransparentToolButton.clicked.connect(self.button_topmost_func)

        self.horizontalLayout3.addWidget(self.TransparentToolButton)

        self.TransparentToolButton2 = TransparentToolButton(self.CardWidget)
        self.TransparentToolButton2.setFixedSize(35, 35)
        self.TransparentToolButton2.setIcon(FIF.SETTING)
        self.TransparentToolButton2.setIconSize(QSize(20, 20))
        self.TransparentToolButton2.setToolTip("更改信息")
        self.TransparentToolButton2.installEventFilter(
            ToolTipFilter(self.TransparentToolButton2)
        )
        self.TransparentToolButton2.clicked.connect(self.button_setting_func)

        self.horizontalLayout3.addWidget(self.TransparentToolButton2)

        self.TransparentToolButton3 = TransparentToolButton(self.CardWidget)
        self.TransparentToolButton3.setFixedSize(35, 35)
        self.TransparentToolButton3.setIcon(FIF.COMPLETED)
        self.TransparentToolButton3.setIconSize(QSize(20, 20))
        self.TransparentToolButton3.setToolTip("完成任务")
        self.TransparentToolButton3.installEventFilter(
            ToolTipFilter(self.TransparentToolButton3)
        )
        self.TransparentToolButton3.clicked.connect(self.button_complete_func)

        self.horizontalLayout3.addWidget(self.TransparentToolButton3)

        self.horizontalSpacer2 = QSpacerItem(
            15, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum
        )

        self.horizontalLayout3.addItem(self.horizontalSpacer2)

        self.verticalLayout.addLayout(self.horizontalLayout3)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout2.addLayout(self.horizontalLayout)

    def set_title(self, title: str):
        # 设置标题
        self.title = title
        self.TitleLabel.setText(title)

    def update_ring(self):
        # 更新进度环
        self.current_date = datetime.datetime.now()
        last_time = self.end_date - self.current_date
        total_time = self.end_date - self.start_date
        if total_time.total_seconds() != 0:
            self.time_left = last_time / total_time  # 计算当前剩余进度
        else:
            self.time_left = 0

        # 限制范围
        if self.time_left > 1:
            self.time_left = 1
        elif self.time_left < 0:
            self.time_left = 0

        # 进度条设置
        self.ProgressRing.setValue(-self.time_left * 100)

        # 进度条颜色设置
        if self.time_left > 0.5:
            self.ring_color.setRed(int(255 * (1 - self.time_left) * 2))
            self.ring_color.setGreen(255)
        else:
            self.ring_color.setRed(255)
            self.ring_color.setGreen(int(255 * self.time_left * 2))

        self.ProgressRing.setCustomBarColor(self.ring_color, self.ring_color)

        # 倒计时显示
        if last_time >= datetime.timedelta(seconds=0):
            if last_time.days > 0:
                self.CaptionLabel.setText(f"距离截止时间还剩{last_time.days}天")
            else:
                sec = last_time.seconds
                self.CaptionLabel.setText(
                    f"距离截止时间仅剩{sec//3600%24}时{sec//60%60}分{sec%60}秒"
                )
        else:
            self.CaptionLabel.setText("截止时间已过!")
            self.ProgressRing.setCustomBarColor("#ff0000", "#ff0000")
            self.ProgressRing.setValue(-100)
            self.time_left = 0

    def mousePressEvent(self, event):
        # 将自己设为选中
        self.selected_signal.emit(self)

    def set_progress(self, progress):
        # 任务完成进度设置
        self.task_progress = progress

    def button_topmost_func(self):
        # 置顶和取消按钮
        self.topmost = not self.topmost
        self.topmost_signal.emit()

        self.update_topmost_icon()

    def update_topmost_icon(self):
        # 更新图标方向
        if self.topmost:
            self.TransparentToolButton.setIcon(FIF.DOWN)
        else:
            self.TransparentToolButton.setIcon(FIF.UP)

    def button_setting_func(self):
        # 设置按钮
        self.set_attribute_signal.emit(self)

    def button_complete_func(self):
        # 任务完成
        msgBox = MessageBox(
            "移除任务", "确认要移除该任务吗?(该操作不可恢复)", self.window()
        )
        msgBox.yesButton.setText("确定")
        msgBox.cancelButton.setText("取消")
        if msgBox.exec():
            self.remove_signal.emit(self)

    def get_start_date(self):
        return self.start_date.isoformat().replace("T", " ")

    def get_end_date(self):
        return self.end_date.isoformat().replace("T", " ")

    def set_attribute(self, data: dict):
        # 设置属性
        self.set_title(data["title"])
        self.start_date = datetime.datetime.fromisoformat(data["start_date"])
        self.end_date = datetime.datetime.fromisoformat(data["end_date"])
        self.update_ring()

    def get_attribute(self):
        # 获取属性
        return {
            "title": self.title,
            "start_date": self.get_start_date(),
            "end_date": self.get_end_date(),
            "topmost": self.topmost,
            "progress": self.task_progress,
        }
