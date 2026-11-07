# coding=utf-8
"""验证账号列表刷新：get_uid_nickname_dict / get_default_user_nickname。

覆盖 doc/登录问题修复说明.md 的问题 4 / 5 / 6，并且**同时跑原版和修复版**，
输出对比表。你当时遇到的 `KeyError: 'data'` 和「账号莫名消失」都在这里复现。

用法：
    python test/loginfix/test_account_list.py
"""
import contextlib
import io
import os
import sys
import types

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _harness as H  # noqa: E402

REC = H.Recorder()

NAV_OK = {"success": True,
          "data": {"isLogin": True, "uname": "示例昵称", "mid": 1000000001}}
NAV_NET_ERROR = {"success": False, "error": "网络连接错误", "status_code": None}
NAV_101 = {"success": False, "api_code": -101, "error": "账号未登录"}
NAV_412 = {"success": False, "api_code": -412, "error": "请求被拦截"}
NAV_TIMEOUT = {"success": False, "error": "请求超时", "status_code": None}


class UserManager:
    def __init__(self, users, default=None):
        self.users = dict(users)
        self.default = default
        self.deleted = []

    def get_all_users(self):
        return {"success": True,
                "data": {"users": [{"user_id": u} for u in self.users],
                         "total": len(self.users)}}

    def get_user_cookies(self, user_id=None):
        if user_id is None:
            if not self.default:
                return {"success": False, "message": "未设置默认用户"}
            user_id = self.default
        uid = str(user_id)
        if uid not in self.users:
            return {"success": False, "message": "用户 %s 不存在" % uid}
        return {"success": True, "data": dict(self.users[uid])}

    def get_default_user_id(self):
        return self.default

    def clear_default_user(self):
        self.default = None

    def delete_user(self, user_id):
        self.deleted.append(str(user_id))
        self.users.pop(str(user_id), None)
        return {"success": True}


class NavManager:
    def __init__(self, result):
        self.result = result

    def get_nav_info(self):
        return self.result


class CardApi:
    def __init__(self, boom=False):
        self.boom = boom

    def get_bilibili_user_card(self, uid):
        if self.boom:
            # 名片接口抖动时返回的结构里没有 data
            return {"success": False, "message": "请求被拒"}
        return {"success": True, "data": {"data": {"card": {"name": "昵称_%s" % uid}}}}


def run(path, users, nav_result, default=None, card_boom=False):
    """在 path 这份源码上跑一次账号列表刷新。"""
    REC.clear()
    mgr = UserManager(users, default)

    ns = {
        "log_save": REC.log_save,
        "obs": H.Obs,
        "get_b_u_c_m": lambda: mgr,
        "BilibiliSpecialApiManager": lambda headers, verify: NavManager(nav_result),
        "BilibiliApiGeneric": lambda headers, verify: CardApi(card_boom),
        "get_b_a_g": lambda: CardApi(card_boom),
        "GlobalVariableOfData": types.SimpleNamespace(sslVerification=False),
        "Tools": types.SimpleNamespace(
            dict_to_cookie_string=lambda d: "; ".join("%s=%s" % kv for kv in d.items())),
        "Optional": object,
    }

    mod, source = H.build_module(
        path, ["get_uid_nickname_dict", "get_default_user_nickname"])
    exec(compile(mod, source, "exec"), ns)

    try:
        # 原版里有一句 print(nav_info)，会把调试输出刷到屏幕上，这里静音
        with contextlib.redirect_stdout(io.StringIO()):
            d = ns["get_uid_nickname_dict"]()
            n = ns["get_default_user_nickname"]()
        return {"ok": True, "dict": d, "nickname": n, "deleted": list(mgr.deleted)}
    except Exception as e:
        return {"ok": False, "error": "%s: %s" % (type(e).__name__, e),
                "deleted": list(mgr.deleted)}


SCENARIOS = [
    ("nav 正常", {"1000000001": {"SESSDATA": "s1"}}, NAV_OK, "1000000001", False),
    ("nav 返回 -101（凭据真失效）", {"1000000001": {"SESSDATA": "s1"}}, NAV_101, "1000000001", False),
    ("nav 网络异常", {"1000000001": {"SESSDATA": "s1"}}, NAV_NET_ERROR, "1000000001", False),
    ("nav 返回 -412（请求被拒）", {"1000000001": {"SESSDATA": "s1"}}, NAV_412, "1000000001", False),
    ("nav 超时", {"1000000001": {"SESSDATA": "s1"}}, NAV_TIMEOUT, "1000000001", False),
    ("名片接口异常", {"1000000001": {"SESSDATA": "s1"}}, NAV_TIMEOUT, "1000000001", True),
    ("账号缺 SESSDATA", {"1000000001": {"bili_jct": "j1"}}, NAV_OK, "1000000001", False),
    ("默认账号不在字典", {"1000000001": {"SESSDATA": "s1"}}, NAV_OK, "999999", False),
]

# 期望行为：(是否该删账号, 是否该崩)
EXPECT = {
    "nav 正常": (False, False),
    "nav 返回 -101（凭据真失效）": (True, False),
    "nav 网络异常": (False, False),
    "nav 返回 -412（请求被拒）": (False, False),
    "nav 超时": (False, False),
    "名片接口异常": (False, False),
    "账号缺 SESSDATA": (False, False),
    "默认账号不在字典": (False, False),
}


def describe(r):
    if not r["ok"]:
        return "❌ 崩溃 " + r["error"]
    flag = "账号被删" if r["deleted"] else "保留"
    return "✅ %s 字典=%r 默认昵称=%r" % (flag, r["dict"], r["nickname"])


def main():
    print("=" * 100)
    print("%-28s | %-42s | %s" % ("场景", "原版 obs27.py", "修复版 loginfix.py"))
    print("=" * 100)

    failures = []
    for label, users, nav, default, boom in SCENARIOS:
        old = run(H.ORIGINAL, users, nav, default, boom)
        new = run(H.FIXED, users, nav, default, boom)

        print("%-28s | %-42s | %s" % (label, describe(old), describe(new)))

        want_delete, want_crash = EXPECT[label]
        got_delete = bool(new["deleted"])
        got_crash = not new["ok"]
        if got_delete != want_delete or got_crash != want_crash:
            failures.append((label, new))

    print("=" * 100)

    if failures:
        print("\n修复版有不符合预期的场景：")
        for label, r in failures:
            print("  -", label, "->", r)
        sys.exit(1)

    print("\n修复版 8 个场景全部符合预期 ✅")
    print("（原版一列可以看到：网络异常/请求被拒会误移除账号，名片接口异常直接 KeyError: 'data'）")


if __name__ == "__main__":
    main()
