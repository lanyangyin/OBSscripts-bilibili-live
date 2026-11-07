# coding=utf-8
"""验证 check_poll()：扫码成功之后保存账号的那段逻辑。

覆盖 doc/登录问题修复说明.md 的问题 1 / 3：
  - 正常登录要写进账号，且只写 cookie 白名单字段
  - 账号已存在要走 update_user
  - 缺 SESSDATA 要报错 + 停定时器（否则会冒出假的「二维码已失效 86038」）
  - 账号列表接口异常不能挡住新增
  - add_user 失败要打错误日志
  - buvid / b_nut 全拿不到要能兜底

用法：
    python test/loginfix/test_check_poll.py
"""
import os
import random
import sys
import time
import types

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _harness as H  # noqa: E402

REC = H.Recorder()
COOKIE_KEYS = ("DedeUserID", "DedeUserID__ckMd5", "SESSDATA",
               "bili_jct", "sid", "buvid3", "buvid4", "b_nut")


class GVD:
    """GlobalVariableOfData 的 stub。"""
    loginQrCodeReturn = {}
    loginQRCodePillowImg = None
    loginQrCode_key = "qrcode_key_for_test"


class Widget:
    """widget.ComboBox.uid.Dictionary 三层嵌套的 stub。"""

    class ComboBox:
        class uid:
            Dictionary = {}


class Manager:
    """UserCookiesManager 的 stub。"""

    def __init__(self, users=None, add_result=None, all_users_fails=False):
        self.users = list(users or [])
        self.add_result = add_result
        self.all_users_fails = all_users_fails
        self.added = None
        self.updated = None

    def get_all_users(self):
        if self.all_users_fails:
            # 真实实现出错时返回 {"success": False, "message": ...}，没有 data 键
            return {"success": False, "message": "配置文件损坏"}
        return {"success": True,
                "data": {"users": [{"user_id": u} for u in self.users],
                         "total": len(self.users)}}

    def get_user_cookies(self, user_id=None):
        return {"success": True, "data": {}}

    def add_user(self, cookies):
        self.added = dict(cookies)
        REC.calls.append("add_user")
        if self.add_result:
            return dict(self.add_result)
        return {"success": True, "user_id": cookies.get("DedeUserID")}

    def update_user(self, cookies, set_as_default=False):
        self.updated = dict(cookies)
        REC.calls.append("update_user")
        return {"success": True, "message": "用户更新成功"}


class ImproveCookies:
    """ImproveCookies 的 stub。"""

    def __init__(self, ok=True):
        self.ok = ok

    def get_buvid_info(self):
        if self.ok:
            return {"success": True, "data": {"b_3": "B3VAL", "b_4": "B4VAL"}}
        return {"success": False, "message": "412", "data": None}

    def fetch_buvid3_and_bnut(self):
        if self.ok:
            return {"success": True,
                    "data": {"buvid3": "B3VAL", "b_nut": "1700000000",
                             "b_3": "B3VAL", "b_4": "B4VAL"}}
        return {"success": False, "error": "缺少: b_nut", "data": {}}


class Obs(H.Obs):
    @staticmethod
    def remove_current_callback():
        REC.calls.append("remove_current_callback")


EXPL = types.SimpleNamespace(
    information4login_qr_return_code={0: "扫码登录成功", 86038: "二维码已失效"}
)

POLL_DATA_FULL = {
    "scan_code": 0,
    "url": "https://passport.biligame.com/crossDomain?ticket=abc",
    "refresh_token": "rt",
    "timestamp": 1700000000,
    "SESSDATA": "2037%2Babc%2Cdef",
    "bili_jct": "tok",
    "DedeUserID": "1000000001",
    "DedeUserID__ckMd5": "ck",
    "sid": "sid9",
}


