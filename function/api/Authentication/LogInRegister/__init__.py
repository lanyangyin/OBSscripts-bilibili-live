from typing import Dict, Any

import requests


class BilibiliLogInRegister:
    """
    B站登录注册相关API
    """

    def __init__(self, headers: Dict[str, str], verify_ssl: bool = True):
        """
        初始化登录注册管理器

        Args:
            headers: 请求头字典
            verify_ssl: 是否验证SSL证书
        """
        self.headers = headers
        self.verify_ssl = verify_ssl


# 使用示例
if __name__ == "__main__":
    # 创建请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # 创建登录注册实例
    login_register = BilibiliLogInRegister(headers, verify_ssl=True)