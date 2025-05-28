from pymavlink import mavutil
import time
import threading

# === 1. Kết nối tới PX4 ===
master = mavutil.mavlink_connection('COM3', baud=2000000)
# master = mavutil.mavlink_connection('COM4', baud=57600)
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
def send_attitude_setpoint(thrust=0.6):
    # Quaternion tương ứng attitude = 0 roll/pitch/yaw
    q = [1, 0, 0, 0]
    master.mav.set_attitude_target_send(
        get_synced_time_boot_ms(),        # time_boot_us
        master.target_system,
        master.target_component,
        0b00000111,                    # ignore body rates & yaw
        q,
        0, 0, 0,                       # body rates
        thrust                         # thrust từ 0.0 đến 1.0
    )

# === 3. Gửi setpoint liên tục trong 1 giây để "mồi" OFFBOARD ===
print("🚀 Gửi setpoint để PX4 chấp nhận OFFBOARD...")
for _ in range(20):
    send_attitude_setpoint(0.5)  # trung lập
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

def task1():
    while True:
        send_attitude_setpoint(0.3)  # thrust > 0.5 → bay lên
        time.sleep(0.05)             # 20Hz

def task2():
    while True:
        msg = master.recv_match(type='SERVO_OUTPUT_RAW', blocking=False, timeout=5)
        if msg is not None:
            print(msg.servo1_raw, msg.servo2_raw, msg.servo3_raw, msg.servo4_raw)

t1 = threading.Thread(target=task1)
t2 = threading.Thread(target=task2) 
t1.start()
t2.start()


# Gửi lệnh DISARM
master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,  # Mã lệnh ARM/DISARM
    0,      # confirmation
    0,      # param1 = 0 để DISARM
    0, 0, 0, 0, 0, 0
)

print("✅ Đã gửi xong setpoint điều khiển")

