# Windows
## 集成Python环境，制作方便OBS导入的脚本

### 1. 下载Python嵌入式版本
- Win7：`https://www.python.org/ftp/python/3.6.8/python-3.6.8-embed-amd64.zip`
- Win10+：`https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip`

### 2. 解压并修改`python<version>._pth`
- 取消`import site`的注释并保存

### 3. 下载Pip
- Win7：`https://bootstrap.pypa.io/pip/3.6/get-pip.py`
- Win10+：`https://bootstrap.pypa.io/get-pip.py`

### 4. 安装Pip
- 打开终端，`cd`到嵌入式版Python的解压目录，输入指令：
```bash
./python get-pip.py
```

### 5. Pip换源
```bash
python -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### 6. 安装依赖
```bash
cd Scripts
./pip install -r requirements.txt
```

### 7. 打包
- 删除Scripts文件夹及其内容（里面的.exe是路径硬编码的）
- 把`bilibili_live_multi.py`和嵌入式版Python的解压目录打成压缩包
- 记得加上使用说明