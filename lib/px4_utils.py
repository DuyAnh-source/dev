import time
import math
from pynput import keyboard

# Biến global
master = None
t0_fc = 0
t0_pc = 0
thrust = 0.4
stop_event = None
servo_output_raw = None
attitude = None

def init_globals(m):
    global master
    master = m

def get_time_px4():
    global master
    global t0_fc, t0_pc

    print("🔄 Đang chờ nhận LOCAL_POSITION_NED từ PX4...")

    msg = master.recv_match(type='LOCAL_POSITION_NED', blocking=True, timeout=5)

    if msg is None or not hasattr(msg, 'time_boot_ms'):
        print("❌ Không nhận được time_boot_ms từ FC. Thoát.")
        exit(1)

    t0_fc = msg.time_boot_ms              # Thời điểm PX4 gửi
    t0_pc = time.time()                   # Thời điểm PC nhận

    print(f"✅ time_boot_ms từ FC: {t0_fc} ms — Thời gian PC: {t0_pc:.3f} s")

    return t0_fc

def get_synced_time_boot_ms():
    global t0_fc, t0_pc
    elapsed_pc_ms = int((time.time() - t0_pc) * 1000)
    return (t0_fc + elapsed_pc_ms) % 4294967295

def euler_to_quaternion(roll, pitch, yaw):
    cy = math.cos(yaw * 0.5)
    sy = math.sin(yaw * 0.5)
    cp = math.cos(pitch * 0.5)
    sp = math.sin(pitch * 0.5)
    cr = math.cos(roll * 0.5)
    sr = math.sin(roll * 0.5)

    w = cr * cp * cy + sr * sp * sy
    x = sr * cp * cy - cr * sp * sy
    y = cr * sp * cy + sr * cp * sy
    z = cr * cp * sy - sr * sp * cy

    return [w, x, y, z]

def send_attitude_setpoint(thrust=0.1, roll_deg=0.0, pitch_deg=0.0, yaw_deg=0.0):
    # Đổi độ → rad
    global master
    roll = math.radians(roll_deg)
    pitch = math.radians(pitch_deg)
    yaw = math.radians(yaw_deg)

    # Tạo quaternion từ góc Euler
    q = euler_to_quaternion(roll, pitch, yaw)

    # Gửi attitude setpoint với quaternion
    master.mav.set_attitude_target_send(
        get_synced_time_boot_ms(),
        master.target_system,
        master.target_component,
        0b00000111,  # bỏ qua body rates & yaw
        q,
        0, 0, 0,
        thrust
    )

def init_setpoint():
    for _ in range(20):
        send_attitude_setpoint(0.5)  
        time.sleep(0.05)             # ~20Hz

def offboard_mode():
    global master
    print("🛫 Chuyển sang OFFBOARD mode...")
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        300,  # MAV_CMD_DO_SET_MODE
        0,
        1,  # MAV_MODE_FLAG_CUSTOM_MODE_ENABLED
        6,  # OFFBOARD
        0, 0, 0, 0, 0
    )
    time.sleep(0.2)  # Đợi một chút để PX4 chuyển sang OFFBOARD

def arm():
    global master
    print("🟢 Gửi lệnh ARM")
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        400,  # MAV_CMD_COMPONENT_ARM_DISARM
        0,  # confirmation
        1,  # param1 = 1 để ARM
        0, 0, 0, 0, 0, 0
    )

def disArm():
    global master
    print("🔴 Gửi lệnh DISARM")
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        400, 0,      # command = MAV_CMD_COMPONENT_ARM_DISARM
        0,           # param1 = 0 → Disarm
        0, 0, 0,     # param2-4
        0, 0, 0      # param5-7 (đã đủ)
    )


def get_servo_output_raw():
    global master
    global servo_output_raw
    msg = master.recv_match(type='SERVO_OUTPUT_RAW', blocking=False, timeout=5)
    if msg is not None:
        servo_output_raw = msg
        return msg
    if servo_output_raw is not None:
        return servo_output_raw
    return None


def get_attitude():
    global master
    global attitude
    msg = master.recv_match(type='ATTITUDE', blocking=False, timeout=5)
    if msg is not None:
        attitude = msg
        return msg
    return attitude
    
def position_mode():
    global master
    print("🛫 Chuyển sang position mode...")
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        176,
        0,
        1,  # base mode
        3,  # custom mode
        0, 0, 0, 0, 0
    )
    time.sleep(0.2)  # Đợi một chút để PX4 chuyển sang OFFBOARD

