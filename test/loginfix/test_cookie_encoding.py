# coding=utf-8
"""验证：cookie 编码 + 从 Set-Cookie / ticket 采集登录凭据。

对应 doc/登录问题修复说明.md 的问题 1（凭据在 Set-Cookie 里）和问题 4（双重编码）。
本地起一个 302 服务器模拟 B 站 ticket 端点，不联网。

用法：
    python test/loginfix/test_cookie_encoding.py
"""
import os
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import quote, unquote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _harness as H  # noqa: E402

import requests  # noqa: E402

REC = H.Recorder()
BASE_GLOBALS = {
    "log_save": REC.log_save,
    "obs": H.Obs,
    "Dict": dict,
    "Any": object,
    "List": list,
    "Optional": object,
    "quote": quote,
    "unquote": unquote,
}

# 模拟 B 站下发的 SESSDATA：本身就是 URL 编码的
SESSDATA_ENCODED = "2037%2Babc123%2Cdef456%2Cghi789%2C1751000000"
SESSDATA_PLAIN = "2037+abc123,def456,ghi789,1751000000"


def check_encoding():
    """问题 4：quote(unquote(v)) 必须是幂等的。"""
    f = H.extract(H.FIXED, "dict_to_cookie_string", BASE_GLOBALS)

    out = f({"SESSDATA": SESSDATA_ENCODED, "bili_jct": "tok"})
    assert "%252C" not in out, "出现双重编码: " + out
    assert "SESSDATA=" + SESSDATA_ENCODED in out, out
    print("[1] 单层编码保持不变            OK  ->", out)

    out2 = f({"SESSDATA": SESSDATA_PLAIN})
    assert out2 == "SESSDATA=" + SESSDATA_ENCODED, out2
    print("[2] 明文值编码一次            OK  ->", out2)

    # 对照：旧实现（直接 quote）会产生 %252C
    legacy = "SESSDATA=" + quote(SESSDATA_ENCODED)
    assert "%252C" in legacy
    print("[2b] 旧实现对照               -> ", legacy[:60], "...(含 %252C，服务端解不出)")


def check_roundtrip(port):
    """端到端闭环：Set-Cookie 原文 -> 采集入库 -> 拼回 Cookie 头，必须还原成原文。

    这一步很关键：采集时会 unquote（存明文），拼头时再 quote（单层编码），
    两者必须互为逆运算，否则存进 config.json 的凭据发给 B 站就是坏的。
    """
    collect = H.extract(H.FIXED, "_collect_cookies_from_response", BASE_GLOBALS)
    to_cookie = H.extract(H.FIXED, "dict_to_cookie_string", BASE_GLOBALS)

    resp = requests.get(
        "http://127.0.0.1:%d/crossDomain?ticket=rt" % port,
        headers={"Referer": "https://www.bilibili.com/"},
        allow_redirects=False,
    )
    stored = {}
    collect(resp, stored)

    header = to_cookie(stored)
    assert "SESSDATA=" + SESSDATA_ENCODED in header, "还原失败: " + header
    assert "%252C" not in header, "还原后出现双重编码: " + header
    print("[3] 采集 -> 入库 -> 拼头 闭环      OK  -> SESSDATA 还原为原文单层编码")


class Handler(BaseHTTPRequestHandler):
    """模拟 https://passport.biligame.com/crossDomain?ticket=..."""

    def do_GET(self):
        if "crossDomain" not in self.path:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")
            return

        referer = self.headers.get("Referer", "")
        if not referer.startswith("https://www.bilibili.com"):
            # 线上行为：没 Referer 只跳转，不写 cookie
            self.send_response(302)
            self.send_header("Location", "https://www.bilibili.com")
            self.end_headers()
            return

        self.send_response(302)
        for cookie in (
            "SESSDATA=%s; Path=/; Domain=.bilibili.com" % SESSDATA_ENCODED,
            "bili_jct=tok123; Path=/; Domain=.bilibili.com",
            "DedeUserID=1000000001; Path=/; Domain=.bilibili.com",
            "DedeUserID__ckMd5=abcd1234; Path=/; Domain=.bilibili.com",
            "sid=zzz9; Path=/; Domain=.bilibili.com",
        ):
            self.send_header("Set-Cookie", cookie)
        self.send_header("Location", "https://passport.bilibili.cn/login")
        self.end_headers()

    def log_message(self, *a):
        pass


