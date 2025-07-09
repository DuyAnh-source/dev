from pymavlink import mavutil
import time
import threading
import px4_utils as px4
import csv

master = mavutil.mavlink_connection('COM4', baud=57600)
master.wait_heartbeat()
print("✅ Kết nối thành công với PX4")

# === Hàm lấy time_boot_ms đã đồng bộ ===
px4.init_globals(master)
px4.get_time_px4()
print(f"🕒 Đồng bộ thành công: time_boot_ms FC = {px4.t0_fc} ms")
# === Hàm lấy gốc ===
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

# === Chuyển sang OFFBOARD mode ===
print("🚀 Gửi setpoint để PX4 chấp nhận OFFBOARD...")
for _ in range(20):  # gửi trong ~1s 
    px4.send_movement_pos_ned(origin_ned = origin_ned,x = 0,y = 0,altitude = 0.5)
    time.sleep(0.05)
px4.offboard_mode()
px4.arm()
print ("✅ Chuyển sang OFFBOARD mode và đã ARM")

# Cất cánh
for _ in range(100):  # gửi trong ~5s 
    px4.send_movement_pos_ned(origin_ned = origin_ned,x = 0,y = 0,altitude = 0.5)
    time.sleep(0.05)

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
trajectory = load_trajectory_from_csv('C:/Users/duyan/Documents/Project/Python/pixhawk1/dev/experiment/trajectory.csv')
print(f"📌 Tải {len(trajectory)} điểm từ CSV.")

def thread_send_commands():
    for x, y, z in trajectory:
        if stop_event.is_set():
            break
        px4.send_movement_pos_ned(origin_ned = origin_ned,x = x,y = y,altitude = z)
        time.sleep(0.05)  # Gửi mỗi 50ms = 20HZ
    stop_event.set() 
    px4.land_mode()
            
def thread_read_msg():
    while not stop_event.is_set():
        msg = master.recv_match(type='POSITION_TARGET_LOCAL_NED', blocking=True, timeout=2)
        if msg:
            print(msg)

t1 = threading.Thread(target=thread_send_commands, name="send_commands")
t2 = threading.Thread(target=thread_read_msg, name="read_msg")

t1.start()
t2.start()
  
time.sleep(10)
stop_event.set() 
px4.land_mode()

t1.join()
t2.join()

print("✅ Dừng tất cả threads và kết thúc chương trình.")
