"""
智能装配平台安装配置文件
"""

from setuptools import setup, find_packages
import os

# 读取README文件
def read_readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()

# 读取requirements文件
def read_requirements():
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        return [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]

setup(
    name="serial-vision-ui",
    version="1.0.0",
    author="Group7",
    author_email="",
    description="智能装配平台 - 基于PyQt5和OpenCV的全自动装配设备上位机控制系统",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/User-o2/SerialVisionUI",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Manufacturing",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: System :: Hardware :: Hardware Drivers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-qt>=4.0.0",
            "black>=21.0.0",
            "flake8>=3.9.0",
            "mypy>=0.900",
        ],
    },
    entry_points={
        "console_scripts": [
            "serial-vision-ui=serial_vision_ui.main_application:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["assets/*", "assets/**/*", "config.ini"],
    },
    zip_safe=False,
    keywords="automation, vision, serial-communication, manufacturing, PyQt5, OpenCV",
)
