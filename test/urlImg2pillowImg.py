import requests
from PIL import Image
from io import BytesIO


def url2pillowImage(url) -> Image.Image:
    """
    将url图片转换为pillow_image实例
    Args:
        url:
    Returns:pillow_image实例
    """
    try:
        # 添加请求头模拟浏览器访问，避免被拒绝
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        # 发送 GET 请求
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()  # 检查 HTTP 错误
        # 将响应内容转为字节流
        image_data = BytesIO(response.content)
        # 用 Pillow 打开图像
        img = Image.open(image_data)
        return img
    except requests.exceptions.RequestException as e:
        print(f"网络请求失败: {e}")
    except Exception as e:
        print(f"处理图像时出错: {e}")


# 使用示例
if __name__ == "__main__":
    image_url = "https://i0.hdslb.com/bfs/live/new_room_cover/855549723deed067b811577afbca531531b9dc31.jpg"
    pillow_img = url2pillowImage(image_url)

    if pillow_img:
        print("图像信息:")
        print(f"格式: {pillow_img.format}")
        print(f"尺寸: {pillow_img.size}")
        pillow_img.show()  # 显示图像（可选）
