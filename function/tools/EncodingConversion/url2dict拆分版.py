from urllib.parse import unquote, parse_qs, urlparse
from typing import Dict, Union, List, Any


def url2dict(url: str, decode: bool = True, handle_multiple: bool = True) -> Dict[str, Union[str, int, float, bool, None, List[Any]]]:
    """
    将 URL 参数解析为字典，支持复杂参数处理

    修复内容：
    1. 修复片段参数解析逻辑，正确处理查询参数和片段参数共存的情况
    2. 调整类型转换顺序，避免数字被错误转换为布尔值
    3. 优化参数合并逻辑，优先使用查询参数

    Args:
        url: 包含查询参数的 URL 字符串
        decode: 是否自动 URL 解码参数值（默认 True）
        handle_multiple: 是否保留多值参数的所有值（默认 True）

    Returns:
        解析后的参数字典，单值参数为基本类型，多值参数为列表
    """
    # 处理空URL或非字符串输入
    if not url or not isinstance(url, str):
        return {}

    # 提取查询参数部分
    parsed = urlparse(url)
    query_str = parsed.query
    fragment_str = parsed.fragment

    # 处理片段中的参数
    frag_query_str = None
    if fragment_str:
        # 处理哈希路由模式 (如: #/path?key=value)
        if '?' in fragment_str:
            # 分割片段，保留查询参数部分
            _, frag_query = fragment_str.split('?', 1)
            frag_query_str = frag_query
        # 处理片段直接包含参数的情况 (如: #key=value)
        elif '=' in fragment_str:
            frag_query_str = fragment_str

    # 分别解析查询参数和片段参数
    query_dict = _parse_query_string(query_str, decode, handle_multiple)
    frag_dict = _parse_query_string(frag_query_str, decode, handle_multiple) if frag_query_str else {}

    # 合并参数：查询参数优先于片段参数
    result = {}
    result.update(frag_dict)  # 先添加片段参数
    result.update(query_dict)  # 查询参数覆盖片段参数

    return result


def _parse_query_string(query_str: str, decode: bool, handle_multiple: bool) -> Dict[str, Any]:
    """解析查询字符串为字典"""
    if not query_str:
        return {}

    try:
        params_dict = parse_qs(query_str, keep_blank_values=True)
    except Exception as e:
        # 回退到手动解析
        return _fallback_parse(query_str, decode, handle_multiple)

    result = {}
    for key, values in params_dict.items():
        # 自动解码键
        clean_key = unquote(key) if decode else key

        if handle_multiple and len(values) > 1:
            # 处理多值参数 - 转换每个值
            converted_values = [_convert_types(unquote(v) if decode else v) for v in values]
            result[clean_key] = converted_values
        else:
            # 单值参数 - 转换单个值
            value = values[0] if values else ''
            clean_value = unquote(value) if decode else value
            result[clean_key] = _convert_types(clean_value)

    return result


def _fallback_parse(query_str: str, decode: bool, handle_multiple: bool) -> Dict[str, Any]:
    """手动解析回退方案"""
    result = {}
    # 处理空查询字符串
    if not query_str:
        return result

    pairs = [p for p in query_str.split('&') if p]

    for pair in pairs:
        # 处理键值对 (最多分割一次)
        parts = pair.split('=', 1)
        key = parts[0]
        value = parts[1] if len(parts) > 1 else ''

        # 解码处理
        key = unquote(key) if decode else key
        value_str = unquote(value) if decode else value

        # 类型转换
        converted_value = _convert_types(value_str)

        # 处理多值参数
        if handle_multiple and key in result:
            existing = result[key]
            if isinstance(existing, list):
                existing.append(converted_value)
            else:
                result[key] = [existing, converted_value]
        else:
            result[key] = converted_value

    return result


