# Windows10 或 Windows11
## 环境配置
- Python3.9+，请尽量保持安装路径无中文，将python配置到环境变量中
- OBS，需要使obs以管理员身份运行
## 配置插件
- 打开OBS
- 在菜单栏的【工具】中，选择`脚本`
- 在脚本窗口中的`python设置`中配置python安装路径
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

![img_2.png](img_2.png)
- 在脚本窗口中的`脚本`中添加脚本`bilibili-live.py`
![img.png](img.png)
![img_1.png](img_1.png)
