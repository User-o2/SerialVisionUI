"""
UI生成代码 - 由PyQt5 UI代码生成器自动生成
警告：手动修改此文件时请谨慎，重新生成时会丢失更改
"""

from PyQt5 import QtCore, QtGui, QtWidgets


class UiMainWindow:
    """主窗口UI类"""
    
    def setup_ui(self, main_window):
        """设置UI界面"""
        main_window.setObjectName("MainWindow")
        main_window.resize(1431, 976)
        
        # 快捷按钮组
        self.shortcut_group = QtWidgets.QGroupBox(main_window)
        self.shortcut_group.setGeometry(QtCore.QRect(20, 500, 381, 461))
        self.shortcut_group.setObjectName("shortcut_group")
        self.shortcut_group.setTitle("快捷按钮")
        
        # 启动按钮
        self.start_button = QtWidgets.QPushButton(self.shortcut_group)
        self.start_button.setGeometry(QtCore.QRect(20, 60, 151, 91))
        self.start_button.setObjectName("start_button")
        self.start_button.setText("启动")
        font = QtGui.QFont()
        font.setPointSize(11)
        self.start_button.setFont(font)
        
        # 电机控制按钮
        self.motor_start_button = QtWidgets.QPushButton(self.shortcut_group)
        self.motor_start_button.setGeometry(QtCore.QRect(200, 60, 161, 91))
        self.motor_start_button.setObjectName("motor_start_button")
        self.motor_start_button.setText("启动电机")
        font.setPointSize(10)
        self.motor_start_button.setFont(font)
        
        self.motor_reset_button = QtWidgets.QPushButton(self.shortcut_group)
        self.motor_reset_button.setGeometry(QtCore.QRect(20, 210, 151, 91))
        self.motor_reset_button.setObjectName("motor_reset_button")
        self.motor_reset_button.setText("电机归位")
        self.motor_reset_button.setFont(font)
        
        # 气缸控制按钮
        self.cylinder1_button = QtWidgets.QPushButton(self.shortcut_group)
        self.cylinder1_button.setGeometry(QtCore.QRect(200, 210, 161, 91))
        self.cylinder1_button.setObjectName("cylinder1_button")
        self.cylinder1_button.setText("启动→气缸1")
        
        self.cylinder2_button = QtWidgets.QPushButton(self.shortcut_group)
        self.cylinder2_button.setGeometry(QtCore.QRect(20, 360, 151, 81))
        self.cylinder2_button.setObjectName("cylinder2_button")
        self.cylinder2_button.setText("启动→气缸2")
        self.cylinder2_button.setFont(font)
        
        self.cylinder3_button = QtWidgets.QPushButton(self.shortcut_group)
        self.cylinder3_button.setGeometry(QtCore.QRect(200, 360, 161, 81))
        self.cylinder3_button.setObjectName("cylinder3_button")
        self.cylinder3_button.setText("启动→气缸3")
        self.cylinder3_button.setFont(font)
        
        # 串口设置组
        self.serial_group = QtWidgets.QGroupBox(main_window)
        self.serial_group.setGeometry(QtCore.QRect(20, 260, 411, 231))
        self.serial_group.setObjectName("serial_group")
        self.serial_group.setTitle("设置串口")
        
        self.serial_check_button = QtWidgets.QPushButton(self.serial_group)
        self.serial_check_button.setGeometry(QtCore.QRect(40, 100, 131, 81))
        self.serial_check_button.setObjectName("serial_check_button")
        self.serial_check_button.setText("检测串口")
        font.setPointSize(11)
        self.serial_check_button.setFont(font)
        
        self.serial_open_button = QtWidgets.QPushButton(self.serial_group)
        self.serial_open_button.setGeometry(QtCore.QRect(230, 80, 121, 51))
        self.serial_open_button.setObjectName("serial_open_button")
        self.serial_open_button.setText("关闭串口")
        self.serial_open_button.setFont(font)
        
        self.serial_close_button = QtWidgets.QPushButton(self.serial_group)
        self.serial_close_button.setGeometry(QtCore.QRect(230, 150, 121, 51))
        self.serial_close_button.setObjectName("serial_close_button")
        self.serial_close_button.setText("关闭串口")
        self.serial_close_button.setFont(font)
        
        self.serial_label = QtWidgets.QLabel(self.serial_group)
        self.serial_label.setGeometry(QtCore.QRect(30, 30, 81, 31))
        self.serial_label.setObjectName("serial_label")
        self.serial_label.setText("选择串口")
        
        self.serial_combo = QtWidgets.QComboBox(self.serial_group)
        self.serial_combo.setGeometry(QtCore.QRect(120, 30, 221, 31))
        self.serial_combo.setObjectName("serial_combo")
        
        # 摄像头显示组
        self.camera_group = QtWidgets.QGroupBox(main_window)
        self.camera_group.setGeometry(QtCore.QRect(450, 10, 431, 481))
        self.camera_group.setObjectName("camera_group")
        self.camera_group.setTitle("摄像头画面")
        
        self.camera_label = QtWidgets.QLabel(self.camera_group)
        self.camera_label.setGeometry(QtCore.QRect(20, 20, 391, 371))
        self.camera_label.setObjectName("camera_label")
        
        self.camera_open_button = QtWidgets.QPushButton(self.camera_group)
        self.camera_open_button.setGeometry(QtCore.QRect(150, 410, 111, 61))
        self.camera_open_button.setObjectName("camera_open_button")
        self.camera_open_button.setText("关闭摄像头")
        font.setPointSize(10)
        self.camera_open_button.setFont(font)
        
        self.camera_close_button = QtWidgets.QPushButton(self.camera_group)
        self.camera_close_button.setGeometry(QtCore.QRect(280, 410, 121, 61))
        self.camera_close_button.setObjectName("camera_close_button")
        self.camera_close_button.setText("关闭摄像头")
        self.camera_close_button.setFont(font)
        
        self.camera_combo = QtWidgets.QComboBox(self.camera_group)
        self.camera_combo.setGeometry(QtCore.QRect(30, 430, 101, 31))
        self.camera_combo.setObjectName("camera_combo")
        
        # 识别结果显示组
        self.result_group = QtWidgets.QGroupBox(main_window)
        self.result_group.setGeometry(QtCore.QRect(900, 10, 511, 481))
        self.result_group.setObjectName("result_group")
        self.result_group.setTitle("识别结果")
        
        self.result_label = QtWidgets.QLabel(self.result_group)
        self.result_label.setGeometry(QtCore.QRect(20, 30, 471, 421))
        self.result_label.setObjectName("result_label")
        
        # 系统日志组
        self.log_group = QtWidgets.QGroupBox(main_window)
        self.log_group.setGeometry(QtCore.QRect(420, 500, 551, 361))
        self.log_group.setObjectName("log_group")
        self.log_group.setTitle("系统日志")
        
        self.log_text = QtWidgets.QPlainTextEdit(self.log_group)
        self.log_text.setGeometry(QtCore.QRect(10, 40, 531, 311))
        self.log_text.setObjectName("log_text")
        font = QtGui.QFont()
        font.setFamily("Adobe 黑体 Std R")
        font.setPointSize(12)
        font.setBold(True)
        self.log_text.setFont(font)
        
        # 进度条组
        self.progress_group = QtWidgets.QGroupBox(main_window)
        self.progress_group.setGeometry(QtCore.QRect(420, 880, 991, 81))
        self.progress_group.setObjectName("progress_group")
        self.progress_group.setTitle("当前进度")
        
        self.progress_bar = QtWidgets.QProgressBar(self.progress_group)
        self.progress_bar.setGeometry(QtCore.QRect(30, 40, 931, 31))
        self.progress_bar.setObjectName("progress_bar")
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.progress_bar.setFont(font)
        self.progress_bar.setProperty("value", 0)
        
        # 3D模型显示组
        self.model_group = QtWidgets.QGroupBox(main_window)
        self.model_group.setGeometry(QtCore.QRect(990, 500, 421, 361))
        self.model_group.setObjectName("model_group")
        self.model_group.setTitle("装配模型图")
        
        self.model_label = QtWidgets.QLabel(self.model_group)
        self.model_label.setGeometry(QtCore.QRect(10, 40, 391, 291))
        self.model_label.setObjectName("model_label")
        
        # Logo图片
        self.logo_label = QtWidgets.QLabel(main_window)
        self.logo_label.setGeometry(QtCore.QRect(30, 20, 401, 221))
        self.logo_label.setObjectName("logo_label")
        
    def setup_connections(self, main_window):
        """设置信号连接"""
        # 这里可以添加信号连接代码
        pass
