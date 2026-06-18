widget.widget_Group_dict = {
    "props": {
        "account": {
            "Name": "account_group",
            "Description": "账号",
            "Type": obs.OBS_GROUP_CHECKABLE,
            "GroupProps": "account_props",
            "ModifiedIs": True
        },
        "room": {
            "Name": "room_group",
            "Description": "直播间",
            "Type": obs.OBS_GROUP_CHECKABLE,
            "GroupProps": "room_props",
            "ModifiedIs": True
        },
        "booking": {
            "Name": "booking_group",
            "Description": "直播预约",
            "Type": obs.OBS_GROUP_CHECKABLE,
            "GroupProps": "booking_props",
            "ModifiedIs": True
        },
        "danmu": {
            "Name": "danmu_group",
            "Description": "弹幕",
            "Type": obs.OBS_GROUP_CHECKABLE,
            "GroupProps": "danmu_props",
            "ModifiedIs": True
        },
        "scriptSet": {
            "Name": "script_set_group",
            "Description": "脚本设置",
            "Type": obs.OBS_GROUP_CHECKABLE,
            "GroupProps": "script_set_props",
            "ModifiedIs": True
        },
    },
    "room_props": {
        "liveBroadcastCover": {
            "Name": "live_broadcast_cover_group",
            "Description": "直播封面",
            "Type": obs.OBS_GROUP_CHECKABLE,
            "GroupProps": "live_broadcast_cover_props",
            "ModifiedIs": True
        },
        "liveBroadcastTitle": {
            "Name": "live_broadcast_title_group",
            "Description": "直播标题",
            "Type": obs.OBS_GROUP_CHECKABLE,
            "GroupProps": "live_broadcast_title_props",
            "ModifiedIs": True
        },
        "liveBroadcastAnnouncement": {
            "Name": "live_broadcast_announcement_group",
            "Description": "直播公告",
            "Type": obs.OBS_GROUP_CHECKABLE,
            "GroupProps": "live_broadcast_announcement_props",
            "ModifiedIs": True
        },
        "liveStreamingSection": {
            "Name": "live_streaming_section_group",
            "Description": "直播分区",
            "Type": obs.OBS_GROUP_CHECKABLE,
            "GroupProps": "live_streaming_section_props",
            "ModifiedIs": True
        },
        "live": {
            "Name": "live_group",
            "Description": "直播",
            "Type": obs.OBS_GROUP_CHECKABLE,
            "GroupProps": "live_props",
            "ModifiedIs": True
        },
    },
    "booking_props": {
        "bookingSend": {
            "Name": "booking_send_group",
            "Description": "直播预约发送",
            "Type": obs.OBS_GROUP_NORMAL,
            "GroupProps": "booking_send_props",
            "ModifiedIs": False
        },
    },
    "danmu_props": {
        "danmuDisplayOptions": {
            "Name": "danmu_display_options_group",
            "Description": "显示选项",
            "Type": obs.OBS_GROUP_NORMAL,
            "GroupProps": "danmu_display_options_props",
            "ModifiedIs": False
        },
        "danmuOnOff": {
            "Name": "danmu_onoff_group",
            "Description": "on/off",
            "Type": obs.OBS_GROUP_CHECKABLE,
            "GroupProps": "danmu_onoff_props",
            "ModifiedIs": True
        },
        "danmuSend": {
            "Name": "danmu_send_group",
            "Description": "弹幕发送",
            "Type": obs.OBS_GROUP_CHECKABLE,
            "GroupProps": "danmu_send_props",
            "ModifiedIs": True
        },
    },
    "script_set_props": {
        "scriptLiveSet": {
            "Name": "script_live_set_group",
            "Description": "直播设置",
            "Type": obs.OBS_GROUP_NORMAL,
            "GroupProps": "script_live_set_props",
            "ModifiedIs": True
        },
        "scriptDanmuSet": {
            "Name": "script_danmu_set_group",
            "Description": "弹幕设置",
            "Type": obs.OBS_GROUP_NORMAL,
            "GroupProps": "script_danmu_set_props",
            "ModifiedIs": True
        },
    },
}

