"""
qr_text8pil_img 是一个更健壮、更安全的文本转二维码工具，它解决了原函数中的线程安全和异常处理问题。

主要改进
    - 移除了 sys.stdout 重定向：
        - 使用 io.StringIO 对象直接捕获输出，而不是重定向全局 sys.stdout
        - 避免了多线程环境中的竞争条件
        - 消除了异常情况下 sys.stdout 无法恢复的风险
    - 更清晰的错误处理：
        - 使用更明确的错误消息
        - 确保所有资源都被正确关闭
    - 更简洁的代码结构：
        - 减少了不必要的代码复杂性
        - 提高了可读性和可维护性
函数功能
    - 二维码生成：将任意文本字符串转换为二维码
    - 双格式输出：
        - ASCII 字符画形式：适用于终端显示或文本环境
        - PIL 图像对象：适用于图形界面或图像处理
    - 高度可定制：
        - 可调整边框大小
        - 可选择纠错级别（L/M/Q/H）
        - 可反转颜色（黑底白字或白底黑字）
    - 健壮性：
        - 输入参数验证
        - 异常处理
        - 资源管理
"""
from typing import Dict, Union, Literal
from PIL import Image, ImageOps
import qrcode
import io


def qr_text8pil_img(
        qr_str: str,
        border: int = 2,
        error_correction: Literal[0, 1, 2, 3] = qrcode.constants.ERROR_CORRECT_L,
        invert: bool = False
) -> Dict[str, Union[str, Image.Image]]:
    """
    将文本字符串转换为二维码，返回包含 ASCII 字符画和 PIL 图像对象的字典

    Args:
        qr_str: 要编码为二维码的文本字符串
        border: 二维码边框大小（默认为2）
        error_correction: 纠错级别（默认L级）
            - 0: ERROR_CORRECT_M (约15%的错误可纠正)
            - 1: ERROR_CORRECT_L (约7%的错误可纠正)
            - 2: ERROR_CORRECT_H (约30%的错误可纠正)
            - 3: ERROR_CORRECT_Q (约25%的错误可纠正)
        invert: 是否反转颜色（默认False，黑底白字）

    Returns:
        包含两个键的字典:
        - 'str': ASCII 字符画形式的二维码
        - 'img': PIL.Image 对象形式的二维码图像

    Raises:
        ValueError: 当输入参数无效时抛出
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

    # 生成 ASCII 表示而不重定向 sys.stdout
    output = io.StringIO()
    qr.print_ascii(out=output, tty=False, invert=invert)
    output_str = output.getvalue()
    output.close()

    # 处理颜色反转
    if invert:
        # 将二维码图像转换为RGBA模式以便正确处理反转
        if img.mode == '1':
            img = img.convert('L')
        img = ImageOps.invert(img)

    return {"str": output_str, "img": img}


if __name__ == "__main__":
    t = "https://account.bilibili.com/h5/account-h5/auth/scan-web?navhide=1&callback=close&qrcode_key=a60221be32dc24d986208970ba129a19&from="
    # 示例用法
    result = qr_text8pil_img(t, invert=True)

    # 获取ASCII表示
    print(result["str"])

    # 获取PIL图像并显示
    result["img"].show()