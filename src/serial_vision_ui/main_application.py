"""
主应用程序类
整合所有模块功能的主控制器
"""

import sys
import cv2
import numpy as np
from typing import List, Optional
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap

from src.serial_vision_ui.ui.main_window_ui import UiMainWindow
from src.serial_vision_ui.vision.camera_manager import CameraManager
from src.serial_vision_ui.vision.image_processor import VisionMatcher, ImageProcessor
from src.serial_vision_ui.communication.serial_comm import SerialManager
from src.serial_vision_ui.utils.resource_manager import get_asset_path
from src.serial_vision_ui.utils.logger import OutputRedirector


class SerialVisionUI(QtWidgets.QWidget, UiMainWindow):
    """智能装配平台主应用程序类"""
    
    def __init__(self):
        """初始化主应用程序"""
        super().__init__()
        self.setup_ui(self)
        self._init_components()
        self._setup_ui_properties()
        self._load_resources()
        self._connect_signals()
        self._init_variables()
        
    def _init_components(self):
        """初始化各个组件"""
        # 摄像头管理器
        self.camera_manager = CameraManager()
        
        # 计算机视觉处理器
        self.vision_matcher = VisionMatcher()
        self.image_processor = ImageProcessor()
        
        # 串口通信管理器
        self.serial_manager = SerialManager()
        
        # UI定时器
        self.frame_timer = QTimer(self)
        self.progress_timer = QTimer(self)
        
        # 日志重定向
        sys.stdout = OutputRedirector(self.log_text)
        
    def _setup_ui_properties(self):
        """设置UI属性"""
        self.setWindowTitle("智能装配平台")
        self.setWindowIcon(QtGui.QIcon(get_asset_path('icons', 'blue_circle.jpg')))
        
        # 进度条设置
        self.progress_bar.setValue(0)
        self.progress_bar.setAlignment(QtCore.Qt.AlignCenter)
        self.progress_bar.setFormat("%p%")
        self.progress_bar.setTextVisible(True)
        
    def _load_resources(self):
        """加载资源文件"""
        try:
            # 加载Logo
            logo_pixmap = QPixmap(get_asset_path('images', 'logo.jpg'))
            self.logo_label.setPixmap(logo_pixmap)
            self.logo_label.setScaledContents(True)
            
            # 加载3D模型图
            model_pixmap = QPixmap(get_asset_path('images', '3Dmodel.jpg'))
            self.model_label.setPixmap(model_pixmap)
            self.model_label.setScaledContents(True)
            
            # 加载模板图像
            self.template_images = [
                cv2.imread(get_asset_path('images', 'img_circle1.jpg')),
                cv2.imread(get_asset_path('images', 'img_circle2.jpg')),
                cv2.imread(get_asset_path('images', 'img_circle3.jpg'))
            ]
            
        except Exception as e:
            print(f"资源加载失败: {str(e)}")
            
    def _connect_signals(self):
        """连接信号和槽"""
        # 串口按钮
        self.serial_check_button.clicked.connect(self._check_serial_ports)
        self.serial_open_button.clicked.connect(self._open_serial_port)
        self.serial_close_button.clicked.connect(self._close_serial_port)
        
        # 摄像头按钮
        self.camera_open_button.clicked.connect(self._open_camera)
        self.camera_close_button.clicked.connect(self._close_camera)
        
        # 控制按钮
        self.start_button.clicked.connect(self._start_system)
        self.motor_reset_button.clicked.connect(self._reset_motor)
        self.motor_start_button.clicked.connect(self._start_motor)
        self.cylinder1_button.clicked.connect(self._activate_cylinder1)
        self.cylinder2_button.clicked.connect(self._activate_cylinder2)
        self.cylinder3_button.clicked.connect(self._activate_cylinder3)
        
        # 定时器
        self.frame_timer.timeout.connect(self._update_frame)
        self.progress_timer.timeout.connect(self._update_progress)
        
        # 串口管理器信号
        self.serial_manager.data_received.connect(self._handle_serial_data)
        self.serial_manager.connection_changed.connect(self._on_serial_connection_changed)
        
    def _init_variables(self):
        """初始化变量"""
        # 识别状态
        self.recognition_active = False
        self.last_matched_template = None
        
        # 进度条
        self.current_progress = 0
        self.target_progress = 0
        
        # 气缸计数器
        self.cylinder_counters = {'1': 0, '2': 0, '3': 0}
        
        # 初始化串口和摄像头列表
        self._check_serial_ports()
        self._populate_camera_list()
        
        # 欢迎信息
        print("-" * 50)
        print("        欢迎使用智能装配平台")
        print("-" * 50)
        
    def _check_serial_ports(self):
        """检测可用串口"""
        print("开始检测串口...")
        ports = self.serial_manager.get_available_ports()
        
        self.serial_combo.clear()
        for port_name in ports.keys():
            self.serial_combo.addItem(port_name)
            
        print(f"检测到 {len(ports)} 个可用串口")
        
    def _open_serial_port(self):
        """打开串口"""
        port_name = self.serial_combo.currentText()
        if port_name:
            if self.serial_manager.open_port(port_name):
                print(f"串口 {port_name} 打开成功")
                self.serial_manager.start_monitoring()
            else:
                QMessageBox.critical(self, "错误", "串口打开失败！")
                
    def _close_serial_port(self):
        """关闭串口"""
        self.serial_manager.stop_monitoring()
        self.serial_manager.close_port()
        print("串口已关闭")
        
    def _populate_camera_list(self):
        """填充摄像头列表"""
        self.camera_combo.clear()
        available_cameras = self.camera_manager.get_available_cameras()
        
        for camera_index in available_cameras:
            self.camera_combo.addItem(f"Camera {camera_index}")
            
    def _open_camera(self):
        """打开摄像头"""
        if self.camera_combo.currentText():
            camera_index = int(self.camera_combo.currentText().split()[-1])
            
            if self.camera_manager.open_camera(camera_index):
                self.frame_timer.start(30)  # 30ms间隔更新帧
                self.camera_open_button.setEnabled(False)
                self.camera_close_button.setEnabled(True)
                self.last_matched_template = None
                print(f"摄像头 {camera_index} 打开成功")
            else:
                QMessageBox.warning(self, "错误", "无法打开摄像头！")
                
    def _close_camera(self):
        """关闭摄像头"""
        self.frame_timer.stop()
        self.camera_manager.close_camera()
        self.camera_label.clear()
        self.result_label.clear()
        self.camera_open_button.setEnabled(True)
        self.camera_close_button.setEnabled(False)
        self.recognition_active = False
        print("摄像头已关闭")
        self._populate_camera_list()
        
    def _start_system(self):
        """启动系统"""
        self.recognition_active = True
        print("智能装配平台启动...")
        
    def _reset_motor(self):
        """电机归位"""
        if self.serial_manager.send_data(b'2'):
            print("执行电机归位命令...")
        else:
            self._show_serial_error()
            
    def _start_motor(self):
        """启动电机"""
        if self.serial_manager.send_data(b'3'):
            print("执行启动电机命令...")
        else:
            self._show_serial_error()
            
    def _activate_cylinder1(self):
        """激活1号气缸"""
        if self.serial_manager.send_data(b'4'):
            print("执行1号气缸命令...")
        else:
            self._show_serial_error()
            
    def _activate_cylinder2(self):
        """激活2号气缸"""
        if self.serial_manager.send_data(b'5'):
            print("执行2号气缸命令...")
        else:
            self._show_serial_error()
            
    def _activate_cylinder3(self):
        """激活3号气缸"""
        if self.serial_manager.send_data(b'6'):
            print("执行3号气缸命令...")
        else:
            self._show_serial_error()
            
    def _show_serial_error(self):
        """显示串口错误"""
        if not self.serial_manager.is_connected():
            QMessageBox.warning(self, "错误", "请先打开串口连接！")
        else:
            QMessageBox.critical(self, "错误", "数据发送失败！")
            
    def _update_frame(self):
        """更新视频帧"""
        if not self.camera_manager.is_opened():
            return
            
        frame = self.camera_manager.capture_frame()
        if frame is None:
            return
            
        # 显示原始摄像头画面
        self._display_frame(frame, self.camera_label)
        
        # 执行图像识别
        if self.recognition_active:
            self._process_recognition(frame)
            
    def _display_frame(self, frame: np.ndarray, label_widget):
        """在标签组件中显示图像帧"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        
        qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        scaled_image = qt_image.scaled(
            label_widget.width(), label_widget.height(), 
            QtCore.Qt.KeepAspectRatio
        )
        label_widget.setPixmap(QPixmap.fromImage(scaled_image))
        
    def _process_recognition(self, frame: np.ndarray):
        """处理图像识别"""
        print("尝试识别物料标签...")
        
        matched_frame = None
        matched_template = None
        
        # 尝试与每个模板匹配
        for template in self.template_images:
            if template is not None:
                result_img, success = self.vision_matcher.orb_match(template, frame)
                if success:
                    matched_frame = result_img
                    matched_template = template
                    break
                    
        # 处理匹配结果
        if matched_frame is not None:
            print("成功识别到物料")
            self._set_progress(10)
            self._display_frame(matched_frame, self.result_label)
            self.recognition_active = False
            
            # 检查是否为新的匹配结果
            if self._is_new_match(matched_template):
                self._send_start_command()
                self.last_matched_template = matched_template
        else:
            # 显示原始帧
            self._display_frame(frame, self.result_label)
            
    def _is_new_match(self, template) -> bool:
        """检查是否为新的匹配结果"""
        return (self.last_matched_template is None or 
                not np.array_equal(self.last_matched_template, template))
                
    def _send_start_command(self):
        """发送启动命令"""
        if self.serial_manager.send_data(b'1'):
            print("上位机命令下位机启动项目流程...")
        else:
            self._show_serial_error()
            
    def _set_progress(self, target: int):
        """设置进度条目标值"""
        self.target_progress = target
        self.progress_timer.start(20)
        
    def _update_progress(self):
        """更新进度条"""
        if self.current_progress < self.target_progress:
            self.current_progress += 1
            self.progress_bar.setValue(self.current_progress)
        else:
            self.progress_timer.stop()
            
    def _handle_serial_data(self, data: str):
        """处理接收到的串口数据"""
        for char in data:
            if char == '2':
                print("收到反馈：电机已经归位")
                self._set_progress(30)
            elif char == '3':
                print("收到反馈：电机已经到达翻转位置")
                self._set_progress(40)
            elif char == '4':
                self.cylinder_counters['1'] += 1
                if self.cylinder_counters['1'] % 2 == 1:
                    print("收到反馈：1号电磁阀已经启动")
                    self._set_progress(50)
                else:
                    print("收到反馈：1号电磁阀已经关闭")
                    self._set_progress(80)
            elif char == '5':
                self.cylinder_counters['2'] += 1
                if self.cylinder_counters['2'] % 2 == 1:
                    print("收到反馈：2号电磁阀已经启动")
                    self._set_progress(60)
                else:
                    print("收到反馈：2号电磁阀已经关闭")
                    self._set_progress(70)
            elif char == '6':
                self.cylinder_counters['3'] += 1
                if self.cylinder_counters['3'] % 2 == 1:
                    print("收到反馈：3号电磁阀已经启动")
                else:
                    print("收到反馈：3号电磁阀已经关闭")
                self._set_progress(100)
                
    def _on_serial_connection_changed(self, connected: bool):
        """串口连接状态变化处理"""
        self.serial_open_button.setEnabled(not connected)
        self.serial_close_button.setEnabled(connected)
        
    def closeEvent(self, event):
        """窗口关闭事件"""
        # 清理资源
        if self.camera_manager.is_opened():
            self.camera_manager.close_camera()
        
        self.serial_manager.stop_monitoring()
        self.serial_manager.close_port()
        
        # 恢复标准输出
        sys.stdout = sys.__stdout__
        
        event.accept()
