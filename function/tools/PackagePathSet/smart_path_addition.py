"""添加模块目录"""
import os
import sys
from pathlib import Path

# 单行获取当前文件目录并添加到路径
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
print(Path(__file__).parent)
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

# 现在可以导入当前目录下的模块
# import my_module  # 假设 my_module.py 在当前目录