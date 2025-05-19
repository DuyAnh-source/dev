from pymavlink import mavutil

import time 

# Kết nối tới Pixhawk qua cổng UART/USB hoặc UDP
master = mavutil.mavlink_connection('COM4', baud=57600)  # Thay đổi cổng COM hoặc ttyACMx tùy hệ điều hành

# Chờ cho đến khi nhận được heartbeat từ hệ thống
master.wait_heartbeat()
print("Heartbeat từ hệ thống nhận được")

# Gửi lệnh ARM
master.mav.command_long_send(
    master.target_system,           # target_system
    master.target_component,        # target_component
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, # command
    0,                              # confirmation
    1, 0, 0, 0, 0, 0, 0             # param1 = 1 để arm, các param khác không dùng
)
print("Đã gửi lệnh ARM")

# Đọc phản hồi từ Pixhawk (tùy chọn)
ack = master.recv_match(type='COMMAND_ACK', blocking=True)
print(f"ACK: {ack}")

time.sleep(3)  # Chờ 3 giây để động cơ chạy

# Gửi lệnh DISARM
master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,  # Mã lệnh ARM/DISARM
    0,      # confirmation
    0,      # param1 = 0 để DISARM
    0, 0, 0, 0, 0, 0
)

# (Tuỳ chọn) In phản hồi ACK
ack = master.recv_match(type='COMMAND_ACK', blocking=True)
print(f"DISARM ACK: {ack}")