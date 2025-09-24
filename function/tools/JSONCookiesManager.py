import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from urllib.parse import quote, unquote


class MultiUserCookieManager:
    """多人 Cookies 管理器，支持多种格式的导入导出和快速查询"""

    def __init__(self, file_path: str = "cookies.json"):
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
                self.data = json.load(f)
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
            "netscape_format": ""
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

        # 更新其他格式
        self._update_cookie_string(user_key)
        self._update_netscape_format(user_key)

        # 更新索引
        self._update_cookie_indexes(user_key)

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
        self._update_netscape_format(user_key)
        self._update_cookie_indexes(user_key)

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
        self._update_cookie_string(user_key)
        self._update_cookie_indexes(user_key)

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

    def export_user_cookies(self, user_identifier: str, format_type: str = "json") -> Optional[Union[Dict, str]]:
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
        else:
            return None


# 使用示例
if __name__ == "__main__":
    # 创建管理器实例
    manager = MultiUserCookieManager("./TestOutput/JSONCookiesManager/cookies.json")

    # 添加用户
    user_key = manager.add_user("143474500", "example_user", "bilibili")

    # 导入 JSON 格式的 cookies
    json_cookies = [
        {
            "domain": ".bilibili.com",
            "expirationDate": 1780906990,
            "hostOnly": False,
            "httpOnly": False,
            "name": "_uuid",
            "path": "/",
            "sameSite": "unspecified",
            "secure": False,
            "session": False,
            "storeId": "0",
            "value": "DC6101E21-B1E9-8934-97CE-5AB10D3110C51890364infoc",
            "id": 1
        }
        # 更多 cookies...
    ]
    manager.import_cookies_json(user_key, json_cookies)

    # 导入字符串格式的 cookies
    cookie_string = r"buvid3=24B878AA-65D8-B50F-115F-93620321758D34011infoc; b_nut=1756097834; _uuid=63397FF4-FC4C-8C5E-9D47-17799AB2610D529737infoc; buvid_fp=0909838887fa47f5d59a246818cf1969; enable_web_push=DISABLE; buvid4=6214F410-3FE8-53F4-D104-4838A446323434991-025082512-c55Uq60Y364aMkJdw+nh+WWaSElXXo+lKz1+lLtT33nfw+HhY7joPxfdJLNTR4mu; theme-tip-show=SHOWED; theme-avatar-tip-show=SHOWED; LIVE_BUVID=AUTO7917560980008599; theme-switch-show=SHOWED; DedeUserID=3546974607379019; DedeUserID__ckMd5=220bc66fcc74f43e; home_feed_column=4; browser_resolution=1059-1629; SESSDATA=85b3171d%2C1774179577%2C6cab5%2A91CjBSVIR17iygOYBCeeja3TZnjvDOadTlt0hGLBKOsrR4SzOrIWsyUpN9WBEq4XjCepMSVkZSSi01Rmx6RjhNaXNDS2Znd0s3TUdjR2Z5MWN3NGQ0WHFTaG5abXVoOEY0WVNnckRDa1RMU2E1bUg3YmZzd2Q0a2tUekJfNXVWMl9RZmZ3cGRqcV93IIEC; bili_jct=3ec9b89f79456a4c50ed068bf22f3eac; b_lsid=33D57815_199768D9C1D; bsource=search_bing; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTg4ODk4NTAsImlhdCI6MTc1ODYzMDU5MCwicGx0IjotMX0.FSW68IsOnr5suB8iRNRQ0zbQCPNZi21Z-JL8LUVJtaI; bili_ticket_expires=1758889790; CURRENT_QUALITY=0; rpdid=0zbfAKYWU2|v4zZtxHq|4fY|3w1V12aH; CURRENT_FNVAL=2000; sid=8l716553; PVID=3"
    manager.import_cookie_string(user_key, cookie_string)

    # 查找特定 cookie 的值
    sessdata = manager.get_cookie_value("143474500", "SESSDATA")
    print(f"SESSDATA: {sessdata}")

    # 通过 cookie 查找用户
    users_with_sessdata = manager.find_users_by_cookie("SESSDATA")
    print(f"Users with SESSDATA: {users_with_sessdata}")

    # 导出特定格式的 cookies
    netscape_cookies = manager.export_user_cookies("143474500", "netscape")
    print("Netscape format:")
    print(netscape_cookies)

    # 导出特定格式的 cookies
    netscape_cookies = manager.export_user_cookies("143474500", "string")
    print("string format:")
    print(netscape_cookies)

    # 保存到文件
    manager.save()