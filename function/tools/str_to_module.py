import types


def str_to_module(module_name, module_str):
    """将字符串转换为模块对象"""
    # 创建一个新的模块对象
    module = types.ModuleType(module_name)

    # 执行字符串代码，将结果存储在模块的命名空间中
    exec(module_str, module.__dict__)

    return module


if __name__ == '__main__':
    # 使用示例
    strmodule = "print('12')"
    strmodule = str_to_module("strmodule", strmodule)
