from pyulog import ULog
import ulogfile as ulogfile 

ulog =ulogfile.get_ulog()

print("✅ Danh sách topic:")
for name in ulog.data_list:
    print(f"- {name.name} ({name.multi_id})")
