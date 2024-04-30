from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QSizePolicy
from PySide6.QtCore import QSize, QTimer, Qt, QEasingCurve, QDate, QTime
from qfluentwidgets import (
    CardWidget,
    PushButton,
    SmoothScrollArea,
    TitleLabel,
    SubtitleLabel,
    LargeTitleLabel,
    Slider,
    FlowLayout,
    MessageBoxBase,
    MessageBox,
    LineEdit,
    ZhDatePicker,
    TimePicker,
    ToolTipFilter,
)
from qfluentwidgets import FluentIcon as FIF
from TaskBar import TaskBar


class TaskInfoBox(MessageBoxBase):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.yesButton.setText("完成")
        self.cancelButton.setText("取消")

        self.title = TitleLabel("创建任务", self)
        self.title.setFixedWidth(400)
        self.subTitle = SubtitleLabel("任务名称", self)
        self.lineEdit = LineEdit(self)
        self.lineEdit.setPlaceholderText("输入任务名称")
        self.lineEdit.setText("任务1")
        self.subTitle2 = SubtitleLabel("开始日期", self)
        self.datePicker_start = ZhDatePicker(self)
        self.datePicker_start.setDate(QDate.currentDate())
        self.timePicker_start = TimePicker(self)
        self.timePicker_start.setTime(QTime(0, 0))
        self.subTitle3 = SubtitleLabel("结束日期", self)
        self.datePicker_end = ZhDatePicker(self)
        self.datePicker_end.setDate(QDate.currentDate())
        self.timePicker_end = TimePicker(self)
        self.timePicker_end.setTime(QTime(0, 0))

        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()

        self.hbox1.addWidget(self.datePicker_start)
        self.hbox1.addWidget(self.timePicker_start)
        self.hbox2.addWidget(self.datePicker_end)
        self.hbox2.addWidget(self.timePicker_end)

        self.viewLayout.addWidget(self.title)
        self.viewLayout.addWidget(self.subTitle)
        self.viewLayout.addWidget(self.lineEdit)
        self.viewLayout.addWidget(self.subTitle2)
        self.viewLayout.addLayout(self.hbox1)
        self.viewLayout.addWidget(self.subTitle3)
        self.viewLayout.addLayout(self.hbox2)

    def get_data(self):
        start_date = (
            self.datePicker_start.getDate().toString("yyyy-MM-dd ")
            + self.timePicker_start.getTime().toString("hh:mm")
            + ":00"
        )
        end_date = (
            self.datePicker_end.getDate().toString("yyyy-MM-dd ")
            + self.timePicker_end.getTime().toString("hh:mm")
            + ":00"
        )

        if start_date < end_date:
            return {
                "title": self.lineEdit.text(),
                "start_date": start_date,
                "end_date": end_date,
            }
        else:
            warn = MessageBox("日期错误", "开始时间应小于结束时间", self.window())
            warn.yesButton.setText("确认")

            # 移除取消按钮
            warn.cancelButton.setParent(None)
            warn.buttonLayout.removeWidget(warn.cancelButton)

            warn.exec()

            return None


