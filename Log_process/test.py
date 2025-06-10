from pyulog import ULog

ulog = ULog("log_file/12_20_00.ulg")

print("✅ Danh sách topic:")
for name in ulog.data_list:
    print(f"- {name.name} ({name.multi_id})")
