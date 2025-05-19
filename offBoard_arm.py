from pymavlink import mavutil
import time
import threading

# Connect to the vehicle
master = mavutil.mavlink_connection('COM4', baud=57600)
master.wait_heartbeat()
print("✔ Heartbeat received")

system_id = master.target_system
component_id = master.target_component
boot_time = time.time()

def send_setpoints_loop():
    while True:
        time_boot_ms = int((time.time() - boot_time) * 1000)
        master.mav.set_position_target_local_ned_send(
            time_boot_ms,
            system_id,
            component_id,
            mavutil.mavlink.MAV_FRAME_LOCAL_NED,
            0b0000111111000111,  # bỏ qua velocity, acceleration, yaw_rate
            0, 0, -2,            # vị trí mong muốn (x, y, z)
            0, 0, 0,
            0, 0, 0,
            0, 0
        )
        time.sleep(0.1)  # 10Hz

def arm_offboard_thread():
    # Gửi lệnh ARM
    print("🛡 Arming...")
    master.arducopter_arm()
    master.motors_armed_wait()
    print("✔ Vehicle is armed")

    # Khởi động cả hai luồng
threading.Thread(target=send_setpoints_loop, daemon=True).start()
time.sleep(1)  # Đợi một chút trước khi gửi lệnh OFFBOARD
threading.Thread(target=arm_offboard_thread, daemon=True).start()

# Giữ chương trình chạy
while True:
    time.sleep(1)