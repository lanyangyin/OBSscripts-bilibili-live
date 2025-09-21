"""
CommonDataManager 是一个用于管理用户多种类型常用数据的 Python 类。它提供了一个结构化的方式来存储、检索和管理用户的各种数据项，如标题、分类、标签等。

核心功能
    - 多数据类型支持：可以管理多种类型的数据，而不仅仅是单一类型
    - 用户隔离：每个用户的数据独立存储，互不干扰
    - 数量限制：每种数据类型最多保留指定数量的元素（默认5个）
    - 自动格式转换：能够自动将旧格式数据转换为新格式
    - 持久化存储：所有数据自动保存到 JSON 文件中
构造函数
    - python
    - def __init__(self, directory: Union[str, Path], default_data_type: str = "title", maximum_quantity_of_elements: int = 5)
参数：
    - directory: 数据文件存储目录
    - default_data_type: 默认数据类型（用于处理旧格式数据）
    - maximum_quantity_of_elements: 每种数据类型保留的最大元素数量
功能：
    - 初始化数据管理器，创建或加载数据文件，并自动转换旧格式数据。
主要方法详解
    1. get_data(user_id: str, data_type: str) -> List[str]
        - 功能：获取指定用户的指定类型数据列表
        - 参数：
            - user_id: 用户ID
            - data_type: 数据类型
        - 返回值：该用户的指定类型数据列表（如果没有则为空列表）
        - 示例：
            - python
            - titles = manager.get_data("143474500", "title")
            - # 返回: ["常用标题1", "常用标题2"]
    2. add_data(user_id: str, data_type: str, item: str) -> None
        - 功能：为用户添加新数据项
        - 特点：
            - 如果数据项已存在，则移动到列表最前面
            - 确保列表长度不超过设定的最大值
            - 如果用户不存在，则创建新条目
            - 如果数据类型不存在，则创建新类型
        - 参数：
            - user_id: 用户ID
            - data_type: 数据类型
            - item: 要添加的数据项
        - 示例：
            - python
            - manager.add_data("143474500", "title", "新标题")
            - manager.add_data("143474500", "category", "科技")
    3. remove_data(user_id: str, data_type: str, item: str) -> bool
        - 功能：移除用户的指定数据项
        - 参数：
            - user_id: 用户ID
            - data_type: 数据类型
            - item: 要移除的数据项
        - 返回值：
            - True: 成功移除
            - False: 数据项不存在
        - 示例：
            - python
            - success = manager.remove_data("143474500", "title", "常用标题1")
    4. update_data(user_id: str, data_type: str, old_item: str, new_item: str) -> bool
        - 功能：更新用户的数据项
        - 参数：
            - user_id: 用户ID
            - data_type: 数据类型
            - old_item: 要替换的旧数据项
            - new_item: 新数据项
        - 返回值：
            - True: 更新成功
            - False: 旧数据项不存在
        - 示例：
            - python
            - success = manager.update_data("143474500", "title", "旧标题", "新标题")
    5. clear_user_data(user_id: str, data_type: Optional[str] = None) -> None
        - 功能：清除指定用户的指定类型数据或所有数据
        - 参数：
            - user_id: 用户ID
            - data_type: 数据类型（如果为None，则清除所有数据）
        - 示例：
            - python
            - # 清除特定类型数据
            - manager.clear_user_data("143474500", "title")
            - # 清除所有数据
            - manager.clear_user_data("143474500")
    6. get_all_users() -> List[str]
        - 功能：获取所有有数据的用户ID列表
        - 返回值：用户ID列表
        - 示例：
            - python
            - users = manager.get_all_users()
            - # 返回: ["143474500", "223344"]
    7. get_user_data_types(user_id: str) -> List[str]
        - 功能：获取指定用户的所有数据类型
        - 参数：
            - user_id: 用户ID
        - 返回值：数据类型列表
        - 示例：
            - python
            - data_types = manager.get_user_data_types("143474500")
            - # 返回: ["title", "category", "tag"]
    8. get_all_data() -> Dict[str, Dict[str, List[str]]]
        - 功能：获取所有数据
        - 返回值：完整的{user_id: {data_type: items}}字典
        - 示例：
            - python
            - all_data = manager.get_all_data()
            - # 返回: {
            - #   "143474500": {
            - #     "title": ["标题1", "标题2"],
            - #     "category": ["科技", "生活"]
            - #   },
            - #   "223344": {
            - #     "title": ["用户2标题"]
            - #   }
            - # }
使用示例
    - 基本用法
        - python
        - # 创建管理器实例
        - manager = CommonDataManager(directory="data", maximum_quantity_of_elements=5)
        - # 添加数据
        - manager.add_data("user1", "title", "我的第一个标题")
        - manager.add_data("user1", "title", "我的第二个标题")
        - manager.add_data("user1", "category", "科技")
        - manager.add_data("user1", "tag", "教程")
        - # 获取数据
        - titles = manager.get_data("user1", "title")
        - categories = manager.get_data("user1", "category")
        - # 更新数据
        - manager.update_data("user1", "title", "我的第一个标题", "更新后的标题")
        - # 删除数据
        - manager.remove_data("user1", "tag", "教程")
        - # 获取所有用户
        - all_users = manager.get_all_users()
        - # 获取用户的所有数据类型
        - user_data_types = manager.get_user_data_types("user1")
        - # 获取所有数据
        - all_data = manager.get_all_data()
        - # 清除数据
        - manager.clear_user_data("user1", "category")  # 清除特定类型
        - manager.clear_user_data("user1")  # 清除所有数据
    - 实际应用场景
        - 用户偏好设置：存储用户常用的搜索关键词、分类偏好等
        - 历史记录：保存用户最近访问的页面、最近使用的功能等
        - 个性化推荐：基于用户常用数据提供个性化内容推荐
        - 多设备同步：在不同设备间同步用户的常用数据
数据文件格式
    - 新格式（当前）
        - json
        - {
          - "143474500": {
            - "title": ["标题1", "标题2"],
            - "category": ["科技", "生活"],
            - "tag": ["教程", "高级"]
          - },
          - "223344": {
            - "title": ["用户2标题"]
          - }
        - }
    - 旧格式（自动转换）
        - json
        - {
          - "143474500": ["标题1", "标题2"],
          - "223344": ["用户2标题"]
        - }
"""
import json
import os
from pathlib import Path
from typing import Dict, List, Union, Optional, Any


