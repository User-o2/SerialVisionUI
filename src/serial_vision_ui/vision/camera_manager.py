"""
摄像头管理器
"""

import cv2
from typing import List, Optional
from PyQt5.QtCore import QObject, pyqtSignal


class CameraManager(QObject):
    """摄像头管理器类"""
    
    frame_ready = pyqtSignal(object)  # 新帧准备就绪信号
    
    def __init__(self):
        """初始化摄像头管理器"""
        super().__init__()
        self.camera = None
        self.current_camera_index = 0
    
    def get_available_cameras(self) -> List[int]:
        """
        获取可用的摄像头列表
        
        Returns:
            可用摄像头索引列表
        """
        available_cameras = []
        
        for i in range(5):  # 检查前5个摄像头
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                available_cameras.append(i)
                cap.release()
        
        return available_cameras
    
    def open_camera(self, camera_index: int = 0) -> bool:
        """
        打开指定摄像头
        
        Args:
            camera_index: 摄像头索引
            
        Returns:
            是否成功打开摄像头
        """
        try:
            self.camera = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
            self.camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
            
            if self.camera.isOpened():
                self.current_camera_index = camera_index
                return True
            
        except Exception as e:
            print(f"摄像头打开失败: {str(e)}")
        
        return False
    
    def close_camera(self) -> None:
        """关闭摄像头"""
        if self.camera is not None:
            self.camera.release()
            self.camera = None
    
    def capture_frame(self) -> Optional[object]:
        """
        捕获一帧图像
        
        Returns:
            捕获的图像帧，如果失败返回None
        """
        if self.camera is not None and self.camera.isOpened():
            ret, frame = self.camera.read()
            if ret:
                return frame
        
        return None
    
    def is_opened(self) -> bool:
        """
        检查摄像头是否已打开
        
        Returns:
            摄像头开启状态
        """
        return self.camera is not None and self.camera.isOpened()
