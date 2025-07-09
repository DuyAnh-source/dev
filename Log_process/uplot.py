from pyulog import ULog
import matplotlib.pyplot as plt
import numpy as np

# Load ULog file
import ulogfile as ulogfile 
ulog =ulogfile.get_ulog()

# --- 1. Quỹ đạo bay (vẫn như cũ) ---
local_pos = [msg for msg in ulog.data_list if msg.name == 'vehicle_local_position' ][0]
x = np.array(local_pos.data['x'])
y = np.array(local_pos.data['y'])
z = np.array(local_pos.data['z'])  # Đảo dấu trục Z để hướng lên

# --- 2. Chuẩn hoá về điểm đầu (gốc tọa độ) ---
x = x - x[0]
y = y - y[0]
z = z - z[0]
t = np.array(local_pos.data['timestamp']) * 1e-6  # microseconds → seconds
t = t - t[0]

fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

axs[0].plot(t, x, label='X (North)')
axs[0].set_ylabel("X [m]")
axs[0].legend()
axs[0].grid()

axs[1].plot(t, y, label='Y (East)', color='orange')
axs[1].set_ylabel("Y [m]")
axs[1].legend()
axs[1].grid()

axs[2].plot(t, z, label='Z (Up)', color='green')
axs[2].set_ylabel("Z [m]")
axs[2].set_xlabel("Time [s]")
axs[2].legend()
axs[2].grid()

plt.suptitle("Toạ độ bay theo thời gian (Local Position - X/Y/Z)")
plt.tight_layout()

plt.figure(figsize=(8, 6))
plt.plot(x, y)
plt.title("Quỹ đạo bay (X-Y)")
plt.xlabel("X [m]")
plt.ylabel("Y [m]")
plt.grid()
plt.axis('equal')
plt.tight_layout()

# --- 2. Góc Roll-Pitch-Yaw ---
att = [msg for msg in ulog.data_list if msg.name == 'vehicle_attitude'][0]
q0 = np.array(att.data['q[0]'])
q1 = np.array(att.data['q[1]'])
q2 = np.array(att.data['q[2]'])
q3 = np.array(att.data['q[3]'])
att_time = (np.array(att.data['timestamp']) - att.data['timestamp'][0])* 1e-6 # s

def quaternion_to_euler(q0, q1, q2, q3):
    roll = np.arctan2(2*(q0*q1 + q2*q3), 1 - 2*(q1**2 + q2**2))
    pitch = np.arcsin(np.clip(2*(q0*q2 - q3*q1), -1.0, 1.0))  # tránh lỗi domain
    yaw = np.arctan2(2*(q0*q3 + q1*q2), 1 - 2*(q2**2 + q3**2))
    return roll, pitch, yaw

roll, pitch, yaw = quaternion_to_euler(q0, q1, q2, q3)
roll = np.degrees(roll)
pitch = np.degrees(pitch)
yaw = np.degrees(yaw)

# --- 3. PWM động cơ ---
actuator = [msg for msg in ulog.data_list if 'actuator_outputs' in msg.name][0]
pwm_time = (np.array(actuator.data['timestamp']) - actuator.data['timestamp'][0])*  1e-6 # s
motor0 = actuator.data['output[0]']
motor1 = actuator.data['output[1]']
motor2 = actuator.data['output[2]']
motor3 = actuator.data['output[3]']

# --- VẼ hình thứ 2: góc + PWM theo thời gian ---
fig, axs = plt.subplots(2, 1, figsize=(12, 8))

# Góc
axs[0].plot(att_time, roll, label='Roll')
axs[0].plot(att_time, pitch, label='Pitch')
axs[0].plot(att_time, yaw, label='Yaw')
axs[0].set_title("Góc Roll - Pitch - Yaw theo thời gian")
axs[0].set_ylabel("Độ")
axs[0].set_xlabel("Thời gian (s)")
axs[0].legend()
axs[0].grid()

# PWM
axs[1].plot(pwm_time, motor0, label='Motor 0')
axs[1].plot(pwm_time, motor1, label='Motor 1')
axs[1].plot(pwm_time, motor2, label='Motor 2')
axs[1].plot(pwm_time, motor3, label='Motor 3')
axs[1].set_title("PWM Động cơ theo thời gian")
axs[1].set_ylabel("PWM")
axs[1].set_xlabel("Thời gian (s)")
axs[1].legend()
axs[1].grid()

plt.tight_layout()
plt.show()
