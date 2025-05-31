 <h1 align="center">OBSscripts<br>bilibili-live<br>【Anchor】</h1>

obs用于B站直播的插件，这里是对主播方进行了特化的版本，阉割了弹幕相关的，以减少bug产生，尽量保证稳定性

> [!CAUTION]\
> 请遵守相关法律法规
> 使用本插件从事违法行为后果请自行承担

## 配置依赖
```bash
echo 'pip换源'
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```
```bash
echo '更新pip'
pip install -U pip
```
```bash
echo '安装依赖包'
pip install -r requirements.txt
```
## obs载入python及脚本
### Windows
[Windows.md](doc%2FWindows.md)
### MacOS
[MacOS.md](doc%2FMacOS.md)
### Liunx
ing...
## 功能
>☑ 为已实现
>
> □ 为待实现
> 
> ~~例~~ 为不在此实现
### 登录
1. [x] 二维码登录账号
2. [x] 保存多个账号
3. [x] 删除账号
4. [ ] 备份账号
5. [ ] 恢复账号
6. [x] 展示二维码图片
7. [x] 登出账号
### 更改直播间设置
1. [ ] 开通直播间
2. [x] 查看直播间封面
3. [x] 更改直播间封面
4. [x] 更改直播间标题
5. [x] 更改直播间公告
6. [ ] 更改直播间标签
7. [x] 更改直播间分区
8. [ ] 发布直播预告
9. [x] 跳转直播管理网页
### 直播
1. [x] 选择直播平台
2. [x] 开播
3. [x] 复制服务器地址
4. [x] 复制推流码
5. [x] 更新推流码
6. [x] 下播
### ~~发送弹幕~~
1. [ ] 保存多个账户
2. [ ] 保存多个直播间
3. [ ] 自动字数切分
4. [ ] 自动检测弹幕是否发出
5. [ ] 自动更改违规弹幕
6. [ ] 发送表情
### ~~输出弹幕~~
1. [ ] 自动切换直播间
2. [ ] 调整输出内容
3. [ ] 输出普通弹幕
4. [ ] 输出礼物弹幕
5. [ ] 输出SC弹幕
6. [ ] 输出进房弹幕
7. [ ] 输出点赞消息
8. [ ] 输出关注消息
