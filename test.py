from Modbus_Connection_Handler import Modbus_Connection_Handler
from Devices import Switch
import device_configurations
import time

modbus = Modbus_Connection_Handler(True)
switch = Switch(device_configurations.POWER_CONTROL_REG,device_configurations.DEVICE_SLAVE_ID)
switch.enable()
time.sleep(1)
switch.disable()
