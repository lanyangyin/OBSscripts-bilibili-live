"""装饰器"""

def add_aliases(*aliases):
    """
    为方法创建多个别名方法
    """
    def decorator(func):
        func._aliases = aliases
        return func
    return decorator

class AliasMeta(type):
    """元类，用于自动创建别名方法（支持staticmethod和classmethod）"""
    def __new__(cls, name, bases, attrs):
        for attr_name, attr_value in list(attrs.items()):
            # 处理 staticmethod 和 classmethod
            if isinstance(attr_value, (staticmethod, classmethod)):
                # 提取原始函数
                original = attr_value.__func__
                if hasattr(original, '_aliases'):
                    for alias in original._aliases:
                        # 将别名也设置为相同类型的描述器
                        attrs[alias] = attr_value
            elif callable(attr_value) and hasattr(attr_value, '_aliases'):
                for alias in attr_value._aliases:
                    attrs[alias] = attr_value
        return super().__new__(cls, name, bases, attrs)

if __name__ == "__main__":
    class A(metaclass=AliasMeta):
        def __init__(self, n):
            self.num = n

        @add_aliases("newfd")
        @add_aliases("newfa", "newfb", "newfc", "newfn")
        def test(self):
            return self.num

    ca = A(1)
    print(ca.test())  # 10086
    print(ca.newfd())  # 10086
    print(ca.newfa())  # 10086
    print(ca.newfn())  # 10086