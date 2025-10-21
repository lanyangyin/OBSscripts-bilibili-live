import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from urllib.parse import quote, unquote


class MultiUserCookieManager:
    """多人 Cookies 管理器，支持多种格式的导入导出和快速查询"""

    def __init__(self, file_path: str = ""):
        self.file_path = file_path
        self.data = {
            "version": "1.0",
            "metadata": {
                "created_at": datetime.utcnow().isoformat() + "Z",
                "updated_at": datetime.utcnow().isoformat() + "Z",
                "description": "Multi-user cookies storage"
            },
            "users": {},
            "indexes": {
                "by_user_id": {},
                "by_username": {},
                "by_cookie_name": {}
            }
        }
        self.load()

    def load(self) -> bool:
        """从文件加载 cookies 数据"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)
                # 确保向后兼容，如果旧数据没有simplified_json字段，则添加
                for user_key, user_data in loaded_data.get("users", {}).items():
                    if "simplified_json" not in user_data:
                        user_data["simplified_json"] = {}
                self.data.update(loaded_data)
            return True
        except (FileNotFoundError, json.JSONDecodeError):
            # 文件不存在或格式错误，使用默认数据
            return False

    def save(self) -> bool:
        """保存 cookies 数据到文件"""
        try:
            self.data["metadata"]["updated_at"] = datetime.utcnow().isoformat() + "Z"
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存文件失败: {e}")
            return False

    def add_user(self, user_id: str, username: str = None, platform: str = None) -> str:
        """添加新用户"""
        user_key = f"user_{user_id}"
        if user_key in self.data["users"]:
            return user_key

        self.data["users"][user_key] = {
            "user_id": user_id,
            "username": username or "",
            "platform": platform or "",
            "cookies": [],
            "cookie_string": "",
            "netscape_format": "",
            "simplified_json": {}  # 新增简化JSON字段
        }

        # 更新索引
        self.data["indexes"]["by_user_id"][user_id] = user_key
        if username:
            self.data["indexes"]["by_username"][username] = user_key

        return user_key

    def import_cookies_json(self, user_key: str, cookies: List[Dict]) -> bool:
        """导入 JSON 格式的 cookies"""
        if user_key not in self.data["users"]:
            return False

        self.data["users"][user_key]["cookies"] = cookies
        self._update_all_formats(user_key)
        return True

    def import_cookie_string(self, user_key: str, cookie_string: str) -> bool:
        """导入字符串格式的 cookies"""
        if user_key not in self.data["users"]:
            return False

        self.data["users"][user_key]["cookie_string"] = cookie_string

        # 解析为 JSON 格式
        cookies = []
        for part in cookie_string.split(';'):
            part = part.strip()
            if not part:
                continue

            if '=' in part:
                name, value = part.split('=', 1)
                cookies.append({
                    "name": name.strip(),
                    "value": value.strip(),
                    "domain": "",  # 需要额外信息
                    "path": "/",  # 默认值
                    "secure": False,
                    "httpOnly": False,
                    "session": True  # 默认会话cookie
                })

        self.data["users"][user_key]["cookies"] = cookies
        self._update_all_formats(user_key)
        return True

    def import_netscape_format(self, user_key: str, netscape_text: str) -> bool:
        """导入 Netscape 格式的 cookies"""
        if user_key not in self.data["users"]:
            return False

        self.data["users"][user_key]["netscape_format"] = netscape_text

        # 解析为 JSON 格式
        cookies = []
        for line in netscape_text.split('\n'):
            line = line.strip()
            if line.startswith('#') or not line:
                continue

            parts = line.split('\t')
            if len(parts) >= 7:
                cookies.append({
                    "domain": parts[0],
                    "flag": parts[1] == "TRUE",
                    "path": parts[2],
                    "secure": parts[3] == "TRUE",
                    "expiration": int(parts[4]) if parts[4] != "0" else None,
                    "name": parts[5],
                    "value": parts[6]
                })

        self.data["users"][user_key]["cookies"] = cookies
        self._update_all_formats(user_key)
        return True

    def import_simplified_json(self, user_key: str, simplified_cookies: Dict[str, Any]) -> bool:
        """导入简化的 JSON 格式 cookie 数据"""
        if user_key not in self.data["users"]:
            return False

        # 获取现有的完整 cookies
        existing_cookies = self.data["users"][user_key]["cookies"]

        # 更新或添加简化的 cookie 值
        for name, value in simplified_cookies.items():
            found = False
            for cookie in existing_cookies:
                if cookie.get("name") == name:
                    cookie["value"] = str(value)  # 确保值为字符串
                    found = True
                    break

            # 如果不存在，添加新的 cookie
            if not found:
                existing_cookies.append({
                    "name": name,
                    "value": str(value),
                    "domain": ".bilibili.com",
                    "path": "/",
                    "secure": False,
                    "httpOnly": False,
                    "session": True
                })

        # 更新所有格式和索引
        self._update_all_formats(user_key)
        return True

    def _update_cookie_string(self, user_key: str):
        """更新 cookie 字符串格式"""
        cookies = self.data["users"][user_key]["cookies"]
        cookie_parts = []

        for cookie in cookies:
            if "name" in cookie and "value" in cookie:
                cookie_parts.append(f"{cookie['name']}={cookie['value']}")

        self.data["users"][user_key]["cookie_string"] = "; ".join(cookie_parts)

    def _update_netscape_format(self, user_key: str):
        """更新 Netscape 格式"""
        cookies = self.data["users"][user_key]["cookies"]
        lines = ["# Netscape HTTP Cookie File", "# http://curl.haxx.se/rfc/cookie_spec.html"]

        for cookie in cookies:
            domain = cookie.get("domain", "")
            flag = "TRUE" if cookie.get("hostOnly", False) else "FALSE"
            path = cookie.get("path", "/")
            secure = "TRUE" if cookie.get("secure", False) else "FALSE"
            expiration = str(cookie.get("expirationDate", 0))
            name = cookie.get("name", "")
            value = cookie.get("value", "")

            lines.append(f"{domain}\t{flag}\t{path}\t{secure}\t{expiration}\t{name}\t{value}")

        self.data["users"][user_key]["netscape_format"] = "\n".join(lines)

    def _update_simplified_json(self, user_key: str, keys: List[str] = None):
        """更新简化 JSON 格式"""
        cookies = self.data["users"][user_key]["cookies"]

        # 默认导出的关键 cookie 键
        default_keys = ["DedeUserID", "DedeUserID__ckMd5", "SESSDATA", "bili_jct", "b_nut", "buvid3"]
        target_keys = keys or default_keys

        result = {}
        for cookie in cookies:
            cookie_name = cookie.get("name")
            if cookie_name in target_keys:
                # 尝试将数字字符串转换为整数
                value = cookie.get("value", "")
                if cookie_name == "DedeUserID" and value.isdigit():
                    result[cookie_name] = int(value)
                else:
                    result[cookie_name] = value

        self.data["users"][user_key]["simplified_json"] = result

    def _update_cookie_indexes(self, user_key: str):
        """更新 cookie 索引"""
        user_data = self.data["users"][user_key]

        # 清除旧索引
        for cookie_name in list(self.data["indexes"]["by_cookie_name"].keys()):
            if user_key in self.data["indexes"]["by_cookie_name"][cookie_name]:
                self.data["indexes"]["by_cookie_name"][cookie_name].remove(user_key)
                if not self.data["indexes"]["by_cookie_name"][cookie_name]:
                    del self.data["indexes"]["by_cookie_name"][cookie_name]

        # 添加新索引
        for cookie in user_data["cookies"]:
            cookie_name = cookie.get("name")
            if cookie_name:
                if cookie_name not in self.data["indexes"]["by_cookie_name"]:
                    self.data["indexes"]["by_cookie_name"][cookie_name] = []
                if user_key not in self.data["indexes"]["by_cookie_name"][cookie_name]:
                    self.data["indexes"]["by_cookie_name"][cookie_name].append(user_key)

    def _update_all_formats(self, user_key: str):
        """更新所有需要预计算的 cookie 格式"""
        self._update_cookie_string(user_key)
        self._update_netscape_format(user_key)
        self._update_simplified_json(user_key)  # 新增：更新简化JSON格式
        self._update_cookie_indexes(user_key)

    def get_cookie_value(self, user_identifier: str, cookie_name: str) -> Optional[str]:
        """获取指定用户的特定 cookie 值"""
        user_key = None

        # 根据标识符类型确定用户键
        if user_identifier in self.data["indexes"]["by_user_id"]:
            user_key = self.data["indexes"]["by_user_id"][user_identifier]
        elif user_identifier in self.data["indexes"]["by_username"]:
            user_key = self.data["indexes"]["by_username"][user_identifier]
        elif user_identifier in self.data["users"]:
            user_key = user_identifier

        if not user_key or user_key not in self.data["users"]:
            return None

        # 查找 cookie 值
        for cookie in self.data["users"][user_key]["cookies"]:
            if cookie.get("name") == cookie_name:
                return cookie.get("value")

        return None

    def find_users_by_cookie(self, cookie_name: str, cookie_value: str = None) -> List[str]:
        """通过 cookie 查找用户"""
        if cookie_name not in self.data["indexes"]["by_cookie_name"]:
            return []

        user_keys = self.data["indexes"]["by_cookie_name"][cookie_name]

        if cookie_value is None:
            return [self.data["users"][key]["user_id"] for key in user_keys]

        # 如果需要匹配值，进一步筛选
        result = []
        for user_key in user_keys:
            for cookie in self.data["users"][user_key]["cookies"]:
                if cookie.get("name") == cookie_name and cookie.get("value") == cookie_value:
                    result.append(self.data["users"][user_key]["user_id"])
                    break

        return result

    def export_simplified_json(self, user_identifier: str, keys: List[str] = None) -> Optional[Dict[str, Any]]:
        """导出简化的 JSON 格式，包含指定的 cookie 键值对"""
        user_key = None

        if user_identifier in self.data["indexes"]["by_user_id"]:
            user_key = self.data["indexes"]["by_user_id"][user_identifier]
        elif user_identifier in self.data["indexes"]["by_username"]:
            user_key = self.data["indexes"]["by_username"][user_identifier]
        elif user_identifier in self.data["users"]:
            user_key = user_identifier

        if not user_key or user_key not in self.data["users"]:
            return None

        # 如果指定了键，则实时生成
        if keys:
            # 默认导出的关键 cookie 键
            target_keys = keys

            result = {}
            for cookie in self.data["users"][user_key]["cookies"]:
                cookie_name = cookie.get("name")
                if cookie_name in target_keys:
                    # 尝试将数字字符串转换为整数
                    value = cookie.get("value", "")
                    if cookie_name == "DedeUserID" and value.isdigit():
                        result[cookie_name] = int(value)
                    else:
                        result[cookie_name] = value

            return result if result else None
        else:
            # 返回存储的简化JSON
            return self.data["users"][user_key]["simplified_json"]

    def export_user_cookies(self, user_identifier: str, format_type: str = "json", **kwargs) -> Optional[
        Union[Dict, str]]:
        """导出指定用户的 cookies，支持多种格式"""
        user_key = None

        if user_identifier in self.data["indexes"]["by_user_id"]:
            user_key = self.data["indexes"]["by_user_id"][user_identifier]
        elif user_identifier in self.data["indexes"]["by_username"]:
            user_key = self.data["indexes"]["by_username"][user_identifier]
        elif user_identifier in self.data["users"]:
            user_key = user_identifier

        if not user_key or user_key not in self.data["users"]:
            return None

        if format_type == "json":
            return self.data["users"][user_key]["cookies"]
        elif format_type == "string":
            return self.data["users"][user_key]["cookie_string"]
        elif format_type == "netscape":
            return self.data["users"][user_key]["netscape_format"]
        elif format_type == "simplified_json":
            keys = kwargs.get('keys', None)
            return self.export_simplified_json(user_identifier, keys)
        else:
            return None


# 使用示例
if __name__ == "__main__":
    from _Input.function.tools.ConfigControl import JSONCookiesManager
    # 创建管理器实例
    manager = MultiUserCookieManager(JSONCookiesManager.path)

    # 添加用户1
    user_key = manager.add_user(JSONCookiesManager.user1.id, JSONCookiesManager.user1.name, JSONCookiesManager.user1.platform)

    # # 导入 JSON 格式的 cookies
    # manager.import_cookies_json(user_key, JSONCookiesManager.json_cookies)
    #
    # # 导入字符串格式的 cookies
    # manager.import_cookie_string(user_key, JSONCookiesManager.cookie_string)

    # 导入 简化JSON 格式的 cookies
    manager.import_simplified_json(user_key, JSONCookiesManager.simplified_cookies)

    # 查找特定 cookie 的值
    sessdata = manager.get_cookie_value(JSONCookiesManager.user1.id, "SESSDATA")
    print(f"SESSDATA: {sessdata}")

    # 通过 cookie 查找用户
    users_with_sessdata = manager.find_users_by_cookie("SESSDATA")
    print(f"Users with SESSDATA: {users_with_sessdata}")

    # 导出特定格式的 cookies
    netscape_cookies = manager.export_user_cookies(JSONCookiesManager.user1.id, "netscape")
    print("Netscape format:")
    print(netscape_cookies)

    # 导出特定格式的 cookies
    json_cookies = manager.export_user_cookies(JSONCookiesManager.user1.id, "json")
    print("json format:")
    print(json_cookies)

    # 导出特定格式的 cookies
    string_cookies = manager.export_user_cookies(JSONCookiesManager.user1.id, "string")
    print("string format:")
    print(string_cookies)

    # 导出特定格式的 cookies
    simplified_json_cookies = manager.export_user_cookies(JSONCookiesManager.user1.id, "simplified_json")
    print("simplified_json format:")
    print(simplified_json_cookies)

    # 保存到文件
    manager.save()