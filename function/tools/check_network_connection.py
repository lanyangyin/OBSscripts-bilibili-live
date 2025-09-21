"""
check_network_connection 函数是一个专业的网络连通性检测工具，它通过多种方式检查设备是否能够访问互联网，并以结构化的方式返回检测结果。

主要功能
    - 多层次网络检测：使用三种不同的方法检测网络连接状态
    - 结构化数据返回：返回包含详细信息的字典，而不是简单的布尔值
    - 无副作用设计：函数内部没有任何 print 语句，纯粹返回数据
    - 错误分类系统：使用预定义的错误码对不同类型的网络问题进行分类

检测策略
    1. DNS 连接检查（首选方法）
        - 尝试连接到 Google 的公共 DNS 服务器（8.8.8.8:53）
        - 这是最快的方法，通常能最先确定网络是否连通
        - 测量连接延迟，提供网络质量指标
    2. 多服务提供商检查（次要方法）
        - 尝试连接多个知名互联网公司的服务端点
        - 包括 Google、Apple、Microsoft、Cloudflare 等提供的连接检测服务
        - 使用 HEAD 请求减少数据传输量，提高检测效率
    3. 基本 HTTP 连接检查（备用方法）
        - 作为最后的手段，尝试连接到标准的 example.com
        - 这是一个简单但可靠的网络连通性测试

返回值结构
    函数返回一个包含四个键的字典：
        - connected (布尔值)
        - True: 网络连接正常
        - False: 网络连接失败
        - code (整数)
            - 使用预定义的错误码常量：
                - NETWORK_CONNECTION_SUCCESS = 0: 连接成功
                - NETWORK_DNS_FAILED = 1: DNS 连接失败
                - NETWORK_ALL_SERVICES_FAILED = 2: 所有服务连接尝试失败
                - NETWORK_HTTP_FAILED = 3: HTTP 连接失败
        - data (字典)
            - 包含详细的检测信息：
                - dns_checked: 是否进行了 DNS 检查
                - services_checked: 所有尝试过的服务及其结果的列表
                - successful_service: 成功连接的服务提供商（如果有）
                - latency_ms: 连接延迟（毫秒）
                - message (字符串)
                    - 描述网络状态或错误信息的可读消息
"""
import socket
import urllib.request
from urllib.error import URLError
import time

# 定义错误码
NETWORK_CONNECTION_SUCCESS = 0
"网络连接成功"
NETWORK_DNS_FAILED = 1
"DNS 连接失败"
NETWORK_ALL_SERVICES_FAILED = 2
"所有服务连接尝试失败"
NETWORK_HTTP_FAILED = 3
"HTTP 连接失败"


