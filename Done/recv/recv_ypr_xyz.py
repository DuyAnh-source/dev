# Đọc OK

from pymavlink import mavutil

# Thay đổi cổng COM hoặc ttyACMx tùy hệ điều hành
# Windows: 'COM4' — Linux/Mac: '/dev/ttyACM0'
connection = mavutil.mavlink_connection('COM3', baud=2000000)

# Chờ tín hiệu heartbeat từ Pixhawk
connection.wait_heartbeat()
print("Đã kết nối với hệ thống MAVLink")

# Lặp để đọc dữ liệu cảm biến
while True:
    msg = connection.recv_match(blocking=True)
    msg_type = msg.get_type()

    if msg_type == 'ATTITUDE':
        print(f"[ATTITUDE] Time: {msg.time_boot_ms} ms, Roll: {msg.roll:.2f}, Pitch: {msg.pitch:.2f}, Yaw: {msg.yaw:.2f}")
    elif msg_type == 'LOCAL_POSITION_NED':
        print(f"[LOCAL_POSITION_NED] Time: {msg.time_boot_ms} ms, x: {msg.x:.2f} m, y: {msg.y:.2f} m, z: {msg.z:.2f} m")
        print(f"[LOCAL_POSITION_NED] Time: {msg.time_boot_ms} ms, vx: {msg.vx:.2f} m/s, vy: {msg.vy:.2f} m/s, vz: {msg.vz:.2f} m/s")

    # Bạn có thể thêm các message khác tùy nhu cầu
