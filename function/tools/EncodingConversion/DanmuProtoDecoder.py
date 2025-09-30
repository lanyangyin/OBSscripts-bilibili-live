import base64
import json
from function.tools.EncodingConversion.str_to_module import str_to_module

class DanmuProtoDecoder:
    def __init__(self):
        self.online_rank_v3_pb2 = """
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    6,
    32,
    1,
    '',
    'bilibili/live/decode_online_rank_v3/v1.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\\n,bilibili/live/decode_online_rank_v3/v1.proto\\x12\\x17\\x62ilibili.live.rankdb.v1\\")\\n\\x0b\\x41\\x63\\x63ountInfo\\x12\\x0c\\n\\x04name\\x18\\x01 \\x01(\\t\\x12\\x0c\\n\\x04\\x66\\x61\\x63\\x65\\x18\\x02 \\x01(\\t\\"\\x9a\\x02\\n\\x04\\x42\\x61se\\x12\\x0c\\n\\x04name\\x18\\x01 \\x01(\\t\\x12\\x0c\\n\\x04\\x66\\x61\\x63\\x65\\x18\\x02 \\x01(\\t\\x12\\x12\\n\\nname_color\\x18\\x03 \\x01(\\x05\\x12\\x12\\n\\nis_mystery\\x18\\x04 \\x01(\\x08\\x12=\\n\\x0erisk_ctrl_info\\x18\\x05 \\x01(\\x0b\\x32%.bilibili.live.rankdb.v1.RiskCtrlInfo\\x12\\x39\\n\\x0borigin_info\\x18\\x06 \\x01(\\x0b\\x32$.bilibili.live.rankdb.v1.AccountInfo\\x12<\\n\\rofficial_info\\x18\\x07 \\x01(\\x0b\\x32%.bilibili.live.rankdb.v1.OfficialInfo\\x12\\x16\\n\\x0ename_color_str\\x18\\x08 \\x01(\\t\\"\\xb2\\x01\\n\\nBaseOption\\x12\\x14\\n\\x0cneed_mystery\\x18\\x01 \\x01(\\x08\\x12\\x34\\n\\trisk_ctrl\\x18\\x02 \\x01(\\x0b\\x32!.bilibili.live.rankdb.v1.RiskCtrl\\x12=\\n\\x0eroom_anon_ctrl\\x18\\x03 \\x01(\\x0b\\x32%.bilibili.live.rankdb.v1.RoomAnonCtrl\\x12\\x19\\n\\x11risk_ctrl_handles\\x18\\x04 \\x03(\\x05\\"+\\n\\x05Guard\\x12\\r\\n\\x05level\\x18\\x01 \\x01(\\x03\\x12\\x13\\n\\x0b\\x65xpired_str\\x18\\x02 \\x01(\\t\\"&\\n\\x0bGuardLeader\\x12\\x17\\n\\x0fis_guard_leader\\x18\\x01 \\x01(\\x08\\"2\\n\\x11GuardLeaderOption\\x12\\x0c\\n\\x04ruid\\x18\\x01 \\x01(\\x03\\x12\\x0f\\n\\x07room_id\\x18\\x02 \\x01(\\x03\\"K\\n\\x0bGuardOption\\x12\\x0c\\n\\x04ruid\\x18\\x01 \\x01(\\x03\\x12\\x17\\n\\x0fuse_local_cache\\x18\\x02 \\x01(\\x08\\x12\\x15\\n\\rstrong_depend\\x18\\x03 \\x01(\\x08\\"\\xce\\x03\\n\\x05Medal\\x12\\x0c\\n\\x04name\\x18\\x01 \\x01(\\t\\x12\\r\\n\\x05level\\x18\\x02 \\x01(\\x03\\x12\\x13\\n\\x0b\\x63olor_start\\x18\\x03 \\x01(\\x03\\x12\\x11\\n\\tcolor_end\\x18\\x04 \\x01(\\x03\\x12\\x14\\n\\x0c\\x63olor_border\\x18\\x05 \\x01(\\x03\\x12\\r\\n\\x05\\x63olor\\x18\\x06 \\x01(\\x03\\x12\\n\\n\\x02id\\x18\\x07 \\x01(\\x03\\x12\\x33\\n\\x03typ\\x18\\x08 \\x01(\\x0e\\x32&.bilibili.live.rankdb.v1.HaveMedalType\\x12\\x10\\n\\x08is_light\\x18\\t \\x01(\\x03\\x12\\x0c\\n\\x04ruid\\x18\\n \\x01(\\x03\\x12\\x13\\n\\x0bguard_level\\x18\\x0b \\x01(\\x03\\x12\\r\\n\\x05score\\x18\\x0c \\x01(\\x03\\x12\\x12\\n\\nguard_icon\\x18\\r \\x01(\\t\\x12\\x12\\n\\nhonor_icon\\x18\\x0e \\x01(\\t\\x12\\x1c\\n\\x14v2_medal_color_start\\x18\\x0f \\x01(\\t\\x12\\x1a\\n\\x12v2_medal_color_end\\x18\\x10 \\x01(\\t\\x12\\x1d\\n\\x15v2_medal_color_border\\x18\\x11 \\x01(\\t\\x12\\x1b\\n\\x13v2_medal_color_text\\x18\\x12 \\x01(\\t\\x12\\x1c\\n\\x14v2_medal_color_level\\x18\\x13 \\x01(\\t\\x12\\x1a\\n\\x12user_receive_count\\x18\\x14 \\x01(\\x03\\"\\x8b\\x01\\n\\x0bMedalOption\\x12/\\n\\x03typ\\x18\\x01 \\x01(\\x0e\\x32\\".bilibili.live.rankdb.v1.MedalType\\x12\\x0c\\n\\x04ruid\\x18\\x02 \\x01(\\x03\\x12\\x12\\n\\nneed_guard\\x18\\x03 \\x01(\\x08\\x12\\x15\\n\\rstrong_depend\\x18\\x04 \\x01(\\x08\\x12\\x12\\n\\nneed_group\\x18\\x05 \\x01(\\x08\\"G\\n\\x0cOfficialInfo\\x12\\x0c\\n\\x04role\\x18\\x01 \\x01(\\x03\\x12\\r\\n\\x05title\\x18\\x02 \\x01(\\t\\x12\\x0c\\n\\x04\\x64\\x65sc\\x18\\x03 \\x01(\\t\\x12\\x0c\\n\\x04type\\x18\\x04 \\x01(\\x03\\"T\\n\\x08RiskCtrl\\x12\\x0f\\n\\x07room_id\\x18\\x01 \\x01(\\x03\\x12\\x37\\n\\x06policy\\x18\\x02 \\x01(\\x0e\\x32\\'.bilibili.live.rankdb.v1.RiskPolicyEnum\\"*\\n\\x0cRiskCtrlInfo\\x12\\x0c\\n\\x04name\\x18\\x01 \\x01(\\t\\x12\\x0c\\n\\x04\\x66\\x61\\x63\\x65\\x18\\x02 \\x01(\\t\\"G\\n\\x0cRoomAnonCtrl\\x12\\x37\\n\\x04type\\x18\\x01 \\x01(\\x0e\\x32).bilibili.live.rankdb.v1.RoomAnonTypeEnum\\"7\\n\\x05Title\\x12\\x18\\n\\x10old_title_css_id\\x18\\x01 \\x01(\\t\\x12\\x14\\n\\x0ctitle_css_id\\x18\\x02 \\x01(\\t\\"5\\n\\x0bTitleOption\\x12\\x0f\\n\\x07room_id\\x18\\x01 \\x01(\\x03\\x12\\x15\\n\\rstrong_depend\\x18\\x02 \\x01(\\x08\\".\\n\\rUserHeadFrame\\x12\\n\\n\\x02id\\x18\\x01 \\x01(\\x03\\x12\\x11\\n\\tframe_img\\x18\\x02 \\x01(\\t\\"\\xfb\\x02\\n\\x08UserInfo\\x12\\x0b\\n\\x03uid\\x18\\x01 \\x01(\\x03\\x12+\\n\\x04\\x62\\x61se\\x18\\x02 \\x01(\\x0b\\x32\\x1d.bilibili.live.rankdb.v1.Base\\x12-\\n\\x05medal\\x18\\x03 \\x01(\\x0b\\x32\\x1e.bilibili.live.rankdb.v1.Medal\\x12/\\n\\x06wealth\\x18\\x04 \\x01(\\x0b\\x32\\x1f.bilibili.live.rankdb.v1.Wealth\\x12-\\n\\x05title\\x18\\x05 \\x01(\\x0b\\x32\\x1e.bilibili.live.rankdb.v1.Title\\x12-\\n\\x05guard\\x18\\x06 \\x01(\\x0b\\x32\\x1e.bilibili.live.rankdb.v1.Guard\\x12;\\n\\x0buhead_frame\\x18\\x07 \\x01(\\x0b\\x32&.bilibili.live.rankdb.v1.UserHeadFrame\\x12:\\n\\x0cguard_leader\\x18\\x08 \\x01(\\x0b\\x32$.bilibili.live.rankdb.v1.GuardLeader\\",\\n\\x06Wealth\\x12\\r\\n\\x05level\\x18\\x01 \\x01(\\x03\\x12\\x13\\n\\x0b\\x64m_icon_key\\x18\\x02 \\x01(\\t\\"U\\n\\x0cWealthOption\\x12\\x0e\\n\\x06roomid\\x18\\x01 \\x01(\\x03\\x12\\x10\\n\\x08view_uid\\x18\\x02 \\x01(\\x03\\x12\\x0c\\n\\x04ruid\\x18\\x03 \\x01(\\x03\\x12\\x15\\n\\rstrong_depend\\x18\\x04 \\x01(\\x08\\"\\x86\\x03\\n\\x11GoldRankBroadcast\\x12\\x11\\n\\trank_type\\x18\\x01 \\x01(\\t\\x12M\\n\\x04list\\x18\\x02 \\x03(\\x0b\\x32?.bilibili.live.rankdb.v1.GoldRankBroadcast.GoldRankBrodcastItem\\x12T\\n\\x0bonline_list\\x18\\x03 \\x03(\\x0b\\x32?.bilibili.live.rankdb.v1.GoldRankBroadcast.GoldRankBrodcastItem\\x1a\\xb8\\x01\\n\\x14GoldRankBrodcastItem\\x12\\x0b\\n\\x03uid\\x18\\x01 \\x01(\\x03\\x12\\x0c\\n\\x04\\x66\\x61\\x63\\x65\\x18\\x02 \\x01(\\t\\x12\\r\\n\\x05score\\x18\\x03 \\x01(\\t\\x12\\r\\n\\x05uname\\x18\\x04 \\x01(\\t\\x12\\x0c\\n\\x04rank\\x18\\x05 \\x01(\\x03\\x12\\x13\\n\\x0bguard_level\\x18\\x06 \\x01(\\x03\\x12\\x12\\n\\nis_mystery\\x18\\x07 \\x01(\\x08\\x12\\x30\\n\\x05uinfo\\x18\\x08 \\x01(\\x0b\\x32!.bilibili.live.rankdb.v1.UserInfo*2\\n\\rHaveMedalType\\x12\\x10\\n\\x0cMedal_Common\\x10\\x00\\x12\\x0f\\n\\x0bMedal_Group\\x10\\x01*+\\n\\tMedalType\\x12\\x0e\\n\\nMedal_Wear\\x10\\x00\\x12\\x0e\\n\\nMedal_Spec\\x10\\x01*X\\n\\x0eRiskPolicyEnum\\x12\\r\\n\\tRP_NORMAL\\x10\\x00\\x12\\r\\n\\tRP_POLICY\\x10\\x01\\x12\\x0e\\n\\nRP_SILENCE\\x10\\x02\\x12\\n\\n\\x06RP_CNY\\x10\\x03\\x12\\x0c\\n\\x08RP_BIGEV\\x10\\x04*3\\n\\x10RoomAnonTypeEnum\\x12\\n\\n\\x06RA_ALL\\x10\\x00\\x12\\x13\\n\\x0fRA_With_Subject\\x10\\x01\\x62\\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'bilibili.live.decode_online_rank_v3.v1_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_HAVEMEDALTYPE']._serialized_start=2747
  _globals['_HAVEMEDALTYPE']._serialized_end=2797
  _globals['_MEDALTYPE']._serialized_start=2799
  _globals['_MEDALTYPE']._serialized_end=2842
  _globals['_RISKPOLICYENUM']._serialized_start=2844
  _globals['_RISKPOLICYENUM']._serialized_end=2932
  _globals['_ROOMANONTYPEENUM']._serialized_start=2934
  _globals['_ROOMANONTYPEENUM']._serialized_end=2985
  _globals['_ACCOUNTINFO']._serialized_start=73
  _globals['_ACCOUNTINFO']._serialized_end=114
  _globals['_BASE']._serialized_start=117
  _globals['_BASE']._serialized_end=399
  _globals['_BASEOPTION']._serialized_start=402
  _globals['_BASEOPTION']._serialized_end=580
  _globals['_GUARD']._serialized_start=582
  _globals['_GUARD']._serialized_end=625
  _globals['_GUARDLEADER']._serialized_start=627
  _globals['_GUARDLEADER']._serialized_end=665
  _globals['_GUARDLEADEROPTION']._serialized_start=667
  _globals['_GUARDLEADEROPTION']._serialized_end=717
  _globals['_GUARDOPTION']._serialized_start=719
  _globals['_GUARDOPTION']._serialized_end=794
  _globals['_MEDAL']._serialized_start=797
  _globals['_MEDAL']._serialized_end=1259
  _globals['_MEDALOPTION']._serialized_start=1262
  _globals['_MEDALOPTION']._serialized_end=1401
  _globals['_OFFICIALINFO']._serialized_start=1403
  _globals['_OFFICIALINFO']._serialized_end=1474
  _globals['_RISKCTRL']._serialized_start=1476
  _globals['_RISKCTRL']._serialized_end=1560
  _globals['_RISKCTRLINFO']._serialized_start=1562
  _globals['_RISKCTRLINFO']._serialized_end=1604
  _globals['_ROOMANONCTRL']._serialized_start=1606
  _globals['_ROOMANONCTRL']._serialized_end=1677
  _globals['_TITLE']._serialized_start=1679
  _globals['_TITLE']._serialized_end=1734
  _globals['_TITLEOPTION']._serialized_start=1736
  _globals['_TITLEOPTION']._serialized_end=1789
  _globals['_USERHEADFRAME']._serialized_start=1791
  _globals['_USERHEADFRAME']._serialized_end=1837
  _globals['_USERINFO']._serialized_start=1840
  _globals['_USERINFO']._serialized_end=2219
  _globals['_WEALTH']._serialized_start=2221
  _globals['_WEALTH']._serialized_end=2265
  _globals['_WEALTHOPTION']._serialized_start=2267
  _globals['_WEALTHOPTION']._serialized_end=2352
  _globals['_GOLDRANKBROADCAST']._serialized_start=2355
  _globals['_GOLDRANKBROADCAST']._serialized_end=2745
  _globals['_GOLDRANKBROADCAST_GOLDRANKBRODCASTITEM']._serialized_start=2561
  _globals['_GOLDRANKBROADCAST_GOLDRANKBRODCASTITEM']._serialized_end=2745
# @@protoc_insertion_point(module_scope)
"""
        self.interact_word_v2_pb2 = """
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    6,
    32,
    1,
    '',
    'bilibili/live/decode_interact_word_v2/v1.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\\n.bilibili/live/decode_interact_word_v2/v1.proto\\x12(bilibili.live.decode_interact_word_v2.v1\\"E\\n\\x0fGroupMedalBrief\\x12\\x10\\n\\x08medal_id\\x18\\x01 \\x01(\\x03\\x12\\x0c\\n\\x04name\\x18\\x02 \\x01(\\t\\x12\\x12\\n\\nis_lighted\\x18\\x03 \\x01(\\x03\\")\\n\\x0b\\x41\\x63\\x63ountInfo\\x12\\x0c\\n\\x04name\\x18\\x01 \\x01(\\t\\x12\\x0c\\n\\x04\\x66\\x61\\x63\\x65\\x18\\x02 \\x01(\\t\\"\\xcd\\x02\\n\\x04\\x42\\x61se\\x12\\x0c\\n\\x04name\\x18\\x01 \\x01(\\t\\x12\\x0c\\n\\x04\\x66\\x61\\x63\\x65\\x18\\x02 \\x01(\\t\\x12\\x12\\n\\nname_color\\x18\\x03 \\x01(\\x05\\x12\\x12\\n\\nis_mystery\\x18\\x04 \\x01(\\x08\\x12N\\n\\x0erisk_ctrl_info\\x18\\x05 \\x01(\\x0b\\x32\\x36.bilibili.live.decode_interact_word_v2.v1.RiskCtrlInfo\\x12J\\n\\x0borigin_info\\x18\\x06 \\x01(\\x0b\\x32\\x35.bilibili.live.decode_interact_word_v2.v1.AccountInfo\\x12M\\n\\rofficial_info\\x18\\x07 \\x01(\\x0b\\x32\\x36.bilibili.live.decode_interact_word_v2.v1.OfficialInfo\\x12\\x16\\n\\x0ename_color_str\\x18\\x08 \\x01(\\t\\"\\xd4\\x01\\n\\nBaseOption\\x12\\x14\\n\\x0cneed_mystery\\x18\\x01 \\x01(\\x08\\x12\\x45\\n\\trisk_ctrl\\x18\\x02 \\x01(\\x0b\\x32\\x32.bilibili.live.decode_interact_word_v2.v1.RiskCtrl\\x12N\\n\\x0eroom_anon_ctrl\\x18\\x03 \\x01(\\x0b\\x32\\x36.bilibili.live.decode_interact_word_v2.v1.RoomAnonCtrl\\x12\\x19\\n\\x11risk_ctrl_handles\\x18\\x04 \\x03(\\x05\\"+\\n\\x05Guard\\x12\\r\\n\\x05level\\x18\\x01 \\x01(\\x03\\x12\\x13\\n\\x0b\\x65xpired_str\\x18\\x02 \\x01(\\t\\"&\\n\\x0bGuardLeader\\x12\\x17\\n\\x0fis_guard_leader\\x18\\x01 \\x01(\\x08\\"2\\n\\x11GuardLeaderOption\\x12\\x0c\\n\\x04ruid\\x18\\x01 \\x01(\\x03\\x12\\x0f\\n\\x07room_id\\x18\\x02 \\x01(\\x03\\"K\\n\\x0bGuardOption\\x12\\x0c\\n\\x04ruid\\x18\\x01 \\x01(\\x03\\x12\\x17\\n\\x0fuse_local_cache\\x18\\x02 \\x01(\\x08\\x12\\x15\\n\\rstrong_depend\\x18\\x03 \\x01(\\x08\\"\\xdf\\x03\\n\\x05Medal\\x12\\x0c\\n\\x04name\\x18\\x01 \\x01(\\t\\x12\\r\\n\\x05level\\x18\\x02 \\x01(\\x03\\x12\\x13\\n\\x0b\\x63olor_start\\x18\\x03 \\x01(\\x03\\x12\\x11\\n\\tcolor_end\\x18\\x04 \\x01(\\x03\\x12\\x14\\n\\x0c\\x63olor_border\\x18\\x05 \\x01(\\x03\\x12\\r\\n\\x05\\x63olor\\x18\\x06 \\x01(\\x03\\x12\\n\\n\\x02id\\x18\\x07 \\x01(\\x03\\x12\\x44\\n\\x03typ\\x18\\x08 \\x01(\\x0e\\x32\\x37.bilibili.live.decode_interact_word_v2.v1.HaveMedalType\\x12\\x10\\n\\x08is_light\\x18\\t \\x01(\\x03\\x12\\x0c\\n\\x04ruid\\x18\\n \\x01(\\x03\\x12\\x13\\n\\x0bguard_level\\x18\\x0b \\x01(\\x03\\x12\\r\\n\\x05score\\x18\\x0c \\x01(\\x03\\x12\\x12\\n\\nguard_icon\\x18\\r \\x01(\\t\\x12\\x12\\n\\nhonor_icon\\x18\\x0e \\x01(\\t\\x12\\x1c\\n\\x14v2_medal_color_start\\x18\\x0f \\x01(\\t\\x12\\x1a\\n\\x12v2_medal_color_end\\x18\\x10 \\x01(\\t\\x12\\x1d\\n\\x15v2_medal_color_border\\x18\\x11 \\x01(\\t\\x12\\x1b\\n\\x13v2_medal_color_text\\x18\\x12 \\x01(\\t\\x12\\x1c\\n\\x14v2_medal_color_level\\x18\\x13 \\x01(\\t\\x12\\x1a\\n\\x12user_receive_count\\x18\\x14 \\x01(\\x03\\"\\x9c\\x01\\n\\x0bMedalOption\\x12@\\n\\x03typ\\x18\\x01 \\x01(\\x0e\\x32\\x33.bilibili.live.decode_interact_word_v2.v1.MedalType\\x12\\x0c\\n\\x04ruid\\x18\\x02 \\x01(\\x03\\x12\\x12\\n\\nneed_guard\\x18\\x03 \\x01(\\x08\\x12\\x15\\n\\rstrong_depend\\x18\\x04 \\x01(\\x08\\x12\\x12\\n\\nneed_group\\x18\\x05 \\x01(\\x08\\"G\\n\\x0cOfficialInfo\\x12\\x0c\\n\\x04role\\x18\\x01 \\x01(\\x03\\x12\\r\\n\\x05title\\x18\\x02 \\x01(\\t\\x12\\x0c\\n\\x04\\x64\\x65sc\\x18\\x03 \\x01(\\t\\x12\\x0c\\n\\x04type\\x18\\x04 \\x01(\\x03\\"e\\n\\x08RiskCtrl\\x12\\x0f\\n\\x07room_id\\x18\\x01 \\x01(\\x03\\x12H\\n\\x06policy\\x18\\x02 \\x01(\\x0e\\x32\\x38.bilibili.live.decode_interact_word_v2.v1.RiskPolicyEnum\\"*\\n\\x0cRiskCtrlInfo\\x12\\x0c\\n\\x04name\\x18\\x01 \\x01(\\t\\x12\\x0c\\n\\x04\\x66\\x61\\x63\\x65\\x18\\x02 \\x01(\\t\\"X\\n\\x0cRoomAnonCtrl\\x12H\\n\\x04type\\x18\\x01 \\x01(\\x0e\\x32:.bilibili.live.decode_interact_word_v2.v1.RoomAnonTypeEnum\\"7\\n\\x05Title\\x12\\x18\\n\\x10old_title_css_id\\x18\\x01 \\x01(\\t\\x12\\x14\\n\\x0ctitle_css_id\\x18\\x02 \\x01(\\t\\"5\\n\\x0bTitleOption\\x12\\x0f\\n\\x07room_id\\x18\\x01 \\x01(\\x03\\x12\\x15\\n\\rstrong_depend\\x18\\x02 \\x01(\\x08\\".\\n\\rUserHeadFrame\\x12\\n\\n\\x02id\\x18\\x01 \\x01(\\x03\\x12\\x11\\n\\tframe_img\\x18\\x02 \\x01(\\t\\"\\xf2\\x03\\n\\x08UserInfo\\x12\\x0b\\n\\x03uid\\x18\\x01 \\x01(\\x03\\x12<\\n\\x04\\x62\\x61se\\x18\\x02 \\x01(\\x0b\\x32..bilibili.live.decode_interact_word_v2.v1.Base\\x12>\\n\\x05medal\\x18\\x03 \\x01(\\x0b\\x32/.bilibili.live.decode_interact_word_v2.v1.Medal\\x12@\\n\\x06wealth\\x18\\x04 \\x01(\\x0b\\x32\\x30.bilibili.live.decode_interact_word_v2.v1.Wealth\\x12>\\n\\x05title\\x18\\x05 \\x01(\\x0b\\x32/.bilibili.live.decode_interact_word_v2.v1.Title\\x12>\\n\\x05guard\\x18\\x06 \\x01(\\x0b\\x32/.bilibili.live.decode_interact_word_v2.v1.Guard\\x12L\\n\\x0buhead_frame\\x18\\x07 \\x01(\\x0b\\x32\\x37.bilibili.live.decode_interact_word_v2.v1.UserHeadFrame\\x12K\\n\\x0cguard_leader\\x18\\x08 \\x01(\\x0b\\x32\\x35.bilibili.live.decode_interact_word_v2.v1.GuardLeader\\",\\n\\x06Wealth\\x12\\r\\n\\x05level\\x18\\x01 \\x01(\\x03\\x12\\x13\\n\\x0b\\x64m_icon_key\\x18\\x02 \\x01(\\t\\"U\\n\\x0cWealthOption\\x12\\x0e\\n\\x06roomid\\x18\\x01 \\x01(\\x03\\x12\\x10\\n\\x08view_uid\\x18\\x02 \\x01(\\x03\\x12\\x0c\\n\\x04ruid\\x18\\x03 \\x01(\\x03\\x12\\x15\\n\\rstrong_depend\\x18\\x04 \\x01(\\x08\\"\\xc8\\n\\n\\x0cInteractWord\\x12\\x0b\\n\\x03uid\\x18\\x01 \\x01(\\x03\\x12\\r\\n\\x05uname\\x18\\x02 \\x01(\\t\\x12\\x13\\n\\x0buname_color\\x18\\x03 \\x01(\\t\\x12\\x12\\n\\nidentities\\x18\\x04 \\x03(\\x03\\x12\\x10\\n\\x08msg_type\\x18\\x05 \\x01(\\x03\\x12\\x0e\\n\\x06roomid\\x18\\x06 \\x01(\\x03\\x12\\x11\\n\\ttimestamp\\x18\\x07 \\x01(\\x03\\x12\\r\\n\\x05score\\x18\\x08 \\x01(\\x03\\x12X\\n\\nfans_medal\\x18\\t \\x01(\\x0b\\x32\\x44.bilibili.live.decode_interact_word_v2.v1.InteractWord.FansMedalInfo\\x12\\x11\\n\\tis_spread\\x18\\n \\x01(\\x03\\x12\\x13\\n\\x0bspread_info\\x18\\x0b \\x01(\\t\\x12]\\n\\x0c\\x63ontribution\\x18\\x0c \\x01(\\x0b\\x32G.bilibili.live.decode_interact_word_v2.v1.InteractWord.ContributionInfo\\x12\\x13\\n\\x0bspread_desc\\x18\\r \\x01(\\t\\x12\\x11\\n\\ttail_icon\\x18\\x0e \\x01(\\x03\\x12\\x14\\n\\x0ctrigger_time\\x18\\x0f \\x01(\\x03\\x12\\x16\\n\\x0eprivilege_type\\x18\\x10 \\x01(\\x03\\x12\\x16\\n\\x0e\\x63ore_user_type\\x18\\x11 \\x01(\\x03\\x12\\x11\\n\\ttail_text\\x18\\x12 \\x01(\\t\\x12\\x62\\n\\x0f\\x63ontribution_v2\\x18\\x13 \\x01(\\x0b\\x32I.bilibili.live.decode_interact_word_v2.v1.InteractWord.ContributionInfoV2\\x12N\\n\\x0bgroup_medal\\x18\\x14 \\x01(\\x0b\\x32\\x39.bilibili.live.decode_interact_word_v2.v1.GroupMedalBrief\\x12\\x12\\n\\nis_mystery\\x18\\x15 \\x01(\\x08\\x12\\x41\\n\\x05uinfo\\x18\\x16 \\x01(\\x0b\\x32\\x32.bilibili.live.decode_interact_word_v2.v1.UserInfo\\x12`\\n\\rrelation_tail\\x18\\x17 \\x01(\\x0b\\x32I.bilibili.live.decode_interact_word_v2.v1.InteractWord.UserAnchorRelation\\x1a!\\n\\x10\\x43ontributionInfo\\x12\\r\\n\\x05grade\\x18\\x01 \\x01(\\x03\\x1a\\x44\\n\\x12\\x43ontributionInfoV2\\x12\\r\\n\\x05grade\\x18\\x01 \\x01(\\x03\\x12\\x11\\n\\trank_type\\x18\\x02 \\x01(\\t\\x12\\x0c\\n\\x04text\\x18\\x03 \\x01(\\t\\x1a\\xa1\\x02\\n\\rFansMedalInfo\\x12\\x11\\n\\ttarget_id\\x18\\x01 \\x01(\\x03\\x12\\x13\\n\\x0bmedal_level\\x18\\x02 \\x01(\\x03\\x12\\x12\\n\\nmedal_name\\x18\\x03 \\x01(\\t\\x12\\x13\\n\\x0bmedal_color\\x18\\x04 \\x01(\\x03\\x12\\x19\\n\\x11medal_color_start\\x18\\x05 \\x01(\\x03\\x12\\x17\\n\\x0fmedal_color_end\\x18\\x06 \\x01(\\x03\\x12\\x1a\\n\\x12medal_color_border\\x18\\x07 \\x01(\\x03\\x12\\x12\\n\\nis_lighted\\x18\\x08 \\x01(\\x03\\x12\\x13\\n\\x0bguard_level\\x18\\t \\x01(\\x03\\x12\\x0f\\n\\x07special\\x18\\n \\x01(\\t\\x12\\x0f\\n\\x07icon_id\\x18\\x0b \\x01(\\x03\\x12\\x15\\n\\ranchor_roomid\\x18\\x0c \\x01(\\x03\\x12\\r\\n\\x05score\\x18\\r \\x01(\\x03\\x1aS\\n\\x12UserAnchorRelation\\x12\\x11\\n\\ttail_icon\\x18\\x01 \\x01(\\t\\x12\\x17\\n\\x0ftail_guide_text\\x18\\x02 \\x01(\\t\\x12\\x11\\n\\ttail_type\\x18\\x03 \\x01(\\x03*2\\n\\rHaveMedalType\\x12\\x10\\n\\x0cMedal_Common\\x10\\x00\\x12\\x0f\\n\\x0bMedal_Group\\x10\\x01*+\\n\\tMedalType\\x12\\x0e\\n\\nMedal_Wear\\x10\\x00\\x12\\x0e\\n\\nMedal_Spec\\x10\\x01*X\\n\\x0eRiskPolicyEnum\\x12\\r\\n\\tRP_NORMAL\\x10\\x00\\x12\\r\\n\\tRP_POLICY\\x10\\x01\\x12\\x0e\\n\\nRP_SILENCE\\x10\\x02\\x12\\n\\n\\x06RP_CNY\\x10\\x03\\x12\\x0c\\n\\x08RP_BIGEV\\x10\\x04*3\\n\\x10RoomAnonTypeEnum\\x12\\n\\n\\x06RA_ALL\\x10\\x00\\x12\\x13\\n\\x0fRA_With_Subject\\x10\\x01\\x62\\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'bilibili.live.decode_interact_word_v2.v1_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_HAVEMEDALTYPE']._serialized_start=4071
  _globals['_HAVEMEDALTYPE']._serialized_end=4121
  _globals['_MEDALTYPE']._serialized_start=4123
  _globals['_MEDALTYPE']._serialized_end=4166
  _globals['_RISKPOLICYENUM']._serialized_start=4168
  _globals['_RISKPOLICYENUM']._serialized_end=4256
  _globals['_ROOMANONTYPEENUM']._serialized_start=4258
  _globals['_ROOMANONTYPEENUM']._serialized_end=4309
  _globals['_GROUPMEDALBRIEF']._serialized_start=92
  _globals['_GROUPMEDALBRIEF']._serialized_end=161
  _globals['_ACCOUNTINFO']._serialized_start=163
  _globals['_ACCOUNTINFO']._serialized_end=204
  _globals['_BASE']._serialized_start=207
  _globals['_BASE']._serialized_end=540
  _globals['_BASEOPTION']._serialized_start=543
  _globals['_BASEOPTION']._serialized_end=755
  _globals['_GUARD']._serialized_start=757
  _globals['_GUARD']._serialized_end=800
  _globals['_GUARDLEADER']._serialized_start=802
  _globals['_GUARDLEADER']._serialized_end=840
  _globals['_GUARDLEADEROPTION']._serialized_start=842
  _globals['_GUARDLEADEROPTION']._serialized_end=892
  _globals['_GUARDOPTION']._serialized_start=894
  _globals['_GUARDOPTION']._serialized_end=969
  _globals['_MEDAL']._serialized_start=972
  _globals['_MEDAL']._serialized_end=1451
  _globals['_MEDALOPTION']._serialized_start=1454
  _globals['_MEDALOPTION']._serialized_end=1610
  _globals['_OFFICIALINFO']._serialized_start=1612
  _globals['_OFFICIALINFO']._serialized_end=1683
  _globals['_RISKCTRL']._serialized_start=1685
  _globals['_RISKCTRL']._serialized_end=1786
  _globals['_RISKCTRLINFO']._serialized_start=1788
  _globals['_RISKCTRLINFO']._serialized_end=1830
  _globals['_ROOMANONCTRL']._serialized_start=1832
  _globals['_ROOMANONCTRL']._serialized_end=1920
  _globals['_TITLE']._serialized_start=1922
  _globals['_TITLE']._serialized_end=1977
  _globals['_TITLEOPTION']._serialized_start=1979
  _globals['_TITLEOPTION']._serialized_end=2032
  _globals['_USERHEADFRAME']._serialized_start=2034
  _globals['_USERHEADFRAME']._serialized_end=2080
  _globals['_USERINFO']._serialized_start=2083
  _globals['_USERINFO']._serialized_end=2581
  _globals['_WEALTH']._serialized_start=2583
  _globals['_WEALTH']._serialized_end=2627
  _globals['_WEALTHOPTION']._serialized_start=2629
  _globals['_WEALTHOPTION']._serialized_end=2714
  _globals['_INTERACTWORD']._serialized_start=2717
  _globals['_INTERACTWORD']._serialized_end=4069
  _globals['_INTERACTWORD_CONTRIBUTIONINFO']._serialized_start=3589
  _globals['_INTERACTWORD_CONTRIBUTIONINFO']._serialized_end=3622
  _globals['_INTERACTWORD_CONTRIBUTIONINFOV2']._serialized_start=3624
  _globals['_INTERACTWORD_CONTRIBUTIONINFOV2']._serialized_end=3692
  _globals['_INTERACTWORD_FANSMEDALINFO']._serialized_start=3695
  _globals['_INTERACTWORD_FANSMEDALINFO']._serialized_end=3984
  _globals['_INTERACTWORD_USERANCHORRELATION']._serialized_start=3986
  _globals['_INTERACTWORD_USERANCHORRELATION']._serialized_end=4069
# @@protoc_insertion_point(module_scope)
"""

    # 更完整的解决方案：使用protobuf库编译proto文件
    def decode_online_rank_v3_protobuf(self, base64_string):
        """
        使用protobuf库完整解码（需要先编译proto文件）
        """
        # 导入编译后的模块
        online_rank_v3_pb2 = str_to_module("online_rank_v3_pb2", self.online_rank_v3_pb2)
        # 解码
        pb_data = base64.b64decode(base64_string)
        message = online_rank_v3_pb2.GoldRankBroadcast()
        message.ParseFromString(pb_data)

        # 转换为字典
        return self.protobuf_to_dict(message)

    def decode_interact_word_v2_protobuf(self, base64_string):
        """
        使用protobuf库完整解码（需要先编译proto文件）
        """
        # 导入编译后的模块
        interact_word_v2_pb2 = str_to_module("interact_word_v2_pb2", self.interact_word_v2_pb2)
        # 解码
        pb_data = base64.b64decode(base64_string)
        message = interact_word_v2_pb2.InteractWord()
        message.ParseFromString(pb_data)

        # 转换为字典
        return self.protobuf_to_dict(message)

    def protobuf_to_dict(self, obj):
        """将protobuf对象转换为字典"""
        result = {}

        for field in obj.DESCRIPTOR.fields:
            field_name = field.name
            value = getattr(obj, field_name)

            if field.label == field.LABEL_REPEATED:
                # 重复字段
                result[field_name] = [self.protobuf_to_dict(item) if hasattr(item, 'DESCRIPTOR') else item
                                      for item in value]
            elif field.type == field.TYPE_MESSAGE:
                # 消息类型字段
                if hasattr(value, 'DESCRIPTOR'):
                    result[field_name] = self.protobuf_to_dict(value)
                else:
                    result[field_name] = value
            else:
                # 基本类型字段
                result[field_name] = value

        return result


