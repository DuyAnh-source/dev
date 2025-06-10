
from pyulog import ULog
import matplotlib.pyplot as plt
import pandas as pd

import ulogfile as ulogfile 
ulog =ulogfile.get_ulog()

ao = next(d for d in ulog.data_list if d.name == 'actuator_outputs' and d.multi_id == 0)
df_pwm = pd.DataFrame(ao.data)

for i in range(4):  # chỉ 4 motor đầu
    plt.plot(df_pwm['timestamp'] / 1e6, df_pwm[f'output[{i}]'], label=f'Motor {i+1}')

plt.xlabel("Thời gian (s)")
plt.ylabel("PWM output")
plt.title("⚙️ PWM các động cơ")
plt.legend()
plt.grid()
plt.show()
