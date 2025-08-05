"""
SerialVisionUI - 智能装配平台

一个基于PyQt5和OpenCV的全自动装配设备上位机控制系统。
集成了机器视觉、串口通信和实时监控功能。
"""

__version__ = "1.0.0"
__author__ = "Group7"
__description__ = "智能装配平台上位机控制系统"

from .main_application import SerialVisionUI

__all__ = ["SerialVisionUI"]
