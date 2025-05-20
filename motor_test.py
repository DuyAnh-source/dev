# Chưa hoạt động

from pymavlink import mavutil

# 1. Kết nối tới UAV (có thể là udp hoặc serial)
master = mavutil.mavlink_connection('COM4', baud=57600)
master.wait_heartbeat()
print("✅ Đã kết nối tới UAV")

# 2. Gửi lệnh set PWM cho kênh SERVO9 (AUX1) = 1500us
channel = 9      # PWM output kênh 9 = AUX1
pwm_value = 1500 # Giá trị PWM từ 1000 đến 2000

print(f"📤 Gửi lệnh PWM kênh {channel} = {pwm_value}")
master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_DO_SET_SERVO,
    0,          # confirmation
    channel,    # param1: kênh PWM (1~16)
    pwm_value,  # param2: giá trị PWM microsecond (1000-2000)
    0, 0, 0, 0, 0  # param3-7: không dùng
)