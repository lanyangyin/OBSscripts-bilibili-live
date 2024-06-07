# coding=utf-8
import obspython as obs

# --[[正式插件]]

# --- 设置默认值
def script_defaults(settings):
    pass

# --- 一个名为script_description的函数返回显示给的描述
def script_description():
    t = '<html lang="zh-CN"><body><pre>\
本插件基于python3<br>\
    如果未安装python3，请前往<br>\
        <a href="https://www.python.org/">python官网</a><br>\
        或者<br>\
        <a href="https://python.p2hp.com/">python中文网 官网</a>下载安装<br>\
        不同操作系统请查看<br>\
            菜鸟教程<a href="https://www.runoob.com/python3/python3-install.html">Python3 环境搭建</a><br>\
<font color=yellow>!脚本路径中尽量不要有中文</font><br>\
<font color=green size=4>请在认为完成全部操作后点击<font color="white" size=5>⟳</font>重新载入插件</font><br>\
配置cookie：<br>\
<font color=yellow>！请看着脚本日志操作</font><br>\
扫描配置cookie请 提前增加<br>\
   脚本日志窗口 宽高<br>\
手动配置cookie请前往<br>\
   <a href="https://link.bilibili.com/p/center/index#/my-room/start-live">B站直播设置后台</a> 使用<br>\
       浏览器的开发人员工具获取cookie<br><br>\
<font color="#ee4343">【cookie！为账号的{极重要}的隐私信息!】</font><br>\
<font color="#ee4343">【！请 不要泄露给他人!】</font><br>\
<br>\
如果报错：<br>\
   请关闭梯子和加速器<br>\
   Windows请尝试使用管理员权限运行obs<br>\
   其它系统请联系制作者<br></pre></body></html>'
    return t

