"""
计算未来的Unix时间戳。它接受天、小时、分钟和秒作为参数，基于当前UTC时间计算未来某个时间点的时间戳。

主要改进
    - 函数名称优化：
        - 从 get_future_timestamp 改为 get_future_timestamp_utc
        - 明确表明函数基于UTC时间计算，避免时区混淆
    - 参数扩展：
        - 增加了 seconds 参数，提供更精确的时间控制
        - 支持浮点数参数，可以表示更精细的时间间隔
    - 时区处理改进：
        - 使用 datetime.timezone.utc 确保基于UTC时间计算
        - 避免本地时区对时间戳计算的影响
    - 输入验证：
        - 添加参数验证，确保所有时间参数为非负数
        - 提供清晰的错误信息
    - 文档字符串改进：
        - 更详细的函数说明
        - 明确的参数和返回值说明
        - 添加示例用法
    - 类型提示：
        - 添加完整的类型提示，提高代码可读性和工具支持
使用场景
    - 这个函数特别适用于：
        - 设置过期时间：为缓存、会话或令牌设置未来的过期时间
        - 定时任务：计算未来某个时间点执行任务的时间戳
        - 跨时区应用：基于UTC时间戳确保不同时区的一致性
        - 时间计算：任何需要计算未来时间点的场景
"""
import datetime
from typing import Union


def get_future_timestamp_utc(
        days: Union[int, float] = 0,
        hours: Union[int, float] = 0,
        minutes: Union[int, float] = 0,
        seconds: Union[int, float] = 0
) -> int:
    """
    获取当前UTC时间加上指定时间偏移后的Unix时间戳（秒级）。

    此函数基于UTC时间计算，确保时间戳不受本地时区影响，适合跨时区应用。

    Args:
        days: 要添加的天数（可以是整数或浮点数）
        hours: 要添加的小时数（可以是整数或浮点数）
        minutes: 要添加的分钟数（可以是整数或浮点数）
        seconds: 要添加的秒数（可以是整数或浮点数）

    Returns:
        10位Unix时间戳（秒级），表示未来的UTC时间

    Raises:
        ValueError: 如果任何参数为负数

    Examples:
        >>> get_future_timestamp_utc(days=1)  # 1天后的时间戳
        >>> get_future_timestamp_utc(hours=2, minutes=30)  # 2小时30分钟后的时间戳
    """
    # 验证参数非负
    if any(x < 0 for x in [days, hours, minutes, seconds]):
        raise ValueError("所有时间参数必须为非负数")

    # 获取当前UTC时间
    current_utc_time = datetime.datetime.now(datetime.timezone.utc)

    # 创建时间增量
    time_delta = datetime.timedelta(
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds
    )

    # 计算未来时间
    future_time = current_utc_time + time_delta

    # 转换为Unix时间戳（10位整数）
    return int(future_time.timestamp())


# 示例用法
if __name__ == "__main__":
    # 添加1天2小时30分钟15秒
    future_timestamp = get_future_timestamp_utc(days=1, hours=2, minutes=30, seconds=15)

    print(f"10位UTC时间戳: {future_timestamp}")
    print(f"对应UTC时间: {datetime.datetime.fromtimestamp(future_timestamp, datetime.timezone.utc)}")
    print(f"对应本地时间: {datetime.datetime.fromtimestamp(future_timestamp)}")