def _convert_types(value: str) -> Union[str, int, float, bool, None]:
    """尝试将字符串值转换为合适的类型（修复类型转换顺序）"""
    # 处理空值
    if value == '':
        return None

    # 先尝试数字转换（避免数字被误转为布尔值）

    # 整数 (仅当完全由数字组成)
    if value.isdigit():
        try:
            return int(value)
        except (ValueError, TypeError):
            pass

    # 浮点数 (包含小数点或科学计数法)
    if '.' in value or 'e' in value.lower():
        try:
            return float(value)
        except (ValueError, TypeError):
            pass

    # 百分比值 (如 "75%")
    if value.endswith('%') and value[:-1].replace('.', '', 1).isdigit():
        try:
            return float(value[:-1]) / 100.0
        except (ValueError, TypeError):
            pass

    # 最后尝试布尔值
    if value.lower() in {'true', 'yes', 'on', '1'}:
        return True
    if value.lower() in {'false', 'no', 'off', '0'}:
        return False

    # 保留原始字符串
    return value


if __name__ == '__main__':
    # 完整测试用例
    def test_url2dict():
        test_cases = [
            # 基础测试
            ("?name=John", {'name': 'John'}),
            ("https://example.com?age=30", {'age': 30}),

            # 多值参数
            ("?color=red&color=blue", {'color': ['red', 'blue']}),
            ("?flag=1&flag=0", {'flag': [1, 0]}),  # 多值处理

            # 类型转换
            ("?enabled=true&disabled=off", {'enabled': True, 'disabled': False}),
            ("?count=5&price=9.99", {'count': 5, 'price': 9.99}),
            ("?percent=75%", {'percent': 0.75}),

            # 空值和特殊值
            ("?empty=&null", {'empty': None, 'null': None}),
            ("?special=a=b=c", {'special': 'a=b=c'}),

            # 编码处理
            ("https://example.com?q=hello%20world&city=%E5%8C%97%E4%BA%AC",
             {'q': 'hello world', 'city': '北京'}),

            # 无参数情况
            ("https://example.com", {}),
            ("", {}),

            # 哈希路由模式
            ("#/path?page=2", {'page': 2}),
            ("app#?view=detail", {'view': 'detail'}),
            ("#access_token=ABC123", {'access_token': 'ABC123'}),

            # 混合模式 (查询参数 + 片段参数)
            ("https://example.com/path?main=1#fragment?sub=2", {'main': 1, 'sub': 2}),
            ("https://example.com?query=val#frag=value", {'query': 'val', 'frag': 'value'}),

            # 参数优先级测试 (查询参数应优先于片段参数)
            ("https://example.com?param=query#param=fragment", {'param': 'query'}),

            # 数字不应被转为布尔值
            ("?flag=1&test=0", {'flag': 1, 'test': 0}),
        ]

        for i, (url, expected) in enumerate(test_cases, 1):
            try:
                # 特殊处理多值测试
                if "flag=1&flag=0" in url:
                    result = url2dict(url, handle_multiple=True)
                else:
                    result = url2dict(url)

                assert result == expected, f"期望 {expected}，得到 {result}"
                print(f"测试 {i} 通过: {url}")
            except AssertionError as e:
                print(f"测试 {i} 失败: {url}")
                print(f"  期望: {expected}")
                print(f"  实际: {result}")
                print(f"  错误: {e}")

        print("测试完成!")


    test_url2dict()

    # 基础用法
    url = "https://api.example.com/data?ids=1,2,3&format=json&pretty=true"
    params = url2dict(url)
    print(params)
    # 输出: {'ids': '1,2,3', 'format': 'json', 'pretty': True}

    # 多值参数处理
    url = "https://store.example.com/search?category=electronics&category=books&sort=price"
    params = url2dict(url)
    print(params)
    # 输出: {'category': ['electronics', 'books'], 'sort': 'price'}

    # 类型转换
    url = "config?width=1920&height=1080&scale=1.5&dark_mode=true&volume=80%"
    params = url2dict(url)
    print(params)
    # 输出: {'width': 1920, 'height': 1080, 'scale': 1.5, 'dark_mode': True, 'volume': 0.8}

    # 特殊字符处理
    url = "submit?name=John+Doe&email=john%40example.com&message=Hello%20World%21"
    params = url2dict(url)
    print(params)
    # 输出: {'name': 'John Doe', 'email': 'john@example.com', 'message': 'Hello World!'}

    # 可以单独使用转换函数
    value = _convert_types("123")
    print(value)
