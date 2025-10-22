from PIL import Image
import io
import zlib


class StegoImageText:
    def __init__(self):
        # 创建一个10x10像素的基础PNG图像
        self.minimal_png = None

    def text_to_image(self, text, output_path):
        """
        将文本加密为10x10像素的伪装图片文件

        Args:
            text: 要隐藏的文本内容
            output_path: 输出的图片文件路径
        """
        # 将文本编码为字节并压缩
        text_bytes = text.encode('utf-8')
        compressed_text = zlib.compress(text_bytes)

        # 创建10x10像素的PNG图像
        img = Image.new('RGB', (10, 10), (240, 240, 240))  # 浅灰色背景

        # 在图像中添加一些随机像素点，使其看起来更像真实图片
        pixels = img.load()
        for i in range(10):
            for j in range(10):
                if (i + j) % 7 == 0:  # 添加一些随机像素
                    pixels[i, j] = (200, 200, 200)

        # 将图像保存到内存缓冲区
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG', optimize=True)
        img_data = img_buffer.getvalue()

        # 将压缩后的文本数据追加到图像数据之后
        # 使用特定分隔符标记文本数据的开始
        separator = b'%%TEXT_DATA%%'
        combined_data = img_data + separator + compressed_text

        # 保存到文件
        with open(output_path, 'wb') as f:
            f.write(combined_data)

        return True

    def file_to_image(self, input_file_path, output_image_path):
        """
        从文本文件读取内容并加密为10x10像素的伪装图片文件

        Args:
            input_file_path: 输入的文本文件路径
            output_image_path: 输出的图片文件路径
        """
        # 读取文本文件内容
        try:
            with open(input_file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            raise ValueError(f"无法读取文本文件: {e}")

        # 使用text_to_image方法创建伪装图片
        return self.text_to_image(text, output_image_path)

    def image_to_text(self, image_path):
        """
        从伪装的图片文件中提取文本

        Args:
            image_path: 图片文件路径

        Returns:
            提取的文本内容
        """
        with open(image_path, 'rb') as f:
            data = f.read()

        # 查找分隔符位置
        separator = b'%%TEXT_DATA%%'
        sep_pos = data.find(separator)

        if sep_pos == -1:
            raise ValueError("未找到文本数据，文件可能不是有效的伪装图片")

        # 提取文本数据部分
        compressed_text = data[sep_pos + len(separator):]

        # 解压缩并解码文本
        try:
            text_bytes = zlib.decompress(compressed_text)
            text = text_bytes.decode('utf-8')
        except (zlib.error, UnicodeDecodeError):
            raise ValueError("无法解码文本数据，文件可能已损坏")

        return text

    def image_to_file(self, image_path, output_file_path):
        """
        从伪装的图片文件中提取文本并保存到文件

        Args:
            image_path: 图片文件路径
            output_file_path: 输出的文本文件路径
        """
        # 提取文本
        text = self.image_to_text(image_path)

        # 保存到文件
        try:
            with open(output_file_path, 'w', encoding='utf-8') as f:
                f.write(text)
            return True
        except Exception as e:
            raise ValueError(f"无法保存文本到文件: {e}")

    def create_minimal_image(self, output_path, text=None, input_file_path=None):
        """
        创建一个极简的10x10像素图像，并将文本隐藏在文件末尾

        Args:
            output_path: 输出的图片文件路径
            text: 要隐藏的文本内容（可选）
            input_file_path: 包含要隐藏文本的文件路径（可选）
        """
        # 确定文本来源
        if input_file_path:
            try:
                with open(input_file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
            except Exception as e:
                raise ValueError(f"无法读取文本文件: {e}")
        elif text is None:
            raise ValueError("必须提供文本内容或文件路径")

        # 创建最简单的10x10像素PNG图像
        width, height = 10, 10
        img = Image.new('RGB', (width, height), (255, 255, 255))  # 白色背景

        # 添加几个像素点使图片看起来更自然
        pixels = img.load()
        pixels[0, 0] = (200, 200, 200)
        pixels[5, 5] = (200, 200, 200)
        pixels[9, 9] = (200, 200, 200)

        # 将文本编码为字节并压缩
        text_bytes = text.encode('utf-8')
        compressed_text = zlib.compress(text_bytes)

        # 将图像保存到内存缓冲区
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG', optimize=True)
        img_data = img_buffer.getvalue()

        # 将压缩后的文本数据追加到图像数据之后
        separator = b'%%TEXT_DATA%%'
        combined_data = img_data + separator + compressed_text

        # 保存到文件
        with open(output_path, 'wb') as f:
            f.write(combined_data)

        return True


# 使用示例
if __name__ == "__main__":
    from _Input.function.tools.DataEncryption import StegoImageText as StegoImageText_c
    stego = StegoImageText()

    # 示例1: 直接使用文本创建伪装图片
    stego.text_to_image(StegoImageText_c.in_secret_text1, StegoImageText_c.out_secret_text1)
    print(f"文本已加密为10x10图片: {StegoImageText_c.out_secret_text1}")

    # 示例2: 从文本文件创建伪装图片
    stego.file_to_image(StegoImageText_c.in_txt1_path, StegoImageText_c.out_txt1_path)
    print(f"文本文件内容已加密为图片: {StegoImageText_c.out_txt1_path}")

    # 示例3: 从图片提取文本到文件
    stego.image_to_file(StegoImageText_c.in_img1_path, StegoImageText_c.out_img1_path)
    print(f"从图片提取的文本已保存到: {StegoImageText_c.out_img1_path}")

    # 示例4: 使用极简方法从文件创建图片
    stego.create_minimal_image(StegoImageText_c.out_txt2_path, input_file_path=StegoImageText_c.in_txt2_path)
    print(f"使用极简方法从文件创建图片: {StegoImageText_c.out_txt2_path}")

    # 验证提取的文本
    try:
        recovered_text = stego.image_to_text(StegoImageText_c.out_txt2_path)
        print("从图片中提取的文本:", recovered_text)  # [:50] + "..." if len(recovered_text) > 50 else recovered_text
    except Exception as e:
        print("解密失败:", e)
