import configparser
import os
import sys

import cx_Oracle
import PyQt5
from PyQt5.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
                             QMessageBox, QPushButton, QTableWidget,
                             QTableWidgetItem, QVBoxLayout, QWidget)

dirname = os.path.dirname(PyQt5.__file__)
qt_dir = os.path.join(dirname, 'Qt5', 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = qt_dir

# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

# 初始化 Oracle 客户端
try:
    if sys.platform.startswith("darwin"):
        lib_dir = os.path.expanduser(config['Paths']['darwin_lib_dir'])
        cx_Oracle.init_oracle_client(lib_dir=lib_dir)
    elif sys.platform.startswith("win32"):
        lib_dir = config['Paths']['win32_lib_dir']
        cx_Oracle.init_oracle_client(lib_dir=lib_dir)
except Exception as err:
    print("初始化 Oracle 客户端失败!")
    print(err)
    sys.exit(1)

# 数据库连接信息
user = config['database']['user']
password = config['database']['password']
host = config['database']['host']
instance = config['database']['instance']
port = config['database']['port']
connect_str = f'{user}/{password}@{host}/{instance}'

# 查询语句
with open(config['SQL']['query_file'], 'r') as file:
    query = file.read()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Oracle 查询结果')
        self.setGeometry(100, 100, 2000, 1200)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        # Label for lib_dir input
        self.label = QLabel('请输入新的 lib_dir 路径:')
        layout.addWidget(self.label)

        # Input field for lib_dir
        self.lib_dir_input = QLineEdit()
        layout.addWidget(self.lib_dir_input)

        # Button to save the new lib_dir
        # self.save_button = QPushButton('保存路径')
        # self.save_button.clicked.connect(self.save_lib_dir)
        # layout.addWidget(self.save_button)
        self.table = QTableWidget()
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
