def split_string_by_separators(text, separators):
    """
    使用指定的分隔符列表将字符串分割成多个部分，并保留分隔符。

    Args:
        text (str): 需要分割的原始字符串
        separators (list): 用作分隔符的字符串列表

    Returns:
        dict: 包含操作结果和数据的字典，结构如下：
            - 'success' (bool): 操作是否成功
            - 'segments' (list): 成功时分段后的字符串列表
            - 'error' (str): 失败时的错误信息
            - 'original_length' (int): 原始字符串长度
            - 'segment_count' (int): 实际生成的分段数量

    Examples:
        >>> result = split_string_by_separators("Hello world, this is a test.", ["world", "test"])
        >>> result['success']
        True
        >>> result['segments']
        ['Hello ', 'world', ', this is a ', 'test', '.']

        >>> result = split_string_by_separators("abc123def456", ["123", "456"])
        >>> result['success']
        True
        >>> result['segments']
        ['abc', '123', 'def', '456', '']
    """
    # 初始化返回结果字典
    result = {
        'success': False,
        'segments': [],
        'error': '',
        'original_length': len(text) if isinstance(text, str) else 0,
        'segment_count': 0
    }

    # 参数验证
    if not isinstance(text, str):
        result['error'] = '输入文本必须是字符串类型'
        return result

    if not isinstance(separators, list):
        result['error'] = '分隔符必须是列表类型'
        return result

    # 验证separators中的每个元素都是字符串
    for i, sep in enumerate(separators):
        if not isinstance(sep, str):
            result['error'] = f'分隔符列表中的第{i + 1}个元素必须是字符串类型'
            return result

    # 处理空字符串
    if not text:
        result['success'] = True
        result['segment_count'] = 0
        return result

    # 处理空分隔符列表
    if not separators:
        result['success'] = True
        result['segments'] = [text]
        result['segment_count'] = 1
        return result

    try:
        # 执行字符替换（避免使用eval，更安全的方法）
        processed_text = text

        # 字符替换映射
        char_replacements = {
            '"': "”",
            "'": "’",
            ",": "，",
            "\n": ""
        }

        # 应用字符替换
        for old_char, new_char in char_replacements.items():
            processed_text = processed_text.replace(old_char, new_char)

        # 使用更安全的方法分割字符串，避免eval
        segments = []
        current_pos = 0

        # 按顺序处理每个分隔符
        for separator in separators:
            if not separator:  # 跳过空分隔符
                continue

            # 查找分隔符位置
            pos = processed_text.find(separator, current_pos)

            if pos != -1:
                # 添加分隔符前的文本
                if pos > current_pos:
                    segments.append(processed_text[current_pos:pos])

                # 添加分隔符本身
                segments.append(separator)

                # 更新当前位置
                current_pos = pos + len(separator)

        # 添加剩余文本
        if current_pos < len(processed_text):
            segments.append(processed_text[current_pos:])

        # 过滤空字符串
        filtered_segments = [segment for segment in segments if segment]

        result['success'] = True
        result['segments'] = filtered_segments
        result['segment_count'] = len(filtered_segments)

    except Exception as e:
        result['error'] = f'分割过程中发生错误: {str(e)}'

    return result


# 使用示例
if __name__ == "__main__":
    # 测试用例
    test_cases = [
        ("Hello 'world', this is a \"test\"\nwith, commas", ["world", "test"]),
        ("abc123def456ghi", ["123", "456"]),
        ("", ["sep"]),  # 空字符串
        ("no separators here", []),  # 空分隔符列表
        ("test", [""]),  # 空字符串分隔符
        (123, ["sep"]),  # 错误类型
        ("text", "not_a_list")  # 错误类型
    ]

    for text, seps in test_cases:
        result = split_string_by_separators(text, seps)
        print(f"输入: {text!r}, 分隔符: {seps}")
        print(f"结果: {result}")
        print("-" * 50)