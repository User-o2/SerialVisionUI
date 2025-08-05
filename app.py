#!/usr/bin/env python3
"""
智能装配平台主程序入口
"""

import sys
import os
from PyQt5 import QtWidgets, QtCore, QtGui
from qt_material import apply_stylesheet

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.serial_vision_ui.main_application import SerialVisionUI


def setup_application_style(app: QtWidgets.QApplication) -> None:
    """设置应用程序样式"""
    # 应用暗色主题
    apply_stylesheet(app, theme='dark_amber.xml')
    
    # 自定义进度条样式
    progress_bar_style = """
    QProgressBar {
        border: 1px solid grey;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
    }
    QProgressBar::chunk {
        background-color: #4CAF50;
        width: 10px;
        margin: 0.5px;
        border-radius: 3px;
    }
    """
    
    return progress_bar_style


def main():
    """主函数"""
    # 创建应用程序实例
    app = QtWidgets.QApplication(sys.argv)
    
    # 设置应用程序属性
    app.setApplicationName("智能装配平台")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Group7")
    
    # 创建主窗口
    main_window = SerialVisionUI()
    
    # 应用样式
    progress_style = setup_application_style(app)
    main_window.progress_bar.setStyleSheet(progress_style)
    
    # 设置窗口图标（如果存在）
    try:
        app_icon = QtGui.QIcon('assets/icons/blue_circle.ico')
        app.setWindowIcon(app_icon)
        main_window.setWindowIcon(app_icon)
    except:
        pass  # 如果图标文件不存在，忽略错误
    
    # 显示窗口
    main_window.show()
    
    # 运行应用程序
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
