# macOS Sonoma 14.5

## 配置插件
- 打开OBS
- 在菜单栏的【工具】中，选择`脚本`
- 在脚本窗口中的`python设置`中配置python安装路径
- 使用以下代码获得python安装路径
```bash
python3
```
```python
import sys
print(sys.prefix)
exit()

```
- python路径示例
```
/opt/homebrew/Cellar/python@3.10/3.10.14/Frameworks
```
- Frameworks目录结构大致如下
```
./
└── Python.framework
    ├── Headers
    ├── Python
    ├── Resources
    └── Versions
        ├── 3.10
        │   ├── Headers -> include/python3.10
        │   ├── Python
        │   ├── Resources
        │   │   ├── Info.plist
        │   │   └── Python.app
        │   ├── _CodeSignature
        │   │   └── CodeResources
        │   ├── bin
        │   │   ├── 2to3
        │   │   ├── 2to3-3.10
        │   │   ├── idle3
        │   │   ├── idle3.10
        │   │   ├── pip3
        │   │   ├── pip3.10
        │   │   ├── pydoc3
        │   │   ├── pydoc3.10
        │   │   ├── python3
        │   │   ├── python3-config
        │   │   ├── python3.10
        │   │   └── python3.10-config
        │   ├── include
        │   │   └── python3.10
        │   ├── lib
        │   │   ├── libpython3.10.dylib -> ../Python
        │   │   ├── pkgconfig
        │   │   └── python3.10
        │   └── share
        │       └── doc
        └── Current
            ├── Headers -> include/python3.10
            ├── Python
            ├── Resources
            │   ├── Info.plist
            │   └── Python.app
            ├── _CodeSignature
            │   └── CodeResources
            ├── bin
            │   ├── 2to3
            │   ├── 2to3-3.10
            │   ├── idle3
            │   ├── idle3.10
            │   ├── pip3
            │   ├── pip3.10
            │   ├── pydoc3
            │   ├── pydoc3.10
            │   ├── python3
            │   ├── python3-config
            │   ├── python3.10
            │   └── python3.10-config
            ├── include
            │   └── python3.10
            ├── lib
            │   ├── libpython3.10.dylib -> ../Python
            │   ├── pkgconfig
            │   └── python3.10
            └── share
                └── doc

```
- 可尝试用 `ln -s `将***3.10***与***Current***软连接
- 在脚本窗口中的`脚本`中添加脚本`bilibili-live.py`

```bash
cd /opt/homebrew/Cellar/python@3.10/3.10.14/Frameworks/Python.framework/Versions
```
```bash
ln -s 3.10 Current
```