class TaskMain(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.init_widget()

        # 记录当前组件
        self.bars = []
        self.selected_bar = None

        # 定时更新
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)

    def init_widget(self):
        self.horizontalLayout = QHBoxLayout(self)
        self.CardWidget = CardWidget(self)
        self.CardWidget.setFixedWidth(440)
        self.verticalLayout = QVBoxLayout(self.CardWidget)
        self.PushButton = PushButton(self.CardWidget)
        self.PushButton.setIcon(FIF.ADD_TO)
        self.PushButton.setIconSize(QSize(40, 40))
        self.PushButton.setMinimumSize(0, 75)
        self.PushButton.setToolTip("添加任务")
        self.PushButton.installEventFilter(ToolTipFilter(self.PushButton))
        self.PushButton.clicked.connect(self.add_new_task)

        self.verticalLayout.addWidget(self.PushButton)

        self.SmoothScrollArea = SmoothScrollArea(self.CardWidget)
        self.SmoothScrollArea.setWidgetResizable(True)
        self.SmoothScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.SmoothScrollArea.setStyleSheet(
            "background-color: transparent; border: none"
        )
        self.scrollAreaWidgetContents = QWidget()
        self.flowLayout = FlowLayout(self.scrollAreaWidgetContents, needAni=True)
        self.flowLayout.ease = QEasingCurve.Type.OutQuart
        self.flowLayout.setAlignment(Qt.AlignTop)
        self.SmoothScrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.SmoothScrollArea)

        self.horizontalLayout.addWidget(self.CardWidget)

        self.CardWidget2 = CardWidget(self)
        self.verticalLayout3 = QVBoxLayout(self.CardWidget2)
        self.verticalLayout3.setSpacing(6)
        self.verticalLayout3.setAlignment(Qt.AlignTop)

        self.CardWidget3 = CardWidget()
        self.verticalLayout4 = QVBoxLayout(self.CardWidget3)
        self.verticalLayout4.setSpacing(6)
        self.verticalLayout4.setAlignment(Qt.AlignTop)

        self.LargeTitleLabel = LargeTitleLabel(self.CardWidget3)
        self.LargeTitleLabel.setWordWrap(True)
        self.LargeTitleLabel.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding
        )
        self.verticalLayout4.addWidget(self.LargeTitleLabel)
        self.verticalLayout3.addWidget(self.CardWidget3)

        self.CardWidget4 = CardWidget()
        self.verticalLayout5 = QVBoxLayout(self.CardWidget4)
        self.verticalLayout5.setSpacing(6)
        self.verticalLayout5.setAlignment(Qt.AlignTop)

        self.TitleLabel = TitleLabel("开始日期", self.CardWidget4)
        self.verticalLayout5.addWidget(self.TitleLabel)

        self.SubtitleLabel = SubtitleLabel(self.CardWidget4)
        self.verticalLayout5.addWidget(self.SubtitleLabel)
        self.verticalLayout3.addWidget(self.CardWidget4)

        self.CardWidget5 = CardWidget()
        self.verticalLayout6 = QVBoxLayout(self.CardWidget5)
        self.verticalLayout6.setSpacing(6)
        self.verticalLayout6.setAlignment(Qt.AlignTop)

        self.TitleLabel2 = TitleLabel("结束日期", self.CardWidget5)
        self.verticalLayout6.addWidget(self.TitleLabel2)

        self.SubtitleLabel2 = SubtitleLabel(self.CardWidget5)
        self.verticalLayout6.addWidget(self.SubtitleLabel2)
        self.verticalLayout3.addWidget(self.CardWidget5)

        self.CardWidget6 = CardWidget()
        self.verticalLayout7 = QVBoxLayout(self.CardWidget6)
        self.verticalLayout7.setSpacing(6)
        self.verticalLayout7.setAlignment(Qt.AlignTop)

        self.TitleLabel3 = TitleLabel("任务进度", self.CardWidget6)
        self.verticalLayout7.addWidget(self.TitleLabel3)

        self.Slider = Slider(self.CardWidget6)
        self.Slider.setOrientation(Qt.Horizontal)
        self.verticalLayout7.addWidget(self.Slider)
        self.verticalLayout3.addWidget(self.CardWidget6)

        self.horizontalLayout.addWidget(self.CardWidget2)

        self.setObjectName("MainWindow")

    def add_new_task(self):
        # 添加任务
        msgBox = TaskInfoBox(self.window())
        if msgBox.exec():
            # 获取输入
            data = msgBox.get_data()
            if data:
                task = TaskBar(
                    None, data["title"], data["start_date"], data["end_date"]
                )
                self.add_task_bar(task)

    def set_selected_bar(self, task_bar: TaskBar):
        # 设置选中组件
        if self.selected_bar:
            self.Slider.valueChanged.disconnect(self.selected_bar.set_progress)  # 解绑
            self.selected_bar.CardWidget.setStyleSheet(
                ".CardWidget{background-color:transparent}"
            )

        self.selected_bar = task_bar
        if self.selected_bar:
            task_bar.CardWidget.setStyleSheet(
                ".CardWidget{background-color:gray;border-radius: 50px;}"
            )

            # 设置标题
            self.LargeTitleLabel.setText(self.selected_bar.title)
            self.SubtitleLabel.setText(self.selected_bar.get_start_date())
            self.SubtitleLabel2.setText(self.selected_bar.get_end_date())

            self.Slider.setValue(self.selected_bar.task_progress)
            self.Slider.valueChanged.connect(self.selected_bar.set_progress)

        else:
            self.LargeTitleLabel.setText("")
            self.SubtitleLabel.setText("")
            self.SubtitleLabel2.setText("")
            self.Slider.setValue(0)

    def add_task_bar(self, task_bar: TaskBar):
        # 添加组件
        self.flowLayout.addWidget(task_bar)
        self.bars.append(task_bar)

        # 绑定函数
        task_bar.topmost_signal.connect(self.sort)
        task_bar.selected_signal.connect(self.set_selected_bar)
        task_bar.remove_signal.connect(self.remove_task_bar)
        task_bar.set_attribute_signal.connect(self.change_task_attr)

        # 设置初始显示
        if not self.selected_bar:
            self.set_selected_bar(task_bar)

        self.sort()

    def remove_task_bar(self, task_bar: TaskBar):
        # 移除组件
        task_bar.setParent(None)
        self.flowLayout.removeWidget(task_bar)
        self.bars.remove(task_bar)

        # 解除绑定
        task_bar.topmost_signal.disconnect(self.sort)
        task_bar.selected_signal.disconnect(self.set_selected_bar)
        task_bar.remove_signal.disconnect(self.remove_task_bar)
        task_bar.set_attribute_signal.disconnect(self.change_task_attr)

        if self.selected_bar == task_bar:
            self.set_selected_bar(self.bars[0] if self.bars else None)

    def change_task_attr(self, task_bar: TaskBar):
        # 改变任务设置
        data = task_bar.get_attribute()

        # 输入框设置
        msgBox = TaskInfoBox(self.window())
        msgBox.title.setText("调整任务设置")
        msgBox.lineEdit.setText(data["title"])
        msgBox.datePicker_start.setDate(
            QDate.fromString(data["start_date"][:10], "yyyy-MM-dd")
        )
        msgBox.timePicker_start.setTime(
            QTime.fromString(data["start_date"][11:], "hh:mm:ss")
        )
        msgBox.datePicker_end.setDate(
            QDate.fromString(data["end_date"][:10], "yyyy-MM-dd")
        )
        msgBox.timePicker_end.setTime(
            QTime.fromString(data["end_date"][11:], "hh:mm:ss")
        )

        # 获取，更改输入
        if msgBox.exec():
            data = msgBox.get_data()
            if data:
                task_bar.set_attribute(data)

        self.sort()
        self.set_selected_bar(task_bar)

    def load_tasks(self, tasks_data):
        # 从数据加载任务
        for i in tasks_data:
            task = TaskBar(
                None,
                title=i["title"],
                start_date=i["start_date"],
                end_date=i["end_date"],
                topmost=i["topmost"],
                progress=i["progress"],
            )
            self.add_task_bar(task)

        self.sort()

    def update_bars(self):
        # 定时更新
        for i in self.bars:
            i.update_ring()

    def sort(self):
        # 根据剩余时间排序组件
        self.bars.sort(key=lambda x: x.time_left + x.topmost)

        self.flowLayout.removeAllWidgets()
        for i in self.bars:
            self.flowLayout.addWidget(i)

        # 重绘组件
        self.flowLayout.update()

    def get_tasks_attr(self):
        # 返回所有任务数据
        return [i.get_attribute() for i in self.bars]
