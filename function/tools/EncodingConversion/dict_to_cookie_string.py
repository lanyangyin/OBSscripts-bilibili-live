from urllib.parse import quote
from typing import Dict, Any


def dict_to_cookie_string(data_dict: Dict[str, Any], encode_values: bool = True) -> str:
    """
    将字典转换为 HTTP Cookie 字符串格式

    此函数将键值对字典转换为符合 HTTP Cookie 标准的字符串格式，
    支持对值进行 URL 编码以防止特殊字符问题。

    Args:
        data_dict: 要转换的字典，键值对将被转换为 cookie 格式
        encode_values: 是否对值进行 URL 编码（默认 True）

    Returns:
        符合 HTTP Cookie 标准的字符串

    Examples:
        >>> dict_to_cookie_string({"name": "John", "age": 30})
        'name=John; age=30'

        >>> dict_to_cookie_string({"token": "abc 123"})
        'token=abc%20123'

        >>> dict_to_cookie_string({"session": "id=123&time=456"}, encode_values=False)
        'session=id=123&time=456'
    """
    if not isinstance(data_dict, dict):
        raise TypeError("输入必须是字典类型")

    cookie_parts = []

    for key, value in data_dict.items():
        # 确保键和值是字符串
        key_str = str(key)
        value_str = str(value)

        # 对值进行 URL 编码（如果启用）
        if encode_values:
            value_str = quote(value_str)

        # 添加到结果列表
        cookie_parts.append(f"{key_str}={value_str}")

    # 使用分号和空格连接所有部分
    return "; ".join(cookie_parts)