widget.widget_TextBox_dict = {
    "account_props": {
        "loginStatus": {
            "Name": "login_status_textBox",
            "Description": "登录状态",
            "Type": obs.OBS_TEXT_INFO,
            "ModifiedIs": True
        },
    },
    "room_props": {
        "roomStatus": {
            "Name": "room_status_textBox",
            "Description": "状态",
            "Type": obs.OBS_TEXT_INFO,
            "ModifiedIs": False
        },
    },
    "live_broadcast_announcement_props": {
        "roomNews": {
            "Name": "room_news_textBox",
            "Description": "公告",
            "Type": obs.OBS_TEXT_MULTILINE,
            "ModifiedIs": True
        },
    },
    "booking_send_props": {
        "liveBookingsTitle": {
            "Name": "live_bookings_title_textBox",
            "Description": "直播预约标题",
            "LongDescription": "直播预约标题",
            "Type": obs.OBS_TEXT_DEFAULT,
            "ModifiedIs": True
        },
    },
    "danmu_props": {
        "danmuWssProt": {
            "Name": "danmu_Web_socket_server_prot_textBox",
            "Description": "弹幕端口",
            "LongDescription": "弹幕服务端转发端口，如果冲突尽量更改，1024-49151之间",
            "Type": obs.OBS_TEXT_DEFAULT,
            "ModifiedIs": False
        },
        "danmuWebCss": {
            "Name": "danmu_Web_css_textBox",
            "Description": "弹幕样式",
            "LongDescription": "弹幕css",
            "Type": obs.OBS_TEXT_MULTILINE,
            "ModifiedIs": False
        },
    },
    "danmu_send_props": {
        "danmuSendText": {
            "Name": "danmu_send_text_textBox",
            "Description": "输入",
            "LongDescription": "弹幕发送文字",
            "Type": obs.OBS_TEXT_MULTILINE,
            "ModifiedIs": False
        },
    },
}

widget.widget_ComboBox_dict = {
    "account_props": {
        "uid": {
            "Name": "uid_comboBox",
            "Description": "用户",
            "Type": obs.OBS_COMBO_TYPE_LIST,
            "ModifiedIs": True
        },
    },
    "live_broadcast_title_props": {
        "roomCommonTitles": {
            "Name": "room_Titles_comboBox",
            "Description": "标题",
            "Type": obs.OBS_COMBO_TYPE_EDITABLE,
            "ModifiedIs": True
        },
    },
    "live_streaming_section_props": {
        "roomCommonAreas": {
            "Name": "room_commonAreas_comboBox",
            "Description": "分区",
            "Type": obs.OBS_COMBO_TYPE_LIST,
            "ModifiedIs": True
        },
        "roomParentArea": {
            "Name": "room_parentArea_comboBox",
            "Description": "一级",
            "Type": obs.OBS_COMBO_TYPE_LIST,
            "ModifiedIs": True
        },
        "roomSubArea": {
            "Name": "room_subArea_comboBox",
            "Description": "二级",
            "Type": obs.OBS_COMBO_TYPE_LIST,
            "ModifiedIs": True
        },
    },
    "live_props": {
        "liveStreamingPlatform": {
            "Name": "live_streaming_platform_comboBox",
            "Description": "平台",
            "Type": obs.OBS_COMBO_TYPE_LIST,
            "ModifiedIs": True
        },
    },
    "booking_props": {
        "liveBookings": {
            "Name": "live_bookings_comboBox",
            "Description": "直播预约列表",
            "Type": obs.OBS_COMBO_TYPE_LIST,
            "ModifiedIs": True
        },
    },
    "danmu_props": {
        "danmuRoom": {
            "Name": "danmu_room_comboBox",
            "Description": "直播间",
            "LongDescription": "发送和接收弹幕的直播间，输入房间号也可以添加",
            "Type": obs.OBS_COMBO_TYPE_EDITABLE,
            "ModifiedIs": True
        },
    },
    "danmu_send_props": {
        "danmuEmoticons": {
            "Name": "danmu_emoticons_comboBox",
            "Description": "表情",
            "Type": obs.OBS_COMBO_TYPE_LIST,
            "ModifiedIs": True
        },
    },
}

widget.widget_PathBox_dict = {
    "live_broadcast_cover_props": {
        "roomCover": {
            "Name": "room_cover_fileDialogBox",
            "Description": "封面",
            "Type": obs.OBS_PATH_FILE,
            "Filter": "图片(*.jpg *.jpeg *.png)",
            "StartPath": "",
            "ModifiedIs": False
        },
    },
}

