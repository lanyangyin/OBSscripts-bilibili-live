"""管理员权限检测"""
import os
import platform
import ctypes
import subprocess
from typing import Dict, Any


class AdminDetector:
    """管理员权限检测器（仅检测，不要求提升权限）"""

    @staticmethod
    def is_admin() -> bool:
        """
        检测当前是否具有管理员权限

        Returns:
            bool: 如果有管理员权限返回 True，否则返回 False
        """
        system = platform.system().lower()

        if system == 'windows':
            return AdminDetector._is_admin_windows()
        elif system in ['linux', 'darwin']:  # darwin 是 macOS
            return AdminDetector._is_admin_unix()
        else:
            # 其他系统，尝试使用 Unix 方法
            return AdminDetector._is_admin_unix()

    @staticmethod
    def _is_admin_windows() -> bool:
        """Windows 系统管理员权限检测"""
        try:
            # 方法1: 使用 ctypes 检查 Windows 管理员权限
            return ctypes.windll.shell32.IsUserAnAdmin()
        except Exception:
            # 方法2: 尝试访问需要管理员权限的目录
            try:
                # 尝试访问 Windows 系统目录
                test_path = os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'System32')
                temp_file = os.path.join(test_path, 'test_admin.tmp')
                with open(temp_file, 'w') as f:
                    f.write('test')
                os.remove(temp_file)
                return True
            except (IOError, OSError, PermissionError):
                return False

    @staticmethod
    def _is_admin_unix() -> bool:
        """Unix/Linux/macOS 系统管理员权限检测"""
        try:
            # 方法1: 检查当前用户 ID
            if os.geteuid() == 0:
                return True

            # 方法2: 检查 sudo 环境变量
            sudo_env_vars = ['SUDO_USER', 'SUDO_UID', 'SUDO_GID']
            if any(var in os.environ for var in sudo_env_vars):
                return True

            # 方法3: 尝试执行需要 root 权限的操作（不实际执行，只检查）
            test_cmd = ['id', '-u']
            result = subprocess.run(test_cmd, capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip() == '0':
                return True

            return False
        except Exception:
            return False

    @staticmethod
    def get_admin_info() -> Dict[str, Any]:
        """获取详细的权限信息（不要求提升权限）"""
        system = platform.system().lower()
        info = {
            'is_admin': AdminDetector.is_admin(),
            'system': system,
            'username': os.environ.get('USERNAME') or os.environ.get('USER', 'Unknown'),
        }

        if system == 'windows':
            info['admin_method'] = 'Windows UAC' if info['is_admin'] else '普通用户'
        else:
            info['euid'] = os.geteuid()
            info['sudo_user'] = os.environ.get('SUDO_USER')
            info['sudo_uid'] = os.environ.get('SUDO_UID')
            info['admin_method'] = 'root/sudo' if info['is_admin'] else '普通用户'

        return info

    @staticmethod
    def check_admin_with_reason() -> Dict[str, Any]:
        """
        检查管理员权限并返回详细原因

        Returns:
            Dict: 包含权限状态和详细原因的字典
        """
        system = platform.system().lower()
        result = {
            'has_admin': False,
            'reason': '',
            'details': {}
        }

        if system == 'windows':
            # Windows 检测
            try:
                if ctypes.windll.shell32.IsUserAnAdmin():
                    result['has_admin'] = True
                    result['reason'] = 'Windows UAC 管理员权限'
                else:
                    result['reason'] = 'Windows 普通用户权限'
            except Exception as e:
                result['reason'] = f'Windows 权限检测失败: {str(e)}'

        else:
            # Unix/Linux/macOS 检测
            result['details']['euid'] = os.geteuid()
            result['details']['sudo_user'] = os.environ.get('SUDO_USER')

            if os.geteuid() == 0:
                result['has_admin'] = True
                result['reason'] = 'root 用户权限'
            elif any(var in os.environ for var in ['SUDO_USER', 'SUDO_UID', 'SUDO_GID']):
                result['has_admin'] = True
                result['reason'] = 'sudo 权限'
            else:
                result['reason'] = '普通用户权限'

        return result


class UnixAdminDetector:
    """Unix/Linux 系统专用管理员权限检测"""

    @staticmethod
    def is_root() -> bool:
        """检查当前是否是 root 用户"""
        return os.geteuid() == 0

    @staticmethod
    def is_sudo() -> bool:
        """检查是否通过 sudo 运行"""
        return any(var in os.environ for var in ['SUDO_USER', 'SUDO_UID', 'SUDO_GID'])

    @staticmethod
    def get_privilege_info() -> Dict[str, Any]:
        """获取 Unix/Linux 系统权限信息"""
        return {
            'is_root': UnixAdminDetector.is_root(),
            'is_sudo': UnixAdminDetector.is_sudo(),
            'euid': os.geteuid(),
            'uid': os.getuid(),
            'gid': os.getgid(),
            'sudo_user': os.environ.get('SUDO_USER'),
            'sudo_uid': os.environ.get('SUDO_UID'),
            'sudo_gid': os.environ.get('SUDO_GID'),
            'has_admin': UnixAdminDetector.is_root() or UnixAdminDetector.is_sudo(),
        }


class WindowsAdminDetector:
    """Windows 系统专用管理员权限检测"""

    @staticmethod
    def is_user_admin() -> bool:
        """使用 Windows API 检测管理员权限"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except Exception:
            return False

    @staticmethod
    def get_privilege_info() -> Dict[str, Any]:
        """获取 Windows 系统权限信息"""
        return {
            'is_user_admin': WindowsAdminDetector.is_user_admin(),
            'username': os.environ.get('USERNAME', 'Unknown'),
            'has_admin': WindowsAdminDetector.is_user_admin(),
        }


# 使用示例和演示
if __name__ == "__main__":
    # 基本使用
    print("=== 管理员权限检测 ===")

    # 使用通用检测器
    if AdminDetector.is_admin():
        print("✓ 当前具有管理员权限")
    else:
        print("✗ 当前没有管理员权限")

    # 获取详细信息
    print("\n--- 详细信息 ---")
    info = AdminDetector.get_admin_info()
    for key, value in info.items():
        print(f"  {key}: {value}")

    # 获取带原因的检测结果
    print("\n--- 详细检测结果 ---")
    result = AdminDetector.check_admin_with_reason()
    for key, value in result.items():
        print(f"  {key}: {value}")

    # 系统特定检测
    system = platform.system().lower()
    print(f"\n--- {system} 系统特定信息 ---")

    if system == 'windows':
        win_info = WindowsAdminDetector.get_privilege_info()
        for key, value in win_info.items():
            print(f"  {key}: {value}")
    else:
        unix_info = UnixAdminDetector.get_privilege_info()
        for key, value in unix_info.items():
            print(f"  {key}: {value}")

    print("\n程序可以继续执行，无论是否具有管理员权限...")