"""
日志重定向类
用于将标准输出重定向到UI组件
"""

from PyQt5 import QtWidgets
from PyQt5.QtGui import QTextCursor


class OutputRedirector:
    """将标准输出重定向到QPlainTextEdit组件的类"""
    
    def __init__(self, text_widget):
        """
        初始化输出重定向器
        
        Args:
            text_widget: QPlainTextEdit组件实例
        """
        self.text_widget = text_widget

    def write(self, text: str) -> None:
        """
        写入文本到组件
        
        Args:
            text: 要写入的文本
        """
        self.text_widget.moveCursor(QTextCursor.End)  # 移动光标到末尾
        self.text_widget.insertPlainText(text)  # 显示文本
        self.text_widget.moveCursor(QTextCursor.End)  # 再次移动光标到末尾
        self.text_widget.ensureCursorVisible()  # 设置光标可见，自动滚动
        QtWidgets.QApplication.processEvents()  # 保持快速响应

    def flush(self) -> None:
        """刷新输出缓冲区（此处无需任何操作）"""
        pass
