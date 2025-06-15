from typing import Dict, Union, Literal
from PIL import Image, ImageOps
import qrcode
import io
import sys


def qr_text8pil_img(
        qr_str: str,
        border: int = 2,
        error_correction: Literal[0, 1, 2, 3] = qrcode.constants.ERROR_CORRECT_L,
        invert: bool = False
) -> Dict[str, Union[str, Image.Image]]:
    """
    字符串转二维码（返回包含 PIL 图像对象的字典）

    Args:
        qr_str: 二维码文本（必须是有效的非空字符串）
        border: 边框大小（必须是非负整数，默认2）
        error_correction: 纠错级别（默认L）
            - ERROR_CORRECT_L: 1
            - ERROR_CORRECT_M: 0
            - ERROR_CORRECT_Q: 3
            - ERROR_CORRECT_H: 2
        invert: 是否反转颜色（默认False）

    Returns:
        Dict: 包含以下键的字典
            - str: ASCII 字符串形式的二维码
            - img: PIL.Image 对象（二维码图像）

    Raises:
        ValueError: 输入参数不合法时抛出
    """
    # 验证输入参数
    if not isinstance(qr_str, str) or not qr_str:
        raise ValueError("qr_str 必须是有效的非空字符串")
    if not isinstance(border, int) or border < 0:
        raise ValueError("border 必须是非负整数")

    # 创建 QRCode 对象
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=border,
        error_correction=error_correction,
    )

    # 添加数据并生成二维码
    qr.add_data(qr_str)
    qr.make(fit=True)

    # 生成二维码图像
    img = qr.make_image()

    # 创建内存缓冲区用于ASCII输出
    output = io.StringIO()
    sys.stdout = output

    try:
        # 生成ASCII表示
        qr.print_ascii(out=None, tty=False, invert=invert)
        output_str = output.getvalue()
    finally:
        # 确保恢复标准输出
        sys.stdout = sys.__stdout__

    # 处理颜色反转
    if invert:
        # 将二维码图像转换为RGBA模式以便正确处理反转
        if img.mode == '1':
            img = img.convert('L')
        img = ImageOps.invert(img)

    return {"str": output_str, "img": img}

# 示例用法
result = qr_text8pil_img("https://example.com", invert=True)

# 获取ASCII表示
print(result["str"])

# 获取PIL图像并显示
result["img"].show()
