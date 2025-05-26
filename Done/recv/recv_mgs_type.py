
# Tra xem các thông điệp MAVLink

from pymavlink import mavutil

# Tạo kết nối MAVLink qua serial hoặc UDP
# connection = mavutil.mavlink_connection('COM4', baud=57600)
connection = mavutil.mavlink_connection('COM3', baud=2000000)


# Đọc các thông điệp MAVLink
message_types = set()

# Đọc các thông điệp MAVLink và in ra tên các thông điệp một lần
while True:
    msg = connection.recv_match()  # Nhận một thông điệp MAVLink

    if msg is not None:
        message_type = msg.get_type()

        # Kiểm tra nếu thông điệp này chưa được in ra
        if message_type not in message_types:
            # In ra tên của thông điệp và đánh dấu đã in
            print(f"Received message: {message_type}")
            message_types.add(message_type)  # Thêm vào set để theo dõi
