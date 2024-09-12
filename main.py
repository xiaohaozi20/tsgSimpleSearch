
import configparser
import os
import subprocess
import sys

import cx_Oracle
import pandas as pd
import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QFileDialog, QLabel, QLineEdit,
                             QMainWindow, QMessageBox, QPushButton,
                             QTableWidget, QTableWidgetItem, QVBoxLayout,
                             QWidget)

import Ui_xiaohaozi as myui

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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(2000, 1200)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cxButton = QtWidgets.QPushButton(self.centralwidget)
        self.cxButton.setObjectName("cxButton")
        self.cxButton.clicked.connect(self.load_data)
        self.horizontalLayout.addWidget(self.cxButton)
        self.plcxButton = QtWidgets.QPushButton(self.centralwidget)
        self.plcxButton.setObjectName("plcxButton")
        self.plcxButton.clicked.connect(self.query_batch)
        self.horizontalLayout.addWidget(self.plcxButton)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.exportButton = QtWidgets.QPushButton(self.centralwidget)
        self.exportButton.setObjectName("exportButton")
        self.exportButton.clicked.connect(self.export_to_excel)
        self.horizontalLayout.addWidget(self.exportButton)
        self.setButton = QtWidgets.QPushButton(self.centralwidget)
        self.setButton.setObjectName("setButton")
        self.setButton.clicked.connect(self.open_file_in_notepad)
        self.horizontalLayout.addWidget(self.setButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.table = QtWidgets.QTableWidget(self.centralwidget)
        self.table.setObjectName("table")
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.verticalLayout.addWidget(self.table)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 582, 22))
        self.menubar.setObjectName("menubar")
        self.cx_menu = QtWidgets.QMenu(self.menubar)
        self.cx_menu.setObjectName("cx_menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.cx_menu.menuAction())

        self.retranslateUi(MainWindow)
        
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "图书馆简单查询V1.00"))
        self.cxButton.setText(_translate("MainWindow", "一键查询"))
        self.plcxButton.setText(_translate("MainWindow", "批量查询(待开发)"))
        self.lineEdit.setText(_translate("MainWindow", "输入数量"))
        self.exportButton.setText(_translate("MainWindow", "导出Excel"))
        self.setButton.setText(_translate("MainWindow", "设置"))
        self.cx_menu.setTitle(_translate("MainWindow", "简单查询"))
    
    def load_data(self):
        try:
            connection = cx_Oracle.connect(connect_str)
            cursor = connection.cursor()
            cursor.execute(query)

            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            self.table.setColumnCount(len(columns))
            self.table.setHorizontalHeaderLabels(columns)
            self.table.setRowCount(len(rows))

            for row_idx, row_data in enumerate(rows):
                for col_idx, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))
                    self.table.setItem(row_idx, col_idx, item)
            QtWidgets.QMessageBox.information(None, "提示", "数据加载完成！")
            cursor.close()
            connection.close()
        except cx_Oracle.DatabaseError as e:
            QtWidgets.QMessageBox.critical(None, "错误", f"数据库连接失败，报错：{e}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "错误", f"发生错误：{e}")

    def query_batch(self):
        input_text = self.lineEdit.text()
        try:
            connection = cx_Oracle.connect(connect_str)
            cursor = connection.cursor()
            cursor.execute(query)

            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            self.table.setColumnCount(len(columns))
            self.table.setHorizontalHeaderLabels(columns)
            self.table.setRowCount(len(rows))

            for row_idx, row_data in enumerate(rows):
                for col_idx, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))
                    self.table.setItem(row_idx, col_idx, item)
            QtWidgets.QMessageBox.information(None, "提示", "数据加载完成！")
            cursor.close()
            connection.close()
        except cx_Oracle.DatabaseError as e:
            QtWidgets.QMessageBox.critical(None, "错误", f"数据库连接失败，报错：{e}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "错误", f"发生错误：{e}")


    def export_to_excel(self):
        # 获取表格的数据
        row_count = self.table.rowCount()
        column_count = self.table.columnCount()
        data = []
        headers = []
        
        # 获取表头
        for col in range(column_count):
            headers.append(self.table.horizontalHeaderItem(col).text())
        
        # 获取表格内容
        for row in range(row_count):
            row_data = []
            for col in range(column_count):
                item = self.table.item(row, col)
                row_data.append(item.text() if item else '')
            data.append(row_data)

        # 创建DataFrame并导出到Excel
        df = pd.DataFrame(data, columns=headers)
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(None, "保存为Excel文件", "", "Excel Files (*.xlsx)", options=options)
        if file_path:
            try:
                df.to_excel(file_path, index=False, engine='openpyxl')
                QtWidgets.QMessageBox.information(None, "提示", "数据已成功导出到Excel！")
            except Exception as e:
                QtWidgets.QMessageBox.critical(None, "错误", f"导出失败：{e}")

    def open_file_in_notepad(self):
        file_path = "config.ini"  # 替换成你实际的文件路径
        try:
            # 使用 subprocess 打开文件
            subprocess.Popen(['notepad.exe', file_path])
        except Exception as e:
            print(f"Error opening file: {e}")
if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

