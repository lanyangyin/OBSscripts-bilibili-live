from PIL import Image
from typing import Literal, Optional


def resize_image(
        image: Image.Image,
        quality: Literal[1, 2, 3, 4] = 4,
        target_width: Optional[int] = None,
        scale_factor: Optional[float] = None
) -> Image.Image:
    """
    对 PIL 图像进行缩放操作，支持指定目标宽度或缩放比例

    此函数提供高质量的图像缩放功能，支持多种重采样算法，可以根据需求选择
    不同的质量等级，平衡图像质量与处理速度。

    Args:
        image: 要缩放的 PIL 图像对象
        quality: 缩放质量等级 (1-4)，默认最高质量
            1 = 最近邻 (速度快质量低，适合像素艺术)
            2 = 双线性 (平衡模式，通用用途)
            3 = 双三次 (高质量放大，适合照片)
            4 = Lanczos (最高质量，适合精细图像)
        target_width: 目标宽度（像素），与 scale_factor 二选一
        scale_factor: 缩放比例（例如 0.5 表示缩小一半，2.0 表示放大一倍），与 target_width 二选一

    Returns:
        Image.Image: 缩放后的 PIL 图像对象

    Raises:
        TypeError: 输入图像类型错误时抛出
        ValueError: 参数不符合要求时抛出

    Examples:
        >>> # 将图像宽度调整为 800 像素，使用最高质量
        >>> resized_img = resize_image(original_img, quality=4, target_width=800)

        >>> # 将图像缩小一半
        >>> resized_img = resize_image(original_img, quality=3, scale_factor=0.5)
    """
    # 参数验证
    if not isinstance(image, Image.Image):
        raise TypeError("输入必须是 PIL.Image.Image 对象")

    if quality not in (1, 2, 3, 4):
        raise ValueError("缩放质量等级必须是 1-4 的整数")

    if target_width is None and scale_factor is None:
        raise ValueError("必须指定 target_width 或 scale_factor 中的一个")

    if target_width is not None and scale_factor is not None:
        raise ValueError("只能指定 target_width 或 scale_factor 中的一个")

    # 选择重采样滤波器
    resampling_filters = {
        1: Image.NEAREST,  # 速度快质量低，适合像素艺术
        2: Image.BILINEAR,  # 平衡模式，通用用途
        3: Image.BICUBIC,  # 高质量放大，适合照片
        4: Image.LANCZOS,  # 最高质量，适合精细图像
    }

    resampling_filter = resampling_filters[quality]

    # 获取原始尺寸
    original_width, original_height = image.size

    # 计算新尺寸
    if target_width is not None:
        if target_width <= 0:
            raise ValueError("目标宽度必须大于0")

        # 计算等比例高度
        scale = target_width / original_width
        new_width = target_width
        new_height = int(original_height * scale)
    else:  # scale_factor is not None
        if scale_factor <= 0:
            raise ValueError("缩放比例必须大于0")

        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)

    # 确保最小尺寸为1像素
    new_width = max(1, new_width)
    new_height = max(1, new_height)

    # 执行缩放
    resized_image = image.resize((new_width, new_height), resampling_filter)

    return resized_image