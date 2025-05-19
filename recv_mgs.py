
# Tra xem các thông điệp MAVLink

from pymavlink import mavutil

# Tạo kết nối MAVLink qua serial hoặc UDP
connection = mavutil.mavlink_connection('COM4', baud=57600)
# master = mavutil.mavlink_connection('udp:127.0.0.1:14550')  # Cho kết nối UDP

# Đọc các thông điệp MAVLink và in ra tên các thông điệp một lần
while True:
    msg = connection.recv_match()  # Nhận một thông điệp MAVLink
    if msg is not None:
        print(msg)
        print(' ')