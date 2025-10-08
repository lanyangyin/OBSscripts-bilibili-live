import obspython as obs

# 事件常量
OBS_FRONTEND_EVENT_RECORDING_STARTED = 7
OBS_FRONTEND_EVENT_RECORDING_STOPPED = 8
OBS_FRONTEND_EVENT_RECORDING_PAUSED = 26
OBS_FRONTEND_EVENT_RECORDING_UNPAUSED = 27

# 全局变量
props = None
status_prop = None
recording_active = False
recording_paused = False
last_update_time = 0


def update_status_display():
    """更新状态显示文本"""
    global status_prop, recording_active, recording_paused

    if not status_prop:
        return

    if recording_active:
        if recording_paused:
            status_text = "⏸ 录制已暂停"
        else:
            status_text = "● 正在录制"
    else:
        status_text = "■ 录制已停止"

    # 更新状态文本
    obs.obs_property_set_description(status_prop, status_text)


def event_callback(event):
    """处理录制事件"""
    global recording_active, recording_paused

    if event == OBS_FRONTEND_EVENT_RECORDING_STARTED:
        recording_active = True
        recording_paused = False
        update_status_display()

    elif event == OBS_FRONTEND_EVENT_RECORDING_STOPPED:
        recording_active = False
        recording_paused = False
        update_status_display()

    elif event == OBS_FRONTEND_EVENT_RECORDING_PAUSED:
        recording_paused = True
        update_status_display()

    elif event == OBS_FRONTEND_EVENT_RECORDING_UNPAUSED:
        recording_paused = False
        update_status_display()


def script_tick(seconds):
    """每帧调用，用于状态更新和UI刷新"""
    global last_update_time

    # 每秒更新一次状态（即使没有事件）
    current_time = obs.os_gettime_ns() // 1000000  # 毫秒
    if current_time - last_update_time >= 1000:
        last_update_time = current_time
        update_status_display()


def script_properties():
    """创建脚本UI"""
    global props, status_prop

    props = obs.obs_properties_create()

    # 添加状态显示文本框
    status_prop = obs.obs_properties_add_text(
        props,
        "recording_status",
        "录制状态: 初始化中...",
        obs.OBS_TEXT_INFO
    )

    # 添加分隔线
    obs.obs_properties_add_text(props, "separator", "", obs.OBS_TEXT_INFO)

    # 添加操作按钮
    obs.obs_properties_add_button(
        props,
        "start_recording_btn",
        "开始录制",
        lambda props, prop: start_recording()
    )

    obs.obs_properties_add_button(
        props,
        "pause_recording_btn",
        "暂停/继续录制",
        lambda props, prop: toggle_pause_recording()
    )

    obs.obs_properties_add_button(
        props,
        "stop_recording_btn",
        "停止录制",
        lambda props, prop: stop_recording()
    )

    # 添加日志级别设置
    log_level = obs.obs_properties_add_list(
        props,
        "log_level",
        "日志级别:",
        obs.OBS_COMBO_TYPE_LIST,
        obs.OBS_COMBO_FORMAT_INT
    )
    obs.obs_property_list_add_int(log_level, "无", 0)
    obs.obs_property_list_add_int(log_level, "基础信息", 1)
    obs.obs_property_list_add_int(log_level, "详细信息", 2)
    obs.obs_property_set_modified_callback(log_level, test)

    return props


def script_load(settings):
    """脚本加载时初始化"""
    global recording_active, recording_paused

    # 注册事件回调
    obs.obs_frontend_add_event_callback(event_callback)

    # 获取初始状态
    recording_active = obs.obs_frontend_recording_active()
    recording_paused = obs.obs_frontend_recording_paused()

    # 初始更新显示
    update_status_display()

    # 记录日志
    log_level = obs.obs_data_get_int(settings, "log_level") or 1
    if log_level > 0:
        status = "录制中" if recording_active else "未录制"
        obs.script_log(obs.LOG_INFO, f"脚本加载完成 - 当前状态: {status}")


def script_unload():
    """脚本卸载时清理"""
    # 注销事件回调
    obs.obs_frontend_remove_event_callback(event_callback)

    # 记录日志
    obs.script_log(obs.LOG_INFO, "录制监控脚本已卸载")


def script_update(settings):
    """设置更新时调用"""
    # 可以在这里处理设置变更
    pass


def script_description():
    return (
        "<b>录制状态监控器</b>"
        "<hr>"
        "在脚本界面显示当前录制状态，并提供录制控制按钮。<br><br>"
        "功能：<br>"
        "- 实时显示录制状态（录制中/已停止/已暂停）<br>"
        "- 提供开始/暂停/停止录制按钮"
    )


def start_recording():
    """开始录制"""
    if not obs.obs_frontend_recording_active():
        obs.obs_frontend_recording_start()
        obs.script_log(obs.LOG_INFO, "用户点击了开始录制按钮")


def stop_recording():
    """停止录制"""
    if obs.obs_frontend_recording_active():
        obs.obs_frontend_recording_stop()
        obs.script_log(obs.LOG_INFO, "用户点击了停止录制按钮")


def toggle_pause_recording():
    """暂停/继续录制"""
    if obs.obs_frontend_recording_active():
        if obs.obs_frontend_recording_paused():
            obs.obs_frontend_recording_unpause()
            obs.script_log(obs.LOG_INFO, "用户继续了录制")
        else:
            obs.obs_frontend_recording_pause()
            obs.script_log(obs.LOG_INFO, "用户暂停了录制")


def test(props, prop, settings):
    obs.script_log(obs.LOG_INFO, "测试函数被调用")
    return True
