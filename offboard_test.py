from pymavlink import mavutil
import time

# === 1. Kết nối tới PX4 ===
master = mavutil.mavlink_connection('COM4', baud=57600)
master.wait_heartbeat()
print("✅ Kết nối thành công với PX4")

# === Step 2: Lấy time_boot_ms gốc từ FC để đồng bộ ===
print("⏳ Đang đợi bản tin LOCAL_POSITION_NED để đồng bộ thời gian...")
msg = master.recv_match(type='LOCAL_POSITION_NED', blocking=True, timeout=5)

if msg is None or not hasattr(msg, 'time_boot_ms'):
    print("❌ Không nhận được time_boot_ms từ FC. Thoát.")
    exit(1)

t0_fc = msg.time_boot_ms
t0_pc = time.time()
print(f"🕒 Đồng bộ thành công: time_boot_ms FC = {t0_fc} ms")

# === Hàm lấy time_boot_ms đã đồng bộ ===
def get_synced_time_boot_ms():
    elapsed_pc_ms = int((time.time() - t0_pc) * 1000)
    return (t0_fc + elapsed_pc_ms) % 4294967295

# === 2. Hàm gửi setpoint attitude ===
def send_position_setpoint(x=0, y=0, z=-1, yaw=0):
    master.mav.set_position_target_local_ned_send(
        get_synced_time_boot_ms(),              # time_boot_ms
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,    # hệ tọa độ Local NED
        0b0000111111000111,                     # chỉ dùng vị trí x, y, z và yaw
        x, y, z,                                # vị trí (Z âm là bay lên)
        0, 0, 0,                                # vx, vy, vz
        0, 0, 0,                                # ax, ay, az
        yaw, 0                                  # yaw, yaw_rate
    )
# === 3. Gửi setpoint liên tục trong 1 giây để "mồi" OFFBOARD ===
print("🚀 Gửi setpoint để PX4 chấp nhận OFFBOARD...")
for _ in range(20):
    send_position_setpoint(0, 0, -1.5, yaw=0)  # trung lập
    time.sleep(0.05)             # ~20Hz

# === 4. Gửi lệnh chuyển sang OFFBOARD ===
print("🛫 Chuyển sang OFFBOARD mode...")
master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_DO_SET_MODE,
    0,
    mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
    6,  # OFFBOARD
    0, 0, 0, 0, 0
)

time.sleep(0.2)  # đợi một chút cho PX4 xử lý

# === 5. Gửi lệnh ARM ===
print("🟢 Gửi lệnh ARM")
master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    0,
    1, 0, 0, 0, 0, 0, 0
)

# === 6. Gửi setpoint liên tục để PX4 bay lên (thrust > 0.5) ===
print("📡 Đang gửi setpoint điều khiển...")
for _ in range(100):
    send_position_setpoint(3, 4, -5, yaw=0)  # thrust > 0.5 → bay lên
    time.sleep(0.05)             # 20Hz
    msg = master.recv_match()  # Nhận một thông điệp MAVLink
    if msg is not None:
        message_type = msg.get_type()
        if message_type == "LOCAL_POSITION_NED":
            print(msg.x, msg.y, msg.z)
        if  message_type == "POSITION_TARGET_LOCAL_NED":
            print(msg)
            # print(msg.x, msg.y, msg.z, msg.yaw)


print("✅ Đã gửi xong setpoint điều khiển")
