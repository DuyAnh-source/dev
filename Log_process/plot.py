import pandas as pd
import matplotlib.pyplot as plt

# === Đọc dữ liệu từ file CSV ===
df = pd.read_csv("ulog_extracted/trajectory_data.csv")

# === Vẽ 1: Quỹ đạo bay theo mặt phẳng XY ===
plt.figure()
plt.plot(df['y'], df['x'])
plt.xlabel("Y (m)")
plt.ylabel("X (m)")
plt.title("🛩️ Quỹ đạo bay (XY)")
plt.axis('equal')
plt.grid()

# === Vẽ 2: Độ cao theo thời gian ===
plt.figure()
plt.plot(df['time_s'], -df['z'])
plt.xlabel("Thời gian (s)")
plt.ylabel("Độ cao Z (m)")
plt.title("📈 Độ cao theo thời gian")
plt.grid()

# === Vẽ 3: Vận tốc theo thời gian ===
plt.figure()
plt.plot(df['time_s'], df['vx'], label='vx')
plt.plot(df['time_s'], df['vy'], label='vy')
plt.plot(df['time_s'], df['vz'], label='vz')
plt.xlabel("Thời gian (s)")
plt.ylabel("Vận tốc (m/s)")
plt.title("⚡ Vận tốc theo thời gian")
plt.legend()
plt.grid()

# === Vẽ 4: Góc Roll/Pitch/Yaw theo thời gian ===
plt.figure()
plt.plot(df['time_s'], df['roll_deg'], label='Roll (°)')
plt.plot(df['time_s'], df['pitch_deg'], label='Pitch (°)')
plt.plot(df['time_s'], df['yaw_deg'], label='Yaw (°)')
plt.xlabel("Thời gian (s)")
plt.ylabel("Góc (°)")
plt.title("🌀 Góc Roll, Pitch, Yaw")
plt.legend()
plt.grid()

# === Hiển thị tất cả biểu đồ ===
plt.show()
