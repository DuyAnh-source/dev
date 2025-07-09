from pymavlink import mavutil
import time
# Kết nối MAVLink (qua serial hoặc UDP)
master = mavutil.mavlink_connection('COM3', baud=2000000)
master.wait_heartbeat()
print("Kết nối thành công!")
# master.mav.command_long_send(
#         master.target_system,
#         master.target_component,
#         310,      # MAV_CMD_ACTUATOR_TEST
#         0,
#         0.1,      # Param 1: Output value (40%)
#         0.4,        # Param 2: Timeout 2s
#         0, 0,     # Param 3–4: unused
#         1,      # Param 5: Output Function = Motor1
#         0, 0      # Param 6–7: unused
#     )

for i in range(40):  # gửi lệnh 10 lần
   master.mav.command_long_send(
        master.target_system,
        master.target_component,
        310,      # MAV_CMD_ACTUATOR_TEST
        0,
        0.01*i,      # Param 1: Output value (40%)
        0.1,        # Param 2: Timeout 2s
        0, 0,     # Param 3–4: unused
        1,      # Param 5: Output Function = Motor1
        0, 0      # Param 6–7: unused
    )
   master.mav.command_long_send(
        master.target_system,
        master.target_component,
        310,      # MAV_CMD_ACTUATOR_TEST
        0,
        0.01*i,      # Param 1: Output value (40%)
        0.1,        # Param 2: Timeout 2s
        0, 0,     # Param 3–4: unused
        2,      # Param 5: Output Function = Motor1
        0, 0      # Param 6–7: unused
    )
   master.mav.command_long_send(
        master.target_system,
        master.target_component,
        310,      # MAV_CMD_ACTUATOR_TEST
        0,
        0.01*i,      # Param 1: Output value (40%)
        0.1,        # Param 2: Timeout 2s
        0, 0,     # Param 3–4: unused
        3,      # Param 5: Output Function = Motor1
        0, 0      # Param 6–7: unused
    )
   master.mav.command_long_send(
        master.target_system,
        master.target_component,
        310,      # MAV_CMD_ACTUATOR_TEST
        0,
        0.01*i,      # Param 1: Output value (40%)
        0.1,        # Param 2: Timeout 2s
        0, 0,     # Param 3–4: unused
        4,      # Param 5: Output Function = Motor1
        0, 0      # Param 6–7: unused
    )
   time.sleep(0.1)  # Chờ 100ms giữa các lệnh

