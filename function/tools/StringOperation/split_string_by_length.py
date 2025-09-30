"""
函数功能
    - 这个函数的主要功能是：
    - 将长字符串按照指定长度分割成多个小块
    - 处理边界情况（空字符串、块大小大于字符串长度等）
    - 提供详细的执行结果和错误信息
"""
def split_string_into_chunks(text, chunk_size):
    """
    将字符串按照指定长度分割成多个块。

    Args:
        text (str): 需要分割的原始字符串
        chunk_size (int): 每个块的长度（字符数）

    Returns:
        dict: 包含操作结果和数据的字典，结构如下：
            - 'success' (bool): 操作是否成功
            - 'chunks' (list): 成功时分块后的字符串列表
            - 'error' (str): 失败时的错误信息
            - 'original_length' (int): 原始字符串长度
            - 'chunk_count' (int): 实际生成的块数

    Examples:
        >>> result = split_string_into_chunks("abcdefgh", 3)
        >>> result['success']
        True
        >>> result['chunks']
        ['abc', 'def', 'gh']

        >>> result = split_string_into_chunks("hello", 2)
        >>> result['success']
        True
        >>> result['chunks']
        ['he', 'll', 'o']

        >>> result = split_string_into_chunks("abc", 0)
        >>> result['success']
        False
        >>> result['error']
        '块大小必须大于0'
    """
    # 初始化返回结果字典
    result = {
        'success': False,
        'chunks': [],
        'error': '',
        'original_length': len(text) if isinstance(text, str) else 0,
        'chunk_count': 0
    }

    # 参数验证
    if not isinstance(text, str):
        result['error'] = '输入文本必须是字符串类型'
        return result

    if not isinstance(chunk_size, int):
        result['error'] = '块大小必须是整数'
        return result

    if chunk_size <= 0:
        result['error'] = '块大小必须大于0'
        return result

    # 处理空字符串
    if not text:
        result['success'] = True
        result['chunk_count'] = 0
        return result

    # 执行分割操作
    try:
        chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
        result['success'] = True
        result['chunks'] = chunks
        result['chunk_count'] = len(chunks)
    except Exception as e:
        result['error'] = f'分割过程中发生错误: {str(e)}'

    return result


# 使用示例
if __name__ == "__main__":
    # 测试用例
    test_cases = [
        ("abcdefghij", 3),
        ("", 3),
        ("abc", 5),
        ("hello world", 4),
        (123, 3),  # 错误用例
        ("test", 0)  # 错误用例
    ]

    for text, size in test_cases:
        result = split_string_into_chunks(text, size)
        print(f"输入: {text!r}, 块大小: {size}")
        print(f"结果: {result}")
        print("-" * 50)