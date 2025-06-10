from pymavlink import mavutil
import time
import threading
import lib.px4_utils as px4

master = mavutil.mavlink_connection('COM4', baud=57600)
master.wait_heartbeat()
print("✅ Kết nối thành công với PX4")
# === Hàm lấy time_boot_ms đã đồng bộ ===
px4.init_globals(master)
px4.get_time_px4()
print(f"🕒 Đồng bộ thành công: time_boot_ms FC = {px4.t0_fc} ms")

def send_act():

    master.mav.set_actuator_control_target_send(
        0,
        master.target_system,
        master.target_component,
        0,  # group_mlx = 0
        [0.5, 0.5, 0.5, 0.5, 0, 0, 0, 0]  # 50% PWM cho 4 motor
    )
for _ in range(20):  # gửi trong ~1s 
    send_act()
    time.sleep(0.05)

px4.offboard_mode()
px4.arm()

# 4. Gửi lệnh điều khiển motor (giá trị -1.0 → 1.0)
stop_event = threading.Event()
def thread_send_commands():
    while not stop_event.is_set():
        send_act()
        time.sleep(0.05)

t1 = threading.Thread(target=thread_send_commands, name="send_commands")
t1.start()

time.sleep(4)
stop_event.set()