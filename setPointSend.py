from pymavlink import mavutil
import threading
import time

# === Step 1: Kết nối UAV ===
master = mavutil.mavlink_connection('COM4', baud=57600)
master.wait_heartbeat()
print("✅ Đã kết nối tới UAV")

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

# === Step 3: Hàm gửi setpoint LOCAL_NED ===
def send_setpoint_position(x, y, z, yaw=0.0):
    time_boot_ms = get_synced_time_boot_ms()
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
        time_boot_ms,
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,
        type_mask, 
        x, y, z,
        0, 0, 0,
        0, 0, 0,
        yaw, 0
    )

def read_loop():
    while True:
        msg = master.recv_match(type='POSITION_TARGET_LOCAL_NED', blocking=False)
        if msg:
            print(f"✅ Setpoint active: x={msg.x:.2f}, y={msg.y:.2f}, z={msg.z:.2f}, yaw={msg.yaw:.2f}")
        else:
            print("⏳ Không nhận được phản hồi setpoint.")
        time.sleep(0.1)
     
# === Step 4: Chuyển UAV sang chế độ Manual ===
master.mav.command_long_send(
    1, 1,
    mavutil.mavlink.MAV_CMD_DO_SET_MODE,
    0,
    1,  # base_mode: MAV_MODE_FLAG_CUSTOM_MODE_ENABLED
    0,  # custom_mode: 0: MANUAL (với PX4)
    0, 0, 0, 0, 0
)
print("Chuyển sang chế độ MANUAL")
pause_event = threading.Event()  # Event để điều khiển pause/resume
pause_event.set()  # Cho phép chạy ban đầu
def setpoint_loop():
    while True:
        pause_event.wait()  # Nếu pause_event bị clear thì sẽ block tại đây
        send_setpoint_position(0, 0, -3.0, yaw=0.5)
        print(f"📤 Gửi setpoint: x=0, y=0, z=-3.0, yaw=0.5")
        time.sleep(0.1)  # 10Hz
setpoint_thread = threading.Thread(target=setpoint_loop)   
setpoint_thread.start()
print("Gửi setpoint")
time.sleep(5)
# Đợi 5 giây 
pause_event.clear()  # Dừng lại tại pause_event.wait()
print("⏸️ Đã tạm dừng gửi setpoint")
master.mav.command_long_send(
    1, 1,
    mavutil.mavlink.MAV_CMD_DO_SET_MODE,
    0,
    1,  # base_mode: MAV_MODE_FLAG_CUSTOM_MODE_ENABLED
    6,  # custom_mode: 6: OFFBOARD (với PX4)
    0, 0, 0, 0, 0
)
print ("Chuyển sang chế độ OFFBOARD")
# Gửi lệnh ARM
master.mav.command_long_send(
    master.target_system,           # target_system
    master.target_component,        # target_component
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, # command
    0,                              # confirmation
    1, 0, 0, 0, 0, 0, 0             # param1 = 1 để arm, các param khác không dùng
)
print("Đã gửi lệnh ARM")
pause_event.set()  # Cho phép chạy tiếp
print("▶️ Đã tiếp tục gửi setpoint")