def check_network_connection():
    """
    检查网络连接，通过多个服务提供者的链接验证

    Returns:
        dict: 包含以下键的字典:
            - 'connected': bool, 网络是否连通
            - 'code': int, 错误码 (0表示成功)
            - 'data': dict, 包含详细信息如延迟、使用的服务等
            - 'message': str, 描述性消息
    """
    result = {
        'connected': False,
        'code': NETWORK_ALL_SERVICES_FAILED,
        'data': {
            'dns_checked': False,
            'services_checked': [],
            'successful_service': None,
            'latency_ms': None
        },
        'message': '所有连接尝试均失败'
    }

    # 1. 首先尝试快速DNS连接检查
    try:
        start_time = time.time()
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        elapsed = (time.time() - start_time) * 1000

        result['connected'] = True
        result['code'] = NETWORK_CONNECTION_SUCCESS
        result['data']['dns_checked'] = True
        result['data']['latency_ms'] = elapsed
        result['data']['successful_service'] = 'DNS (8.8.8.8:53)'
        result['message'] = f'DNS连接成功，延迟: {elapsed:.2f}ms'

        return result
    except OSError as e:
        result['code'] = NETWORK_DNS_FAILED
        result['message'] = f'DNS连接失败: {str(e)}'
        # 继续尝试其他方法

    # 2. 尝试多个服务提供者的链接
    test_services = [
        {"url": "http://www.gstatic.com/generate_204", "provider": "Google"},
        {"url": "http://www.google-analytics.com/generate_204", "provider": "Google"},
        {"url": "http://connectivitycheck.gstatic.com/generate_204", "provider": "Google"},
        {"url": "http://captive.apple.com", "provider": "Apple"},
        {"url": "http://www.msftconnecttest.com/connecttest.txt", "provider": "Microsoft"},
        {"url": "http://cp.cloudflare.com/", "provider": "Cloudflare"},
        {"url": "http://detectportal.firefox.com/success.txt", "provider": "Firefox"},
        {"url": "http://www.v2ex.com/generate_204", "provider": "V2ex"},
        {"url": "http://connect.rom.miui.com/generate_204", "provider": "小米"},
        {"url": "http://connectivitycheck.platform.hicloud.com/generate_204", "provider": "华为"},
        {"url": "http://wifi.vivo.com.cn/generate_204", "provider": "Vivo"}
    ]

    for service in test_services:
        url = service["url"]
        provider = service["provider"]

        service_result = {
            'provider': provider,
            'url': url,
            'success': False,
            'error': None,
            'status_code': None
        }

        try:
            # 发送HEAD请求减少数据传输量
            start_time = time.time()
            req = urllib.request.Request(url, method="HEAD")
            with urllib.request.urlopen(req, timeout=3) as response:
                elapsed = (time.time() - start_time) * 1000

                # 检查响应状态
                if response.status < 500:  # 排除服务器错误
                    result['connected'] = True
                    result['code'] = NETWORK_CONNECTION_SUCCESS
                    result['data']['successful_service'] = provider
                    result['data']['latency_ms'] = elapsed
                    result['message'] = f'通过 {provider} 服务连接成功，延迟: {elapsed:.2f}ms'

                    service_result['success'] = True
                    service_result['status_code'] = response.status
                    result['data']['services_checked'].append(service_result)

                    return result
                else:
                    service_result['error'] = f'服务器错误: 状态码 {response.status}'
                    service_result['status_code'] = response.status
        except TimeoutError:
            service_result['error'] = '连接超时 (3秒)'
        except ConnectionError:
            service_result['error'] = '连接错误 (网络问题)'
        except URLError as e:
            service_result['error'] = f'URL错误: {str(e.reason)}'
        except Exception as e:
            service_result['error'] = f'未知错误: {str(e)}'

        result['data']['services_checked'].append(service_result)

    # 3. 最后尝试基本HTTP连接
    http_result = {
        'provider': 'example.com',
        'url': 'http://example.com',
        'success': False,
        'error': None,
        'status_code': None
    }

    try:
        start_time = time.time()
        response = urllib.request.urlopen("http://example.com", timeout=3)
        elapsed = (time.time() - start_time) * 1000

        result['connected'] = True
        result['code'] = NETWORK_CONNECTION_SUCCESS
        result['data']['successful_service'] = 'example.com'
        result['data']['latency_ms'] = elapsed
        result['message'] = f'HTTP连接成功! 耗时: {elapsed:.2f}ms'

        http_result['success'] = True
        http_result['status_code'] = response.status
        result['data']['services_checked'].append(http_result)

        return result
    except URLError as e:
        http_result['error'] = f'URL错误: {str(e.reason)}'
        result['code'] = NETWORK_HTTP_FAILED
        result['message'] = f'所有连接尝试失败: {str(e)}'
    except Exception as e:
        http_result['error'] = f'未知错误: {str(e)}'
        result['code'] = NETWORK_HTTP_FAILED
        result['message'] = f'所有连接尝试失败: {str(e)}'

    result['data']['services_checked'].append(http_result)
    return result


if __name__ == "__main__":
    # 测试网络连接
    result = check_network_connection()
    print(result)