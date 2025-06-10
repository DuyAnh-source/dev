from pyulog import ULog
import matplotlib.pyplot as plt
import pandas as pd

import ulogfile as ulogfile 
ulog =ulogfile.get_ulog()

pos = next(d for d in ulog.data_list if d.name == 'vehicle_local_position')

df = pd.DataFrame(pos.data)
df['timestamp_s'] = (df['timestamp'] - df['timestamp'][0]) / 1e6  # ms → s

plt.plot(df['timestamp_s'], -df['z'])  # z thường là âm khi bay lên
plt.xlabel("Thời gian (s)")
plt.ylabel("Độ cao (m)")
plt.title("📈 Độ cao theo thời gian")
plt.grid()
plt.show()
