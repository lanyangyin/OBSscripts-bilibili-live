import asyncio
import json
import pprint
import zlib
from pathlib import Path
from typing import Optional
from function.api.Authentication.Wbi.get_danmu_info import WbiSigna
from function.tools.parse_cookie import parse_cookie
from function.api.Special.Get.get_user_live_info import BilibiliCSRFAuthenticator
from function.tools.dict_to_cookie_string import dict_to_cookie_string
from function.tools.BilibiliUserConfigManager import BilibiliUserConfigManager

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
            async with websockets.connect(self.url) as ws:
                await self.on_open(ws)
                while self.danmu_start_is:
                    self.danmu_working_is = True
                    message = await ws.recv()
                    await self.on_message(message)
                self.danmu_working_is = False

        async def on_open(self, ws):
            print("Connected to server...")
            await ws.send(self.pack(self.auth_body, 7))
            asyncio.create_task(self.send_heartbeat(ws))  # 这里不能加await

        async def send_heartbeat(self, ws):
            while True:
                await ws.send(self.pack(None, 2))
                await asyncio.sleep(self.HEARTBEAT_INTERVAL)

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
            package_len = int.from_bytes(byte_buffer[0:4], 'big')
            head_length = int.from_bytes(byte_buffer[4:6], 'big')
            prot_ver = int.from_bytes(byte_buffer[6:8], 'big')
            opt_code = int.from_bytes(byte_buffer[8:12], 'big')

            content_bytes = byte_buffer[16:package_len]
            if prot_ver == self.VERSION_ZIP:
                content_bytes = zlib.decompress(content_bytes)
                self.unpack(content_bytes)
                return

            content = content_bytes.decode('utf-8')
            if opt_code == 8:  # AUTH_REPLY
                print(f"身份验证回复: {content}\n")
            elif opt_code == 5:  # SEND_SMS_REPLY
                # if content not in self.saved_danmudata:
                #     self.saved_danmudata.add(content)
                #     # print(f"Danmu message at {datetime.datetime.now()}: {content}")
                if json.loads(content)['cmd'] == "DANMU_MSG":
                    pass
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
                    print(f"{wfo}{mfo}{ufo}：{afo}{tfo}")
                elif json.loads(content)['cmd'] == "WIDGET_BANNER":
                    pass
                elif json.loads(content)['cmd'] == "INTERACT_WORD":
                    pass
                    contentdata = json.loads(content)['data']
                    # pprint.pprint(contentdata)
                    tfo = "进入直播间或关注消息"
                    if contentdata['msg_type'] == 1:
                        tfo = "进入直播间"
                    elif contentdata['msg_type'] == 2:
                        tfo = "关注直播间"
                    ufo = contentdata['uname']
                    mfo = ""
                    if contentdata['fans_medal']:
                        fmedal = contentdata['fans_medal']
                        mfo = f"【{fmedal['medal_name']}|{fmedal['medal_level']}】"
                    wfo = ''
                    try:
                        if json.loads(content)['data']['uinfo']['wealth']['level']:
                            wfo = f"[{json.loads(content)['data']['uinfo']['wealth']['level']}]"
                    except:
                        pass
                    print(f"{tfo}：\t{wfo}{mfo}{ufo}")
                elif json.loads(content)['cmd'] == "DM_INTERACTION":
                    pass
                    contentdata = json.loads(content)['data']
                    contentdata['data'] = json.loads(contentdata['data'])
                    tfo = "连续发送弹幕或点赞"
                    if contentdata['type'] == 102:
                        tfo = ""
                        for contentdatacombo in contentdata['data']['combo'][:-1]:
                            tfo += f"热词：\t{contentdatacombo['cnt']}\t人{contentdatacombo['guide']}{contentdatacombo['content']}\n"
                        tfo += f"连续弹幕：\t{contentdata['data']['combo'][-1]['cnt']}\t人{contentdata['data']['combo'][-1]['guide']}{contentdata['data']['combo'][-1]['content']}"
                    elif contentdata['type'] == 106:
                        tfo = f"连续点赞：\t{contentdata['data']['cnt']}\t{contentdata['data']['suffix_text']}"
                    print(f"{tfo}")
                elif json.loads(content)['cmd'] == "GUARD_BUY":
                    pass
                    contentdata = json.loads(content)['data']
                    tfo = f"上舰：\t{contentdata['username']}\t购买{contentdata['num']}个\t【{contentdata['gift_name']}】"
                    print(f"{tfo}")
                elif json.loads(content)['cmd'] == "LIKE_INFO_V3_CLICK":
                    pass
                    contentdata = json.loads(content)['data']
                    tfo = contentdata['like_text']
                    ufo = contentdata['uname']
                    mfo = ""
                    if contentdata['fans_medal']:
                        fmedal = contentdata['fans_medal']
                        mfo = f"【{fmedal['medal_name']}|{fmedal['guard_level']}】"
                    wfo = ''
                    try:
                        if contentdata['uinfo']['wealth']['level']:
                            wfo = f"[{contentdata['uinfo']['wealth']['level']}]"
                    except:
                        pass
                    print(f"点赞：\t{wfo}{mfo}{ufo}\t{tfo}")
                elif json.loads(content)['cmd'] == "LIKE_INFO_V3_UPDATE":
                    contentdata = json.loads(content)['data']
                    print(f"点赞数：\t{contentdata['click_count']}")
                    pass
                elif json.loads(content)['cmd'] == "ONLINE_RANK_COUNT":
                    contentdata = json.loads(content)['data']
                    print(f"高能用户数：\t{contentdata['count']}")
                    pass
                elif json.loads(content)['cmd'] == "WATCHED_CHANGE":
                    contentdata = json.loads(content)['data']
                    print(f"直播间看过人数：\t{contentdata['num']}\t{contentdata['text_large']}")
                    pass
                elif json.loads(content)['cmd'] == "ONLINE_RANK_V2":
                    pass
                elif json.loads(content)['cmd'] == "STOP_LIVE_ROOM_LIST":
                    pass
                elif json.loads(content)['cmd'] == "PK_BATTLE_PRE_NEW":
                    pass
                elif json.loads(content)['cmd'] == "PK_BATTLE_PRE":
                    pass
                elif json.loads(content)['cmd'] == "PK_BATTLE_START":
                    pass
                elif json.loads(content)['cmd'] == "RECOMMEND_CARD":
                    pass
                elif json.loads(content)['cmd'] == "SEND_GIFT":
                    contentdata = json.loads(content)['data']
                    # pprint.pprint(contentdata)
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
                    print(f'礼物：\t{wfo}{mfo}{ufo}\t{tfo}')
                    pass
                elif json.loads(content)['cmd'] == "NOTICE_MSG":
                    pass
                else:
                    pprint.pprint("未收录：", json.loads(content)['cmd'])

            if len(byte_buffer) > package_len:
                self.unpack(byte_buffer[package_len:])

        def start(self):
            asyncio.run(self.connect())


if __name__ == "__main__":
    # 示例用法
    BULC = BilibiliUserConfigManager(Path('../../cookies/config.json'))
    cookies = BULC.get_user_cookies()['data']
    print(cookies)
    Headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'cookie': dict_to_cookie_string(cookies)
    }
    dm = Danmu(Headers)
    cdm = dm.connect_room(32439613)
    cdm.start()