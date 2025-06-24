import ssl
import urllib3
import requests
from requests.exceptions import SSLError


def check_ssl_verification(test_url="https://api.bilibili.com", timeout=5):
    """
    检测 SSL 证书验证是否可用

    参数:
    test_url (str): 用于测试的 URL（默认为 Bilibili API）
    timeout (int): 测试请求的超时时间（秒）

    返回:
    tuple: (verify_ssl: bool, warning: str)
        verify_ssl: 是否启用 SSL 验证
        warning: 警告信息（如果存在问题）
    """
    # 默认启用 SSL 验证
    verify_ssl = True
    warning = ""

    try:
        # 尝试使用 SSL 验证进行请求
        response = requests.head(
            test_url,
            timeout=timeout,
            verify=True  # 强制启用验证
        )

        # 检查响应状态
        if response.status_code >= 400:
            warning = f"测试请求返回错误状态: {response.status_code}"

    except SSLError as e:
        # 捕获 SSL 验证错误
        verify_ssl = False
        warning = f"SSL 验证失败: {e}\n已禁用 SSL 证书验证（可能存在安全风险）"

        # 禁用 SSL 验证警告
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    except requests.exceptions.RequestException as e:
        # 其他网络错误
        verify_ssl = False
        warning = f"网络请求错误: {e}\n已禁用 SSL 证书验证（可能存在安全风险）"

    except Exception as e:
        # 其他未知错误
        verify_ssl = False
        warning = f"未知错误: {e}\n已禁用 SSL 证书验证（可能存在安全风险）"

    # 如果验证失败，配置全局 SSL 上下文
    if not verify_ssl:
        try:
            ssl._create_default_https_context = ssl._create_unverified_context
        except Exception as e:
            warning += f"\n配置全局 SSL 上下文失败: {e}"

    return verify_ssl, warning

# 执行 SSL 检测
verify_ssl, ssl_warning = check_ssl_verification()

# 如果存在警告，打印到控制台
if ssl_warning:
    print(f"[SSL 警告] {ssl_warning}")