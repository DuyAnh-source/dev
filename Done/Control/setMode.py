

# Chuyển mode OK
from pymavlink import mavutil


# Connect to the vehicle
master = mavutil.mavlink_connection('COM4', baud=57600)
master.wait_heartbeat()
print("✔ Heartbeat received")
# Mapping mode
print(master.mode_mapping())

base_mode = 29
custom_mode = 6
custom_sub_mode = 0

master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_DO_SET_MODE,
    0,  # confirmation
    base_mode,        # param1
    custom_mode,      # param2
    custom_sub_mode,  # param3
    0, 0, 0, 0        # param4-7 unused
)
