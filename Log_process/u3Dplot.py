from pyulog import ULog
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from matplotlib import cm

# Load file
import ulogfile as ulogfile 
ulog =ulogfile.get_ulog()

# --- 1. Lấy dữ liệu từ vehicle_local_position ---
local_pos = [msg for msg in ulog.data_list if msg.name == 'vehicle_local_position'][0]
y = np.array(local_pos.data['x'])
x = np.array(local_pos.data['y'])
z = - np.array(local_pos.data['z'])
t = np.array(local_pos.data['timestamp']) * 1e-6  # microseconds → seconds

# --- 2. Chuẩn hóa vị trí và thời gian ---
x = x - x[0]
y = y - y[0]
z = z - z[0]
t = t - t[0]

# --- 3. Tạo các đoạn line nhỏ để tô màu ---
points = np.array([x, y, -z]).T.reshape(-1, 1, 3)  # reshape cho đúng định dạng
segments = np.concatenate([points[:-1], points[1:]], axis=1)

# --- 4. Chuẩn hóa thời gian thành màu ---
norm = plt.Normalize(t.min(), t.max())
colors = cm.viridis(norm(t[:-1]))  # bỏ điểm cuối vì đoạn line <=> giữa 2 điểm

# --- 5. Vẽ bằng Line3DCollection ---
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

lc = Line3DCollection(segments, colors=colors, linewidth=2)
ax.add_collection3d(lc)

# Thiết lập trục và tiêu đề
ax.set_title("Quỹ đạo bay 3D tô màu theo thời gian")
ax.set_xlabel("X [m]")
ax.set_ylabel("Y [m]")
ax.set_zlabel("Z [m]")
ax.grid(True)
ax.auto_scale_xyz(x, y, z)

# --- 6. Thêm colorbar ---
mappable = cm.ScalarMappable(cmap='viridis', norm=norm)
mappable.set_array([])
cbar = plt.colorbar(mappable, ax=ax, pad=0.1)
cbar.set_label("Thời gian bay (s)")

plt.tight_layout()
plt.show()
