from pyulog import ULog
ulog_file = "E:/log/2025-06-10/07_32_17.ulg"
def get_ulog():
    global ulog_file
    ulog = ULog(ulog_file)
    return ulog
