from typing import Dict


class ImproveCookies:
    def __init__(self, headers: Dict[str, str], verify_ssl: bool = True):
        """完善浏览器headers"""
        self.headers = headers
        self.verify_ssl = verify_ssl




if __name__ == "__main__":
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # 创建API实例
    api = ImproveCookies(headers)