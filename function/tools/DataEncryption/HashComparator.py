import hashlib
import base64
import hmac
from typing import Optional, Dict, Any
from enum import Enum


class HashAlgorithm(Enum):
    """支持的哈希算法枚举"""
    MD5 = "md5"
    SHA1 = "sha1"
    SHA256 = "sha256"
    SHA512 = "sha512"
    BLAKE2B = "blake2b"
    BLAKE2S = "blake2s"
    SHA3_256 = "sha3_256"
    SHA3_512 = "sha3_512"


class HashComparator:
    """
    哈希编码和哈希字符比对类

    提供多种哈希算法的编码功能，以及哈希值与原始字符串的比对验证。

    Attributes:
        algorithm (HashAlgorithm): 使用的哈希算法
        encoding (str): 编码格式，默认为 'utf-8'
        output_format (str): 输出格式，'hex' 或 'base64'
    """

    def __init__(self,
                 algorithm: HashAlgorithm = HashAlgorithm.SHA256,
                 encoding: str = 'utf-8',
                 output_format: str = 'hex'):
        """
        初始化哈希比较器

        Args:
            algorithm: 哈希算法，默认为 SHA256
            encoding: 字符串编码格式，默认为 'utf-8'
            output_format: 输出格式，'hex' 或 'base64'
        """
        self.algorithm = algorithm
        self.encoding = encoding
        self.output_format = output_format

        # 验证参数
        if output_format not in ['hex', 'base64']:
            raise ValueError("输出格式必须是 'hex' 或 'base64'")

    def hash_string(self, text: str, salt: Optional[str] = None) -> str:
        """
        对字符串进行哈希编码

        Args:
            text: 要哈希的原始字符串
            salt: 可选的盐值，用于增强安全性

        Returns:
            哈希后的字符串
        """
        # 将字符串编码为字节
        text_bytes = text.encode(self.encoding)

        # 如果有盐值，添加盐值
        if salt:
            salt_bytes = salt.encode(self.encoding)
            if self.algorithm.value in hashlib.algorithms_available:
                # 使用hmac进行加盐哈希
                hmac_obj = hmac.new(salt_bytes, text_bytes, getattr(hashlib, self.algorithm.value))
                hash_bytes = hmac_obj.digest()
            else:
                raise ValueError(f"不支持的哈希算法: {self.algorithm.value}")
        else:
            # 普通哈希
            hash_obj = hashlib.new(self.algorithm.value)
            hash_obj.update(text_bytes)
            hash_bytes = hash_obj.digest()

        # 根据输出格式转换
        if self.output_format == 'hex':
            return hash_bytes.hex()
        else:  # base64
            return base64.b64encode(hash_bytes).decode(self.encoding)

    def verify_hash(self, original_text: str, hash_value: str, salt: Optional[str] = None) -> bool:
        """
        验证原始字符串与哈希值是否匹配

        Args:
            original_text: 原始字符串
            hash_value: 要比较的哈希值
            salt: 可选的盐值，必须与生成哈希时使用的盐值相同

        Returns:
            bool: 如果匹配返回 True，否则返回 False
        """
        try:
            # 重新计算原始字符串的哈希
            computed_hash = self.hash_string(original_text, salt)

            # 安全比较哈希值，避免时序攻击
            return self._secure_compare(computed_hash, hash_value)
        except Exception:
            return False

    def _secure_compare(self, a: str, b: str) -> bool:
        """
        安全字符串比较，避免时序攻击

        Args:
            a: 第一个字符串
            b: 第二个字符串

        Returns:
            bool: 如果字符串相等返回 True
        """
        if len(a) != len(b):
            return False

        result = 0
        for x, y in zip(a, b):
            result |= ord(x) ^ ord(y)
        return result == 0

    def get_hash_info(self, text: str, salt: Optional[str] = None) -> Dict[str, Any]:
        """
        获取字符串的哈希信息

        Args:
            text: 要哈希的字符串
            salt: 可选的盐值

        Returns:
            包含哈希信息的字典
        """
        hash_value = self.hash_string(text, salt)

        return {
            'algorithm': self.algorithm.value,
            'original_text': text,
            'hash_value': hash_value,
            'output_format': self.output_format,
            'encoding': self.encoding,
            'salt_used': salt is not None,
            'hash_length': len(hash_value)
        }

    def compare_multiple(self,
                         original_text: str,
                         hash_values: list,
                         salt: Optional[str] = None) -> Dict[str, bool]:
        """
        比较原始字符串与多个哈希值的匹配情况

        Args:
            original_text: 原始字符串
            hash_values: 要比较的哈希值列表
            salt: 可选的盐值

        Returns:
            字典，键为哈希值，值为是否匹配的布尔值
        """
        results = {}
        for hash_val in hash_values:
            results[hash_val] = self.verify_hash(original_text, hash_val, salt)
        return results

    def change_algorithm(self, new_algorithm: HashAlgorithm):
        """
        更改哈希算法

        Args:
            new_algorithm: 新的哈希算法
        """
        self.algorithm = new_algorithm

    def change_output_format(self, new_format: str):
        """
        更改输出格式

        Args:
            new_format: 新的输出格式，'hex' 或 'base64'
        """
        if new_format not in ['hex', 'base64']:
            raise ValueError("输出格式必须是 'hex' 或 'base64'")
        self.output_format = new_format

    @classmethod
    def get_available_algorithms(cls) -> list:
        """
        获取系统可用的哈希算法列表

        Returns:
            可用的哈希算法名称列表
        """
        return sorted(hashlib.algorithms_available)

    @staticmethod
    def quick_hash(text: str,
                   algorithm: HashAlgorithm = HashAlgorithm.SHA256,
                   output_format: str = 'hex') -> str:
        """
        快速哈希方法（静态方法）

        Args:
            text: 要哈希的字符串
            algorithm: 哈希算法
            output_format: 输出格式

        Returns:
            哈希后的字符串
        """
        comparator = HashComparator(algorithm, output_format=output_format)
        return comparator.hash_string(text)

    @staticmethod
    def quick_verify(original_text: str,
                     hash_value: str,
                     algorithm: HashAlgorithm = HashAlgorithm.SHA256,
                     output_format: str = 'hex') -> bool:
        """
        快速验证方法（静态方法）

        Args:
            original_text: 原始字符串
            hash_value: 哈希值
            algorithm: 哈希算法
            output_format: 输出格式

        Returns:
            bool: 如果匹配返回 True
        """
        comparator = HashComparator(algorithm, output_format=output_format)
        return comparator.verify_hash(original_text, hash_value)

    def __repr__(self) -> str:
        return f"<HashComparator algorithm={self.algorithm.value} format={self.output_format}>"


