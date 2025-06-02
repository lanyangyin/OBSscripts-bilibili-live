# macOS 14+

## 环境配置
<details>
<summary>使用macOS内置python</summary>

### 使用macOS内置python
#### 完善python文件结构
```bash
cd /Library/Developer/CommandLineTools/Library/Frameworks
sudo ln -s Python3.framework Python.framework
```
#### 配置python
- 检查版本
```bash
python3 --version
```
- pip换源
```bash
python3 -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```
- 安装插件依赖的python包
```bash
python3 -m pip install -r requirements.txt
```
</details>
<details>
<summary>使用官方python</summary>

### 使用官方python
#### 安装 git
```bash
git --version
```
#### 安装homebrew
- 安装脚本
```bash
/bin/zsh -c "$(curl -fsSL https://gitee.com/cunkai/HomebrewCN/raw/master/Homebrew.sh)"
```
- 检查版本
```bash
brew --version 
```
#### 配置python
- 安装python
```bash
brew install python@3.10
```
- 检查版本
```bash
python3.10 --version
```
- pip换源
```bash
python3.10 -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```
- 安装插件依赖的python包
```bash
python3.10 -m pip install -r requirements.txt
```
#### 完善python文件结构

<details>
<summary>Frameworks目录结构大致如下</summary>

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
</details>

- 完善文件结构
```bash
cd /opt/homebrew/opt/python@3.10/Frameworks/Python.framework/Versions
sudo ln -s 3.10 Current
```
</details>

***
## OBS配置
### OBS连接python
#### 在菜单栏的`工具`中，选择`脚本`，点击`python设置`
图0![mo0.gif](macOS/mo0.gif)
#### 使用以下代码获得python安装路径

<details>
<summary>使用macOS内置python</summary>

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
/Library/Developer/CommandLineTools/Library/Frameworks
```
#### 在脚本窗口中的`python设置`中配置python安装路径
图1![mo1.gif](macOS/mo1.gif)
</details>
<details>
<summary>使用官方python</summary>

```bash
python3.10
```
```python
import sys
print(sys.prefix)
exit()
```
- python路径示例
```
/opt/homebrew/opt/python@3.10/Frameworks
```
#### 在脚本窗口中的`python设置`中配置python安装路径
图2![mo2.gif](macOS/mo2.gif)
</details>

***
### OBS载入脚本
#### 在脚本窗口中的`脚本`中添加脚本`bilibili_live_Anchor.py`
图3![mo3.gif](macOS/mo3.gif)
