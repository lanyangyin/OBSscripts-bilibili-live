"""
快速检查 Python 路径的脚本
将这段代码保存为 path_check.py 并运行
"""
import site
import sys
import os


def quick_path_check():
    """快速路径检查"""

    print("🔍 Python 路径快速检查")
    print("=" * 50)

    # 基本信息
    print(f"Python 版本: {sys.version.split()[0]}")
    print(f"执行文件: {sys.executable}")
    print(f"工作目录: {os.getcwd()}")
    print()

    # 关键路径
    key_paths = [
        ("当前目录", ""),
        ("用户包目录", site.getusersitepackages() if 'site' in globals() else "N/A"),
        ("标准库",
         [p for p in sys.path if 'lib/python' in p][0] if any('lib/python' in p for p in sys.path) else "未找到")
    ]

    print("关键路径:")
    for name, path in key_paths:
        exists = "✓" if path and os.path.exists(path) else "✗"
        print(f"  {exists} {name}: {path}")

    print(f"\n💡 建议:")
    print(f"1. 将 .py 文件放在: {os.getcwd()}")
    print(f"2. 或在当前目录创建 'lib/' 文件夹存放模块")
    print(f"3. 使用: import sys; sys.path.append('/your/module/path') 添加自定义路径")


if __name__ == "__main__":
    quick_path_check()