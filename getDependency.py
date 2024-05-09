# -----------------------------
#
# 由于pyinstaller打包体积太过庞大
# 所以不提供打包后的程序
# 使用本模块安装需要的依赖
#
# -----------------------------

import os


has_pyside6 = True
has_qfluentwidgets = True

try:
    import PySide6
    import PySide6.QtWidgets
    import PySide6.QtGui
except ImportError:
    has_pyside6 = False

try:
    import qfluentwidgets
except ImportError:
    has_qfluentwidgets = False


if not (has_pyside6 and has_qfluentwidgets):
    print("缺少运行库:")
    if not has_pyside6:
        print("- PySide6")
    if not has_qfluentwidgets:
        print("- qfluentwidgets")

    if input("是否安装?:(y/n)") == "y":
        if not has_pyside6:
            os.system("pip install PySide6")
        if not has_qfluentwidgets:
            os.system("pip install qfluentwidgets")
