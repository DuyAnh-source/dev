
# Tra xem các thông điệp MAVLink

from pymavlink import mavutil

# Tạo kết nối MAVLink qua serial hoặc UDP
connection = mavutil.mavlink_connection('COM4', baud=57600)
# master = mavutil.mavlink_connection('udp:127.0.0.1:14550')  # Cho kết nối UDP


# Đọc các thông điệp MAVLink và in ra tên các thông điệp một lần
while True:
    msg = connection.recv_match()  # Nhận một thông điệp MAVLink

    if msg is not None:
        message_type = msg.get_type()

        # Kiểm tra nếu thông điệp này chưa được in ra
        if message_type == "GPS_RAW_INT":
            # In ra tên của thông điệp và đánh dấu đã in
            print(msg.lat, msg.lon, msg.alt, msg.satellites_visible)
        if message_type == "LOCAL_POSITION_NED":
            print(msg.x, msg.y, msg.z)
            