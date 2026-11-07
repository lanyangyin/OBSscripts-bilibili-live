# loginfix 验证脚本

对应修复说明：[`doc/登录问题修复说明.md`](../../doc/登录问题修复说明.md)

成品脚本是 3 万多行的单体文件，且运行时依赖 `obspython`，没法直接 `import` 测试。
这里用 `ast` 把目标函数从**真实源码**里抽出来单独编译，再配 stub 运行 —— 测的是源码本身，
不是复制出来的副本，所以改了源码测试会跟着变。

## 依赖

只用到 `requests`：

```bash
pip install requests
```

## 运行

```bash
# 在仓库根目录
python test/loginfix/test_cookie_encoding.py    # cookie 编码 + Set-Cookie/ticket 采集
python test/loginfix/test_check_poll.py         # 扫码成功后保存账号的逻辑
python test/loginfix/test_account_list.py       # 账号列表刷新（原版 vs 修复版对比）
```

`test_account_list.py` 会**同时跑原版 `bilibili_live_multi_py36_obs27.py` 和修复版**，
直接打印对比表，跑完退出码为 0 表示修复版全部符合预期。

## 三个脚本各测什么

| 脚本 | 覆盖 | 说明 |
|---|---|---|
| `test_cookie_encoding.py` | 问题 1、2、4 | 起一个本地 302 服务器模拟重定向端点，验证 `Referer` 为补取凭据的必要条件、`allow_redirects=False` 能读到首个响应头、`quote(unquote(v))` 不会产生 `%252C`、`fetch_buvid3_and_bnut()` 失败时仍带 `data` 键 |
| `test_check_poll.py` | 问题 1、3 | 6 个场景：正常登录 / 账号已存在 / 缺 SESSDATA / 账号列表接口异常 / `add_user` 返回失败 / buvid 全部失败。重点断言「缺凭据时必须停定时器」和「只写 8 个 cookie 字段」 |
| `test_account_list.py` | 问题 4、5、6 | 8 个场景的新旧版本对比：仅 `-101` 移除账号，网络异常、超时、`-412` 请求被拒均保留；名片接口异常和默认账号缺失不再崩 |

## 在本机跑过的结果

```
test_cookie_encoding.py   →  8 项断言通过
test_check_poll.py        →  6 个场景通过
test_account_list.py      →  修复版 8/8 符合预期；原版 3 个场景误移除账号、2 个场景崩溃
```

原版在同一套 stub 下的实际表现（可复现）：

| 场景 | 原版 | 修复版 |
|---|---|---|
| nav 网络异常 | 移除账号，列表变空 | 保留账号 |
| nav 返回 -412 | 移除账号 | 保留账号 |
| nav 超时 | 移除账号 | 保留账号 |
| 名片接口异常 | `KeyError: 'data'` | 正常（显示 uid） |
| 默认账号不在字典 | `ValueError` | 回退显示 uid |
