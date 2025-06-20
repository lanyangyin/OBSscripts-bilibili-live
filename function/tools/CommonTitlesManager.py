import json
import os
from pathlib import Path
from typing import Dict, List, Union, Optional


class CommonTitlesManager:
    """
    管理用户常用标题的JSON文件

    功能:
    - 管理 {user_id: [title1, title2, ...]} 格式的JSON文件
    - 每个用户的标题列表最多包含5个元素
    - 支持增删改查操作
    - 自动创建不存在的目录和文件

    参数:
        directory: 文件存放目录
    """

    def __init__(self, directory: Union[str, Path]):
        """
        初始化CommonTitlesManager

        Args:
            directory: 文件存放目录
        """
        self.directory = Path(directory)
        self.filepath = self.directory / "commonTitles.json"
        self.data: Dict[str, List[str]] = {}

        # 确保目录存在
        self.directory.mkdir(parents=True, exist_ok=True)

        # 如果文件不存在则创建
        if not self.filepath.exists():
            self._save_data()
        else:
            self._load_data()

    def _load_data(self) -> None:
        """从文件加载数据"""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            # 文件为空或格式错误时创建新文件
            self.data = {}
            self._save_data()

    def _save_data(self) -> None:
        """保存数据到文件"""
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def get_titles(self, user_id: str) -> List[str]:
        """
        获取指定用户的常用标题列表

        Args:
            user_id: 用户ID

        Returns:
            该用户的常用标题列表（如果没有则为空列表）
        """
        return self.data.get(user_id, [])

    def add_title(self, user_id: str, title: str) -> None:
        """
        为用户添加新标题

        特点:
        - 如果标题已存在，则移动到列表最前面
        - 确保列表长度不超过5个
        - 如果用户不存在，则创建新条目

        Args:
            user_id: 用户ID
            title: 要添加的标题
        """
        titles = self.get_titles(user_id)

        # 移除重复项（如果存在）
        if title in titles:
            titles.remove(title)

        # 添加到列表开头
        titles.insert(0, title)

        # 确保不超过5个元素
        if len(titles) > 5:
            titles = titles[:5]

        # 更新数据并保存
        self.data[user_id] = titles
        self._save_data()

    def remove_title(self, user_id: str, title: str) -> bool:
        """
        移除用户的指定标题

        Args:
            user_id: 用户ID
            title: 要移除的标题

        Returns:
            True: 成功移除
            False: 标题不存在
        """
        if user_id not in self.data:
            return False

        titles = self.data[user_id]

        if title in titles:
            titles.remove(title)
            # 如果列表为空，则删除用户条目
            if not titles:
                del self.data[user_id]
            self._save_data()
            return True
        return False

    def update_title(self, user_id: str, old_title: str, new_title: str) -> bool:
        """
        更新用户的标题

        Args:
            user_id: 用户ID
            old_title: 要替换的旧标题
            new_title: 新标题

        Returns:
            True: 更新成功
            False: 旧标题不存在
        """
        if user_id not in self.data:
            return False

        titles = self.data[user_id]

        if old_title in titles:
            # 替换标题并移动到列表前面
            index = titles.index(old_title)
            titles.pop(index)
            titles.insert(0, new_title)
            self._save_data()
            return True
        return False

    def clear_user_titles(self, user_id: str) -> None:
        """
        清除指定用户的所有标题

        Args:
            user_id: 用户ID
        """
        if user_id in self.data:
            del self.data[user_id]
            self._save_data()

    def get_all_users(self) -> List[str]:
        """
        获取所有有标题的用户ID列表

        Returns:
            用户ID列表
        """
        return list(self.data.keys())

    def get_all_data(self) -> Dict[str, List[str]]:
        """
        获取所有数据

        Returns:
            完整的{user_id: titles}字典
        """
        return self.data.copy()

    def __str__(self) -> str:
        """返回数据的字符串表示"""
        return json.dumps(self.data, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # 创建管理器实例
    manager = CommonTitlesManager(directory="CommonTitlesManager")

    # 添加标题
    manager.add_title("112233", "常用标题1")
    manager.add_title("112233", "常用标题2")
    manager.add_title("112233", "常用标题2")
    manager.add_title("112233", "常用标题3")
    manager.add_title("2233", "测试标题A")
    manager.add_title("233", "测试标题A")

    # 获取标题
    print("用户112233的标题:", manager.get_titles("112233"))
    # 输出: ['常用标题3', '常用标题2', '常用标题1']

    # 更新标题
    manager.update_title("112233", "常用标题2", "更新后的标题2")
    print("更新后:", manager.get_titles("112233"))
    # 输出: ['更新后的标题2', '常用标题3', '常用标题1']

    # 添加更多标题以测试限制
    manager.add_title("112233", "新标题4")
    manager.add_title("112233", "新标题5")
    manager.add_title("112233", "新标题6")  # 这个会移除最早添加的标题
    print("添加6个标题后:", manager.get_titles("112233"))
    # 输出: ['新标题6', '新标题5', '新标题4', '更新后的标题2', '常用标题3'] (常用标题1被移除)

    # 移除标题
    manager.remove_title("2233", "测试标题A")
    manager.remove_title("2233", "测试标题")
    print("用户2233的标题:", manager.get_titles("2233"))
    # 输出: []

    # 获取所有用户
    print("所有用户:", manager.get_all_users())
    # 输出: ['112233'] (2233已被移除)

    # 清除用户
    manager.clear_user_titles("112233")
    manager.clear_user_titles("1133")
    print("清除后:", manager.get_titles("112233"))
    # 输出: []

    # 打印完整数据
    print("完整数据:")
    print(manager)
