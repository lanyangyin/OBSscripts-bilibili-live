import obspython as obs


class BrowserSourceManager:
    set_ing_gol = None
    def __init__(self):
        self.browser_source = None
        self.source_name = "Python浏览器源"

    def create_browser_source(self, source_name=None):
        """创建浏览器源"""
        if source_name:
            self.source_name = source_name

        # 创建浏览器源
        self.browser_source = obs.obs_source_create("browser_source", self.source_name, None, None)

        if not self.browser_source:
            print("创建浏览器源失败!")
            return False

        print(f"成功创建浏览器源: {self.source_name}")
        return True

    def configure_browser_source(self, url, width, height, fps=None, css=None):
        """配置浏览器源属性"""
        if not self.browser_source:
            print("错误: 未创建浏览器源")
            return False

        settings = obs.obs_data_create()

        # 基本设置
        obs.obs_data_set_string(settings, "url", url)
        obs.obs_data_set_int(settings, "width", width)
        obs.obs_data_set_int(settings, "height", height)

        # 可选设置
        if fps:
            obs.obs_data_set_bool(settings, "fps_custom", True)
            obs.obs_data_set_int(settings, "fps", fps)

        if css:
            obs.obs_data_set_string(settings, "css", css)

        # 其他常用设置
        obs.obs_data_set_bool(settings, "shutdown", False)  # 不关闭源
        obs.obs_data_set_bool(settings, "restart_when_active", True)  # 激活时重启

        # 应用设置
        obs.obs_source_update(self.browser_source, settings)
        obs.obs_data_release(settings)

        print(f"浏览器源配置完成 - URL: {url}, 尺寸: {width}x{height}")
        return True

    def add_to_current_scene(self):
        """将浏览器源添加到当前场景"""
        if not self.browser_source:
            print("错误: 未创建浏览器源")
            return False

        # 获取当前场景
        current_scene = obs.obs_frontend_get_current_scene()
        if not current_scene:
            print("无法获取当前场景")
            return False

        scene = obs.obs_scene_from_source(current_scene)
        if scene:
            # 添加到场景
            obs.obs_scene_add(scene, self.browser_source)
            print(f"已将浏览器源 '{self.source_name}' 添加到当前场景")

            # 释放引用（场景现在持有源的引用）
            obs.obs_source_release(self.browser_source)
            self.browser_source = None
        else:
            print("无法获取场景对象")

        # 释放场景源
        obs.obs_source_release(current_scene)
        return True

    def create_and_add_browser_source(self, props, prop):
        """创建并添加浏览器源的完整流程"""
        # 从脚本设置获取参数


        url = obs.obs_data_get_string(BrowserSourceManager.set_ing_gol, "browser_url")
        width = obs.obs_data_get_int(BrowserSourceManager.set_ing_gol, "browser_width")
        height = obs.obs_data_get_int(BrowserSourceManager.set_ing_gol, "browser_height")
        fps = obs.obs_data_get_int(BrowserSourceManager.set_ing_gol, "browser_fps")
        source_name = obs.obs_data_get_string(BrowserSourceManager.set_ing_gol, "browser_source_name")
        css = obs.obs_data_get_string(BrowserSourceManager.set_ing_gol, "browser_css")

        # 如果FPS为0，则不设置自定义FPS
        if fps == 0:
            fps = None

        # 如果CSS为空，则不设置
        if not css or css.strip() == "":
            css = None

        # 执行创建和配置
        if self.create_browser_source(source_name):
            if self.configure_browser_source(url, width, height, fps, css):
                self.add_to_current_scene()


        return True


# 全局管理器实例
browser_manager = BrowserSourceManager()
def a(ps, p):
    browser_manager.create_and_add_browser_source(ps, p)

def script_properties():
    """定义脚本界面"""
    props = obs.obs_properties_create()

    # 创建按钮
    obs.obs_properties_add_button(props, "create_browser_source", "创建浏览器源", a)
    # 源名称
    obs.obs_properties_add_text(props, "browser_source_name", "源名称", obs.OBS_TEXT_DEFAULT)

    # URL设置
    obs.obs_properties_add_text(props, "browser_url", "网页URL", obs.OBS_TEXT_DEFAULT)

    # 尺寸设置
    obs.obs_properties_add_int(props, "browser_width", "宽度", 1, 4096, 1)
    obs.obs_properties_add_int(props, "browser_height", "高度", 1, 4096, 1)

    # FPS设置 (0表示使用默认)
    obs.obs_properties_add_int(props, "browser_fps", "自定义FPS (0=默认)", 0, 60, 1)

    # CSS自定义样式
    css_prop = obs.obs_properties_add_text(props, "browser_css", "自定义CSS", obs.OBS_TEXT_MULTILINE)
    obs.obs_property_set_long_description(css_prop, "可选的CSS样式，用于修改浏览器源的外观")


    # 说明文本
    info_text_p = obs.obs_properties_add_text(props, "info_text", "说明", obs.OBS_TEXT_INFO)
    obs.obs_property_set_long_description(info_text_p,  "点击'创建浏览器源'按钮将在当前场景中添加一个新的浏览器源。\n确保输入的URL是有效的，并且OBS有网络访问权限。")

    return props


def script_defaults(settings):
    """设置默认值"""
    BrowserSourceManager.set_ing_gol = settings
    obs.obs_data_set_string(settings, "browser_source_name", "Python浏览器源")
    obs.obs_data_set_string(settings, "browser_url", "https://www.example.com")
    obs.obs_data_set_int(settings, "browser_width", 1280)
    obs.obs_data_set_int(settings, "browser_height", 720)
    obs.obs_data_set_int(settings, "browser_fps", 0)
    obs.obs_data_set_string(settings, "browser_css", "body { background-color: transparent; }")


def script_description():
    """脚本描述"""
    return ("OBS浏览器源创建脚本\n\n"
            "使用此脚本可以创建和配置浏览器源，并将其添加到当前场景中。\n"
            "支持自定义URL、尺寸、FPS和CSS样式。")


def script_load(settings):
    """脚本加载时调用"""
    print("浏览器源管理器脚本已加载")


def script_unload():
    """脚本卸载时调用"""
    print("浏览器源管理器脚本已卸载")


def script_update(settings):
    """脚本设置更新时调用"""
    # 这里可以添加设置更新时的处理逻辑
    pass