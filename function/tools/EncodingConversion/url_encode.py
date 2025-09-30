from urllib.parse import quote


def url_encode(string_to_encode: str, safe: str = '/', encoding: str = 'utf-8') -> str:
    """
    将字符串转换为 URL 编码格式（百分号编码）

    此函数使用 UTF-8 编码将字符串转换为符合 URL 标准的格式，特殊字符会被转换为 %XX 形式。

    Args:
        string_to_encode: 要编码的字符串
        safe: 指定不应被编码的字符（默认为 '/'）
        encoding: 使用的字符编码（默认为 'utf-8'）

    Returns:
        URL 编码后的字符串

    Examples:
        >>> url_encode("hello world")
        'hello%20world'

        >>> url_encode("路径/文件.html")
        '%E8%B7%AF%E5%BE%84/%E6%96%87%E4%BB%B6.html'

        >>> url_encode("hello world", safe="")
        'hello%20world'

        >>> url_encode("hello world", safe=" ")
        'hello world'
    """
    # 使用 quote() 函数进行 URL 编码
    encoded_string = quote(string_to_encode, safe=safe, encoding=encoding)
    return encoded_string


if __name__ == '__main__':
    # 基本用法
    encoded = url_encode("hello world")
    print(encoded)  # 输出: hello%20world

    # 包含中文的字符串
    encoded = url_encode("中文测试")
    print(encoded)  # 输出: %E4%B8%AD%E6%96%87%E6%B5%8B%E8%AF%95

    # 保留某些字符不编码
    encoded = url_encode("path/to/file", safe="/")
    print(encoded)  # 输出: path/to/file

    # 保留空格不编码
    encoded = url_encode("hello world", safe=" ")
    print(encoded)  # 输出: hello world

    # 使用不同的编码
    encoded = url_encode("текст", encoding="utf-8")
    print(encoded)  # 输出: %D1%82%D0%B5%D0%BA%D1%81%D1%82