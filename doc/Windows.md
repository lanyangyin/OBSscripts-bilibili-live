# Windows10+
## 环境配置
- Python3.9-3.12，请尽量保持安装路径无中文，将python配置到环境变量中
- OBS，需要使obs以管理员身份运行
![gif0.gif](gif0.gif)
## 配置插件
- 打开OBS
- 在菜单栏的【工具】中，选择`脚本`
![gif1.gif](gif1.gif)

- 使用以下代码获得python安装路径
```bash
python
```
```python
import sys
print(sys.prefix)
exit()

```
- python路径示例
```
C:/Users/lanan/AppData/Local/Programs/Python/Python310
```
- 在脚本窗口中的`python设置`中配置python安装路径
![gif2.gif](gif2.gif)
- 在脚本窗口中的`脚本`中添加脚本`bilibili-live.py`
![gif3.gif](gif3.gif)