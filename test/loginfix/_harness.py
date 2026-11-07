# coding=utf-8
"""loginfix 验证脚本的公共脚手架。

这个脚本有 3 万多行、依赖 obspython，没法直接 import 测。所以我们用 ast
把需要验证的函数/方法从源码里抽出来单独编译，再配 stub 运行。

好处：测的是**真实源码文本**，不是复制粘贴的副本，改了源码测试会跟着变。
"""
import ast
import os
import warnings

# 成品脚本内嵌了一大段 CSS/HTML，里面有 "\e6a0" 这类非 Python 转义，
# ast.parse 会刷 SyntaxWarning。那是原脚本就有的历史问题，跟登录修复无关，
# 测试时静音即可。
warnings.filterwarnings("ignore", category=SyntaxWarning)

# test/loginfix/_harness.py -> 仓库根目录
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FIXED = os.path.join(ROOT, "finishedProduct", "bilibili_live_multi_py36_obs27_loginfix.py")
ORIGINAL = os.path.join(ROOT, "finishedProduct", "bilibili_live_multi_py36_obs27.py")


def load_source(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def build_module(path, names, keep_decorators=False):
    """从 path 中抽出名为 names 的函数定义，编译成一个可 exec 的 module。

    Args:
        path: 源文件
        names: 函数名列表（支持嵌套在方法里的内部函数，如 check_poll）
        keep_decorators: 是否保留装饰器（默认去掉 @staticmethod / @lru_cache）

    Returns:
        (module, source_path)
    """
    source = load_source(path)
    tree = ast.parse(source)

    found = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name in names:
            found[node.name] = node

    missing = [n for n in names if n not in found]
    if missing:
        raise LookupError("在 %s 里找不到: %s" % (path, ", ".join(missing)))

    body = []
    for name in names:
        node = found[name]
        if not keep_decorators:
            node.decorator_list = []
        body.append(node)

    mod = ast.Module(body=body, type_ignores=[])
    ast.fix_missing_locations(mod)
    return mod, source


def extract(path, name, extra_globals=None):
    """抽一个函数出来，返回可直接调用的对象。"""
    mod, source = build_module(path, [name])
    ns = dict(extra_globals or {})
    exec(compile(mod, source, "exec"), ns)
    return ns[name]


class Obs:
    """obspython 的最小 stub。"""
    LOG_INFO = "info"
    LOG_WARNING = "warning"
    LOG_ERROR = "error"


class Recorder:
    """收集 log_save 输出和副作用调用，方便断言。"""

    def __init__(self):
        self.logs = []
        self.calls = []

    def log_save(self, level, msg):
        self.logs.append((level, str(msg)))

    def got(self, keyword):
        return [m for lv, m in self.logs if keyword in m]

    def text(self):
        return " ".join(m for lv, m in self.logs)

    def clear(self):
        self.logs.clear()
        self.calls.clear()
