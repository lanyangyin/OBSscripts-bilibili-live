import hashlib
import time
from collections import OrderedDict


class OptimizedMessageDeduplication:
    """优化的消息去重类"""

    def __init__(self, max_size: int = 1000, ttl_seconds: int = 5):
        """
        Args:
            max_size: 最大存储数量
            ttl_seconds: 消息存活时间（秒），None表示不过期
        """
        self.max_size = max_size
        """最大存储数量"""
        self.ttl_seconds = ttl_seconds
        """消息存活时间（秒），None表示不过期"""
        # 使用OrderedDict同时维护顺序和快速查找
        self.message_store = OrderedDict()  # {hash: timestamp}

    def add(self, message: str) -> bool:
        """添加消息，返回True如果是新消息"""
        message_hash = self._get_hash(message)
        current_time = time.time()

        # 清理过期消息
        if self.ttl_seconds:
            self._cleanup_expired(current_time)

        # 检查是否重复
        if message_hash in self.message_store:
            # 更新访问时间
            self.message_store.move_to_end(message_hash)
            return False

        # 添加新消息
        self.message_store[message_hash] = current_time

        # 限制大小
        if len(self.message_store) > self.max_size:
            self.message_store.popitem(last=False)

        return True

    def contains(self, message: str) -> bool:
        """检查消息是否重复"""
        message_hash = self._get_hash(message)

        if self.ttl_seconds:
            self._cleanup_expired(time.time())

        return message_hash in self.message_store

    def _get_hash(self, message: str) -> str:
        """获取消息哈希（使用更快的哈希算法）"""
        return hashlib.md5(message.encode()).hexdigest()
        # 或者使用更快的：return hashlib.sha1(message.encode()).hexdigest()

    def _cleanup_expired(self, current_time: float):
        """清理过期消息"""
        expired_hashes = []

        for msg_hash, timestamp in self.message_store.items():
            if current_time - timestamp > self.ttl_seconds:
                expired_hashes.append(msg_hash)
            else:
                break  # 由于是有序的，后面的都不会过期

        for msg_hash in expired_hashes:
            del self.message_store[msg_hash]

    def size(self) -> int:
        """返回当前消息数量"""
        if self.ttl_seconds:
            self._cleanup_expired(time.time())
        return len(self.message_store)

    def clear(self):
        """清空所有消息"""
        self.message_store.clear()

    def get_memory_usage(self) -> int:
        """估算内存使用（字节）"""
        # 每个条目大约：哈希(32字节) + 时间戳(8字节) + 字典开销
        return len(self.message_store) * 50  # 近似值
