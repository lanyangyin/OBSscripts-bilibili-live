"""文件夹权限检查器"""
import os
import stat
from typing import Dict, Any, Union


class FolderPermissionChecker:
    """
    文件夹权限检查器

    提供多种方法检查文件夹的读写权限，包括实际文件操作验证。
    """

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def check_permissions(self, folder_path: str) -> Dict[str, Any]:
        """
        全面检查文件夹权限

        Args:
            folder_path: 文件夹路径

        Returns:
            详细的权限检查结果
        """
        folder_path = os.path.abspath(folder_path)

        if self.verbose:
            print(f"检查文件夹权限: {folder_path}")

        result = {
            'folder_path': folder_path,
            'exists': os.path.exists(folder_path),
            'is_directory': False,
            'permissions': {}
        }

        if not result['exists']:
            result['error'] = "文件夹不存在"
            return result

        if not os.path.isdir(folder_path):
            result['error'] = "路径不是文件夹"
            return result

        result['is_directory'] = True

        # 1. 使用 os.access 检查
        result['permissions']['os_access'] = self._check_os_access(folder_path)

        # 2. 使用实际文件操作检查
        result['permissions']['file_operations'] = self._check_file_operations(folder_path)

        # 3. 使用 stat 检查权限位
        result['permissions']['stat_bits'] = self._check_stat_permissions(folder_path)

        # 4. 综合评估
        result['summary'] = self._summarize_permissions(result['permissions'])

        return result

    def _check_os_access(self, folder_path: str) -> Dict[str, bool]:
        """使用 os.access 检查权限"""
        return {
            'readable': os.access(folder_path, os.R_OK),
            'writable': os.access(folder_path, os.W_OK),
            'executable': os.access(folder_path, os.X_OK)
        }

    def _check_file_operations(self, folder_path: str) -> Dict[str, Any]:
        """通过实际文件操作检查权限"""
        result: dict[str, Union[bool, str, int, Dict[str, str]]] = {
            'readable': False,
            'writable': False,
            'errors': {}
        }

        # 测试读取权限
        try:
            files = os.listdir(folder_path)
            result['readable'] = True
            result['file_count'] = len(files)  # 顺便获取文件数量
        except PermissionError as e:
            result['errors']['read'] = str(e)
        except Exception as e:
            result['errors']['read'] = f"读取错误: {str(e)}"

        # 测试写入权限
        test_filename = f".perm_test_{os.getpid()}_{os.urandom(4).hex()}.tmp"
        test_filepath = os.path.join(folder_path, test_filename)

        try:
            # 测试创建文件
            with open(test_filepath, 'w') as f:
                f.write("permission_test")
            result['writable'] = True

            # 测试读取刚创建的文件
            with open(test_filepath, 'r') as f:
                content = f.read()
                result['write_read_consistent'] = (content == "permission_test")

            # 测试删除文件
            os.remove(test_filepath)
            result['deletable'] = True

        except PermissionError as e:
            result['errors']['write'] = str(e)
            # 如果文件创建成功但无法删除，尝试清理
            if os.path.exists(test_filepath):
                try:
                    os.remove(test_filepath)
                except:
                    pass
        except Exception as e:
            result['errors']['write'] = f"写入错误: {str(e)}"
            # 清理临时文件
            if os.path.exists(test_filepath):
                try:
                    os.remove(test_filepath)
                except:
                    pass

        return result

    def _check_stat_permissions(self, folder_path: str) -> Dict[str, Any]:
        """使用 stat 检查权限位"""
        try:
            st = os.stat(folder_path)
            mode = st.st_mode

            # 解析权限位
            permissions = {
                'owner_read': bool(mode & stat.S_IRUSR),
                'owner_write': bool(mode & stat.S_IWUSR),
                'owner_execute': bool(mode & stat.S_IXUSR),
                'group_read': bool(mode & stat.S_IRGRP),
                'group_write': bool(mode & stat.S_IWGRP),
                'group_execute': bool(mode & stat.S_IXGRP),
                'others_read': bool(mode & stat.S_IROTH),
                'others_write': bool(mode & stat.S_IWOTH),
                'others_execute': bool(mode & stat.S_IXOTH),
                'mode_octal': oct(mode & 0o777)
            }

            # 计算当前用户是否有权限
            import getpass
            current_user = getpass.getuser()
            current_uid = os.getuid()

            # 简单判断：如果是文件所有者，检查所有者权限
            if st.st_uid == current_uid:
                permissions['effective_read'] = permissions['owner_read']
                permissions['effective_write'] = permissions['owner_write']
            else:
                # 简化处理：实际应该检查用户组等，这里简单使用 others 权限
                permissions['effective_read'] = permissions['others_read']
                permissions['effective_write'] = permissions['others_write']

            return permissions

        except Exception as e:
            return {'error': f"无法获取权限信息: {str(e)}"}

    def _summarize_permissions(self, permissions: Dict[str, Any]) -> Dict[str, bool]:
        """综合评估权限"""
        file_ops = permissions.get('file_operations', {})
        stat_bits = permissions.get('stat_bits', {})

        # 优先使用文件操作验证的结果
        readable = file_ops.get('readable', False)
        writable = file_ops.get('writable', False)

        # 如果文件操作检查失败，回退到其他方法
        if not readable:
            readable = permissions.get('os_access', {}).get('readable', False)

        if not writable:
            writable = permissions.get('os_access', {}).get('writable', False)

        return {
            'readable': readable,
            'writable': writable,
            'fully_accessible': readable and writable
        }

    def check_multiple_folders(self, folder_paths: list) -> Dict[str, Dict[str, Any]]:
        """
        批量检查多个文件夹权限

        Args:
            folder_paths: 文件夹路径列表

        Returns:
            每个文件夹的权限检查结果
        """
        results = {}
        for path in folder_paths:
            results[path] = self.check_permissions(path)

        return results

    def format_report(self, result: Dict[str, Any]) -> str:
        """格式化权限检查报告"""
        if not result['exists']:
            return f"❌ 文件夹不存在: {result['folder_path']}"

        if not result['is_directory']:
            return f"❌ 不是文件夹: {result['folder_path']}"

        summary = result.get('summary', {})
        readable = summary.get('readable', False)
        writable = summary.get('writable', False)

        report = []
        report.append(f"📁 文件夹: {result['folder_path']}")
        report.append(f"  读取权限: {'✅ 有' if readable else '❌ 无'}")
        report.append(f"  写入权限: {'✅ 有' if writable else '❌ 无'}")

        # 添加详细权限信息
        file_ops = result['permissions'].get('file_operations', {})
        if file_ops.get('errors'):
            for op, error in file_ops['errors'].items():
                report.append(f"  {op}错误: {error}")

        return "\n".join(report)


# 使用示例
if __name__ == "__main__":
    checker = FolderPermissionChecker(verbose=True)

    # 测试一些常见路径
    test_paths = [
        os.getcwd(),  # 当前目录
        "/tmp",  # 临时目录 (Linux/Mac)
        "C:\\Windows\\Temp" if os.name == 'nt' else "/var/tmp",  # Windows 临时目录
        "C:\\Users\\18898\\Documents\\Github\ArknightsGameData\\zh_CN\\gamedata",
        "/root",  # 通常需要权限的目录
        "/nonexistent/path"  # 不存在的路径
    ]

    print("文件夹权限检查报告")
    print("=" * 50)

    for path in test_paths:
        result = checker.check_permissions(path)
        print(checker.format_report(result))
        print("-" * 30)