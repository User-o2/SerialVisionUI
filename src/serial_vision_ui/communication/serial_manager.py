"""
串口通信管理类
"""

import serial
import serial.tools.list_ports
from typing import List, Dict, Optional
from PyQt5.QtCore import QTimer, pyqtSignal, QObject


class SerialCommunicator(QObject):
    """串口通信管理类"""
    
    # 定义信号
    data_received = pyqtSignal(str)  # 接收到数据时发出信号
    connection_status_changed = pyqtSignal(bool)  # 连接状态改变时发出信号
    
    def __init__(self, baudrate: int = 9600):
        """
        初始化串口通信器
        
        Args:
            baudrate: 波特率，默认9600
        """
        super().__init__()
        self.serial_connection = serial.Serial()
        self.serial_connection.baudrate = baudrate
        self.check_timer = QTimer()
        self.check_timer.timeout.connect(self._check_serial_data)
        
    def get_available_ports(self) -> Dict[str, str]:
        """
        获取系统中可用的串口
        
        Returns:
            包含串口名称和描述信息的字典
        """
        port_dict = {}
        port_list = list(serial.tools.list_ports.comports())
        
        for port in port_list:
            port_dict[port[0]] = port[1]
            
        return port_dict
    
    def open_port(self, port_name: str) -> bool:
        """
        打开指定串口
        
        Args:
            port_name: 串口名称
            
        Returns:
            是否成功打开串口
        """
        try:
            self.serial_connection.port = port_name
            self.serial_connection.open()
            
            if self.serial_connection.is_open:
                self.check_timer.start(100)  # 每100ms检查一次数据
                self.connection_status_changed.emit(True)
                return True
                
        except Exception as e:
            print(f"串口打开失败: {str(e)}")
            
        return False
    
    def close_port(self) -> None:
        """关闭串口连接"""
        try:
            self.check_timer.stop()
            if self.serial_connection.is_open:
                self.serial_connection.close()
            self.connection_status_changed.emit(False)
        except Exception:
            pass
    
    def send_data(self, data: bytes) -> bool:
        """
        发送数据到串口
        
        Args:
            data: 要发送的字节数据
            
        Returns:
            是否发送成功
        """
        if not self.serial_connection.is_open:
            return False
            
        try:
            self.serial_connection.write(data)
            return True
        except Exception as e:
            print(f"数据发送失败: {str(e)}")
            return False
    
    def _check_serial_data(self) -> None:
        """检查串口接收的数据"""
        if self.serial_connection.is_open and self.serial_connection.in_waiting:
            try:
                received_data = self.serial_connection.read(
                    self.serial_connection.in_waiting
                ).decode()
                self.data_received.emit(received_data)
            except Exception as e:
                print(f"串口数据读取错误: {str(e)}")
    
    def is_connected(self) -> bool:
        """
        检查串口是否已连接
        
        Returns:
            串口连接状态
        """
        return self.serial_connection.is_open
