def parse_color_value(color_value: int, has_alpha: bool = True):
    """
    从 color_value 解析出 RGBA 分量。
    返回 (red, green, blue, alpha) 元组，alpha 仅当 has_alpha=True 时有效，否则固定为 255。
    """
    blue = (color_value >> 16) & 0xFF
    green = (color_value >> 8) & 0xFF
    red = color_value & 0xFF
    if has_alpha:
        alpha = (color_value >> 24) & 0xFF
    else:
        alpha = 0xFF  # 默认完全不透明
    return red, green, blue, alpha

def int_to_color_str(value: int) -> str:
    """
    将 RGBA 整数 (0xAARRGGBB) 转换为 "#RRGGBB AA" 格式的字符串。
    如果希望显示为 "#FFFF FFFF"，只需调换顺序。
    """
    alpha = (value >> 24) & 0xFF
    red   = (value >> 16) & 0xFF   # 注意：OBS 低24位是 BGR，所以这里可能需要调整
    green = (value >> 8) & 0xFF
    blue  = value & 0xFF

    # 常见显示顺序：Alpha 在最后，如 "#RRGGBB AA"
    return f"#{red:02X}{green:02X}{blue:02X} {alpha:02X}"