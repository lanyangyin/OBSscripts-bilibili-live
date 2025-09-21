import urllib.parse
from typing import Dict


def parse_cookie(
        cookie_str: str,
        decode_url: bool = True,
        strip_quotes: bool = True,
        filter_empty: bool = True
) -> Dict[str, str]:
    """
    解析 Cookie 字符串为字典格式，支持多种 Cookie 格式。

    此函数能够处理各种来源的 Cookie 字符串，提供灵活的解析选项。

    Args:
        cookie_str: 要解析的 Cookie 字符串
        decode_url: 是否对值进行 URL 解码（默认 True）
        strip_quotes: 是否去除值两端的引号（默认 True）
        filter_empty: 是否过滤空值（默认 True）

    Returns:
        解析后的字典，键值均为字符串类型

    Raises:
        TypeError: 当输入不是字符串时抛出
        ValueError: 当输入为空或只包含空白字符时抛出
    """
    if not isinstance(cookie_str, str):
        raise TypeError("输入必须是字符串类型")

    # 去除首尾空白字符
    cookie_str = cookie_str.strip()
    if not cookie_str:
        raise ValueError("输入字符串不能为空或只包含空白字符")

    cookie_dict = {}

    # 分割 Cookie 字符串
    for pair in cookie_str.split(';'):
        pair = pair.strip()
        if not pair:
            continue

        # 检查并分割第一个等号
        if '=' not in pair:
            continue  # 跳过没有等号的无效条目

        parts = pair.split('=', 1)
        key = parts[0].strip()
        value = parts[1].strip() if len(parts) > 1 else ""

        # 跳过空键
        if not key:
            continue

        # 处理带引号的值
        if strip_quotes and len(value) >= 2 and value.startswith('"') and value.endswith('"'):
            value = value[1:-1]

        # 执行 URL 解码（如果启用）
        if decode_url:
            try:
                value = urllib.parse.unquote(value)
            except Exception:
                pass  # 解码失败保留原始值

        # 过滤空值（如果启用）
        if filter_empty and not value:
            continue

        cookie_dict[key] = value

    return cookie_dict


if __name__ == "__main__":
    # 测试用例
    test_cases = [
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
         {'a': '1', 'c': '3', 'd': 'four'}),

        # 测试 URL 编码关闭
        ("encoded=%E4%B8%AD%E6%96%87", False,
         {'encoded': '%E4%B8%AD%E6%96%87'}),

        # 测试引号处理关闭
        ("quoted=\"hello\"", True, False,
         {'quoted': '"hello"'})
    ]

    print("Running tests...")
    for i, test in enumerate(test_cases):
        if len(test) == 2:
            cookie_str, expected = test
            result = parse_cookie(cookie_str)
        elif len(test) == 3:
            cookie_str, decode_url, expected = test
            result = parse_cookie(cookie_str, decode_url=decode_url)
        else:
            cookie_str, decode_url, strip_quotes, expected = test
            result = parse_cookie(cookie_str, decode_url=decode_url, strip_quotes=strip_quotes)

        assert result == expected, (f"测试 #{i + 1} 失败:\n"
                                    f"输入: {cookie_str}\n"
                                    f"预期: {expected}\n"
                                    f"实际: {result}")
        print(f"测试 {i + 1} 通过: {cookie_str}")

    print("所有测试通过！")

    # 示例用法
    cookie_string = "name=John%20Doe; age=30; session_id=abc123%20def456"
    parsed = parse_cookie(cookie_string)
    print(f"\n解析结果: {parsed}")