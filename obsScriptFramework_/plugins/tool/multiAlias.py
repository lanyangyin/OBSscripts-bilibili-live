"""装饰器，为方法创建多个别名"""
def multi_alias(*aliases):
    """
    装饰器，为方法创建多个别名
    可以一次性指定多个别名，也可以多次叠加使用

    示例：
        @multi_alias("alias1", "alias2")
        def method(self):
            pass

        或

        @multi_alias("alias3")
        @multi_alias("alias2")
        @multi_alias("alias1")
        def method(self):
            pass
    """

    def decorator(method):
        # 获取或创建别名列表
        if not hasattr(method, '_multi_aliases'):
            method._multi_aliases = []

        # 添加新的别名
        method._multi_aliases.extend(aliases)

        return method

    return decorator


# 使用元类实现别名方法的添加
class MultiAliasMeta(type):
    """元类，处理multi_alias装饰器添加的方法别名"""

    def __new__(cls, name, bases, attrs):
        # 创建类
        klass = super().__new__(cls, name, bases, attrs)

        # 先收集所有需要添加别名的方法
        methods_to_process = []
        for attr_name, attr_value in attrs.items():
            if callable(attr_value) and hasattr(attr_value, '_multi_aliases'):
                methods_to_process.append((attr_name, attr_value))

        # 然后为每个方法添加别名
        for method_name, method_value in methods_to_process:
            # 为每个别名创建方法
            for alias in method_value._multi_aliases:
                if not hasattr(klass, alias):
                    # 创建别名方法
                    setattr(klass, alias, method_value)

        return klass


# 为了更好的灵活性，也可以使用类装饰器版本
def process_multi_aliases(cls):
    """
    类装饰器，处理multi_alias装饰器添加的方法别名
    """
    import inspect

    # 先收集所有需要处理的方法
    methods_to_process = []
    for name, attr in cls.__dict__.items():
        if callable(attr) and hasattr(attr, '_multi_aliases'):
            methods_to_process.append((name, attr))

    # 然后为每个方法添加别名
    for method_name, method_value in methods_to_process:
        # 为每个别名创建方法
        for alias in method_value._multi_aliases:
            if not hasattr(cls, alias):
                # 创建别名方法
                setattr(cls, alias, method_value)

    return cls


# 一个更灵活的版本，支持动态实例别名（在__init__中创建）
def multi_alias_dynamic(*aliases):
    """动态版本的multi_alias，在实例层面创建别名方法"""

    def decorator(method):
        if not hasattr(method, '_dynamic_aliases'):
            method._dynamic_aliases = []
        method._dynamic_aliases.extend(aliases)
        return method

    return decorator

import functools

def creat(func):
    @functools.wraps(func)  # 保留原函数的元数据
    def wrapper(*args, **kwargs):
        return 9090909
    return wrapper
if __name__ == "__main__":
    # 测试类
    class A(metaclass=MultiAliasMeta):
        def __init__(self, num=10086):
            self.num = num

        # 方式1：一次性指定多个别名
        @multi_alias("newfa", "newfb", "newfc", "newfn")
        def test(self):
            return self.num


    # 测试类 - 使用叠加装饰器的方式
    class B(metaclass=MultiAliasMeta):
        def __init__(self, num=10086):
            self.num = num

        # 方式2：多次叠加使用装饰器
        @creat
        @multi_alias("newfn")
        @multi_alias("newfc")
        @multi_alias("newfb")
        @multi_alias("newfa")
        def test(self):
            return self.num


    # 使用类装饰器的版本
    @process_multi_aliases
    class C:
        def __init__(self, num=10086):
            self.num = num

        @multi_alias("newfa", "newfb")
        @multi_alias("newfc", "newfn")
        def test(self):
            return self.num


    class D:
        def __init__(self, num=10086):
            self.num = num

            # 为所有有_dynamic_aliases属性的方法创建别名
            for attr_name in dir(self.__class__):
                attr = getattr(self.__class__, attr_name)
                if callable(attr) and hasattr(attr, '_dynamic_aliases'):
                    for alias in attr._dynamic_aliases:
                        # 为当前实例创建别名方法
                        # 需要捕获当前的alias值，否则lambda会使用循环中最后一个alias
                        setattr(self, alias, lambda m=attr, a=alias: m(self))

        @multi_alias_dynamic("newfa", "newfb", "newfc", "newfn")
        def test(self):
            return self.num


    print("测试一次性指定多个别名:")
    ca = A()
    print(f"ca.test() == {ca.test()}")
    print(f"ca.newfa() == {ca.newfa()}")
    print(f"ca.newfb() == {ca.newfb()}")
    print(f"ca.newfc() == {ca.newfc()}")
    print(f"ca.newfn() == {ca.newfn()}")

    print("\n测试叠加装饰器:")
    cb = B()
    print(f"cb.test() == {cb.test()}")
    print(f"cb.newfa() == {cb.newfa()}")
    print(f"cb.newfb() == {cb.newfb()}")
    print(f"cb.newfc() == {cb.newfc()}")
    print(f"cb.newfn() == {cb.newfn()}")

    print("\n测试类装饰器版本:")
    cc = C()
    print(f"cc.test() == {cc.test()}")
    print(f"cc.newfa() == {cc.newfa()}")
    print(f"cc.newfb() == {cc.newfb()}")
    print(f"cc.newfc() == {cc.newfc()}")
    print(f"cc.newfn() == {cc.newfn()}")

    print("\n测试动态实例别名:")
    cd = D()
    print(f"cd.test() == {cd.test()}")
    print(f"cd.newfa() == {cd.newfa()}")
    print(f"cd.newfb() == {cd.newfb()}")
    print(f"cd.newfc() == {cd.newfc()}")
    print(f"cd.newfn() == {cd.newfn()}")

    # 测试叠加的效果
    print("\n测试叠加装饰器别名合并:")


    @multi_alias("a", "b")
    @multi_alias("c", "d")
    def example():
        return "example"


    print(f"example._multi_aliases = {example._multi_aliases}")
    # 输出: ['c', 'd', 'a', 'b']