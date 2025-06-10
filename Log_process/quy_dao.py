from pyulog import ULog
import matplotlib.pyplot as plt
import pandas as pd

import ulogfile as ulogfile 
ulog =ulogfile.get_ulog()

pos = next(d for d in ulog.data_list if d.name == 'vehicle_local_position')

df = pd.DataFrame(pos.data)
plt.plot(df['y'], df['x'])  # quỹ đạo theo mặt phẳng ngang
plt.xlabel("Y (m)")
plt.ylabel("X (m)")
plt.title("🛩️ Quỹ đạo bay XY (local)")
plt.grid()
plt.axis("equal")
plt.show()