widget.widget_DigitalDisplay_dict = {
    "booking_send_props": {
        "liveBookingsDay": {
            "Name": "live_bookings_day_digitalSlider",
            "Description": "预约天",
            "Type": "ThereIsASlider",
            "Suffix": "天",
            "ModifiedIs": True
        },
        "liveBookingsHour": {
            "Name": "live_bookings_hour_digitalSlider",
            "Description": "预约时",
            "Type": "ThereIsASlider",
            "Suffix": "时",
            "ModifiedIs": True
        },
        "liveBookingsMinute": {
            "Name": "live_bookings_minute_digitalSlider",
            "Description": "预约分",
            "Type": "ThereIsASlider",
            "Suffix": "分",
            "ModifiedIs": True
        },
    },
    "danmu_props": {
        "danmuNumCommentsClient": {
            "Name": "danmu_number_of_comments_client_digitalSlider",
            "Description": "弹幕客户端创建数",
            "Type": "ThereIsAUnSlider",
            "Suffix": "个",
            "ModifiedIs": True
        },
        "danmuIntervalNumCommentsClient": {
            "Name": "danmu_interval_number_of_comments_client_digitalSlider",
            "Description": "弹幕客户端创建间隔",
            "Type": "ThereIsAUnSlider",
            "Suffix": "毫秒",
            "ModifiedIs": True
        },
        "danmuNumCacheEntries": {
            "Name": "danmu_number_of_cache_entries_digitalSlider",
            "Description": "防重复的缓存条数",
            "Type": "ThereIsASlider",
            "Suffix": "条",
            "ModifiedIs": True
        },
        "danmuCacheDuration": {
            "Name": "danmu_cache_duration_digitalSlider",
            "Description": "防重复的缓存时长",
            "Type": "ThereIsASlider",
            "Suffix": "秒",
            "ModifiedIs": True
        },
        "danmuFacePictureSize": {
            "Name": "danmu_face_picture_size_digitalSlider",
            "Description": "头像大小",
            "Type": "ThereIsASlider",
            "Suffix": "px",
            "ModifiedIs": True
        },
        "danmuFanMedalTextSize": {
            "Name": "danmu_fan_medal_text_size_digitalSlider",
            "Description": "粉丝勋章文字大小",
            "Type": "ThereIsASlider",
            "Suffix": "px",
            "ModifiedIs": True
        },
        "danmuMessageTextSize": {
            "Name": "danmu_message_text_size_digitalSlider",
            "Description": "内容文字大小",
            "Type": "ThereIsASlider",
            "Suffix": "px",
            "ModifiedIs": True
        },
        "danmuTimeTextSize": {
            "Name": "danmu_time_text_size_digitalSlider",
            "Description": "时间文字大小",
            "Type": "ThereIsASlider",
            "Suffix": "px",
            "ModifiedIs": True
        },
    },
}

widget.widget_CheckBox_dict = {
    "booking_send_props": {
        "liveBookingsDynamic": {
            "Name": "live_bookings_dynamic_checkBox",
            "Description": "是否发直播预约动态",
            "ModifiedIs": True
        },
    },
    "danmu_display_options_props": {
        "enterRoomDisplay": {
            "Name": "enter_room_display_checkBox",
            "Description": "是否显示进房消息",
            "ModifiedIs": True
        },
        "medalDisplay": {
            "Name": "medal_display_checkBox",
            "Description": "是否显示粉丝徽章",
            "ModifiedIs": True
        },
        "medalOtherDisplay": {
            "Name": "medal_other_display_checkBox",
            "Description": "是否显示其他的粉丝徽章",
            "ModifiedIs": True
        },
        "medalUnLightDisplay": {
            "Name": "medal_un_light_display_checkBox",
            "Description": "是否显示未点亮的粉丝徽章",
            "ModifiedIs": True
        },
        "lineBreakDisplay": {
            "Name": "line_break_display_checkBox",
            "Description": "换行显示",
            "ModifiedIs": True
        },
        "tagAdministratorDisplay": {
            "Name": "tag_administrator_checkBox",
            "Description": "是否标记管理员，is_admin不受影响",
            "ModifiedIs": True
        },
        "timestampDisplay": {
            "Name": "timestamp_display_checkBox",
            "Description": "是否显示时间",
            "ModifiedIs": True
        },
    },
    "script_live_set_props": {
        "linkStreamLiveStart": {
            "Name": "link_stream_live_start_checkBox",
            "Description": "联动推流和开播",
            "ModifiedIs": True
        },
        "linkStreamLiveStop": {
            "Name": "link_stream_live_stop_checkBox",
            "Description": "联动推流和停播",
            "ModifiedIs": True
        },
        "autoFillStreamServer": {
            "Name": "auto_fill_stream_server_checkBox",
            "Description": "自动填写推流服务器",
            "ModifiedIs": True
        },
    },
    "script_danmu_set_props": {
        "resetDanmuSource": {
            "Name": "reset_danmu_source_checkBox",
            "Description": "每次重置弹幕源",
            "ModifiedIs": True
        },
    },
}

