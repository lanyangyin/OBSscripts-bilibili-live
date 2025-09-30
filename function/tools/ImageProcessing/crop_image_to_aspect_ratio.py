from PIL import Image
from typing import Optional


def crop_image_to_aspect_ratio(
        image: Image.Image,
        target_aspect_ratio: float,
        tolerance: float = 0.01
) -> Optional[Image.Image]:
    """
    将图像裁切为指定的宽高比，保持图像内容居中

    此函数通过中心裁切的方式，将输入图像调整为指定的宽高比。
    裁切时会尽可能保留图像的中心区域，确保重要内容不被裁切掉。

    Args:
        image: 要处理的 PIL 图像对象
        target_aspect_ratio: 目标宽高比（宽度/高度的比值）
            示例：
            - 16:9 → 16/9 ≈ 1.778
            - 1:1 → 1.0
            - 4:3 → 1.333
            - 9:16 → 9/16 ≈ 0.5625
        tolerance: 容差范围，当原始宽高比与目标宽高比差异小于此值时，不进行裁切
            默认值为 0.01（1%）

    Returns:
        Image.Image: 裁切后的新图像对象，如果不需要裁切或裁切失败返回原图像

    Raises:
        TypeError: 输入不是有效的 PIL 图像对象
        ValueError: 目标比例不是正数或裁切尺寸无效
    """
    # 参数验证
    if not isinstance(image, Image.Image):
        raise TypeError("输入必须是有效的 PIL.Image.Image 对象")

    if target_aspect_ratio <= 0:
        raise ValueError("目标宽高比必须是正数")

    if tolerance < 0 or tolerance > 1:
        raise ValueError("容差必须在 0 到 1 之间")

    # 获取原始尺寸
    original_width, original_height = image.size
    original_ratio = original_width / original_height

    # 检查是否需要裁切（考虑容差）
    if abs(original_ratio - target_aspect_ratio) < tolerance:
        return image.copy()  # 返回原图像的副本

    try:
        # 计算裁切区域
        if original_ratio > target_aspect_ratio:
            # 过宽：固定高度，计算宽度
            crop_height = original_height
            crop_width = int(round(crop_height * target_aspect_ratio))
        else:
            # 过高：固定宽度，计算高度
            crop_width = original_width
            crop_height = int(round(crop_width / target_aspect_ratio))

        # 验证裁切尺寸
        if crop_width <= 0 or crop_height <= 0:
            raise ValueError("计算出的裁切尺寸无效")
        if crop_width > original_width or crop_height > original_height:
            raise ValueError("原始图片尺寸不足以完成裁切")

        # 计算裁切坐标（居中裁切）
        left = (original_width - crop_width) // 2
        top = (original_height - crop_height) // 2
        right = left + crop_width
        bottom = top + crop_height

        return image.crop((left, top, right, bottom))

    except Exception as e:
        # 发生任何错误时返回原图像
        return image.copy()