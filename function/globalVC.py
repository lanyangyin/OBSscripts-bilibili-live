class GvProp:
    def __init__(self, obj=None):
        self.obj = obj


class GvProps:
    def __init__(self, obj=None):
        self.obj = obj


class GvGroup:
    def __init__(self, obj=None, name: str = "", description: str = "", visible: bool = False, enabled: bool = False, props=None, modified_is: bool = False, group_props=None):
        """
        分组框控件
        Args:
            obj: 控件脚本对象
            name: 唯一名称
            description: 说明文本
            visible: 可见状态
            enabled: 可用状态
            props: 隶属属性集
            modified_is: 是否监听
            group_props: 统辖属性集
        """
        self.obj = obj
        self.name = name
        self.description = description
        self.visible = visible
        self.enabled = enabled
        self.props = props
        self.modifiedIs = modified_is
        self.group_props = group_props


class GvGroups:
    def __init__(self):
        self.objList = []

    def add(self, group_obj_name):
        setattr(self, group_obj_name, GvGroup(name=f"{group_obj_name}_group"))


class Widget:
    def __init__(self):
        pass