def check_collect(port):
    """问题 1：能从 302 的 Set-Cookie 里拿到字段，且值已 unquote。"""
    collect = H.extract(H.FIXED, "_collect_cookies_from_response", BASE_GLOBALS)

    resp = requests.get(
        "http://127.0.0.1:%d/crossDomain?ticket=1" % port,
        headers={"Referer": "https://www.bilibili.com/"},
        allow_redirects=False,
    )
    target = {}
    collect(resp, target)

    assert target.get("SESSDATA") == SESSDATA_PLAIN, target
    assert target.get("DedeUserID") == "1000000001", target
    assert target.get("bili_jct") == "tok123", target
    assert "%" not in target["SESSDATA"], "采集时没有 unquote"
    print("[4] _collect_cookies_from_response OK ->", sorted(target.keys()))

    # 对照：不带 Referer 时拿不到任何 cookie
    resp2 = requests.get(
        "http://127.0.0.1:%d/crossDomain?ticket=2" % port,
        allow_redirects=False,
    )
    target2 = {}
    collect(resp2, target2)
    assert not target2.get("SESSDATA"), target2
    print("[5] 无 Referer -> 取不到 SESSDATA    OK（证明 Referer 是必要条件）")


def check_ticket(port):
    """问题 1：_fetch_cookies_by_ticket 在第一跳（禁跳转）就取到 SESSDATA。"""
    ns = dict(BASE_GLOBALS)
    ns["requests"] = requests
    ns["LOGIN_FIX_COOKIE_KEYS"] = ()

    fetch_ticket = H.extract(H.FIXED, "_fetch_cookies_by_ticket", ns)
    collect = H.extract(H.FIXED, "_collect_cookies_from_response", ns)

    class FakeLogin:
        headers = {"User-Agent": "test"}
        verify_ssl = False

    FakeLogin._collect_cookies_from_response = staticmethod(collect)
    FakeLogin._fetch_cookies_by_ticket = fetch_ticket

    got = FakeLogin()._fetch_cookies_by_ticket(
        "http://127.0.0.1:%d/crossDomain?ticket=abc" % port)

    assert got.get("SESSDATA") == SESSDATA_PLAIN, got
    assert got.get("sid") == "zzz9", got
    print("[6] _fetch_cookies_by_ticket      OK ->", sorted(got.keys()))

    # 关键日志：确认是先禁跳转取到的
    assert REC.got("ticket 换取(跟跳=False)"), REC.text()
    print("[7] 日志含「跟跳=False」           OK（ticket 一次性，第一跳就得拿到）")


def check_buvid_fallback():
    """问题 2：fetch_buvid3_and_bnut 失败时也必须返回带 data 键的字典。"""
    class DeadRequests:
        @staticmethod
        def head(*a, **kw):
            raise requests.exceptions.ConnectionError("blocked")

        exceptions = requests.exceptions

    ns = dict(BASE_GLOBALS)
    ns["requests"] = DeadRequests
    ns["time"] = time

    f = H.extract(H.FIXED, "fetch_buvid3_and_bnut", ns)

    class FakeImprove:
        pass

    FakeImprove.fetch_buvid3_and_bnut = f
    res = FakeImprove().fetch_buvid3_and_bnut()

    assert isinstance(res, dict), res
    assert "data" in res, "缺少 data 键 -> 调用方会 KeyError: 'data'"
    assert res["data"] == {}, res
    assert res["success"] is False

    # 调用方现在这样写是安全的
    b_nut = (res.get("data") or {}).get("b_nut") or str(int(time.time()))
    assert b_nut
    print("[8] 失败时仍带 data 键            OK -> data=%r 兜底 b_nut=%s" % (res["data"], b_nut))


def main():
    server = HTTPServer(("127.0.0.1", 0), Handler)
    port = server.server_address[1]
    threading.Thread(target=server.serve_forever, daemon=True).start()
    time.sleep(0.2)

    try:
        check_encoding()
        check_roundtrip(port)
        check_collect(port)
        check_ticket(port)
        check_buvid_fallback()
    finally:
        server.shutdown()

    print("\n全部通过 ✅")


if __name__ == "__main__":
    main()
