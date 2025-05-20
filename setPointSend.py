from pymavlink import mavutil
import time

# === Step 1: Kết nối tới UAV ===
master =  mavutil.mavlink_connection('COM4', baud=57600)
master.wait_heartbeat()
print("✅ Đã kết nối tới UAV")

master.mav.command_long_send(
    1, 1,
    mavutil.mavlink.MAV_CMD_DO_SET_MODE,
    0,
    1,  # base_mode: MAV_MODE_FLAG_CUSTOM_MODE_ENABLED
    6,  # custom_mode: 6 = OFFBOARD (với PX4)
    0, 0, 0, 0, 0
)

# === Step 2: Gửi setpoint vị trí LOCAL_NED ===
def send_setpoint_position(x, y, z):

    master.mav.set_position_target_local_ned_send(
        0,
        master.target_system,
        0,
        8,
        4039,
        0, 0, 0,
        x, y, z,
        0, 0, 0,
        0, 0
    )

# === Step 3: Gửi liên tục vài lần để UAV nhận ===
print("📡 Đang gửi setpoint...")
for _ in range(10):  # gửi liên tục để bảo đảm nhận
    send_setpoint_position(0, 0, 0.2)
    time.sleep(0.1)

# === Step 4: Kiểm tra phản hồi POSITION_TARGET_LOCAL_NED ===
print("🔍 Đang kiểm tra phản hồi setpoint từ UAV...")
msg = master.recv_match(type='POSITION_TARGET_LOCAL_NED', blocking=True, timeout=3)

if msg:
    print(f"✅ Setpoint đang active: x={msg.x:.2f}, y={msg.y:.2f}, z={msg.z:.2f}, yaw={msg.yaw:.2f}")
else:
    print("❌ Không nhận được phản hồi setpoint từ UAV.")
