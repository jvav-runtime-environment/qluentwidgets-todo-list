# -----------------------------
#
# 由于pyinstaller打包体积太过庞大
# 所以不提供打包后的程序
# 使用本模块安装需要的依赖
#
# -----------------------------

import os


has_all_dependencies = True

try:
    import PySide6
    import PySide6.QtWidgets
    import PySide6.QtGui
except ImportError:
    has_all_dependencies = False
    print("missing pyside6, installing ...")
    os.system("pip install pyside6")

try:
    import qfluentwidgets
except ImportError:
    has_all_dependencies = False
    print("missing qfluentwidgets, installing ...")
    os.system("pip install qfluentwidgets")

if not has_all_dependencies:
    print("安装完成, 请重新启动程序")
    os.system("pause")
    exit()