# 使用示例和测试
if __name__ == "__main__":
    from _Input.DataEncryption import HashComparator as HashComparator_c
    # 创建哈希比较器实例
    comparator = HashComparator(HashAlgorithm.SHA256)

    # 基本使用示例
    text = HashComparator_c.text
    hashed = comparator.hash_string(text)
    print(f"原始文本: {text}")
    print(f"哈希值: {hashed}")
    print(f"验证结果: {comparator.verify_hash(text, hashed)}")
    print()

    # 使用盐值
    salt = "my_salt"
    hashed_with_salt = comparator.hash_string(text, salt)
    print(f"加盐哈希: {hashed_with_salt}")
    print(f"加盐验证: {comparator.verify_hash(text, hashed_with_salt, salt)}")
    print(f"错误盐值验证: {comparator.verify_hash(text, hashed_with_salt, 'wrong_salt')}")
    print()

    # 获取哈希信息
    info = comparator.get_hash_info(text, salt)
    print("哈希信息:")
    for key, value in info.items():
        print(f"  {key}: {value}")
    print()

    # 比较多个哈希值
    hash_list = [
        hashed_with_salt,
        "wrong_hash_value",
        comparator.hash_string("different_text", salt)
    ]
    results = comparator.compare_multiple(text, hash_list, salt)
    print("多哈希比较结果:")
    for hash_val, match in results.items():
        print(f"  {hash_val}: {'匹配' if match else '不匹配'}")
    print()

    # 更改算法
    comparator.change_algorithm(HashAlgorithm.MD5)
    md5_hash = comparator.hash_string(text)
    print(f"MD5 哈希: {md5_hash}")
    print()

    # 使用base64输出格式
    comparator.change_output_format('base64')
    base64_hash = comparator.hash_string(text)
    print(f"Base64 格式哈希: {base64_hash}")
    print()

    # 静态方法使用
    quick_hash = HashComparator.quick_hash(text, HashAlgorithm.SHA512)
    print(f"快速哈希: {quick_hash}")

    is_valid = HashComparator.quick_verify(text, quick_hash, HashAlgorithm.SHA512)
    print(f"快速验证: {is_valid}")
    print()

    # 查看可用算法
    algorithms = HashComparator.get_available_algorithms()
    print(f"可用哈希算法: {algorithms[:5]}...")  # 只显示前5个