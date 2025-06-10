from pymavlink import mavutil
import time
# 1. Kết nối tới PX4
master = mavutil.mavlink_connection('COM4', baud=57600)
master.wait_heartbeat()
print("✅ Đã kết nối PX4")

# 2. Thiết lập chu kỳ gửi: 10Hz = 100000 µs
interval_us = 100000

# # 3. Yêu cầu PX4 gửi gói SERVO_OUTPUT_RAW ở 10Hz
# master.mav.command_long_send(
#     master.target_system,
#     master.target_component,
#     mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,
#     0,
#     mavutil.mavlink.MAVLINK_MSG_ID_SERVO_OUTPUT_RAW,
#     interval_us,
#     0, 0, 0, 0, 0
# )
# print("📤 Đã yêu cầu SERVO_OUTPUT_RAW @ 10Hz")

# # 4. Yêu cầu PX4 gửi gói ATTITUDE ở 10Hz
# master.mav.command_long_send(
#     master.target_system,
#     master.target_component,
#     mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,
#     0,
#     mavutil.mavlink.MAVLINK_MSG_ID_ATTITUDE,
#     interval_us,
#     0, 0, 0, 0, 0
# )
# print("📤 Đã yêu cầu ATTITUDE @ 10Hz")

# 2. Danh sách lưu timestamp từng loại
last_time = {'ATTITUDE': None, 'SERVO_OUTPUT_RAW': None}
intervals = {'ATTITUDE': [], 'SERVO_OUTPUT_RAW': []}
count_target = 20  # Số mẫu để tính trung bình tần số

print("⏳ Đang thu thập dữ liệu...")

while True:
    msg = master.recv_match(type=['ATTITUDE', 'SERVO_OUTPUT_RAW'], blocking=True, timeout=3)
    if not msg:
        print("❌ Không nhận được dữ liệu")
        continue

    msg_type = msg.get_type()
    now = time.time()

    if last_time[msg_type]:
        delta = now - last_time[msg_type]
        intervals[msg_type].append(delta)
        print(f"[{msg_type}] {1/delta:.2f} Hz")

    last_time[msg_type] = now

    # Khi đủ mẫu, tính tần số trung bình
    if all(len(lst) >= count_target for lst in intervals.values()):
        print("\n📊 Kết quả tần số trung bình:")
        for t in intervals:
            avg_interval = sum(intervals[t]) / len(intervals[t])
            print(f"⏺ {t}: {1/avg_interval:.2f} Hz (trung bình từ {len(intervals[t])} mẫu)")
        break