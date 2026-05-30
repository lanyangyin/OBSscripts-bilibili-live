from functools import lru_cache


def add_clear_cache(func):
    """
    装饰器：标记需要被 clear() 方法清理缓存的目标函数。
    可正确处理 @staticmethod 包装。
    """
    # 如果 func 是 staticmethod 对象，获取其内部的原始函数
    if isinstance(func, staticmethod):
        wrapped = func.__func__
    else:
        wrapped = func
    # 在原始函数上添加标记
    wrapped._clear_cache = True
    return func


class ClearableCache:
    """继承该基类即可自动获得 clear() 静态方法，用于清理所有被 @add_clear_cache 标记的 lru_cache 缓存。"""

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cache_clear_funcs = []
        seen_names = set()

        # 遍历 MRO（方法解析顺序），从当前类开始，忽略 object
        for base in cls.__mro__:
            if base is object:
                continue
            for name, value in base.__dict__.items():
                if name in seen_names:
                    continue  # 已被更近的类覆盖，跳过

                # 获取底层的可调用对象
                if isinstance(value, staticmethod):
                    func = value.__func__
                else:
                    func = value

                # 检查是否被 add_clear_cache 标记且拥有 cache_clear 方法
                if hasattr(func, '_clear_cache') and func._clear_cache:
                    if hasattr(func, 'cache_clear'):
                        cache_clear_funcs.append(func.cache_clear)
                        seen_names.add(name)
                    # 若没有 cache_clear，说明可能误用，忽略并可选发出警告

        if cache_clear_funcs:
            def clear():
                for cc in cache_clear_funcs:
                    cc()

            cls.clear = staticmethod(clear)


if __name__ == '__main__':
    class ControlDataSetFunction(ClearableCache):
        def __init__(self):
            self._clear_cache = True
            self.t = "True"

        @staticmethod
        @lru_cache(maxsize=None)
        @add_clear_cache
        def test():
            print("Computing test")
            return True

        @staticmethod
        @lru_cache(maxsize=None)
        @add_clear_cache
        def test1():
            print("Computing test1")
            return True

        @lru_cache(maxsize=None)
        @add_clear_cache
        def test2(self):
            print(f"Computing test{self.t}")
            return True

    cdf = ControlDataSetFunction()
    # 验证
    print(ControlDataSetFunction.test())  # 输出 "Computing test" 并返回 True
    print(ControlDataSetFunction.test())  # 无输出（缓存命中）
    print(ControlDataSetFunction.test1())  # 输出 "Computing test1"
    print(cdf.test2())  # 输出 "Computing testTrue"
    print(cdf.test2())  # 无输出（缓存命中）

    ControlDataSetFunction.clear()  # 清除所有被标记方法的缓存
    print(ControlDataSetFunction.test())  # 再次输出 "Computing test"（缓存已清）
    print(ControlDataSetFunction.test1())  # 再次输出 "Computing test1"
    print(cdf.test2())  # 再次输出 "Computing testTrue"

    # ===== 结合别名装饰器与缓存清理（修复后） =====
    from addAliases import add_aliases, AliasMeta

    class AliasWithCache(ClearableCache, metaclass=AliasMeta):
        def __init__(self, value):
            self.value = value

        @add_aliases("add", "sum")
        @lru_cache(maxsize=None)
        @add_clear_cache
        def compute(self, x):
            print(f"Computing {self.value} + {x}")
            return self.value + x

        # 静态方法：@staticmethod 在外，@add_aliases 在内
        @staticmethod
        @add_aliases("static_add", "static_sum")
        @lru_cache(maxsize=None)
        @add_clear_cache
        def static_compute(x, y):
            print(f"Static computing {x} + {y}")
            return x + y

    print("\n=== 测试别名与缓存清理 ===")
    obj = AliasWithCache(10)
    print("首次调用 compute(5):", obj.compute(5))   # 输出 Computing 10 + 5 → 15
    print("再次调用 compute(5):", obj.compute(5))   # 无输出，缓存命中 → 15
    print("通过别名 add(5):", obj.add(5))           # 无输出，缓存命中 → 15
    print("通过别名 sum(5):", obj.sum(5))           # 无输出，缓存命中 → 15
    print("首次调用 compute(5):", obj.compute(6))   # 输出 Computing 10 + 6 → 16
    print("\n================")

    print("\n首次调用 static_compute(3,4):", AliasWithCache.static_compute(3,4))   # 输出 → 7
    print("再次调用 static_compute(3,4):", AliasWithCache.static_compute(3,4))     # 无输出 → 7
    print("通过别名 static_add(3,4):", AliasWithCache.static_add(3,4))             # 无输出 → 7
    print("通过别名 static_sum(3,4):", AliasWithCache.static_sum(3,4))             # 无输出 → 7

    # 清除缓存
    AliasWithCache.clear()
    print("\n缓存已清除")
    print("再次调用 compute(5):", obj.compute(5))   # 重新输出 → 15
    print("通过别名 add(5):", obj.add(5))           # 重新输出 → 15
    print("再次调用 static_compute(3,4):", AliasWithCache.static_compute(3,4))     # 重新输出 → 7