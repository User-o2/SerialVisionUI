"""
资源管理工具类
用于处理资源文件路径和加载
"""

import os
import sys
from typing import Union


def get_resource_path(relative_path: str) -> str:
    """
    获取资源文件的绝对路径
    
    Args:
        relative_path: 相对路径
        
    Returns:
        资源文件的绝对路径
    """
    if hasattr(sys, '_MEIPASS'):
        # 打包后，资源文件存储在临时目录
        return os.path.join(sys._MEIPASS, relative_path)
    else:
        # 未打包时，资源文件存储在当前工作目录
        return os.path.join(os.path.abspath("."), relative_path)


def get_asset_path(asset_type: str, filename: str) -> str:
    """
    获取指定类型资源文件的路径
    
    Args:
        asset_type: 资源类型 ('images', 'icons', 'ui', 'libs')
        filename: 文件名
        
    Returns:
        资源文件的绝对路径
    """
    return get_resource_path(f"assets/{asset_type}/{filename}")
