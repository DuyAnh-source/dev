from pyulog import ULog
ulog_file = "F:/log/2025-07-02/09_26_47.ulg"
def get_ulog():
    global ulog_file
    ulog = ULog(ulog_file)
    return ulog
