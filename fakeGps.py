from pymavlink import mavutil
import time

# === 1. Kết nối tới PX4 ===
master = mavutil.mavlink_connection('COM4', baud=57600)
master.wait_heartbeat()
print("✅ Đã kết nối với PX4")

# === 2. Lấy time_boot_ms từ LOCAL_POSITION_NED ===
print("⏳ Đợi LOCAL_POSITION_NED để đồng bộ thời gian...")
msg = master.recv_match(type='LOCAL_POSITION_NED', blocking=True, timeout=5)

if msg is None or not hasattr(msg, 'time_boot_ms'):
    print("❌ Không nhận được time_boot_ms từ PX4. Thoát.")
    exit(1)

t0_fc = msg.time_boot_ms
t0_pc = time.time()
print(f"🕒 Đồng bộ: time_boot_ms = {t0_fc} ms")

# === 3. Hàm tính time_boot_ms hiện tại ===
def get_synced_time_boot_ms():
    return (t0_fc + int((time.time() - t0_pc) * 1000)) % 4294967295
def get_synced_time_boot_us():
    elapsed_us = int((time.time() - t0_pc) * 1_000_000)
    return (t0_fc * 1000 + elapsed_us) % 0xFFFFFFFFFFFFFFFF

# === 4. Gửi fake VISION_POSITION_ESTIMATE để EKF định vị ===
def send_fake_vision_position(x=0.0, y=0.0, z=0.0, roll=0.0, pitch=0.0, yaw=0.0):
    master.mav.vision_position_estimate_send(
        get_synced_time_boot_us(),
        x, y, z,
        roll, pitch, yaw
    )

# === 5. Gửi Position Setpoint LOCAL_NED ===
def send_position_setpoint(x, y, z, yaw=0.0):
    type_mask = (
        mavutil.mavlink.POSITION_TARGET_TYPEMASK_VX_IGNORE |
        mavutil.mavlink.POSITION_TARGET_TYPEMASK_VY_IGNORE |
        mavutil.mavlink.POSITION_TARGET_TYPEMASK_VZ_IGNORE |
        mavutil.mavlink.POSITION_TARGET_TYPEMASK_AX_IGNORE |
        mavutil.mavlink.POSITION_TARGET_TYPEMASK_AY_IGNORE |
        mavutil.mavlink.POSITION_TARGET_TYPEMASK_AZ_IGNORE |
        mavutil.mavlink.POSITION_TARGET_TYPEMASK_YAW_RATE_IGNORE
    )

    master.mav.set_position_target_local_ned_send(
        get_synced_time_boot_ms(),
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,
        type_mask,
        x, y, z,
        0, 0, 0,
        0, 0, 0,
        yaw, 0
    )

# === 6. Mồi fake vision + setpoint trước OFFBOARD ===
print("🌀 Mồi VISION + POSITION_SETPOINT...")
for _ in range(50):  # ~2.5s
    send_fake_vision_position(0, 0, 0)
    send_position_setpoint(0, 0, -1.5)
    time.sleep(0.05)

# === 7. Chuyển sang OFFBOARD ===
print("🛫 Chuyển OFFBOARD...")
master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_DO_SET_MODE,
    0,
    mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
    6, 0, 0, 0, 0, 0
)

# === 8. ARM ===
print("🟢 Gửi ARM...")
master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    0,
    1, 0, 0, 0, 0, 0, 0
)

# === 9. Gửi vision + setpoint liên tục ===
print("📡 Điều khiển bay đến (0,0,-1.5)...")
for _ in range(100):  # ~5s
    send_fake_vision_position(0, 0, 0)
    send_position_setpoint(0, 0, -1.5)
    time.sleep(0.05)

# === 10. Kiểm tra phản hồi từ PX4 ===
print("📊 Kiểm tra phản hồi PX4:")

# 10.1. ODOMETRY
msg1 = master.recv_match(type='ODOMETRY', blocking=True, timeout=2)
if msg1:
    print(f"✅ PX4 nhận ODOMETRY: pos=({msg1.x:.2f}, {msg1.y:.2f}, {msg1.z:.2f})")
else:
    print("❌ Không nhận được ODOMETRY")

# 10.2. LOCAL_POSITION_NED
msg2 = master.recv_match(type='LOCAL_POSITION_NED', blocking=True, timeout=2)
if msg2:
    print(f"✅ LOCAL_POSITION_NED: x={msg2.x:.2f}, y={msg2.y:.2f}, z={msg2.z:.2f}")
else:
    print("❌ Không nhận được LOCAL_POSITION_NED")

print("✅ Hoàn tất.")
