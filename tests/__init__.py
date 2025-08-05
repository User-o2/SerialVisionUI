"""
测试模块初始化文件
"""

import sys
import os

# 确保src目录在Python路径中
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
src_dir = os.path.join(parent_dir, 'src')

if src_dir not in sys.path:
    sys.path.insert(0, src_dir)
