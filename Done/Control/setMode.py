

# Chuyển mode OK
from pymavlink import mavutil


# Connect to the vehicle
master = mavutil.mavlink_connection('COM4', baud=57600)
master.wait_heartbeat()
print("✔ Heartbeat received")

master.mav.command_long_send(
    1, 1,
    mavutil.mavlink.MAV_CMD_DO_SET_MODE,
    0,
    1,  # base_mode: MAV_MODE_FLAG_CUSTOM_MODE_ENABLED
    1,  # custom_mode: 1 = Manual Control
    0, 0, 0, 0, 0
)
