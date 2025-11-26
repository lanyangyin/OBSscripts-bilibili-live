# Windows 7
## 环境配置
### 配置Python
#### 安装python
- Python版本号3.6.8
- 请尽量保持安装路径无中文
#### 配置python环境变量
```python
import sys
print(sys.prefix)
exit()
```
图![gif.gif](Windows/gif.gif)
#### 检查版本
```bash
python --version
```
#### pip换源
```bash
python -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```
#### 安装插件依赖的python包
```bash
python -m pip install -r requirements_python3.6.txt
```
***
## OBS配置
### OBS需要使obs以管理员身份运行
#### 右键obs --> 属性 --> 兼容性 --> 以管理员身份运行此程序
图![gif0.gif](Windows/gif0.gif)
### OBS连接python
#### 在菜单栏的`工具`中，选择`脚本`，点击`python设置`
图![gif1.gif](Windows/gif1.gif)
#### 使用以下代码获得python安装路径
```bash
python
```
```python
import sys
print(sys.prefix)
exit()
```
- python安装路径示例
```
C:/Users/$USER/AppData/Local/Programs/Python/Python36
```
#### 在脚本窗口中的`python设置`中配置python安装路径
图![gif2.gif](Windows/gif2.gif)
***
## OBS载入脚本
### 在脚本窗口中的`脚本`中添加脚本`bilibili_live_multi_py36_obs27.py`
图![gif3.gif](Windows/gif3.gif)