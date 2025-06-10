from pymavlink import mavutil
import time
import threading
import lib.px4_utils as px4
import csv
print("📦 px4_utils path:", px4.__file__)
master = mavutil.mavlink_connection('COM4', baud=57600)
master.wait_heartbeat()
print("✅ Kết nối thành công với PX4")
# === Hàm lấy time_boot_ms đã đồng bộ ===
px4.init_globals(master)
px4.get_time_px4()
print(f"🕒 Đồng bộ thành công: time_boot_ms FC = {px4.t0_fc} ms")

origin_msg = master.recv_match(type='LOCAL_POSITION_NED', blocking=True, timeout=10)
if origin_msg is None:
    print("❌ Không nhận được vị trí từ PX4.")
    exit(1)

origin_ned = {
    'x': origin_msg.x,
    'y': origin_msg.y,
    'z': origin_msg.z
}

print(f"✅ Gốc tọa độ (NED): {origin_ned}")

print("🚀 Gửi setpoint để PX4 chấp nhận OFFBOARD...")
   
def send_movement_command(x = 0,y = 0,altitude = 0):
    master.mav.set_position_target_local_ned_send(
        px4.get_synced_time_boot_ms(),
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,
        0b0000111111111000,  # chỉ x, y, z
        origin_ned['x'] + x, origin_ned['y'] + y, origin_ned['z'] - altitude,  # Z là độ cao so với gốc
        0, 0, 0, 0, 0, 0, 
        0, 0
    )

for _ in range(20):  # gửi trong ~1s 
    send_movement_command(0,0,1)
    time.sleep(0.05)

px4.offboard_mode()
px4.arm()
print ("✅ Chuyển sang OFFBOARD mode và đã ARM")

def load_trajectory_from_csv(path):
    trajectory = []
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                x = float(row['x'])
                y = float(row['y'])
                z = float(row['z'])
                trajectory.append((x, y, z))
            except Exception as e:
                print(f"❌ Lỗi khi đọc dòng: {row} → {e}")
    return trajectory

stop_event = threading.Event()
def thread_send_commands():

    trajectory = load_trajectory_from_csv('C:/Users/duyan/Documents/Project/Python/pixhawk1/dev/dev/trajectory.csv')
    print(f"📌 Tải {len(trajectory)} điểm từ CSV.")
    while not stop_event.is_set():
        for x, y, z in trajectory:
            if stop_event.is_set():
                break
            send_movement_command(x, y, z)
            time.sleep(0.05)  # Gửi mỗi 50ms = 20HZ
def thread_read_msg():
    while not stop_event.is_set():
        msg = master.recv_match(type='POSITION_TARGET_LOCAL_NED', blocking=True, timeout=2)
        if msg:
            print(msg)

t1 = threading.Thread(target=thread_send_commands, name="send_commands")
t2 = threading.Thread(target=thread_read_msg, name="read_msg")

t1.start()
t2.start()
  
time.sleep(15)
stop_event.set() 
px4.land_mode()

t1.join()
t2.join()

print("✅ Dừng tất cả threads và kết thúc chương trình.")
