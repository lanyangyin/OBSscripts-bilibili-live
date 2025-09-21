from PIL import Image
from io import BytesIO
from typing import Literal


def convert_pil_image_to_bytes(
        image: Image.Image,
        output_format: Literal["PNG", "JPEG"],
        compression_level: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9] = 6
) -> bytes:
    """
    将 PIL 图像对象转换为指定格式的二进制数据，支持多种压缩选项

    此函数提供了对 PNG 和 JPEG 格式的精细控制，允许调整压缩级别和质量设置，
    以满足不同的存储和传输需求。

    Args:
        image: PIL 图像对象，需要转换的图像
        output_format: 输出图像格式
            - "PNG": 使用无损压缩，支持透明度
            - "JPEG": 使用有损压缩，适合照片类图像
        compression_level: 压缩级别 (0-9)
            对于 PNG: 0=无压缩/最快，9=最大压缩/最慢
            对于 JPEG: 0=最低质量/最小文件，9=最高质量/最大文件

    Returns:
        bytes: 图像的二进制数据，可直接用于保存或传输

    Raises:
        ValueError: 当输入参数不合法时抛出
        OSError: 当图像保存失败时抛出

    Examples:
        >>> from PIL import Image
        >>> img = Image.open("example.jpg")
        >>> png_data = convert_pil_image_to_bytes(img, "PNG", 6)
        >>> jpeg_data = convert_pil_image_to_bytes(img, "JPEG", 8)

        # 保存到文件
        >>> with open("output.png", "wb") as f:
        >>>     f.write(png_data)
    """
    # 参数验证
    if not isinstance(image, Image.Image):
        raise ValueError("输入必须是有效的 PIL.Image.Image 对象")

    if output_format not in ("PNG", "JPEG"):
        raise ValueError(f"不支持的图像格式: {output_format}，只支持 PNG/JPEG")

    if compression_level not in range(10):  # 0-9
        raise ValueError(f"不支持的压缩级别: {compression_level}，只支持 0～9")

    # 准备保存参数
    save_kwargs = {}

    if output_format == "PNG":
        save_kwargs = {
            "format": "PNG",
            "compress_level": compression_level
        }
    elif output_format == "JPEG":
        # 将压缩级别映射到质量参数 (0=最低质量，9=最高质量)
        quality_map = [5, 15, 25, 35, 50, 70, 80, 90, 95, 100]
        quality = quality_map[compression_level]

        # 转换图像模式为 RGB (JPEG 不支持透明度)
        if image.mode != "RGB":
            image = image.convert("RGB")

        save_kwargs = {
            "format": "JPEG",
            "quality": quality,
            "optimize": True,
            "subsampling": 0 if quality >= 90 else 1  # 高质量使用全采样
        }

    # 执行转换
    buffer = BytesIO()
    try:
        image.save(buffer, **save_kwargs)
        image_bytes = buffer.getvalue()
    except Exception as e:
        raise OSError(f"图像保存失败: {str(e)}") from e
    finally:
        buffer.close()

    return image_bytes