def run(poll_data, manager, improve=None):
    """跑一次 check_poll()，返回 (日志, 副作用调用)。"""
    REC.clear()
    GVD.loginQrCodeReturn = {"success": True, "data": poll_data}

    ns = {
        "GlobalVariableOfData": GVD,
        "get_b_l_i_r": lambda: types.SimpleNamespace(
            poll=lambda key: {"success": True, "data": poll_data}),
        "log_save": REC.log_save,
        "obs": Obs,
        "get_i_c": lambda: improve or ImproveCookies(),
        "random": random,
        "time": time,
        "LOGIN_FIX_COOKIE_KEYS": COOKIE_KEYS,
        "clear_cache": lambda: REC.calls.append("clear_cache"),
        "get_b_u_c_m": lambda: manager,
        "widget": Widget,
        "ExplanatoryDictionary": EXPL,
    }

    mod, source = H.build_module(H.FIXED, ["check_poll"])
    exec(compile(mod, source, "exec"), ns)
    ns["check_poll"]()  # finally 里会调 remove_current_callback
    return REC


def case_normal():
    m = Manager()
    rec = run(POLL_DATA_FULL, m)

    assert m.added is not None, "账号没有被写入"
    extra = set(m.added) - set(COOKIE_KEYS)
    assert not extra, "写入了非 cookie 字段: %s" % extra
    assert m.added["SESSDATA"] == "2037%2Babc%2Cdef", "SESSDATA 被改写了"
    assert m.added["buvid3"] == "B3VAL"
    assert m.added["b_nut"] == "1700000000"
    assert "remove_current_callback" in rec.calls, "定时器没有停"
    assert rec.got("添加用户成功")
    print("[1] 正常登录 -> 写入字段:", sorted(m.added))
    print("    未混入 url/refresh_token/scan_code      OK")


def case_existing():
    m = Manager(users=["1000000001"])
    run(POLL_DATA_FULL, m)
    assert m.added is None, "已存在的账号不该走 add_user"
    assert m.updated is not None
    print("[2] 账号已存在 -> update_user             OK")


def case_missing_sessdata():
    bad = dict(POLL_DATA_FULL)
    bad.pop("SESSDATA")
    m = Manager()
    rec = run(bad, m)

    assert m.added is None, "缺 SESSDATA 竟然还写账号"
    assert "remove_current_callback" in rec.calls, \
        "缺 SESSDATA 时没停定时器 -> 会继续轮询已消费的 key，用户看到假的「二维码已失效」"
    assert rec.got("登录凭据不完整"), rec.text()
    print("[3] 缺 SESSDATA -> 报错并停止轮询       OK")


def case_all_users_broken():
    m = Manager(all_users_fails=True)
    rec = run(POLL_DATA_FULL, m)
    assert m.added is not None, "账号列表读失败不该挡住新增"
    assert "remove_current_callback" in rec.calls
    print("[4] 账号列表接口异常 -> 仍能新增        OK")


def case_add_user_fails():
    m = Manager(add_result={"success": False, "message": "缺少必要字段: b_nut"})
    rec = run(POLL_DATA_FULL, m)
    assert rec.got("添加用户失败"), "add_user 返回失败却没有日志"
    print("[5] add_user 失败 -> 打错误日志          OK ->", rec.got("添加用户失败")[0])


def case_buvid_all_fail():
    m = Manager()
    run(POLL_DATA_FULL, m, improve=ImproveCookies(ok=False))
    assert m.added is not None, "buvid 拿不到不该挡住登录"
    assert m.added["b_nut"].isdigit(), m.added["b_nut"]
    assert m.added["buvid3"].endswith("infoc"), m.added["buvid3"]
    print("[6] buvid/b_nut 获取失败 -> 本地兜底    OK -> buvid3=%s... b_nut=%s"
          % (m.added["buvid3"][:12], m.added["b_nut"]))


def main():
    case_normal()
    case_existing()
    case_missing_sessdata()
    case_all_users_broken()
    case_add_user_fails()
    case_buvid_all_fail()
    print("\n全部通过 ✅")


if __name__ == "__main__":
    main()
