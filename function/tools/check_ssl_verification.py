"""
check_ssl_verification 函数是一个专业的 SSL/TLS 证书验证检测工具，它检查系统是否能够正确验证 SSL 证书，并以结构化的方式返回检测结果。

主要功能
    - SSL 证书验证检测：测试系统是否能够正确验证 SSL 证书
    - 错误分类与处理：区分不同类型的 SSL 和网络错误
    - 自适应配置：在证书验证失败时自动禁用验证并配置全局 SSL 上下文
    - 结构化数据返回：返回包含详细信息的字典，而不是简单的布尔值
检测策略
    1. SSL 验证测试
        - 向指定的测试 URL 发送 HEAD 请求（默认为 Bilibili API）
        - 强制启用 SSL 证书验证（verify=True）
        - 捕获可能发生的 SSL 验证错误
    2. 错误处理与分类
        - 区分 SSL 证书错误、网络错误和其他未知错误
        - 使用预定义的错误码对不同类型的错误进行分类
    3. 自适应配置
        - 当 SSL 验证失败时，自动禁用 SSL 验证警告
        - 配置全局 SSL 上下文为不验证模式，确保后续请求不会失败
返回值结构
    - 函数返回一个包含四个键的字典：
        - success (布尔值)
            - True: SSL 验证成功
            - False: SSL 验证失败
        - code (整数)
            - 使用预定义的错误码常量：
                - SSL_VERIFICATION_SUCCESS = 0: SSL 验证成功
                - SSL_CERTIFICATE_ERROR = 1: SSL 证书错误
                - SSL_NETWORK_ERROR = 2: 网络错误
                - SSL_UNKNOWN_ERROR = 3: 未知错误
        - data (字典)
            - 包含详细的检测信息：
                - test_url: 用于测试的 URL
                - timeout: 测试超时时间
                - status_code: HTTP 响应状态码（如果有）
                - ssl_verification_enabled: SSL 验证是否启用
                - ssl_context_modified: 是否修改了全局 SSL 上下文
        - message (字符串)
            - 描述 SSL 验证状态或错误信息的可读消息
"""
import ssl
import urllib3
import requests
from requests.exceptions import SSLError

# 定义错误码
SSL_VERIFICATION_SUCCESS = 0
SSL_CERTIFICATE_ERROR = 1
SSL_NETWORK_ERROR = 2
SSL_UNKNOWN_ERROR = 3


def check_ssl_verification(test_url="https://api.bilibili.com", timeout=5):
    """
    检测 SSL 证书验证是否可用

    参数:
    test_url (str): 用于测试的 URL（默认为 Bilibili API）
    timeout (int): 测试请求的超时时间（秒）

    返回:
    dict: 包含以下键的字典:
        - 'success': bool, SSL 验证是否成功
        - 'code': int, 错误码
        - 'data': dict, 包含测试URL、响应状态码等详细信息
        - 'message': str, 描述性消息
    """
    result = {
        'success': True,
        'code': SSL_VERIFICATION_SUCCESS,
        'data': {
            'test_url': test_url,
            'timeout': timeout,
            'status_code': None,
            'ssl_verification_enabled': True
        },
        'message': 'SSL 证书验证正常'
    }

    try:
        # 尝试使用 SSL 验证进行请求
        response = requests.head(
            test_url,
            timeout=timeout,
            verify=True  # 强制启用验证
        )

        # 记录响应状态码
        result['data']['status_code'] = response.status_code

        # 检查响应状态
        if response.status_code >= 400:
            result['success'] = False
            result['code'] = SSL_NETWORK_ERROR
            result['message'] = f"测试请求返回错误状态: {response.status_code}"

    except SSLError as e:
        # 捕获 SSL 验证错误
        result['success'] = False
        result['code'] = SSL_CERTIFICATE_ERROR
        result['data']['ssl_verification_enabled'] = False
        result['message'] = f"SSL 证书验证失败: {str(e)}"

        # 禁用 SSL 验证警告
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # 配置全局 SSL 上下文为不验证
        try:
            ssl._create_default_https_context = ssl._create_unverified_context
            result['data']['ssl_context_modified'] = True
        except Exception as context_error:
            result['data']['ssl_context_modified'] = False
            result['message'] += f"。配置全局 SSL 上下文失败: {str(context_error)}"

    except requests.exceptions.RequestException as e:
        # 其他网络错误
        result['success'] = False
        result['code'] = SSL_NETWORK_ERROR
        result['data']['ssl_verification_enabled'] = False
        result['message'] = f"网络请求错误: {str(e)}"

    except Exception as e:
        # 其他未知错误
        result['success'] = False
        result['code'] = SSL_UNKNOWN_ERROR
        result['data']['ssl_verification_enabled'] = False
        result['message'] = f"未知错误: {str(e)}"

    return result


if __name__ == "__main__":
    # 执行 SSL 检测
    ssl_result = check_ssl_verification()
    print(ssl_result)