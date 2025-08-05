"""
图像处理和计算机视觉相关功能
"""

import cv2
import numpy as np
from typing import Tuple, List, Optional, Union
from pyzbar.pyzbar import decode


class ImageProcessor:
    """图像处理器类"""
    
    @staticmethod
    def scan_qr_code(frame: np.ndarray) -> Tuple[Optional[np.ndarray], Optional[str]]:
        """
        扫描二维码
        
        Args:
            frame: 输入图像帧
            
        Returns:
            处理后的图像帧和解码的二维码数据
        """
        barcodes = decode(frame)
        
        if barcodes:
            for barcode in barcodes:
                qr_data = barcode.data.decode('utf-8')
                
                # 绘制边框
                pts = np.array([barcode.polygon], np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(frame, [pts], True, (0, 255, 0), 2)
                
                # 在二维码上方显示解码信息
                x, y, w, h = barcode.rect
                cv2.putText(frame, qr_data, (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                return frame, qr_data
        
        return None, None


class VisionMatcher:
    """计算机视觉匹配器类"""
    
    def __init__(self):
        """初始化ORB检测器和FLANN匹配器"""
        self.orb = cv2.ORB_create()
        
        # FLANN匹配器参数
        flann_index_lsh = 6
        index_params = dict(
            algorithm=flann_index_lsh,
            table_number=6,
            key_size=12,
            multi_prove_level=1
        )
        search_params = dict(checks=50)
        self.flann = cv2.FlannBasedMatcher(index_params, search_params)
        
        self.min_match_count = 30
    
    def detect_color_regions(self, frame: np.ndarray) -> Tuple[bool, bool]:
        """
        检测红色和蓝色区域
        
        Args:
            frame: 输入图像帧
            
        Returns:
            (是否检测到红色, 是否检测到蓝色)
        """
        # 应用ROI掩码
        img_mask = np.zeros_like(frame)
        img_mask[150:390, 180:425] = 1
        masked_frame = cv2.multiply(frame, img_mask)
        
        # 转换到HSV颜色空间
        hsv_frame = cv2.cvtColor(masked_frame, cv2.COLOR_BGR2HSV)
        
        # 定义颜色范围
        lower_red1 = np.array([0, 50, 50])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 50, 50])
        upper_red2 = np.array([180, 255, 255])
        lower_blue = np.array([100, 50, 50])
        upper_blue = np.array([125, 255, 255])
        
        # 创建颜色掩码
        mask_red1 = cv2.inRange(hsv_frame, lower_red1, upper_red1)
        mask_red2 = cv2.inRange(hsv_frame, lower_red2, upper_red2)
        mask_red = cv2.bitwise_or(mask_red1, mask_red2)
        mask_blue = cv2.inRange(hsv_frame, lower_blue, upper_blue)
        
        # 查找轮廓
        contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # 检测有效区域
        red_detected = self._is_valid_color_region(contours_red)
        blue_detected = self._is_valid_color_region(contours_blue)
        
        return red_detected, blue_detected
    
    def _is_valid_color_region(self, contours: List) -> bool:
        """
        检查轮廓是否为有效的颜色区域
        
        Args:
            contours: 轮廓列表
            
        Returns:
            是否为有效区域
        """
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1800:
                return True
        return False
    
    def detect_circles(self, frame: np.ndarray) -> Tuple[Optional[Tuple], float]:
        """
        检测圆形并计算误差
        
        Args:
            frame: 输入图像帧
            
        Returns:
            圆心坐标和半径，以及计算的误差
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (9, 9), 2)
        edges = cv2.Canny(blurred, 50, 150)
        
        circles = cv2.HoughCircles(
            edges, cv2.HOUGH_GRADIENT, 1, 40,
            param1=20, param2=30, minRadius=100, maxRadius=125
        )
        
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for circle in circles[0, :]:
                center = (circle[0], circle[1])
                radius = circle[2]
                
                # 计算形位公差误差
                error = abs(((radius - 113.37) / 113.37) * 22.4)
                
                return center, radius, error
        
        return None, None, -1
    
    def orb_match(self, template_img: np.ndarray, target_img: np.ndarray) -> Tuple[Optional[np.ndarray], bool]:
        """
        使用ORB算法进行特征点匹配
        
        Args:
            template_img: 模板图像
            target_img: 目标图像
            
        Returns:
            匹配结果图像和是否匹配成功
        """
        # 图像预处理
        blurred_target = cv2.GaussianBlur(target_img, (9, 9), 2)
        
        # 颜色检测
        red_detected, blue_detected = self.detect_color_regions(target_img)
        
        # 圆形检测
        center, radius, error = self.detect_circles(blurred_target)
        
        # ORB特征检测
        kp1, des1 = self.orb.detectAndCompute(template_img, None)
        kp2, des2 = self.orb.detectAndCompute(target_img, None)
        
        if des1 is None or des2 is None:
            return None, False
        
        # 特征匹配
        matches = self.flann.knnMatch(des1, des2, k=2)
        good_points = []
        
        for match in matches:
            if len(match) == 2:
                m, n = match
                if m.distance < 0.75 * n.distance:
                    good_points.append(m)
        
        if len(good_points) > self.min_match_count:
            # 计算单应性矩阵
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good_points]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_points]).reshape(-1, 1, 2)
            
            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            
            if M is not None:
                # 计算旋转角度
                theta = -np.arctan2(M[0, 1], M[0, 0]) * 180 / np.pi
                
                matches_mask = mask.ravel().tolist()
                
                # 绘制匹配结果
                draw_params = dict(
                    matchColor=(0, 255, 0),
                    singlePointColor=(0, 0, 255),
                    matchesMask=matches_mask,
                    flags=2
                )
                
                result_img = cv2.drawMatches(
                    template_img, kp1, target_img, kp2,
                    good_points, None, **draw_params
                )
                
                # 添加检测结果文本
                if red_detected:
                    cv2.putText(result_img, "color:red", (400, 120),
                               cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
                
                if blue_detected:
                    cv2.putText(result_img, "color:blue", (400, 120),
                               cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
                
                # 添加角度和误差信息
                cv2.putText(result_img, f"angle:{int(theta)}", (210, 70),
                           cv2.FONT_HERSHEY_PLAIN, 3, (128, 0, 128), 3)
                cv2.putText(result_img, f"error:{error:.2f}mm", (500, 70),
                           cv2.FONT_HERSHEY_PLAIN, 3, (128, 0, 128), 3)
                
                # 绘制检测到的圆形
                if center is not None:
                    color = (0, 0, 255) if red_detected else (255, 0, 0) if blue_detected else (0, 255, 0)
                    cv2.circle(target_img, center, radius, color, 3)
                    cv2.putText(target_img, "circle", (200, 30),
                               cv2.FONT_HERSHEY_PLAIN, 3, color, 3)
                
                return result_img, True
        
        return None, False
