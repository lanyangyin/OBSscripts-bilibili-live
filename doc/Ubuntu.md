# Ubuntu 24.04.2 LTS


## 系统详情报告
<details>
<summary>系统详情报告</summary>

### 报告详情
- **生成日期：**                                        2025-06-23 13:43:43

### 硬件信息：
- **硬件型号：**                                        VMware, Inc. VMware Virtual Platform
- **内存：**                                          15.6 GiB
- **处理器：**                                         Intel® Core™ 5 220H × 12
- **显卡：**                                          SVGA3D; build: RELEASE; LLVM;
- **磁盘容量：**                                        68.7 GB

### 软件信息：
- **固件版本：**                                        6.00
- **操作系统名称：**                                      Ubuntu 24.04.2 LTS
- **操作系统内部版本：**                                    (null)
- **操作系统类型：**                                      64 位
- **GNOME 版本：**                                    46
- **窗口系统：**                                        Wayland
- **内核版本：**                                        Linux 6.11.0-26-generic
</details>

## 环境配置
- 打开终端
  - ![打开终端.gif](Ubuntu/%E6%89%93%E5%BC%80%E7%BB%88%E7%AB%AF.gif)
- 使用内置python3.12
  - 更新apt
    ```bash
    sudo apt update && sudo apt upgrade -y
    ```
  - 安装venv用于创建虚拟环境
    ```bash
    sudo apt install python3-venv -y
    ```
  - 安装pip用于下载第三方依赖包
    ```bash
    sudo apt install python3-pip -y
    ```
  - 创建名为 "obs-venv" 的虚拟环境
    ```bash
    python3 -m venv ~/obs-venv
    ```
  - 安装依赖包
    - 解压`Anchor_vxxx.zip`，获取`requirements.txt`文件
      - ![解压Anchor_v003.gif](Ubuntu/%E8%A7%A3%E5%8E%8BAnchor_v003.gif)
    - 在`requirements.txt`所在文件夹中打开命令行
      - ![在文件夹中打开命令行.gif](Ubuntu/%E5%9C%A8%E6%96%87%E4%BB%B6%E5%A4%B9%E4%B8%AD%E6%89%93%E5%BC%80%E5%91%BD%E4%BB%A4%E8%A1%8C.gif)
    - 激活虚拟环境：  
      ```bash
      source ~/obs-venv/bin/activate
      ```
      - 激活后，你的命令行提示符会变成 (obs-venv) user@host:~$ 的形式
    - pip安装依赖包
      ```bash
      pip install -r requirements.txt
      ```
    
## 配置obs-studio
- 安装obs-studio命令行
  ```bash
  sudo apt install obs-studio -y
  ```
- 更改obs-studio脚本文件夹权限
  - 打开`脚本控制台`
    - ![打开脚本控制台.gif](Ubuntu/%E6%89%93%E5%BC%80%E8%84%9A%E6%9C%AC%E6%8E%A7%E5%88%B6%E5%8F%B0.gif)
  - 打开`脚本选择对话框`，将`脚本文件夹`添加到`书签`
    - ![将脚本文件夹添加到书签.gif](Ubuntu/%E5%B0%86%E8%84%9A%E6%9C%AC%E6%96%87%E4%BB%B6%E5%A4%B9%E6%B7%BB%E5%8A%A0%E5%88%B0%E4%B9%A6%E7%AD%BE.gif)
  - 在`文件`打开`脚本文件夹`，并打开终端
    - ![在脚本文件夹打开终端.gif](Ubuntu/%E5%9C%A8%E8%84%9A%E6%9C%AC%E6%96%87%E4%BB%B6%E5%A4%B9%E6%89%93%E5%BC%80%E7%BB%88%E7%AB%AF.gif)
  - 修改当前文件夹权限
    ```bash
    sudo chmod 777 .
    ```
    > 如果能在脚本文件夹新建文件夹就是成功
- 载入插件
  - 将插件移动或者复制到obs-studio脚本文件夹
    - ![插件移动.gif](Ubuntu/%E6%8F%92%E4%BB%B6%E7%A7%BB%E5%8A%A8.gif)
  - 添加脚本到obs
    - ![添加脚本.gif](Ubuntu/%E6%B7%BB%E5%8A%A0%E8%84%9A%E6%9C%AC.gif)

## 启动脚本
  - 制作脚本
    ```bash
    echo '#!/bin/bash' > ~/start-obs.sh
    echo source ~/obs-venv/bin/activate >> ~/start-obs.sh
    echo obs >> ~/start-obs.sh
    echo deactivate >> ~/start-obs.sh
    ```
  - 提升权限
    ```bash
    chmod +x ~/start-obs.sh
    ```
  - 制作快捷入口【带命令行】
    ```bash
    echo '[Desktop Entry]' > $(xdg-user-dir DESKTOP)/OBS_Launcher_Creating.desktop 
    echo Name=OBS Launcher >> $(xdg-user-dir DESKTOP)/OBS_Launcher_Creating.desktop 
    echo Exec=~/start-obs.sh >> $(xdg-user-dir DESKTOP)/OBS_Launcher_Creating.desktop 
    echo Icon=com.obsproject.Studio >> $(xdg-user-dir DESKTOP)/OBS_Launcher_Creating.desktop 
    echo Terminal=true >> $(xdg-user-dir DESKTOP)/OBS_Launcher_Creating.desktop 
    echo Type=Application >> $(xdg-user-dir DESKTOP)/OBS_Launcher_Creating.desktop 
    ```
  - 制作快捷入口【不带命令行】
    ```bash
    echo '[Desktop Entry]' > $(xdg-user-dir DESKTOP)/OBS_Launcher_Creating.desktop 
    echo Name=OBS Launcher >> $(xdg-user-dir DESKTOP)/OBS_Launcher_Creating.desktop 
    echo Exec=~/start-obs.sh >> $(xdg-user-dir DESKTOP)/OBS_Launcher_Creating.desktop 
    echo Icon=com.obsproject.Studio >> $(xdg-user-dir DESKTOP)/OBS_Launcher_Creating.desktop 
    echo Terminal=false >> $(xdg-user-dir DESKTOP)/OBS_Launcher_Creating.desktop 
    echo Type=Application >> $(xdg-user-dir DESKTOP)/OBS_Launcher_Creating.desktop 
    ```
  - 提升快捷入口权限
    ```bash
    chmod +x $(xdg-user-dir DESKTOP)/OBS_Launcher_Creating.desktop
    ```
  - 允许快捷入口运行
    - ![允许快捷入口运行.gif](Ubuntu/%E5%85%81%E8%AE%B8%E5%BF%AB%E6%8D%B7%E5%85%A5%E5%8F%A3%E8%BF%90%E8%A1%8C.gif)

## ⚠️解决剪贴板问题
- 安装xclip
  ```bash
  sudo apt-get install xclip -y
  ```
  
# 开始使用
- 双击或者右键桌面OBS Launcher打开
  - ![使用.gif](Ubuntu/%E4%BD%BF%E7%94%A8.gif)

# ⚠️注意
1. 可能会总是弹出“obs studio无响应”
2. 第一次使用可能需要重新载入脚本
3. 开启OBS会较慢