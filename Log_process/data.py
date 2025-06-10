from pyulog import ULog
import pandas as pd
import numpy as np
from scipy.spatial.transform import Rotation as R
import os

import ulogfile as ulogfile 
ulog =ulogfile.get_ulog()

# === Lấy dữ liệu Local Position ===
local_pos = next(d for d in ulog.data_list if d.name == 'vehicle_local_position')
df_pos = pd.DataFrame(local_pos.data)

# === Lấy dữ liệu Attitude ===
att = next(d for d in ulog.data_list if d.name == 'vehicle_attitude')
df_att = pd.DataFrame(att.data)

# === Đồng bộ thời gian (microseconds → seconds) ===
t0 = min(df_pos['timestamp'].iloc[0], df_att['timestamp'].iloc[0])
df_pos['time_s'] = (df_pos['timestamp'] - df_pos['timestamp'][0]) / 1e6
df_att['time_s'] = (df_att['timestamp'] - df_att['timestamp'][0]) / 1e6

# === Chuyển quaternion → Euler (Roll, Pitch, Yaw) ===
rot = R.from_quat(df_att[['q[1]', 'q[2]', 'q[3]', 'q[0]']].values)  # scipy dùng [x, y, z, w]
euler = rot.as_euler('xyz', degrees=True)  # roll, pitch, yaw theo độ
df_att[['roll_deg', 'pitch_deg', 'yaw_deg']] = euler

# === Gộp dữ liệu theo timestamp gần nhất (inner join bằng cách nội suy) ===
df_merge = pd.merge_asof(df_pos.sort_values('timestamp'), df_att.sort_values('timestamp'),
                         on='timestamp', direction='nearest')

df_merge['time_s'] = (df_merge['timestamp'] - df_merge['timestamp'].iloc[0]) / 1e6

# === Lưu ra file CSV ===
out_dir = "ulog_extracted"
os.makedirs(out_dir, exist_ok=True)
df_merge[['time_s', 'x', 'y', 'z', 'vx', 'vy', 'vz',
          'roll_deg', 'pitch_deg', 'yaw_deg']].to_csv(
    os.path.join(out_dir, "trajectory_data.csv"), index=False)

print("✅ Đã lưu dữ liệu vào ulog_extracted/trajectory_data.csv")
