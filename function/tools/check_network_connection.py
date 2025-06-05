# 检查网络连通
import socket
import urllib.request
from urllib.error import URLError
import time


def check_network_connection():
    """检查网络连接，通过多个服务提供者的链接验证"""
    print("\n======= 开始网络连接检查 =======")

    # 1. 首先尝试快速DNS连接检查
    print("\n[步骤1] 尝试通过DNS连接检查网络 (8.8.8.8:53)...")
    try:
        start_time = time.time()
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        elapsed = (time.time() - start_time) * 1000
        print(f"✅ DNS连接成功! 耗时: {elapsed:.2f}ms")
        return True
    except OSError as e:
        print(f"⚠️ DNS连接失败: {str(e)}")

    # 2. 尝试多个服务提供者的链接
    print("\n[步骤2] 开始尝试多个服务提供者的连接...")

    # 定义测试URL及其提供商
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
        print(f"\n- 尝试 {provider} 服务: {url}")

        try:
            # 发送HEAD请求减少数据传输量
            start_time = time.time()
            req = urllib.request.Request(url, method="HEAD")
            with urllib.request.urlopen(req, timeout=3) as response:
                elapsed = (time.time() - start_time) * 1000

                # 检查响应状态
                if response.status < 500:  # 排除服务器错误
                    print(f"  ✅ 连接成功! 状态码: {response.status} | 耗时: {elapsed:.2f}ms")
                    return True
                else:
                    print(f"  ⚠️ 服务器错误: 状态码 {response.status}")
        except TimeoutError:
            print("  ⏱️ 连接超时 (3秒)")
        except ConnectionError:
            print("  🔌 连接错误 (网络问题)")
        except URLError as e:
            print(f"  ❌ URL错误: {str(e.reason)}")
        except Exception as e:
            print(f"  ⚠️ 未知错误: {str(e)}")

    # 3. 最后尝试基本HTTP连接
    print("\n[步骤3] 尝试基本HTTP连接检查 (http://example.com)...")
    try:
        start_time = time.time()
        urllib.request.urlopen("http://example.com", timeout=3)
        elapsed = (time.time() - start_time) * 1000
        print(f"✅ HTTP连接成功! 耗时: {elapsed:.2f}ms")
        return True
    except URLError as e:
        print(f"❌ 所有连接尝试失败: {str(e)}")
        return False


# 测试网络连接
result = check_network_connection()
print(f"\n======= 最终结果: 网络{'可用' if result else '不可用'} =======\n")