widget.widget_Button_dict = {
    "props": {
        "top": {
            "Name": "top_button",
            "Description": "Top",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": lambda ps, p: log_save(obs.LOG_INFO, f"【{'顶部'}】按钮被触发"),
            "ModifiedIs": True
        },
        "startScript": {
            "Name": "start_script_button",
            "Description": "启动脚本",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_start_script,
            "ModifiedIs": False
        },
        "setWidgetVisibility": {
            "Name": "set_widget_visibility_button",
            "Description": "设置控件组可见性",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_set_widget_visibility,
            "ModifiedIs": False
        },
        "bottom": {
            "Name": "bottom_button",
            "Description": "Bottom",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": lambda ps, p: log_save(obs.LOG_INFO, f"【{'底部'}】按钮被触发"),
            "ModifiedIs": True
        },
    },
    "account_props": {
        "login": {
            "Name": "login_button",
            "Description": "登录账号",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_login,
            "ModifiedIs": False
        },
        "accountListUpdate": {
            "Name": "account_list_update_button",
            "Description": "更新账号列表",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_update_account_list,
            "ModifiedIs": False
        },
        "qrAddAccount": {
            "Name": "qr_add_account_button",
            "Description": "二维码添加账户",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_qr_add_account,
            "ModifiedIs": False
        },
        "qrPictureDisplay": {
            "Name": "qr_picture_display_button",
            "Description": "显示二维码图片",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_show_qr_picture,
            "ModifiedIs": False
        },
        "accountDelete": {
            "Name": "account_delete_button",
            "Description": "删除账户",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_del_user,
            "ModifiedIs": False
        },
        "accountBackup": {
            "Name": "account_backup_button",
            "Description": "备份账户",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_backup_users,
            "ModifiedIs": False
        },
        "accountRestore": {
            "Name": "account_restore_button",
            "Description": "恢复账户",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_restore_user,
            "ModifiedIs": False
        },
        "logout": {
            "Name": "logout_button",
            "Description": "登出账号",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_logout,
            "ModifiedIs": False
        },
    },
    "room_props": {
        "roomOpened": {
            "Name": "room_opened_button",
            "Description": "开通直播间",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_opened_room,
            "ModifiedIs": False
        },
        "realNameAuthentication": {
            "Name": "real_name_authentication_button",
            "Description": "实名认证",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_real_name_authentication,
            "ModifiedIs": False
        },
        "bliveWebJump": {
            "Name": "blive_web_jump_button",
            "Description": "跳转直播间后台网页",
            "Type": obs.OBS_BUTTON_URL,
            "Callback": ButtonFunction.button_function_jump_blive_web,
            "Url": "https://link.bilibili.com/p/center/index#/my-room/start-live",
            "ModifiedIs": False
        },
    },
    "live_broadcast_cover_props": {
        "roomCoverView": {
            "Name": "room_cover_view_button",
            "Description": "查看直播间封面",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_check_room_cover,
            "ModifiedIs": False
        },
        "roomCoverUpdate": {
            "Name": "room_cover_update_button",
            "Description": "上传直播间封面",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_update_room_cover,
            "ModifiedIs": False
        },
    },
    "live_broadcast_title_props": {
        "roomTitleChange": {
            "Name": "room_title_change_button",
            "Description": "更改直播间标题",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_change_live_room_title,
            "ModifiedIs": False
        },
    },
    "live_broadcast_announcement_props": {
        "roomNewsChange": {
            "Name": "room_news_change_button",
            "Description": "更改直播间公告",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_change_live_room_news,
            "ModifiedIs": False
        },
    },
    "live_streaming_section_props": {
        "roomCommonAreasTrue": {
            "Name": "room_commonAreas_true_button",
            "Description": "确认分区",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_true_live_room_common_area,
            "ModifiedIs": False
        },
        "roomParentAreaTrue": {
            "Name": "room_parentArea_true_button",
            "Description": "确认一级分区",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_start_parent_area,
            "ModifiedIs": False
        },
        "roomSubAreaTrue": {
            "Name": "room_subArea_true_button",
            "Description": "「确认分区」",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_start_sub_area,
            "ModifiedIs": False
        },
    },
    "live_props": {
        "liveFaceAuth": {
            "Name": "live_face_auth_button",
            "Description": "人脸认证",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_face_auth,
            "ModifiedIs": False
        },
        "liveStart": {
            "Name": "live_start_button",
            "Description": "开始直播并复制推流码",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_start_live,
            "ModifiedIs": False
        },
        "liveRtmpAddressCopy": {
            "Name": "live_rtmp_address_copy_button",
            "Description": "复制直播服务器",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_rtmp_address_copy,
            "ModifiedIs": False
        },
        "liveRtmpCodeCopy": {
            "Name": "live_rtmp_code_copy_button",
            "Description": "复制直播推流码",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_rtmp_stream_code_copy,
            "ModifiedIs": False
        },
        "liveStop": {
            "Name": "live_stop_button",
            "Description": "结束直播",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_stop_live,
            "ModifiedIs": False
        },
    },
    "booking_props": {
        "liveBookingsCancel": {
            "Name": "live_bookings_cancel_button",
            "Description": "取消直播预约",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_cancel_live_appointment,
            "ModifiedIs": False
        },
    },
    "booking_send_props": {
        "liveBookingsDayTrue": {
            "Name": "live_bookings_day_true_button",
            "Description": "确认预约天",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_true_live_appointment_day,
            "ModifiedIs": False
        },
        "liveBookingsHourTrue": {
            "Name": "live_bookings_hour_true_button",
            "Description": "确认预约时",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": lambda ps, p: log_save(obs.LOG_INFO, f"【{'确认预约时'}】按钮被触发"),
            "ModifiedIs": False
        },
        "liveBookingsMinuteTrue": {
            "Name": "live_bookings_minute_true_button",
            "Description": "确认预约分",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": lambda ps, p: log_save(obs.LOG_INFO, f"【{'确认预约分'}】按钮被触发"),
            "ModifiedIs": False
        },
        "liveBookingsCreate": {
            "Name": "live_bookings_create_button",
            "Description": "发布直播预约",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_creat_live_appointment,
            "ModifiedIs": False
        },
    },
    "danmu_props": {
        "settingDanmuData": {
            "Name": "setting_danmu_data_button",
            "Description": "弹幕数据设置",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_setting_danmu_data,
            "ModifiedIs": False
        },
        "applyDanmuCss": {
            "Name": "apply_danmu_css_button",
            "Description": "应用弹幕样式",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_apply_danmu_css,
            "ModifiedIs": False
        },
        "confirmDanmuWssPort": {
            "Name": "confirm_danmu_wss_port_button",
            "Description": "确认弹幕转发端口",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_confirm_danmu_wss_port,
            "ModifiedIs": False
        },
        "addDanmuRoomid": {
            "Name": "add_danmu_roomid_button",
            "Description": "添加直播间",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_add_danmu_roomid,
            "ModifiedIs": False
        },
        "delDanmuRoomid": {
            "Name": "del_danmu_roomid_button",
            "Description": "删除直播间",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_del_danmu_roomid,
            "ModifiedIs": False
        },
    },
    "danmu_onoff_props": {
        "startDanmuForwardingService": {
            "Name": "start_danmu_forwarding_service_button",
            "Description": "开启弹幕转发服务",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_start_danmu_forwarding_service,
            "ModifiedIs": False
        },
        "addDanmuBrowser": {
            "Name": "add_danmu_browser_button",
            "Description": "添加弹幕浏览器源",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_add_danmu_browser,
            "ModifiedIs": False
        },
        "startDanmu": {
            "Name": "start_danmu_button",
            "Description": "开启弹幕",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_start_danmu,
            "ModifiedIs": False
        },
        "stopDanmuForwardingService": {
            "Name": "stop_danmu_forwarding_service_button",
            "Description": "终止弹幕转发服务",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_stop_danmu_forwarding_service,
            "ModifiedIs": False
        },
        "removeDanmuBrowser": {
            "Name": "remove_danmu_browser_button",
            "Description": "移除弹幕浏览器源",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_remove_danmu_browser,
            "ModifiedIs": False
        },
        "stopDanmu": {
            "Name": "stop_danmu_button",
            "Description": "停止弹幕",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_stop_danmu,
            "ModifiedIs": False
        },
    },
    "danmu_send_props": {
        "mergeEmoticons": {
            "Name": "merge_emoticons_button",
            "Description": "输入表情",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_merge_emoticons,
            "ModifiedIs": False
        },
        "danmuSend": {
            "Name": "danmu_send_button",
            "Description": "发送",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_danmu_send,
            "ModifiedIs": False
        },
    },
    "script_set_props": {
        "updateScriptSet": {
            "Name": "update_script_set_button",
            "Description": "更新脚本设置",
            "Type": obs.OBS_BUTTON_DEFAULT,
            "Callback": ButtonFunction.button_function_update_script_set,
            "ModifiedIs": False
        },
    },
}
