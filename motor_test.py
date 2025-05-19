from pymavlink import mavutil
import time

# Kết nối với PX4 thông qua cổng serial hoặc TCP/UDP
# Ví dụ: kết nối qua cổng serial (COM3 cho Windows hoặc /dev/ttyACM0 cho Linux)
connection = mavutil.mavlink_connection('COM3', baud=2000000)

# Đảm bảo kết nối đã được thiết lập
connection.wait_heartbeat()
print("Kết nối thành công!")

# Gửi lệnh điều khiển động cơ
# Giả sử bạn muốn gửi tín hiệu PWM tới 4 động cơ (1, 2, 3, 4)
actuator_controls = [1500, 1500, 1500, 1500]  # PWM cho mỗi động cơ

# Gửi lệnh SET_ACTUATOR_CONTROL_TARGET
# Đầu tiên, xây dựng đối tượng message cho lệnh này
msg = connection.mavlink.MAVLink_actuator_control_target_message(
    1,  # ID của hệ thống (PX4)
    0,  # Timestamp (có thể để 0 nếu không dùng)
    *actuator_controls,  # Các giá trị PWM cho động cơ (chú ý có 4 giá trị ở đây)
    0, 0, 0, 0  # Các actuator khác (nếu có, nếu không thì để 0)
)

# Gửi message này
connection.mav.send(msg)

print(f"Đã gửi tín hiệu PWM tới động cơ: {actuator_controls}")

print(f"Đã gửi tín hiệu PWM tới động cơ: {actuator_controls}")

# Chờ một chút để kiểm tra kết quả
time.sleep(2)

# Đóng kết nối
connection.close()