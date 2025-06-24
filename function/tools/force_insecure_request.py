import ssl
import requests
import urllib3
import warnings
import json
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from urllib3.util import Retry

# 禁用所有 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore", category=UserWarning, module='urllib3')
warnings.filterwarnings("ignore", category=requests.packages.urllib3.exceptions.InsecureRequestWarning)

# 设置全局 SSL 上下文 - 完全禁用验证
try:
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    ssl._create_default_https_context = lambda: ssl_context
except Exception as e:
    print(f"全局 SSL 上下文设置失败: {e}")


class UniversalSSLAdapter(HTTPAdapter):
    """支持所有 HTTP 方法的自定义适配器"""

    def init_poolmanager(self, connections, maxsize, block=False, **pool_kwargs):
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_version=ssl.PROTOCOL_TLS,
            assert_hostname=False,
            cert_reqs=ssl.CERT_NONE
        )


def force_insecure_request(url, method='GET', headers=None, cookies=None, data=None, json_data=None, files=None,
                           timeout=10):
    """
    强制进行不安全的 HTTP 请求，完全绕过 SSL 验证，支持所有 HTTP 方法

    参数:
    url (str): 请求的 URL
    method (str): HTTP 方法 (GET, POST, PUT, DELETE 等)
    headers (dict): 请求头
    cookies (dict): cookies
    data (dict/str): 表单数据
    json_data (dict): JSON 数据
    files (dict): 文件上传
    timeout (int): 超时时间（秒）

    返回:
    requests.Response: 响应对象
    """
    # 创建自定义会话
    session = requests.Session()

    # 使用自定义适配器完全禁用 SSL 验证
    adapter = UniversalSSLAdapter()
    session.mount('https://', adapter)
    session.mount('http://', adapter)

    # 配置重试策略
    retry_strategy = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST", "PUT", "DELETE", "PATCH"]
    )
    session.mount('https://', HTTPAdapter(max_retries=retry_strategy))

    # 设置默认请求头
    if headers is None:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive"
        }

    # 准备请求参数
    request_args = {
        "method": method.upper(),
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": timeout,
        "verify": False  # 双重确认禁用验证
    }

    # 根据请求类型添加数据
    if json_data is not None:
        request_args["json"] = json_data
        if "Content-Type" not in headers:
            headers["Content-Type"] = "application/json"
    elif data is not None:
        request_args["data"] = data
    if files is not None:
        request_args["files"] = files

    try:
        # 执行请求
        response = session.request(**request_args)
        return response
    except requests.exceptions.SSLError as e:
        # 如果仍然出现 SSL 错误，尝试更底层的解决方案
        return fallback_request(url, method, headers, cookies, data, json_data, files, timeout)
    except Exception as e:
        raise Exception(f"强制不安全请求失败: {e}") from e


def fallback_request(url, method='GET', headers=None, cookies=None, data=None, json_data=None, files=None, timeout=10):
    """使用更底层的解决方案进行请求"""
    try:
        # 尝试使用 urllib3 直接请求
        http = urllib3.PoolManager(
            cert_reqs='CERT_NONE',
            assert_hostname=False,
            ssl_version=ssl.PROTOCOL_TLS,
            retries=urllib3.Retry(3, backoff_factor=0.5)
        )

        # 准备请求体
        body = None
        content_type = None

        if json_data is not None:
            body = json.dumps(json_data).encode('utf-8')
            content_type = "application/json"
        elif data is not None:
            if isinstance(data, dict):
                body = urllib3.encode_multipart_formdata(data)[0]
                content_type = "multipart/form-data"
            else:
                body = data.encode('utf-8') if isinstance(data, str) else data
        elif files is not None:
            fields = files.copy()
            if data:
                fields.update(data)
            body, content_type = urllib3.encode_multipart_formdata(fields)

        # 设置请求头
        headers = headers or {}
        if content_type:
            headers["Content-Type"] = content_type

        # 添加 cookies
        if cookies:
            cookie_str = "; ".join([f"{k}={v}" for k, v in cookies.items()])
            headers["Cookie"] = cookie_str

        # 执行请求
        response = http.request(
            method.upper(),
            url,
            body=body,
            headers=headers,
            timeout=timeout
        )

        # 转换为 requests 兼容的响应对象
        resp = requests.Response()
        resp.status_code = response.status
        resp.headers = response.headers
        resp._content = response.data
        return resp
    except Exception as e:
        # 最终回退方案 - 使用系统命令
        return system_fallback_request(url, method, headers, cookies, data, json_data, files, timeout)


def system_fallback_request(url, method='GET', headers=None, cookies=None, data=None, json_data=None, files=None,
                            timeout=10):
    """使用系统命令进行请求（最终回退方案）"""
    import subprocess
    import json
    import tempfile
    import os

    try:
        # 创建临时 cookie 文件
        cookie_file = None
        if cookies:
            cookie_file = tempfile.NamedTemporaryFile(delete=False)
            for k, v in cookies.items():
                cookie_file.write(f"{k}={v}\n".encode())
            cookie_file.close()

        # 准备 curl 命令
        cmd = ["curl", "-s", "-k", "-X", method.upper(), url]

        # 添加超时
        if timeout:
            cmd.extend(["--max-time", str(timeout)])

        # 添加 cookie 文件
        if cookie_file:
            cmd.extend(["-b", cookie_file.name])

        # 添加 headers
        if headers:
            for k, v in headers.items():
                cmd.extend(["-H", f"{k}: {v}"])

        # 添加数据
        if json_data is not None:
            data_str = json.dumps(json_data)
            cmd.extend(["--data-raw", data_str])
            cmd.extend(["-H", "Content-Type: application/json"])
        elif data is not None:
            if isinstance(data, dict):
                # 表单数据
                form_items = [f"{k}={v}" for k, v in data.items()]
                cmd.extend(["--data", "&".join(form_items)])
            else:
                # 原始数据
                cmd.extend(["--data", data])
        elif files is not None:
            # 文件上传
            for field_name, (file_path, file_obj, content_type) in files.items():
                if hasattr(file_obj, 'read'):
                    # 如果是文件对象，保存到临时文件
                    temp_file = tempfile.NamedTemporaryFile(delete=False)
                    temp_file.write(file_obj.read())
                    temp_file.close()
                    file_path = temp_file.name
                cmd.extend(["-F", f"{field_name}=@{file_path}"])

        # 执行命令
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 5)

        # 清理临时文件
        if cookie_file:
            os.unlink(cookie_file.name)

        # 创建模拟响应对象
        resp = requests.Response()
        resp.status_code = 200 if result.returncode == 0 else 500
        resp._content = result.stdout.encode()
        resp.headers = {}
        return resp
    except Exception as e:
        raise Exception(f"系统回退请求失败: {e}") from e


def test_ssl_bypass():
    """测试 SSL 绕过功能是否有效"""
    test_url = "https://api.bilibili.com/x/web-interface/nav"
    print("测试 SSL 绕过功能...")

    try:
        # 使用标准 requests 库（应该失败）
        try:
            requests.get(test_url, timeout=5)
            print("标准请求成功 - 这可能表示问题已解决")
        except Exception as e:
            print(f"标准请求失败（预期）: {e}")

        # 使用我们的强制不安全请求
        response = force_insecure_request(test_url, timeout=10)
        print(f"强制不安全请求状态: {response.status_code}")

        if response.status_code == 200:
            print("✅ SSL 绕过成功！")
            return True
        else:
            print(f"❌ 请求失败，状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ SSL 绕过测试失败: {e}")
        return False


# 在脚本初始化时调用测试
if __name__ == "__main__":
    test_ssl_bypass()