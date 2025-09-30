class BilibiliApiGeneric:
    """
    不登录也能用的B站API
    """

    def __init__(self, headers, verify_ssl: bool = True):
        self.headers = headers
        self.verify_ssl = verify_ssl


if __name__ == "__main__":
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # 创建API实例
    api = BilibiliApiGeneric(headers)