# 使用示例
if __name__ == "__main__":
    online_rank_v3_base64_str = "CgtvbmxpbmVfcmFuaxqIAwjFloCJ+7WmBhJKaHR0cHM6Ly9pMi5oZHNsYi5jb20vYmZzL2ZhY2UvY2FlN2QwNjA2MDQ0YjA4M2VlM2NiNGE0OTljNTA3MmE0MjI3OGY5Ni5qcGcaATkiCEh65rWB5rWqKAFCoQIIxZaAifu1pgYSkwIKCEh65rWB5rWqEkpodHRwczovL2kyLmhkc2xiLmNvbS9iZnMvZmFjZS9jYWU3ZDA2MDYwNDRiMDgzZWUzY2I0YTQ5OWM1MDcyYTQyMjc4Zjk2LmpwZypWCghIeua1gea1qhJKaHR0cHM6Ly9pMi5oZHNsYi5jb20vYmZzL2ZhY2UvY2FlN2QwNjA2MDQ0YjA4M2VlM2NiNGE0OTljNTA3MmE0MjI3OGY5Ni5qcGcyVgoISHrmtYHmtaoSSmh0dHBzOi8vaTIuaGRzbGIuY29tL2Jmcy9mYWNlL2NhZTdkMDYwNjA0NGIwODNlZTNjYjRhNDk5YzUwNzJhNDIyNzhmOTYuanBnOgsg////////////ATIAGpYDCL3xoPQDEkpodHRwczovL2kyLmhkc2xiLmNvbS9iZnMvZmFjZS84N2Q1MmFiZjgyMjA3MWVmOWNjNTI4MzhjNzE2MGQ1ZTM5MzBjYjEzLmpwZxoBOSINa2FndXJhX25heXV0YSgCQq0CCL3xoPQDEqICCg1rYWd1cmFfbmF5dXRhEkpodHRwczovL2kyLmhkc2xiLmNvbS9iZnMvZmFjZS84N2Q1MmFiZjgyMjA3MWVmOWNjNTI4MzhjNzE2MGQ1ZTM5MzBjYjEzLmpwZypbCg1rYWd1cmFfbmF5dXRhEkpodHRwczovL2kyLmhkc2xiLmNvbS9iZnMvZmFjZS84N2Q1MmFiZjgyMjA3MWVmOWNjNTI4MzhjNzE2MGQ1ZTM5MzBjYjEzLmpwZzJbCg1rYWd1cmFfbmF5dXRhEkpodHRwczovL2kyLmhkc2xiLmNvbS9iZnMvZmFjZS84N2Q1MmFiZjgyMjA3MWVmOWNjNTI4MzhjNzE2MGQ1ZTM5MzBjYjEzLmpwZzoLIP///////////wEyABqEAwjA4scFEkpodHRwczovL2kyLmhkc2xiLmNvbS9iZnMvZmFjZS83NTQ5YTQzOWU2NmQ2N2M2MTJlOTcxNjlkODg1YWRmYmExMDY0ZTRhLmpwZxoBNCIJLVRzdWtpaGktKANCoAIIwOLHBRKWAgoJLVRzdWtpaGktEkpodHRwczovL2kyLmhkc2xiLmNvbS9iZnMvZmFjZS83NTQ5YTQzOWU2NmQ2N2M2MTJlOTcxNjlkODg1YWRmYmExMDY0ZTRhLmpwZypXCgktVHN1a2loaS0SSmh0dHBzOi8vaTIuaGRzbGIuY29tL2Jmcy9mYWNlLzc1NDlhNDM5ZTY2ZDY3YzYxMmU5NzE2OWQ4ODVhZGZiYTEwNjRlNGEuanBnMlcKCS1Uc3VraWhpLRJKaHR0cHM6Ly9pMi5oZHNsYi5jb20vYmZzL2ZhY2UvNzU0OWE0MzllNjZkNjdjNjEyZTk3MTY5ZDg4NWFkZmJhMTA2NGU0YS5qcGc6CyD///////////8BMgAalAMI0NiOKBJLaHR0cHM6Ly9pMi5oZHNsYi5jb20vYmZzL2ZhY2UvM2ViZjQ1OGQzNjBiNzliNGFhNTA2MTY4NTVjYzQ4NzIyZjA3N2Y4Mi53ZWJwGgEyIgzlubvmoqbmgYvpm6ooBEKsAgjQ2I4oEqICCgzlubvmoqbmgYvpm6oSS2h0dHBzOi8vaTIuaGRzbGIuY29tL2Jmcy9mYWNlLzNlYmY0NThkMzYwYjc5YjRhYTUwNjE2ODU1Y2M0ODcyMmYwNzdmODIud2VicCpbCgzlubvmoqbmgYvpm6oSS2h0dHBzOi8vaTIuaGRzbGIuY29tL2Jmcy9mYWNlLzNlYmY0NThkMzYwYjc5YjRhYTUwNjE2ODU1Y2M0ODcyMmYwNzdmODIud2VicDJbCgzlubvmoqbmgYvpm6oSS2h0dHBzOi8vaTIuaGRzbGIuY29tL2Jmcy9mYWNlLzNlYmY0NThkMzYwYjc5YjRhYTUwNjE2ODU1Y2M0ODcyMmYwNzdmODIud2VicDoLIP///////////wEyABqAAwj8o7MBEkpodHRwczovL2kxLmhkc2xiLmNvbS9iZnMvZmFjZS9jYzQyNmRmYTYxODU3N2JlZTU2YzM2YWRiZmRhZTdlNDRlMWJjOTI5LmpwZxoBMiIIdmlzbGFyZG8oBUKdAgj8o7MBEpMCCgh2aXNsYXJkbxJKaHR0cHM6Ly9pMS5oZHNsYi5jb20vYmZzL2ZhY2UvY2M0MjZkZmE2MTg1NzdiZWU1NmMzNmFkYmZkYWU3ZTQ0ZTFiYzkyOS5qcGcqVgoIdmlzbGFyZG8SSmh0dHBzOi8vaTEuaGRzbGIuY29tL2Jmcy9mYWNlL2NjNDI2ZGZhNjE4NTc3YmVlNTZjMzZhZGJmZGFlN2U0NGUxYmM5MjkuanBnMlYKCHZpc2xhcmRvEkpodHRwczovL2kxLmhkc2xiLmNvbS9iZnMvZmFjZS9jYzQyNmRmYTYxODU3N2JlZTU2YzM2YWRiZmRhZTdlNDRlMWJjOTI5LmpwZzoLIP///////////wEyABqQAwiNy6IBEkpodHRwczovL2kxLmhkc2xiLmNvbS9iZnMvZmFjZS9iOWFhNzg1MWMwOTRmYThhNGY3ZDE0YmMwOGQ0NzRmMDcxMDVhMGRkLmpwZxoBMiIM6L+H5b6A5reh5b+YKAZCqQIIjcuiARKfAgoM6L+H5b6A5reh5b+YEkpodHRwczovL2kxLmhkc2xiLmNvbS9iZnMvZmFjZS9iOWFhNzg1MWMwOTRmYThhNGY3ZDE0YmMwOGQ0NzRmMDcxMDVhMGRkLmpwZypaCgzov4flvoDmt6Hlv5gSSmh0dHBzOi8vaTEuaGRzbGIuY29tL2Jmcy9mYWNlL2I5YWE3ODUxYzA5NGZhOGE0ZjdkMTRiYzA4ZDQ3NGYwNzEwNWEwZGQuanBnMloKDOi/h+W+gOa3oeW/mBJKaHR0cHM6Ly9pMS5oZHNsYi5jb20vYmZzL2ZhY2UvYjlhYTc4NTFjMDk0ZmE4YTRmN2QxNGJjMDhkNDc0ZjA3MTA1YTBkZC5qcGc6CyD///////////8BMgAavAII/ZCAmrO8pgYSL2h0dHBzOi8vaTAuaGRzbGIuY29tL2Jmcy9mYWNlL21lbWJlci9ub2ZhY2UuanBnGgEwIhBiaWxpXzM2MTczMjE3Nzc2KAdC6AEI/ZCAmrO8pgYS2gEKEGJpbGlfMzYxNzMyMTc3NzYSL2h0dHBzOi8vaTAuaGRzbGIuY29tL2Jmcy9mYWNlL21lbWJlci9ub2ZhY2UuanBnKkMKEGJpbGlfMzYxNzMyMTc3NzYSL2h0dHBzOi8vaTAuaGRzbGIuY29tL2Jmcy9mYWNlL21lbWJlci9ub2ZhY2UuanBnMkMKEGJpbGlfMzYxNzMyMTc3NzYSL2h0dHBzOi8vaTAuaGRzbGIuY29tL2Jmcy9mYWNlL21lbWJlci9ub2ZhY2UuanBnOgsg////////////ATIA"

    print("\n=== 完整解析 ===")
    result2 = DanmuProtoDecoder().decode_online_rank_v3_protobuf(online_rank_v3_base64_str)
    if result2:
        print(json.dumps(result2, indent=2, ensure_ascii=False))

    interact_word_v2_base64_str = "CN+GjCASDOaciOacl+mjjui9uyIBASgBMMv6FziZgeDGBkCfr4nemDNiAHjIqMrn3pnLtBiaAQCyAWYI34aMIBJZCgzmnIjmnJfpo47ovbsSSWh0dHA6Ly9pMC5oZHNsYi5jb20vYmZzL2ZhY2UvMzU2MmY2MjdhNmMwMDE2NmE1ZGVhYTdjZDUxNjA0MDljMDk1N2Y5NS5qcGciAggCMgC6AQDCAQA="

    print("\n=== 完整解析 ===")
    result2 = DanmuProtoDecoder().decode_interact_word_v2_protobuf(interact_word_v2_base64_str)
    if result2:
        print(json.dumps(result2, indent=2, ensure_ascii=False))
