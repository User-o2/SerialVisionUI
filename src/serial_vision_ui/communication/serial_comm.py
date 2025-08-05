"""
串口通信管理器
"""

import serial
import serial.tools.list_ports
from typing import Dict, List, Optional, Callable
from PyQt5.QtCore import QObject, QTimer, pyqtSignal


class SerialManager(QObject):
    """串口通信管理器"""
    
    data_received = pyqtSignal(str)  # 数据接收信号
    connection_changed = pyqtSignal(bool)  # 连接状态变化信号
    
    def __init__(self):
        """初始化串口管理器"""
        super().__init__()
        self.serial_port = serial.Serial()
        self.serial_port.baudrate = 9600
        self.serial_port.timeout = 1
        
        # 定时器用于检查串口数据
        self.check_timer = QTimer()
        self.check_timer.timeout.connect(self._check_serial_data)
        
        self.is_monitoring = False
    
    def get_available_ports(self) -> Dict[str, str]:
        """
        获取可用串口列表
        
        Returns:
            串口字典 {端口名: 端口描述}
        """
        port_dict = {}
        port_list = list(serial.tools.list_ports.comports())
        
        for port in port_list:
            port_dict[str(port[0])] = str(port[1])
        
        return port_dict
    
    def open_port(self, port_name: str) -> bool:
        """
        打开串口
        
        Args:
            port_name: 串口名称
            
        Returns:
            是否成功打开
        """
        try:
            self.serial_port.port = port_name
            self.serial_port.open()
            
            if self.serial_port.is_open:
                self.connection_changed.emit(True)
                return True
                
        except Exception as e:
            print(f"串口打开失败: {str(e)}")
        
        return False
    
    def close_port(self) -> None:
        """关闭串口"""
        try:
            if self.serial_port.is_open:
                self.serial_port.close()
                self.connection_changed.emit(False)
        except Exception as e:
            print(f"串口关闭失败: {str(e)}")
    
    def send_data(self, data: bytes) -> bool:
        """
        发送数据
        
        Args:
            data: 要发送的字节数据
            
        Returns:
            是否发送成功
        """
        try:
            if self.serial_port.is_open:
                self.serial_port.write(data)
                return True
        except Exception as e:
            print(f"数据发送失败: {str(e)}")
        
        return False
    
    def start_monitoring(self, interval: int = 100) -> None:
        """
        开始监控串口数据
        
        Args:
            interval: 检查间隔（毫秒）
        """
        if not self.is_monitoring:
            self.check_timer.start(interval)
            self.is_monitoring = True
    
    def stop_monitoring(self) -> None:
        """停止监控串口数据"""
        if self.is_monitoring:
            self.check_timer.stop()
            self.is_monitoring = False
    
    def _check_serial_data(self) -> None:
        """检查串口数据（内部方法）"""
        if self.serial_port.is_open:
            try:
                if self.serial_port.in_waiting:
                    received_data = self.serial_port.read(self.serial_port.in_waiting).decode('utf-8', errors='ignore')
                    if received_data:
                        self.data_received.emit(received_data)
            except Exception as e:
                print(f"串口数据读取错误: {str(e)}")
    
    def is_connected(self) -> bool:
        """
        检查串口连接状态
        
        Returns:
            是否已连接
        """
        return self.serial_port.is_open
    
    def send_command(self, command: str) -> bool:
        """
        发送字符串命令
        
        Args:
            command: 命令字符串
            
        Returns:
            是否发送成功
        """
        return self.send_data(command.encode('utf-8'))
