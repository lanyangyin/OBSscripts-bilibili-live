import datetime


def get_future_timestamp(days=0, hours=0, minutes=0):
    """
    获取当前时间加上指定天数、小时、分钟后的10位Unix时间戳

    参数:
    days (int): 要添加的天数
    hours (int): 要添加的小时数
    minutes (int): 要添加的分钟数

    返回:
    int: 10位Unix时间戳（秒级）
    """
    # 获取当前时间（本地时区）
    current_time = datetime.datetime.now()

    # 创建时间增量（x天y小时z分钟）
    time_delta = datetime.timedelta(
        days=days,
        hours=hours,
        minutes=minutes
    )

    # 计算未来时间
    future_time = current_time + time_delta

    # 转换为Unix时间戳（10位整数）
    timestamp = int(future_time.timestamp())

    return timestamp


# 示例用法
if __name__ == "__main__":
    # 添加3天4小时30分钟
    future_timestamp = get_future_timestamp(days=3, hours=4, minutes=30)

    print(f"10位时间戳: {future_timestamp}")
    print(f"对应时间: {datetime.datetime.fromtimestamp(future_timestamp)}")



