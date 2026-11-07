<div style="display: flex; justify-content: center;">
<div align="center">

| [![OBS](https://obsproject.com/assets/images/new_icon_small-r.png)](https://obsproject.com/) |           <h1 align="center">OBSscripts<br>bilibili-live<br></h1>           | [![Python](https://www.python.org/static/img/python-logo-large.c36dccadd999.png)](https://www.python.org/) |
|:--------------------------------------------------------------------------------------------:|:-----------------------------------------------------------------------------------:|:----------------------------------------------------------------------------------------------------------:|
|                                                                                              | <div align="center">[![img.png](doc/img/img.png)](https://live.bilibili.com/)</div> |                                                                                                            |

</div>
</div>

obs用于B站直播的插件，只是因为不想直播时网页obs两头跑而制作出来，

并分专业代码写手，随时可能停止维护，或者受到阿B影响不能使用

希望能帮助到有需要的人，也希望有大佬能来优化一下orz
> [!CAUTION]\
> 请遵守相关法律法规
> 使用本插件从事违法行为后果请自行承担

## 环境需求
电脑系统：macOS 14+ / Windows 7 & 10+

python版本：3.9-3.12 or 3.6 (for Win7 only)

obs_studio版本：30+ or 26.1.1+ (for Win7 only)

## 配置方法
* [Windows 7配置方法](doc/Windows7.md)
* [Windows 10+配置方法](doc/Windows10+.md)
* [Windows Python环境集成包制作方法](doc/Windows下制作易用的Python环境集成包.md)
* [MacOS配置方法](doc/MacOS.md)
* [Ubuntu配置方法](doc/Ubuntu.md)

## 登录问题修复版（新增，不改动原脚本）
扫码后提示「登录成功」但没有账号、或提示「二维码已失效」、或更新账号列表报 `KeyError: 'data'`，
是原脚本所依赖的接口返回格式已变更（登录字段改由 `Set-Cookie` 响应头返回，旧版 UA 标识也已不被接口接受），
而脚本未做相应适配。

- 脚本：[finishedProduct/bilibili_live_multi_py36_obs27_loginfix.py](finishedProduct/bilibili_live_multi_py36_obs27_loginfix.py)
- **使用说明**：[doc/loginfix使用说明.md](doc/loginfix使用说明.md)（安装位置、在 OBS 里怎么切换、首次扫码添加账号、切换/登出/删除账号、数据备份位置）
- 问题成因与修复清单：[doc/登录问题修复说明.md](doc/登录问题修复说明.md)
- 验证脚本：[test/loginfix/](test/loginfix/)（全部使用合成数据，不含真实账号信息）

原 `bilibili_live_multi_py36_obs27.py` 保持不变，两版可在 OBS「脚本」窗口里切换，不要同时启用。

## 功能
>☑ 为已实现
>
> □ 为待实现
> 
> ~~例~~ 为可能实现
### 登录
1. [x] [二维码登录账号]()
2. [x] [展示登录二维码图片]()
3. [x] [保存多个账号]()
4. [x] [删除账号]()
5. [ ] 备份账号
6. [ ] 恢复账号
7. [x] [登出账号]()

### 更改直播间设置
1. [x] 开通直播间
2. [x] [查看直播间封面]()
3. [x] [更改直播间封面]()
4. [x] [更改直播间标题]()
5. [x] [更改直播间公告]()
6. [ ] 更改直播间标签
7. [x] [更改直播间分区]()
8. [x] [发布直播预告]()
9. [x] [跳转直播管理网页]()

### 直播管理
1. [ ] 禁言用户
2. [ ] 房管
3. [ ] 黑名单
4. [ ] 直播间屏蔽词

### 直播
1. [x] [选择直播平台]()
2. [x] [开播]()
3. [x] [复制服务器地址]()
4. [x] [复制推流码]()
5. [x] [更新推流码]()
6. [x] [下播]()

### 输出弹幕
1. [ ] 自动切换直播间
2. [ ] 调整输出内容
3. [x] 输出普通弹幕
4. [x] 输出礼物弹幕
5. [x] 输出SC弹幕
6. [x] 输出进房弹幕
7. [ ] 输出点赞消息
8. [ ] 输出关注消息

### ~~弹幕UI~~
1. [ ] 消息背景自定义
2. [ ] 消息动画自定义

### ~~弹幕互动~~
1. [ ] 加班机
2. [ ] 抽奖
3. [ ] 五子棋
4. [ ] 控制

### ~~发送弹幕~~
1. [ ] 保存多个账户
2. [ ] 保存多个直播间
3. [ ] 自动字数切分
4. [ ] 自动检测弹幕是否发出
5. [ ] 自动更改违规弹幕
6. [ ] 发送表情


# 引用
- 哔哩哔哩的api：[SocialSisterYi / bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect?tab=readme-ov-file)
- 发出调用api的网络请求python包：[Requests](https://github.com/psf/requests)
- 调用剪贴板的python包：[pyperclip](https://github.com/asweigart/pyperclip)
- 创建二维码的python包：[qrcode](https://github.com/nayuki/QR-Code-generator)
- 操作图片的python包：[pillow](https://github.com/python-pillow/Pillow)
- 中文转拼音的python包：[pypinyin](https://github.com/mozillazg/python-pinyin)
- 网络长连接用于连接弹幕的python包：[websockets](https://github.com/python-websockets/websockets)
- 开始直播函数的参数：[BLiveWeb](https://github.com/ProgramRipper/BLiveWeb)
- obs的python脚本开始编写时参考：[OBS Python 脚本教程](https://learnscript.net/zh/obs-python-scripting/setup/)
- obs脚本官方文档：[Python/Lua Scripting](https://docs.obsproject.com/scripting#python-lua-scripting)
- 弹幕机参考
  - 参数参考：[xfgryujk/blivechat](https://github.com/xfgryujk/blivechat)
  - 界面参考：[DoodleBears/blivechat](https://github.com/DoodleBears/blivechat)
  - 界面参考：[直播弹幕姬BLC](https://play-live.bilibili.com/details/1675336975685)
  - 界面参考：[LAPLACE Chat](https://chat.laplace.live/)


# 感谢所有贡献者的努力

<a href="https://github.com/lanyangyin/OBSscripts-bilibili-live/graphs/contributors" target="_blank">
  <img src="https://contrib.rocks/image?repo=lanyangyin/OBSscripts-bilibili-live" />
</a>
