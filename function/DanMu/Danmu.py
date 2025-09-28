import asyncio
import json
import zlib
from pathlib import Path
from typing import Optional
from function.api.Authentication.Wbi.get_danmu_info import WbiSigna
from function.tools.parse_cookie import parse_cookie
from function.api.Special.Get.get_user_live_info import BilibiliCSRFAuthenticator
from function.tools.dict_to_cookie_string import dict_to_cookie_string
from function.tools.ConfigControl.BilibiliUserConfigManager import BilibiliUserConfigManager
from function.tools.proto.InteractWordV2Decoder import InteractWordV2Decoder
from function.tools.proto.OnlineRankV3Decoder import OnlineRankV3Decoder
iwv_decoder = InteractWordV2Decoder()
orv3decoder = OnlineRankV3Decoder()

import websockets


class Danmu:

    def __init__(self, headers: dict, verify_ssl: bool = True):
        self.headers = headers
        self.verify_ssl = verify_ssl
        self.cookie = headers['cookie']

    def _get_websocket_client(self, roomid: int):
        danmu_info = WbiSigna(self.headers, self.verify_ssl).get_danmu_info(roomid)
        token = danmu_info['data']['token']
        host = danmu_info['data']['host_list'][-1]
        wss_url = f"wss://{host['host']}:{host['wss_port']}/sub"

        user_info = BilibiliCSRFAuthenticator(self.headers, self.verify_ssl).get_user_live_info()['data']
        cookies = parse_cookie(self.cookie)
        auth_body = {
            "uid": user_info["uid"],
            "roomid": roomid,
            "protover": 2,
            "buvid": cookies['buvid3'],
            "platform": "web",
            "type": 3,
            "key": token
        }
        return wss_url, auth_body

    def connect_room(self, roomid: int):
        wss_url, auth_body = self._get_websocket_client(roomid)
        return self._WebSocketClient(wss_url, auth_body)

    class _WebSocketClient:
        danmu_start_is = True
        danmu_working_is = True
        HEARTBEAT_INTERVAL = 30
        VERSION_NORMAL = 0
        VERSION_ZIP = 2

        def __init__(self, url: str, auth_body: dict):
            self.url = url
            self.auth_body = auth_body
            # pprint.pprint(auth_body)
            # self.saved_danmudata = set()

        async def connect(self):
            retry_count = 0
            max_retries = 5
            base_delay = 3  # 基础重连延迟秒数

            while self.danmu_start_is and retry_count < max_retries:
                try:
                    async with websockets.connect(
                            self.url,
                            ping_interval=20,  # 添加ping间隔
                            ping_timeout=10,  # ping超时时间
                            close_timeout=10  # 关闭超时时间
                    ) as ws:
                        await self.on_open(ws)
                        retry_count = 0  # 重置重试计数

                        while self.danmu_start_is:
                            self.danmu_working_is = True
                            try:
                                message = await asyncio.wait_for(ws.recv(), timeout=40)
                                await self.on_message(message)
                            except asyncio.TimeoutError:
                                print("接收消息超时，发送心跳检测...")
                                # 发送心跳检测连接是否还活着
                                try:
                                    await ws.send(self.pack(None, 2))
                                except:
                                    break
                            except websockets.exceptions.ConnectionClosed as e:
                                print(f"连接关闭: {e}")
                                break

                except Exception as e:
                    retry_count += 1
                    delay = base_delay * (2 ** retry_count)  # 指数退避
                    print(f"连接失败，{delay}秒后重试... (尝试 {retry_count}/{max_retries})")
                    print(f"错误详情: {e}")
                    await asyncio.sleep(delay)

            if retry_count >= max_retries:
                print("达到最大重试次数，停止连接")
            self.danmu_working_is = False

        async def on_open(self, ws):
            try:
                print("正在连接到弹幕服务器...")
                # 先发送认证包
                auth_data = self.pack(self.auth_body, 7)
                await ws.send(auth_data)

                # 等待认证响应
                try:
                    auth_response = await asyncio.wait_for(ws.recv(), timeout=10)
                    print("认证成功，连接已建立")
                    # 启动心跳任务
                    asyncio.create_task(self.send_heartbeat(ws))
                except asyncio.TimeoutError:
                    print("认证响应超时")
                    raise

            except Exception as e:
                print(f"连接初始化失败: {e}")
                raise

        async def send_heartbeat(self, ws):
            while self.danmu_start_is and self.danmu_working_is:
                try:
                    await ws.send(self.pack(None, 2))
                    await asyncio.sleep(self.HEARTBEAT_INTERVAL)
                except websockets.exceptions.ConnectionClosed:
                    print("心跳发送失败，连接已关闭")
                    break
                except Exception as e:
                    print(f"心跳发送异常: {e}")
                    break

        async def on_message(self, message):
            if isinstance(message, bytes):
                self.unpack(message)

        def pack(self, content: Optional[dict], code: int) -> bytes:
            content_bytes = json.dumps(content).encode('utf-8') if content else b''
            header = (len(content_bytes) + 16).to_bytes(4, 'big') + \
                     (16).to_bytes(2, 'big') + \
                     self.VERSION_NORMAL.to_bytes(2, 'big') + \
                     code.to_bytes(4, 'big') + \
                     (1).to_bytes(4, 'big')
            return header + content_bytes

        def unpack(self, byte_buffer: bytes):
            # 头部格式:
            package_len = int.from_bytes(byte_buffer[0:4], 'big')
            """
            封包总大小 (头部大小 + 正文大小)
            """
            head_length = int.from_bytes(byte_buffer[4:6], 'big')
            """
            头部大小 (一般为 0x0010, 即 16 字节)
            """
            prot_ver = int.from_bytes(byte_buffer[6:8], 'big')
            """
            协议版本:
                - 0: 普通包 (正文不使用压缩)
                - 1: 心跳及认证包 (正文不使用压缩)
                - 2: 普通包 (正文使用 zlib 压缩)
                - 3: 普通包 (使用 brotli 压缩的多个带文件头的普通包)
            """
            opt_code = int.from_bytes(byte_buffer[8:12], 'big')
            """
            操作码 (封包类型)
                - 2	心跳包
                - 3	心跳包回复 (人气值)
                - 5	普通包 (命令)
                - 7	认证包
                - 8	认证包回复
            """
            sequence = int.from_bytes(byte_buffer[12:16], 'big')
            """
            sequence, 每次发包时向上递增
            """

            content_bytes = byte_buffer[16:package_len]

            if prot_ver == self.VERSION_ZIP:
                content_bytes = zlib.decompress(content_bytes)
                self.unpack(content_bytes)
                return
            if prot_ver == 3:
                print(3)

            content = content_bytes.decode('utf-8')
            if opt_code == 8:  # AUTH_REPLY
                print(f"身份验证回复: {content}\n")
            elif opt_code == 5:  # SEND_SMS_REPLY
                # print(f"Danmu message at {datetime.datetime.now()}: {content}")
                if json.loads(content)['cmd'] == "LIVE":
                    # 直播开始 (LIVE)
                    # 注：请求了开始直播接口、开始向服务器推流时下发。
                    contentdata = json.loads(content)
                    print(contentdata)
                    pass
                elif json.loads(content)['cmd'] == "DANMU_MSG":
                    # 弹幕 (DANMU_MSG)
                    # 注: 当收到弹幕时接收到此条消息, 10 进制转 16 进制若位数不足则在左侧补 0
                    contentinfo = json.loads(content)['info']
                    contentinfo[0][15]['extra'] = json.loads(contentinfo[0][15]['extra'])
                    tfo = contentinfo[0][15]['extra']['content']
                    afo = ""
                    if contentinfo[0][15]['extra']['reply_uname']:
                        afo = f" @{contentinfo[0][15]['extra']['reply_uname']} "
                    ufo = contentinfo[0][15]['user']['base']['name']
                    mfo = ''
                    if contentinfo[0][15]['user']['medal']:
                        fmedal = contentinfo[0][15]['user']['medal']
                        mfo = f"【{fmedal['name']}|{fmedal['level']}】"
                    wfo = ''
                    if contentinfo[-2] != [0]:
                        wfo = str(contentinfo[-2])
                    print(f"{wfo}{mfo}{ufo}:\n\t>>>{afo}{tfo}")
                    pass
                elif json.loads(content)['cmd'] == "DM_INTERACTION":
                    # 交互信息合并 (DM_INTERACTION)
                    # 注: 连续多条相同弹幕时触发
                    contentdata = json.loads(content)['data']
                    contentdata['data'] = json.loads(contentdata['data'])
                    tfo = "连续发送弹幕或点赞"
                    if contentdata['type'] == 102:
                        tfo = ""
                        for contentdatacombo in contentdata['data']['combo'][:-1]:
                            tfo += f"热词：\t{contentdatacombo['cnt']}\t人{contentdatacombo['guide']}{contentdatacombo['content']}\n"
                        tfo += f"⛓🔠连续弹幕：\t{contentdata['data']['combo'][-1]['cnt']}\t人{contentdata['data']['combo'][-1]['guide']}{contentdata['data']['combo'][-1]['content']}"
                    elif contentdata['type'] == 106:
                        tfo = f"⛓👍连续点赞：\t{contentdata['data']['cnt']}\t{contentdata['data']['suffix_text']}"
                    print(f"{tfo}")
                    pass
                elif json.loads(content)['cmd'] == "SEND_GIFT":
                    # 送礼 (SEND_GIFT)
                    contentdata = json.loads(content)['data']
                    ufo = contentdata['uname']
                    mfo = ""
                    if contentdata['medal_info']['medal_name']:
                        medali = contentdata['medal_info']
                        mfo = f"【{medali['medal_name']}|{medali['medal_level']}】"
                    wfo = ''
                    if contentdata['wealth_level'] != 0:
                        wfo = f"[{contentdata['wealth_level']}]"
                    tfo = ''
                    if contentdata['batch_combo_send']:
                        tfo += contentdata['batch_combo_send']['action']
                        if contentdata['batch_combo_send']['blind_gift']:
                            contentdata_bcsb_g = contentdata['batch_combo_send']['blind_gift']
                            tfo += f"\t【{contentdata_bcsb_g['original_gift_name']}】{contentdata_bcsb_g['gift_action']}"
                            coin = f"{contentdata_bcsb_g['gift_tip_price'] / 1000}￥\t{(contentdata_bcsb_g['gift_tip_price'] - contentdata['total_coin']) / 1000}￥"
                        else:
                            coin = f"{contentdata['total_coin'] / 1000}￥"
                        tfo += f"{contentdata['num']}个《{contentdata['batch_combo_send']['gift_name']}》\t{coin}"
                    else:
                        tfo += f"{contentdata['action']}{contentdata['num']}个《{contentdata['giftName']}》"
                    print(f'🎁礼物：\t{wfo}{mfo}{ufo}\t{tfo}')
                    pass
                elif json.loads(content)['cmd'] == "GUARD_BUY":
                    # 上舰通知 (GUARD_BUY)
                    # 注: 当有用户购买 舰长 / 提督 / 总督 时
                    contentdata = json.loads(content)['data']
                    tfo = f"🚢上舰：\t{contentdata['username']}\t购买{contentdata['num']}个\t【{contentdata['gift_name']}】"
                    print(f"{tfo}")
                    pass

                elif json.loads(content)['cmd'] == "WIDGET_BANNER":
                    # # 顶部横幅 (WIDGET_BANNER)
                    # # 注: 网页端在直播间标题下面的横幅, 例如 限时任务 等
                    # contentdata = json.loads(content)['data']
                    # widget_list = contentdata['widget_list']
                    # print(widget_list)
                    pass
                elif json.loads(content)['cmd'] == "INTERACT_WORD":
                    # # 用户交互消息(INTERACT_WORD)
                    # # 注: 有用户进入直播间、关注主播、分享直播间时触发
                    # contentdata = json.loads(content)['data']
                    # tfo = "❓进入直播间或关注消息"
                    # if contentdata['msg_type'] == 1:
                    #     tfo = "🏠进入直播间"
                    # elif contentdata['msg_type'] == 2:
                    #     tfo = "⭐关注直播间"
                    # ufo = contentdata['uname']
                    # mfo = ""
                    # if contentdata['fans_medal']:
                    #     fmedal = contentdata['fans_medal']
                    #     mfo = f"【{fmedal['medal_name']}|{fmedal['medal_level']}】"
                    # wfo = ''
                    # try:
                    #     if json.loads(content)['data']['uinfo']['wealth']['level']:
                    #         wfo = f"[{json.loads(content)['data']['uinfo']['wealth']['level']}]"
                    # except:
                    #     pass
                    # print(f"{tfo}：\t{wfo}{mfo}{ufo}")
                    pass
                elif json.loads(content)['cmd'] == "INTERACT_WORD_V2":
                    # # 用户交互消息【加密】
                    # contentdata = json.loads(content)['data']
                    # pb = contentdata['pb']
                    # print("INTERACT_WORD_V2", iwv_decoder.decode_with_protobuf(pb))
                    pass
                elif json.loads(content)['cmd'] == "VOICE_JOIN_ROOM_COUNT_INFO":
                    # # ?语音加入房间计数信息
                    # contentdata = json.loads(content)['data']
                    # print("语音加入房间计数信息", contentdata)
                    pass
                elif json.loads(content)['cmd'] == "VOICE_JOIN_LIST":
                    # # ?语音加入列表
                    # contentdata = json.loads(content)['data']
                    # print("语音加入列表", contentdata)
                    pass
                elif json.loads(content)['cmd'] == "PREPARING":
                    # # 主播准备中 (PREPARING)
                    # contentdata = json.loads(content)
                    # print(contentdata)
                    pass
                elif json.loads(content)['cmd'] == "LIKE_INFO_V3_CLICK":
                    # # 直播间用户点赞 (LIKE_INFO_V3_CLICK)
                    # contentdata = json.loads(content)['data']
                    # tfo = contentdata['like_text']
                    # ufo = contentdata['uname']
                    # mfo = ""
                    # if contentdata['fans_medal']:
                    #     fmedal = contentdata['fans_medal']
                    #     mfo = f"【{fmedal['medal_name']}|{fmedal['guard_level']}】"
                    # wfo = ''
                    # try:
                    #     if contentdata['uinfo']['wealth']['level']:
                    #         wfo = f"[{contentdata['uinfo']['wealth']['level']}]"
                    # except:
                    #     pass
                    # print(f"👍点赞：\t{wfo}{mfo}{ufo}\t{tfo}")
                    pass
                elif json.loads(content)['cmd'] == "LIKE_INFO_V3_UPDATE":
                    # # 直播间点赞数更新 (LIKE_INFO_V3_UPDATE)
                    # contentdata = json.loads(content)['data']
                    # print(f"👍🔢点赞数：\t{contentdata['click_count']}")
                    pass
                elif json.loads(content)['cmd'] == "ONLINE_RANK_COUNT":
                    # # 直播间高能用户数量 (ONLINE_RANK_COUNT)
                    # contentdata = json.loads(content)['data']
                    # print(f"🧑🔢高能用户数：\t{contentdata['count']}")
                    pass
                elif json.loads(content)['cmd'] == "ONLINE_RANK_V2":
                    # # 直播间高能榜(ONLINE_RANK_V2)
                    # # 注: 直播间高能用户数据刷新
                    # contentdata = json.loads(content)['data']
                    # high_energy_users_in_the_live_streaming_room_list = contentdata["list"]
                    # """
                    # 在直播间高能用户中的用户信息
                    # """
                    # rank_type = contentdata["rank_type"]
                    # """
                    # 待调查
                    # """
                    # print(high_energy_users_in_the_live_streaming_room_list, rank_type)
                    pass
                elif json.loads(content)['cmd'] == "ONLINE_RANK_V3":
                    # # 直播间高能用户相关【加密】
                    # contentdata = json.loads(content)['data']
                    # pb = contentdata['pb']
                    # print("ONLINE_RANK_V3", orv3decoder.decode_with_protobuf(pb))
                    pass
                elif json.loads(content)['cmd'] == "RANK_CHANGED":
                    # # 榜单排名
                    # contentdata = json.loads(content)['data']
                    # print("RANK_CHANGED", contentdata)
                    pass
                elif json.loads(content)['cmd'] == "RANK_CHANGED_V2":
                    # # 榜单排名
                    # contentdata = json.loads(content)['data']
                    # print("RANK_CHANGED_V2", contentdata)
                    pass
                elif json.loads(content)['cmd'] == "WATCHED_CHANGE":
                    # # 直播间看过人数 (WATCHED_CHANGE)
                    # # 注: 当前直播历史观众数量, 可替代人气
                    # contentdata = json.loads(content)['data']
                    # print(f"👀🔢直播间看过人数：\t{contentdata['num']}|\t{contentdata['text_large']}")
                    pass
                elif json.loads(content)['cmd'] == "MESSAGEBOX_USER_GAIN_MEDAL":
                    # # 获得粉丝勋章 (MESSAGEBOX_USER_GAIN_MEDAL)
                    # # 获得时下发。
                    # contentdata = json.loads(content)['data']
                    # print(contentdata)
                    pass
                elif json.loads(content)['cmd'] == "MESSAGEBOX_USER_MEDAL_CHANGE":
                    # # 粉丝勋章更新 (MESSAGEBOX_USER_MEDAL_CHANGE)
                    # # 升级或点亮时下发
                    # contentdata = json.loads(content)['data']
                    # print(contentdata)
                    pass
                elif json.loads(content)['cmd'] == "STOP_LIVE_ROOM_LIST":
                    # # 下播的直播间 (STOP_LIVE_ROOM_LIST)
                    # # 注: 估计是更新关注的主播直播状态的
                    # contentdata = json.loads(content)['data']
                    # stop_live_room_list = contentdata['room_id_list']
                    # print(stop_live_room_list)
                    pass
                elif json.loads(content)['cmd'] == "NOTICE_MSG":
                    # # 通知消息
                    # contentdata = json.loads(content)
                    # print(contentdata)
                    pass
                elif json.loads(content)['cmd'] == "LIKE_INFO_V3_NOTICE":
                    # # 通知消息
                    # contentdata = json.loads(content)['content_segments']['data']
                    # content_segments_font_color = contentdata['content_segments']['font_color']
                    # content_segments_text = contentdata['content_segments']['text']
                    # content_segments_type = contentdata['content_segments']['type']
                    # print(content_segments_font_color, content_segments_text, content_segments_type)
                    pass
                elif json.loads(content)['cmd'] == "ENTRY_EFFECT":
                    # # 用户进场特效 (ENTRY_EFFECT)
                    # # 注: 有进场特效的用户进入直播间
                    # contentdata = json.loads(content)['data']
                    # print(contentdata)
                    pass
                elif json.loads(content)['cmd'] == "ENTRY_EFFECT_MUST_RECEIVE":
                    # # 必须接受的用户进场特效 (ENTRY_EFFECT_MUST_RECEIVE)
                    # # 注: 在部分主播进入自己的直播间时下发。
                    # contentdata = json.loads(content)['data']
                    # print(contentdata)
                    pass
                elif json.loads(content)['cmd'] == "ROOM_REAL_TIME_MESSAGE_UPDATE":
                    # # 主播信息更新 (ROOM_REAL_TIME_MESSAGE_UPDATE)
                    # contentdata = json.loads(content)['data']
                    # print(contentdata)
                    pass
                elif json.loads(content)['cmd'] == "master_qn_strategy_chg":
                    # # ???
                    # contentdata = json.loads(content)['data']  # 字符串'{"mtime":1758875819,"scatter":[0,300]}'
                    # contentdata = json.loads(contentdata)
                    # mtime = contentdata["mtime"]
                    # """
                    # ?
                    # """
                    # scatter = contentdata["scatter"]
                    # """
                    # ?
                    # """
                    # print(mtime, scatter)
                    pass
                elif json.loads(content)['cmd'] == "LIVE_ROOM_TOAST_MESSAGE":
                    # # ?视频连线
                    # contentdata = json.loads(content)['data']
                    # print(contentdata)
                    pass
                else:
                    # print("❌未收录：", json.loads(content)['cmd'])
                    # contentdata = json.loads(content)
                    # print(contentdata)
                    pass

            if len(byte_buffer) > package_len:
                self.unpack(byte_buffer[package_len:])

        def stop(self):
            """优雅停止连接"""
            self.danmu_start_is = False
            self.danmu_working_is = False
            print("正在停止弹幕客户端...")

        def start(self):
            try:
                asyncio.run(self.connect())
            except KeyboardInterrupt:
                print("用户中断程序")
                self.stop()
            except Exception as e:
                print(f"程序运行异常: {e}")
                self.stop()


if __name__ == "__main__":
    from function.Input.DanMu.Danmu import room_id

    BULC = BilibiliUserConfigManager(Path('../../cookies/config.json'))
    cookies = BULC.get_user_cookies()['data']
    Headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'cookie': dict_to_cookie_string(cookies)
    }

    dm = Danmu(Headers)
    cdm = dm.connect_room(room_id)

    try:
        cdm.start()
    except KeyboardInterrupt:
        print("程序被用户中断")
        cdm.stop()