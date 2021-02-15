import sys
sys.path.insert(1,"./modbus_api")
sys.path.insert(1,"./macros")
sys.path.insert(1,"./configurations")
from Modbus_Connection_Handler import Modbus_Connection_Handler
from Devices import Switch
import device_configurations
import time

modbus = Modbus_Connection_Handler(True)
switch = Switch(device_configurations.POWER_CONTROL_REG,device_configurations.DEVICE_SLAVE_ID)
switch.enable()
time.sleep(1)
switch.disable()


# # import sys
# sys.path.insert(1,"./modbus_api")
# sys.path.insert(1,"./macros")
# sys.path.insert(1,"./configurations")
# from Modbus_Connection_Handler import Modbus_Connection_Handler
# from Devices import Pressure_Sencor
# import device_configurations
# import time
#
# modbus = Modbus_Connection_Handler(True)
# pressure_sencor = Pressure_Sencor(device_configurations.PRESSURE_SENCOR_REG,device_configurations.DEVICE_SLAVE_ID,device_configurations.PRESSURE_SENCOR_VOLTAGE_MULTIPLIER)
# print(pressure_sencor.read_pressure())
# time.sleep(2)
# print(pressure_sencor.read_pressure())
#
###########
# EXAMPLE_1
#
# import sys
# sys.path.insert(1,"./modbus_api")
# sys.path.insert(1,"./macros")
# sys.path.insert(1,"./configurations")
# from Modbus_Connection_Handler import Modbus_Connection_Handler
# from Devices import Step_Motor
# import device_configurations
#
# modbus = Modbus_Connection_Handler(True)
# motor = Step_Motor(device_configurations.MOTOR_REG,device_configurations.slave_ID,device_configurations.MOTOR_PPR_VALUE,device_configurations.MOTOR_DIRECTION_MULTIPLIER)
# motor.enable()
# motor.rotate_until_angle_reached(10,90)
# 
###########
# EXAMPLE_2
#
# import sys
# sys.path.insert(1,"./modbus_api")
# sys.path.insert(1,"./macros")
# sys.path.insert(1,"./configurations")
# from Modbus_Connection_Handler import Modbus_Connection_Handler
# from Devices import Step_Motor
# import device_configurations
# import time
# 
# modbus = Modbus_Connection_Handler(True)
# motor = Step_Motor(device_configurations.MOTOR_REG,device_configurations.slave_ID,device_configurations.MOTOR_PPR_VALUE,device_configurations.MOTOR_DIRECTION_MULTIPLIER)
# motor.enable()
# motor.rotate_clockwise(1)
# time.sleep(2)
# motor.emergency_stop()
