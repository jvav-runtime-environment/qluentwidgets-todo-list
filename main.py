import getDependency

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from qfluentwidgets import FluentWindow, setTheme, Theme

from Tasks import TaskMain

import json
import warnings
import os

warnings.filterwarnings("ignore")


class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("任务管理")
        self.setMinimumSize(800, 600)
        self.setWindowIcon(QIcon("assests/files.svg"))

        self.task_main = TaskMain()
        self.addSubInterface(self.task_main, QIcon("assests/checklist.svg"), "任务")

    def load_tasks(self):
        if os.path.exists("tasks.json"):
            tasks = json.load(open("tasks.json", "r"))
        else:
            tasks = []

        self.task_main.load_tasks(tasks)

    def save_tasks(self):
        data = self.task_main.get_tasks_attr()
        json.dump(data, open("tasks.json", "w"))


setTheme(Theme.DARK)
app = QApplication()

window = MainWindow()
window.load_tasks()
window.show()

app.exec()

window.save_tasks()
