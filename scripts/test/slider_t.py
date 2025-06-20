from PIL.ImageStat import Global

import obspython as obs

# 全局变量存储控件ID
slider_name = "duration_slider"
button_max100 = "btn_max100"
button_max10 = "btn_max10"
button_set20 = "btn_set20"
script_settings = None
slider = None

def script_load(settings):
    global script_settings
    script_settings = settings
    return "Custom Slider with Dynamic Range"


def script_description():
    return "Custom Slider with Dynamic Range"


def script_properties():
    global slider
    props = obs.obs_properties_create()

    # 添加整数滑块 (0-28, 后缀's')
    slider = obs.obs_properties_add_int_slider(
        props,
        slider_name,
        "Duration:",
        0,  # 最小值
        28,  # 初始最大值
        1,  # 步长
    )
    obs.obs_property_int_set_suffix(slider, "s")

    # 添加控制按钮
    obs.obs_properties_add_button(props, button_max100, "Set Max to 100", set_max100)
    obs.obs_properties_add_button(props, button_max10, "Set Max to 10", set_max10)
    obs.obs_properties_add_button(props, button_set20, "Set Value to 20", set_value_to_20)

    return props


def set_max100(props, prop):
    current_val = obs.obs_data_get_int(script_settings, slider_name)

    # 更新滑块范围 (0-100)
    obs.obs_data_set_int(script_settings, slider_name, current_val)
    obs.obs_property_int_set_limits(slider, 0, 100, 1)

    return True


def set_max10(props, prop):
    # settings = obs.obs_data_create()
    current_val = obs.obs_data_get_int(script_settings, slider_name)

    # 限制当前值不超过新最大值
    if current_val > 10:
        obs.obs_data_set_int(script_settings, slider_name, 10)

    # 更新滑块范围 (0-10)
    obs.obs_property_int_set_limits(slider, 0, 10, 1)

    # obs.obs_properties_apply_settings(props, settings)
    # obs.obs_data_release(script_settings)
    return True


def set_value_to_20(props, prop):
    obs.obs_data_set_int(script_settings, slider_name, 20)
    return True