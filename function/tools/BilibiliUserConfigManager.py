import pathlib
import json
from typing import Dict, Optional, List, Union
from collections import OrderedDict


class BilibiliUserConfigManager:
    """
    B站用户配置管理器，负责用户登录信息的增删改查操作。

    配置文件采用JSON格式，结构示例：
    {
        "default_user": "12345",
        "users": {
            "12345": {
                "DedeUserID": "12345",
                "DedeUserID__ckMd5": "xxxxxxxx",
                "SESSDATA": "xxxxxxxx",
                "bili_jct": "xxxxxxxx",
                "buvid3": "xxxxxxxx",
                "b_nut": "xxxxxxxx",
                "last_updated": "2023-01-01T00:00:00"
            },
            "67890": {
                "DedeUserID": "67890",
                ...
            }
        }
    }

    特性：
    - 支持多用户管理
    - 自动维护默认用户设置
    - 验证必要字段完整性
    - 提供用户列表和详细信息获取
    - 支持配置文件的自动创建和修复
    """

    def __init__(self, config_path: pathlib.Path):
        """
        初始化配置文件管理器

        Args:
            config_path: 配置文件路径对象

        Raises:
            IOError: 文件读写失败时抛出
            json.JSONDecodeError: 配置文件内容格式错误时抛出
        """
        self.config_path = config_path
        self._ensure_config_file()

    def _ensure_config_file(self):
        """确保配置文件存在且结构有效"""
        if not self.config_path.exists():
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            self._write_config({
                "default_user": None,
                "users": {}
            })

        config = self._read_config()
        # 修复旧格式配置文件
        if "users" not in config:
            # 迁移旧格式数据
            users = {}
            for key, value in config.items():
                if key != "DefaultUser" and isinstance(value, dict):
                    users[key] = value

            default_user = config.get("DefaultUser")
            self._write_config({
                "default_user": default_user,
                "users": users
            })

    def _read_config(self) -> Dict:
        """读取配置文件内容"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise RuntimeError(f"配置文件损坏或格式错误: {str(e)}") from e

    def _write_config(self, config: Dict):
        """写入配置文件"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
        except IOError as e:
            raise RuntimeError(f"配置文件写入失败: {str(e)}") from e

    def add_user(self, cookies: Dict[str, str]) -> str:
        """
        添加新用户配置

        Args:
            cookies: 包含完整cookie信息的字典，必须包含以下字段：
                     DedeUserID, DedeUserID__ckMd5, SESSDATA,
                     bili_jct, buvid3, b_nut

        Returns:
            添加的用户ID

        Raises:
            ValueError: 缺少必要字段时抛出
        """
        required_keys = {
            "DedeUserID", "DedeUserID__ckMd5", "SESSDATA",
            "bili_jct", "buvid3", "b_nut"
        }
        if not required_keys.issubset(cookies.keys()):
            missing = required_keys - cookies.keys()
            raise ValueError(f"缺少必要字段: {', '.join(missing)}")

        uid = str(cookies["DedeUserID"])
        config = self._read_config()

        if uid in config["users"]:
            # 用户已存在，执行更新操作
            self.update_user(cookies, set_as_default=False)
            return uid

        # 添加时间戳
        from datetime import datetime
        cookies["last_updated"] = datetime.now().isoformat()

        config["users"][uid] = cookies
        self._write_config(config)
        return uid

    def delete_user(self, user_id: Union[int, str]) -> bool:
        """
        删除用户配置

        Args:
            user_id: 要删除的用户ID

        Returns:
            True表示删除成功，False表示用户不存在

        Raises:
            ValueError: 尝试删除默认用户时抛出
        """
        config = self._read_config()
        user_id_str = str(user_id)

        if user_id_str not in config["users"]:
            return False

        # 处理默认用户
        if config["default_user"] == user_id_str:
            raise ValueError("不能删除默认用户，请先更改默认用户设置")

        del config["users"][user_id_str]
        self._write_config(config)
        return True

    def update_user(self, cookies: Dict[str, str], set_as_default: bool = False) -> str:
        """
        更新用户配置

        Args:
            cookies: 包含完整cookie信息的字典
            set_as_default: 是否设为默认用户

        Returns:
            更新的用户ID

        Raises:
            ValueError: 缺少必要字段或用户不存在时抛出
        """
        required_keys = {"DedeUserID", "SESSDATA", "bili_jct"}
        if not required_keys.issubset(cookies.keys()):
            missing = required_keys - cookies.keys()
            raise ValueError(f"缺少必要字段: {', '.join(missing)}")

        uid = str(cookies["DedeUserID"])
        config = self._read_config()

        if uid not in config["users"]:
            raise ValueError(f"用户 {uid} 不存在")

        # 更新用户数据并添加时间戳
        from datetime import datetime
        config["users"][uid].update(cookies)
        config["users"][uid]["last_updated"] = datetime.now().isoformat()

        # 设置默认用户
        if set_as_default:
            config["default_user"] = uid

        self._write_config(config)
        return uid

    def set_default_user(self, user_id: Union[int, str]) -> bool:
        """
        设置默认用户

        Args:
            user_id: 要设置为默认用户的用户ID

        Returns:
            True表示设置成功，False表示用户不存在
        """
        config = self._read_config()
        user_id_str = str(user_id)

        if user_id_str not in config["users"]:
            return False

        config["default_user"] = user_id_str
        self._write_config(config)
        return True

    def clear_default_user(self) -> None:
        """
        清空默认用户设置
        """
        config = self._read_config()
        config["default_user"] = None
        self._write_config(config)

    def get_user_cookies(self, user_id: Optional[Union[int, str]] = None) -> Optional[Dict]:
        """
        获取指定用户的cookie信息

        Args:
            user_id: 用户ID，None表示获取默认用户

        Returns:
            用户cookie字典，未找到返回None
        """
        config = self._read_config()

        # 如果user_id是None表示获取默认用户
        if user_id is None:
            user_id = config.get("default_user")

        # 如果user_id是None或不在用户列表中，返回None
        if user_id is None or str(user_id) not in config["users"]:
            return None

        return config["users"][str(user_id)].copy()

    def get_all_users(self) -> List[Dict]:
        """
        获取所有用户信息列表

        Returns:
            用户信息列表，每个元素包含用户ID和是否是默认用户的信息
        """
        config = self._read_config()
        default_user = config.get("default_user")

        users = []
        for uid, user_data in config["users"].items():
            users.append({
                "user_id": uid,
                "is_default": uid == default_user,
                "last_updated": user_data.get("last_updated")
            })

        return users

    def user_exists(self, user_id: Union[int, str]) -> bool:
        """
        检查用户是否存在

        Args:
            user_id: 要检查的用户ID

        Returns:
            True表示用户存在，False表示不存在
        """
        config = self._read_config()
        return str(user_id) in config["users"]

    def get_default_user_id(self) -> Optional[str]:
        """
        获取默认用户ID

        Returns:
            默认用户ID，如果没有设置默认用户则返回None
        """
        config = self._read_config()
        return config.get("default_user")