class CommonDataManager:
    """
    管理用户多种类型常用数据的JSON文件

    功能:
    - 管理 {user_id: {data_type1: [item1, item2, ...], data_type2: [...]}} 格式的JSON文件
    - 每种数据类型最多包含5个元素
    - 支持增删改查操作
    - 自动创建不存在的目录和文件
    - 自动转换旧格式数据到新格式

    参数:
        directory: 文件存放目录
        default_data_type: 默认数据类型（用于向后兼容）
    """

    def __init__(self, directory: Union[str, Path], default_data_type: str = "title", maximum_quantity_of_elements: int = 5):
        """
        初始化CommonDataManager

        Args:
            directory: 文件存放目录
            default_data_type: 默认数据类型（用于处理旧格式数据）
            maximum_quantity_of_elements: 保留的最大元素数
        """
        self.directory = Path(directory)
        self.filepath = self.directory / "commonData.json"
        self.default_data_type = default_data_type
        self.maximum_quantity_of_elements = maximum_quantity_of_elements
        self.data: Dict[str, Dict[str, List[str]]] = {}

        # 确保目录存在
        self.directory.mkdir(parents=True, exist_ok=True)

        # 如果文件不存在则创建
        if not self.filepath.exists():
            self._save_data()
        else:
            self._load_data()
            self._convert_old_format()

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

    def _convert_old_format(self) -> None:
        """将旧格式数据转换为新格式"""
        needs_save = False

        for user_id, user_data in list(self.data.items()):
            # 如果用户数据是列表格式（旧格式），则转换为新格式
            if isinstance(user_data, list):
                self.data[user_id] = {self.default_data_type: user_data}
                needs_save = True

        if needs_save:
            self._save_data()

    def get_data(self, user_id: str, data_type: str) -> List[str]:
        """
        获取指定用户的指定类型数据列表

        Args:
            user_id: 用户ID
            data_type: 数据类型

        Returns:
            该用户的指定类型数据列表（如果没有则为空列表）
        """
        if user_id not in self.data:
            return []

        return self.data[user_id].get(data_type, [])

    def add_data(self, user_id: str, data_type: str, item: str) -> None:
        """
        为用户添加新数据项

        特点:
        - 如果数据项已存在，则移动到列表最前面
        - 确保列表长度不超过5个
        - 如果用户不存在，则创建新条目
        - 如果数据类型不存在，则创建新类型

        Args:
            user_id: 用户ID
            data_type: 数据类型
            item: 要添加的数据项
        """
        # 确保用户数据存在
        if user_id not in self.data:
            self.data[user_id] = {}

        # 确保数据类型存在
        if data_type not in self.data[user_id]:
            self.data[user_id][data_type] = []

        items = self.data[user_id][data_type]

        # 移除重复项（如果存在）
        if item in items:
            items.remove(item)

        # 添加到列表开头
        items.insert(0, item)

        # 确保不超过5个元素
        if len(items) > self.maximum_quantity_of_elements:
            items = items[:self.maximum_quantity_of_elements]

        # 更新数据并保存
        self.data[user_id][data_type] = items
        self._save_data()

    def remove_data(self, user_id: str, data_type: str, item: str) -> bool:
        """
        移除用户的指定数据项

        Args:
            user_id: 用户ID
            data_type: 数据类型
            item: 要移除的数据项

        Returns:
            True: 成功移除
            False: 数据项不存在
        """
        if user_id not in self.data or data_type not in self.data[user_id]:
            return False

        items = self.data[user_id][data_type]

        if item in items:
            items.remove(item)
            # 如果列表为空，则删除数据类型条目
            if not items:
                del self.data[user_id][data_type]
                # 如果用户数据为空，则删除用户条目
                if not self.data[user_id]:
                    del self.data[user_id]
            self._save_data()
            return True
        return False

    def update_data(self, user_id: str, data_type: str, old_item: str, new_item: str) -> bool:
        """
        更新用户的数据项

        Args:
            user_id: 用户ID
            data_type: 数据类型
            old_item: 要替换的旧数据项
            new_item: 新数据项

        Returns:
            True: 更新成功
            False: 旧数据项不存在
        """
        if user_id not in self.data or data_type not in self.data[user_id]:
            return False

        items = self.data[user_id][data_type]

        if old_item in items:
            # 替换数据项并移动到列表前面
            index = items.index(old_item)
            items.pop(index)
            items.insert(0, new_item)
            self._save_data()
            return True
        return False

    def clear_user_data(self, user_id: str, data_type: Optional[str] = None) -> None:
        """
        清除指定用户的指定类型数据或所有数据

        Args:
            user_id: 用户ID
            data_type: 数据类型（如果为None，则清除所有数据）
        """
        if user_id not in self.data:
            return

        if data_type is None:
            # 清除所有数据
            del self.data[user_id]
        elif data_type in self.data[user_id]:
            # 清除指定类型数据
            del self.data[user_id][data_type]
            # 如果用户数据为空，则删除用户条目
            if not self.data[user_id]:
                del self.data[user_id]

        self._save_data()

    def get_all_users(self) -> List[str]:
        """
        获取所有有数据的用户ID列表

        Returns:
            用户ID列表
        """
        return list(self.data.keys())

    def get_user_data_types(self, user_id: str) -> List[str]:
        """
        获取指定用户的所有数据类型

        Args:
            user_id: 用户ID

        Returns:
            数据类型列表
        """
        if user_id not in self.data:
            return []

        return list(self.data[user_id].keys())

    def get_all_data(self) -> Dict[str, Dict[str, List[str]]]:
        """
        获取所有数据

        Returns:
            完整的{user_id: {data_type: items}}字典
        """
        return self.data.copy()

    def __str__(self) -> str:
        """返回数据的字符串表示"""
        return json.dumps(self.data, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # 创建管理器实例
    manager = CommonDataManager(directory="CommonDataManager", maximum_quantity_of_elements=5)

    # 添加标题数据
    manager.add_data("143474500", "title", "常用标题1")
    manager.add_data("143474500", "title", "常用标题2")

    # 添加其他类型数据
    manager.add_data("143474500", "category", "科技")
    manager.add_data("143474500", "category", "生活")
    manager.add_data("143474500", "tag", "教程")

    # 添加另一个用户的数据
    manager.add_data("223344", "title", "用户2的标题")
    manager.add_data("223344", "category", "娱乐")

    # 获取数据
    print("用户143474500的标题:", manager.get_data("143474500", "title"))
    print("用户143474500的分类:", manager.get_data("143474500", "category"))
    print("用户143474500的标签:", manager.get_data("143474500", "tag"))

    # 获取用户的所有数据类型
    print("用户143474500的数据类型:", manager.get_user_data_types("143474500"))

    # 更新数据
    manager.update_data("143474500", "title", "常用标题2", "更新后的标题2")
    print("更新后:", manager.get_data("143474500", "title"))

    # 添加更多标题以测试限制
    manager.add_data("143474500", "title", "新标题3")
    manager.add_data("143474500", "title", "新标题4")
    manager.add_data("143474500", "title", "新标题5")
    manager.add_data("143474500", "title", "新标题6")  # 这个会移除最早添加的标题
    print("添加6个标题后:", manager.get_data("143474500", "title"))

    # 移除数据
    manager.remove_data("223344", "title", "用户2的标题")
    print("用户223344的标题:", manager.get_data("223344", "title"))

    # 获取所有用户
    print("所有用户:", manager.get_all_users())

    # 清除用户数据
    manager.clear_user_data("223344", "category")
    print("清除分类后用户223344的数据类型:", manager.get_user_data_types("223344"))

    manager.clear_user_data("223344")  # 清除所有数据
    print("清除所有数据后用户223344的数据:", manager.get_data("223344", "title"))

    # 打印完整数据
    print("完整数据:")
    print(manager)