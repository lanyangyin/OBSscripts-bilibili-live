import ssl
import requests
import urllib3
import subprocess
import tempfile
import os
import json
import time
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from urllib3.util import Retry

# 全局禁用所有 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 设置全局 SSL 上下文 - 完全禁用验证
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
ssl._create_default_https_context = lambda: ssl_context


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


def force_insecure_request(url, method='GET', headers=None, cookies=None,
                           data=None, json_data=None, files=None,
                           timeout=10, max_retries=3):
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
    max_retries (int): 最大重试次数

    返回:
    dict: 包含请求结果的字典，包含以下键:
        - 'status': 'success' 或 'error'
        - 'method_used': 'requests', 'urllib3' 或 'curl'
        - 'status_code': HTTP 状态码
        - 'content': 响应内容 (文本或二进制)
        - 'headers': 响应头
        - 'time_elapsed': 请求耗时 (秒)
        - 'error': 错误信息 (如果发生错误)
        - 'retries': 重试次数
    """
    start_time = time.time()
    result = {
        'status': 'error',
        'method_used': '',
        'status_code': 0,
        'content': None,
        'headers': {},
        'time_elapsed': 0,
        'error': '',
        'retries': 0
    }

    # 准备默认请求头
    if headers is None:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "*/*",
            "Connection": "keep-alive"
        }

    # 方法1: 使用自定义适配器的 requests 会话
    for attempt in range(max_retries):
        try:
            session = requests.Session()
            adapter = UniversalSSLAdapter()
            session.mount('https://', adapter)
            session.mount('http://', adapter)

            # 配置重试策略
            retry_strategy = Retry(
                total=0,  # 我们已经在外部循环中处理重试
                backoff_factor=0.5,
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=["GET", "POST", "PUT", "DELETE", "PATCH"]
            )
            session.mount('https://', HTTPAdapter(max_retries=retry_strategy))

            # 准备请求参数
            request_args = {
                "method": method.upper(),
                "url": url,
                "headers": headers,
                "cookies": cookies,
                "timeout": timeout,
                "verify": False
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

            # 执行请求
            response = session.request(**request_args)

            # 收集结果
            result.update({
                'status': 'success',
                'method_used': 'requests',
                'status_code': response.status_code,
                'content': response.content,
                'headers': dict(response.headers),
                'retries': attempt
            })
            return result

        except (requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
            result['error'] = f"Requests SSL/连接错误 (尝试 {attempt + 1}/{max_retries}): {str(e)}"
            result['retries'] = attempt + 1
            if attempt == max_retries - 1:
                break  # 跳出循环尝试其他方法
            time.sleep(0.5 * (attempt + 1))  # 指数退避

        except Exception as e:
            result['error'] = f"Requests 请求错误 (尝试 {attempt + 1}/{max_retries}): {str(e)}"
            result['retries'] = attempt + 1
            break

    # 方法2: 使用 urllib3
    try:
        http = urllib3.PoolManager(
            cert_reqs='CERT_NONE',
            assert_hostname=False,
            ssl_version=ssl.PROTOCOL_TLS,
            retries=False
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
        final_headers = headers.copy()
        if content_type:
            final_headers["Content-Type"] = content_type

        # 添加 cookies
        if cookies:
            cookie_str = "; ".join([f"{k}={v}" for k, v in cookies.items()])
            final_headers["Cookie"] = cookie_str

        # 执行请求
        response = http.request(
            method.upper(),
            url,
            body=body,
            headers=final_headers,
            timeout=timeout,
            retries=False
        )

        # 收集结果
        result.update({
            'status': 'success',
            'method_used': 'urllib3',
            'status_code': response.status,
            'content': response.data,
            'headers': dict(response.headers),
            'error': ''
        })
        return result

    except Exception as e:
        result['error'] = f"Urllib3 错误: {str(e)}"

    # 方法3: 使用系统命令 (curl)
    try:
        # 创建临时 cookie 文件
        cookie_file = None
        if cookies:
            cookie_file = tempfile.NamedTemporaryFile(delete=False)
            for k, v in cookies.items():
                cookie_file.write(f"{k}={v}\n".encode())
            cookie_file.close()

        # 准备 curl 命令
        cmd = ["curl", "-s", "-i", "-k", "-X", method.upper(), url]

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
            # 文件上传 - 只支持路径，不支持文件对象
            for field_name, file_info in files.items():
                if isinstance(file_info, tuple) and len(file_info) > 1:
                    file_path = file_info[0]
                elif isinstance(file_info, str):
                    file_path = file_info
                else:
                    continue
                cmd.extend(["-F", f"{field_name}=@{file_path}"])

        # 执行命令
        result_exec = subprocess.run(cmd, capture_output=True, timeout=timeout + 5)

        # 清理临时文件
        if cookie_file:
            os.unlink(cookie_file.name)

        # 解析 curl 响应
        output = result_exec.stdout.decode('utf-8', errors='ignore')

        # 分离头部和内容
        header_end = output.find("\r\n\r\n")
        if header_end == -1:
            header_end = output.find("\n\n")

        if header_end != -1:
            headers_str = output[:header_end]
            content = output[header_end + 4:]

            # 解析状态码
            status_line = headers_str.split("\n")[0]
            if "HTTP/" in status_line:
                status_parts = status_line.split(" ")
                if len(status_parts) >= 2:
                    result['status_code'] = int(status_parts[1])

            # 解析头部
            headers = {}
            for line in headers_str.split("\n")[1:]:
                if ":" in line:
                    key, value = line.split(":", 1)
                    headers[key.strip()] = value.strip()
        else:
            content = output
            result['status_code'] = 200 if result_exec.returncode == 0 else 500

        # 收集结果
        result.update({
            'status': 'success' if result_exec.returncode == 0 else 'error',
            'method_used': 'curl',
            'content': content,
            'headers': headers,
            'error': result_exec.stderr.decode('utf-8', errors='ignore') if result_exec.returncode != 0 else ''
        })
        return result

    except Exception as e:
        result['error'] = f"Curl 错误: {str(e)}"
        return result

    finally:
        # 确保计算耗时
        result['time_elapsed'] = time.time() - start_time


def test_ssl_bypass():
    """测试 SSL 绕过功能是否有效"""
    test_url = "https://api.bilibili.com/x/web-interface/nav"
    print("测试 SSL 绕过功能...")

    try:
        # 使用标准 requests 库（应该失败）
        try:
            requests.get(test_url, timeout=5, verify=False)
            print("标准请求成功 - 这可能表示问题已解决")
        except Exception as e:
            print(f"标准请求失败（预期）: {e}")

        # 使用我们的强制不安全请求
        response = force_insecure_request(test_url, timeout=10)
        print(f"强制不安全请求状态: {response['status_code']}")

        if response['status_code'] == 200:
            print("✅ SSL 绕过成功！")
            return True
        else:
            print(f"❌ 请求失败，状态码: {response['status_code']}")
            return False
    except Exception as e:
        print(f"❌ SSL 绕过测试失败: {e}")
        return False


# 在脚本初始化时调用测试
if __name__ == "__main__":
    test_ssl_bypass()