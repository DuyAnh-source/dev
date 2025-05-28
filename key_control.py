from pymavlink import mavutil
import time
import threading
import math
from pynput import keyboard

import px4_utils as px4

thrust = 0.4  # Thrust > 0.5 để bay lên
thrust_step = 0.05  # Bước thay đổi thrust
yaw_deg = 0.0  # Góc yaw, có thể thay đổi nếu cần
pitch_deg = 0.0  # Góc pitch, có thể thay đổi nếu cần
roll_deg = 0.0  # Góc roll, có thể thay đổi nếu cần
attitude_step = 0.1  # Bước thay đổi góc attitude

# === 1. Kết nối tới PX4 ===
master = mavutil.mavlink_connection('COM3', baud=2000000)
# master = mavutil.mavlink_connection('COM4', baud=57600)
master.wait_heartbeat()
print("✅ Kết nối thành công với PX4")
px4.init_globals(master)
# === Hàm lấy time_boot_ms đã đồng bộ ===
px4.get_time_px4()
print(f"🕒 Đồng bộ thành công: time_boot_ms FC = {px4.t0_fc} ms")
print("🚀 Gửi setpoint để PX4 chấp nhận OFFBOARD...")
px4.init_setpoint()

px4.offboard_mode()
px4.arm()

# === 6. Gửi setpoint liên tục để PX4 bay lên (thrust > 0.5) ===

stop_event = threading.Event()

def task1():
    global thrust
    while not stop_event.is_set():
        print(f"Thrust: {thrust:.2f}, Pitch: {pitch_deg}°, Roll: {roll_deg}°, Yaw: {yaw_deg}°")
        px4.send_attitude_setpoint(thrust)  # thrust > 0.5 → bay lên
        time.sleep(0.05)             # 20Hz

def task2():
    while not stop_event.is_set():
        msg1 = px4.get_servo_output_raw()
        msg2 = px4.get_attitude()      
        if msg1 is not None and msg2 is not None:
            print(f"🟢 Servo: {msg1}, Atitude: {msg2}")
        time.sleep(0.1)
 
def on_release(key):
    global thrust
    global pitch_deg, roll_deg, yaw_deg
    global thrust_step, attitude_step
    if key == keyboard.Key.esc:
        stop_event.set()    
        print("Thoát chương trình.")
        # time.sleep(0.5)
        # px4.disArm()
        return False  # Dừng listener
    elif key == keyboard.Key.space:
        thrust = thrust - thrust_step
        if thrust < 0:
            thrust = 0
        print(f"Giảm thrust: {thrust:.2f}")
    elif key == keyboard.Key.enter:
        thrust = thrust + thrust_step
        if thrust > 1.0:
            thrust = 1.0
        print(f"Tăng thrust: {thrust:.2f}")
    elif key == keyboard.Key.up:
        pitch_deg += attitude_step
        print(f"Tăng pitch: {pitch_deg}°")
    elif key == keyboard.Key.down:
        pitch_deg -= attitude_step
        print(f"Giảm pitch: {pitch_deg}°")
    elif key == keyboard.Key.left:
        roll_deg -= attitude_step
        print(f"Giảm roll: {roll_deg}°")
    elif key == keyboard.Key.right:
        roll_deg += attitude_step
        print(f"Tăng roll: {roll_deg}°")
def key_listener():
    with keyboard.Listener(on_release=on_release) as listener:
        listener.join()

t1 = threading.Thread(target=task1)
t2 = threading.Thread(target=task2) 
t_key = threading.Thread(target=key_listener)   

t1.start()
t2.start()
t_key.start()

# disArm()

