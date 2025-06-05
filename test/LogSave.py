# 输出日志文件
from datetime import datetime
from typing import Literal

import obspython as obs


class globalVariableOfData:
    # #日志记录
    logRecording = ""


def logSave(logLevel: Literal[0, 1, 2, 3], logStr: str) -> None:
    """
    输出并保存日志
    Args:
        logLevel:
        logStr:
    Returns:
    """
    logType = {
        0: obs.LOG_INFO,
        1: obs.LOG_DEBUG,
        2: obs.LOG_WARNING,
        3: obs.LOG_ERROR,
    }
    now = datetime.now()
    formatted = now.strftime("%Y/%m/%d %H:%M:%S")
    log_text = f"【{formatted}】【{logLevel}】{logStr}"
    obs.script_log(logType[logLevel], log_text)
    globalVariableOfData.logRecording += log_text + "\n"


logSave(0, "已卸载：bilibili-live")
with open(f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.log", "w", encoding="utf-8") as f:
    f.write(str(globalVariableOfData.logRecording))

