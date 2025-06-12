from typing import Dict
import urllib.parse


def cookie2dict(cookie: str) -> Dict[str, str]:
    """
    将符合HTTP标准的Cookie字符串转换为字典
    Args:
        cookie: Cookie字符串
            示例: "name=value; age=20; token=abc%20123"
    Returns:
        解析后的字典，键值均为字符串类型
        示例: {'name': 'value', 'age': '20', 'token': 'abc 123'}
    Raises:
        TypeError: 当输入不是字符串时抛出
    Features:
        - 自动处理URL解码
        - 兼容不同分隔符（; 或 ; ）
        - 过滤空键和空值条目
        - 保留重复键的最后出现值（符合HTTP规范）
        - 处理值中的等号
        - 更健壮的解码错误处理
    """
    if not isinstance(cookie, str):
        raise TypeError("输入必须是字符串类型")

    cookie_dict = {}
    # 处理空字符串
    if not cookie.strip():
        return cookie_dict

    # 分割Cookie字符串
    for pair in cookie.split(';'):
        pair = pair.strip()
        if not pair:
            continue

        # 仅分割第一个等号，正确处理含等号的值
        parts = pair.split('=', 1)
        if len(parts) != 2:
            continue  # 跳过无效条目

        key, value = parts
        key = key.strip()
        if not key:  # 过滤空键
            continue

        # 值处理：去除首尾空格
        value = value.strip()

        # 处理带引号的值 (如: "value")
        if len(value) >= 2 and value.startswith('"') and value.endswith('"'):
            value = value[1:-1]

        # 执行URL解码
        try:
            decoded_value = urllib.parse.unquote(value)
        except Exception:
            decoded_value = value  # 解码失败保留原始值

        # 过滤空值（空字符串）
        if decoded_value == "":
            continue

        cookie_dict[key] = decoded_value

    return cookie_dict


if __name__ == "__main__":
    tests = [
        ("name=value; age=20; token=abc%20123",
         {'name': 'value', 'age': '20', 'token': 'abc 123'}),

        ("key=val=ue; empty=; =invalid; quoted=\"hello\"",
         {'key': 'val=ue', 'quoted': 'hello'}),

        ("a=1;b=2; a=3",
         {'a': '3', 'b': '2'}),

        ("comma,separated=value; semi;colon=test",
         {'comma,separated': 'value', 'colon': 'test'}),

        ("special=%E4%B8%AD%E6%96%87",
         {'special': '中文'}),

        # 测试带空格的值
        ("space=value with space; empty_space=  ",
         {'space': 'value with space'}),

        # 测试带引号的值
        ("quoted_single=\"hello\"; quoted_multi=\"hello world\"",
         {'quoted_single': 'hello', 'quoted_multi': 'hello world'}),

        # 测试混合情况
        ("a=1; b=; c=3; =invalid; d=four",
         {'a': '1', 'c': '3', 'd': 'four'})
    ]

    for i, (cookie_str, expected) in enumerate(tests):
        result = cookie2dict(cookie_str)
        assert result == expected, (f"测试 #{i + 1} 失败:\n"
                                    f"输入: {cookie_str}\n"
                                    f"预期: {expected}\n"
                                    f"实际: {result}")
        print(f"测试 {i} 通过: {cookie_str}")
    print("所有测试通过！")
