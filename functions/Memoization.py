"""
演示了如何使用 lru_cache 来优化函数调用
将函数调用结果缓存到内存中
相同参数再次调用时直接返回缓存结果，避免重复计算
自动管理缓存大小，淘汰最久未使用的条目
显著提升重复调用相同参数的函数性能

使用注意事项
    参数限制：

        所有参数必须是可哈希的（hashable）

        避免使用列表、字典等可变对象作为参数

    函数要求：

        必须是纯函数（相同输入始终产生相同输出）

        不能有副作用（如修改外部变量、文件操作等）

        结果不会随时间或外部状态改变

    内存管理：

        设置合理的 maxsize 避免内存无限增长

        大对象缓存可能导致内存压力

        长期运行服务需监控缓存大小

    数据一致性：

        不适合缓存实时变化的数据

        外部数据变更时缓存不会自动更新

        需要考虑缓存失效策略
"""
from functools import lru_cache
import time


# 模拟一个计算密集型函数
@lru_cache(maxsize=None)
def expensive_calculation(n):
    """模拟一个耗时的计算函数"""
    print(f"计算 {n} 的平方...")
    time.sleep(1)  # 模拟计算耗时
    return n * n


def process_data(n):
    """处理数据的函数，内部会调用 expensive_calculation"""
    result = expensive_calculation(n)  # 这里会使用缓存的结果
    processed = result + 10
    print(f"加10处理后的结果: {processed}")
    return processed


if __name__ == "__main__":
    print("=== 演示 lru_cache 效果 ===")

    # 第一次调用 - 实际计算
    print("\n1. 第一次调用 expensive_calculation(5):")
    start_time = time.time()
    k = expensive_calculation(5)
    end_time = time.time()
    print(f"结果: {k}, 耗时: {end_time - start_time:.2f}秒")

    # 第二次调用相同参数 - 从缓存读取
    print("\n2. 第二次调用 expensive_calculation(5):")
    start_time = time.time()
    k2 = expensive_calculation(5)
    end_time = time.time()
    print(f"结果: {k2}, 耗时: {end_time - start_time:.2f}秒")

    # 清空 expensive_calculation函数的process_data缓存
    print("\n清空 expensive_calculation函数的process_data缓存")
    expensive_calculation.cache_clear()

    # 调用 process_data，内部会使用缓存
    print("\n3. 调用 process_data(5):")
    start_time = time.time()
    n = process_data(5)
    end_time = time.time()
    print(f"结果: {n}, 耗时: {end_time - start_time:.2f}秒")

    # 使用不同参数调用
    print("\n4. 调用 expensive_calculation(10) - 新参数:")
    start_time = time.time()
    k3 = expensive_calculation(10)
    end_time = time.time()
    print(f"结果: {k3}, 耗时: {end_time - start_time:.2f}秒")

    # 使用不同参数调用
    print("\n5. 第二调用 expensive_calculation(10):")
    start_time = time.time()
    k3 = expensive_calculation(10)
    end_time = time.time()
    print(f"结果: {k3}, 耗时: {end_time - start_time:.2f}秒")

    # 查看缓存信息
    print(f"\n6. 缓存统计: {expensive_calculation.cache_info()}")
