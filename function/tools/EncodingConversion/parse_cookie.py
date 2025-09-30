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
    cookie_string = r"buvid3=24B878AA-65D8-B50F-115F-93620321758D34011infoc; b_nut=1756097834; _uuid=63397FF4-FC4C-8C5E-9D47-17799AB2610D529737infoc; buvid_fp=0909838887fa47f5d59a246818cf1969; enable_web_push=DISABLE; buvid4=6214F410-3FE8-53F4-D104-4838A446323434991-025082512-c55Uq60Y364aMkJdw+nh+WWaSElXXo+lKz1+lLtT33nfw+HhY7joPxfdJLNTR4mu; theme-tip-show=SHOWED; theme-avatar-tip-show=SHOWED; LIVE_BUVID=AUTO7917560980008599; theme-switch-show=SHOWED; DedeUserID=3546974607379019; DedeUserID__ckMd5=220bc66fcc74f43e; home_feed_column=4; browser_resolution=1059-1629; SESSDATA=85b3171d%2C1774179577%2C6cab5%2A91CjBSVIR17iygOYBCeeja3TZnjvDOadTlt0hGLBKOsrR4SzOrIWsyUpN9WBEq4XjCepMSVkZSSi01Rmx6RjhNaXNDS2Znd0s3TUdjR2Z5MWN3NGQ0WHFTaG5abXVoOEY0WVNnckRDa1RMU2E1bUg3YmZzd2Q0a2tUekJfNXVWMl9RZmZ3cGRqcV93IIEC; bili_jct=3ec9b89f79456a4c50ed068bf22f3eac; b_lsid=33D57815_199768D9C1D; bsource=search_bing; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTg4ODk4NTAsImlhdCI6MTc1ODYzMDU5MCwicGx0IjotMX0.FSW68IsOnr5suB8iRNRQ0zbQCPNZi21Z-JL8LUVJtaI; bili_ticket_expires=1758889790; CURRENT_QUALITY=0; rpdid=0zbfAKYWU2|v4zZtxHq|4fY|3w1V12aH; CURRENT_FNVAL=2000; sid=8l716553; PVID=3"
    parsed = parse_cookie(cookie_string)
    print(f"\n解析结果: {parsed}")
    print(f"\n解析结果: {parsed['DedeUserID']}")
    print(f"\n解析结果: {parsed['DedeUserID__ckMd5']}")
    print(f"\n解析结果: {parsed['SESSDATA']}")
    print(f"\n解析结果: {parsed['bili_jct']}")
    print(f"\n解析结果: {parsed['b_nut']}")
    print(f"\n解析结果: {parsed['buvid3']}")