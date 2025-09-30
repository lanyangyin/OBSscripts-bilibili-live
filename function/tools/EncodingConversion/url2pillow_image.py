"""
这个文件包含一个名为 url2pillow_image 的函数，它的主要功能是从网络 URL 下载图像并将其转换为 Pillow 库的 Image 对象（PIL 图像）。

主要功能
    - 从 URL 下载图像：使用 HTTP 请求从指定的 URL 获取图像数据
    - 转换为 Pillow 图像对象：将下载的图像数据转换为 Pillow 库可以处理的图像对象
    - 完善的错误处理：处理各种可能的错误情况，包括网络错误和图像处理错误
    - 返回结构化结果：返回包含图像对象、状态码和消息的字典

核心特性
    1. 网络请求处理
        - 使用 requests 库发送 HTTP GET 请求
        - 支持自定义请求头（如 User-Agent），用于模拟浏览器访问
        - 使用流式传输（stream=True）处理大文件，避免内存溢出

    2. 图像处理
        - 使用 Pillow（PIL）库处理图像数据
        - 将字节流转换为 Pillow Image 对象
        - 显式调用 img.load() 确保图像完全加载

    3. 错误处理机制
        - 自定义错误码系统：
        - NETWORK_ERROR = 0：表示没有 HTTP 响应的网络错误
        - IMAGE_PROCESSING_ERROR = 1000：图像处理错误
        - 区分不同类型的异常：
        - requests.exceptions.RequestException：网络请求相关错误
        - 其他 Exception：图像处理相关错误

    4. 结构化返回结果
        - 函数返回一个包含三个键的字典：
        - PilImg：成功时为 Pillow 图像对象，失败时为 None
        - code：成功时为 HTTP 状态码，失败时为错误码
        - Message：描述性消息，成功时为 "Success"，失败时为错误信息
"""
from typing import Dict, Any

import requests
from PIL import Image
from io import BytesIO

# 自定义错误码
NETWORK_ERROR = 0  # 表示没有HTTP响应的网络错误
IMAGE_PROCESSING_ERROR = 1000  # 图像处理错误


def url2pillow_image(url: str, headers: Dict[str, str], verify_ssl: bool = True) -> Dict[str, Any]:
    """
    将url图片转换为 pillow_image 实例

    Args:
        url: 图片的网络直链
        headers: 请求头
        verify_ssl: 默认启用 SSL 验证

    Returns:
        字典包含:
        - 'PilImg': 成功时为Pillow图像对象，失败时为None
        - 'code': 成功时为HTTP状态码 200，失败时为HTTP状态码（如果有）或自定义错误码
        - 'Message': 成功时为"Success"，失败时为错误信息
    """
    try:
        with requests.get(url, headers=headers, stream=True, verify=verify_ssl) as response:
            response.raise_for_status()
            image_data = BytesIO()
            for chunk in response.iter_content(chunk_size=8192):
                image_data.write(chunk)
            image_data.seek(0)
            img = Image.open(image_data)
            img.load()
            return {
                "PilImg": img,
                "code": response.status_code,
                "Message": "Success"
            }
    except requests.exceptions.RequestException as e:
        # 如果有响应，则使用实际的状态码，否则使用自定义网络错误码
        if hasattr(e, 'response') and e.response is not None:
            status_code = e.response.status_code
        else:
            status_code = NETWORK_ERROR
        return {
            "PilImg": None,
            "code": status_code,
            "Message": f"HTTP请求错误: {str(e)}"
        }
    except Exception as e:
        return {
            "PilImg": None,
            "code": IMAGE_PROCESSING_ERROR,
            "Message": f"处理图像时出错: {str(e)}"
        }


# 使用示例
if __name__ == "__main__":
    ImageUrl = "http://i0.hdslb.com/bfs/live/new_room_cover/d3ee7db19eb3e526a874b075e40383033bb0f4d1.jpg"
    Headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    pillow_img = url2pillow_image(ImageUrl, Headers)
    print(pillow_img)
    pillow_img = pillow_img["PilImg"]
    if pillow_img:
        print("图像信息:")
        print(f"格式: {pillow_img.format}")
        print(f"尺寸: {pillow_img.size}")
        # pillow_img.show()  # 显示图像（可选）
        pillow_img.save("./TestOutput/url2pillow_image/Url2PillowImg.jpg")