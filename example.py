from colorama import Fore
import exit_codes
import configurations
import Devices
from Modbus_Connection_Handler import Modbus_Connection_Handler

class example:
    def __init__(self, debug=True):
        self.__connection_handler = Modbus_Connection_Handler(True)
        self.__devices = {
            'Power' : Devices.Switch(device_configurations.POWER_CONTROL_REG,device_configurations.DEVICE_SLAVE_ID),
            'Pressure Sencor' : Devices.Pressure_Sencor(device_configurations.PRESSURE_SENCOR_REG,device_configurations.DEVICE_SLAVE_ID,device_configurations.PRESSURE_SENCOR_VOLTAGE_MULTIPLIER),
            'Valve' : Devices.Step_Motor(device_configurations.MOTOR_REG,device_configurations.slave_ID,device_configurations.MOTOR_PPR_VALUE,device_configurations.MOTOR_DIRECTION_MULTIPLIER)
        }
        self.__reset_devices()

    def power_enable(self, enable):
        if (enable):
            retval = self.__devices['Power'].enable()
        else:
            retval = self.__devices['Power'].disable()
        if (retval == exit_codes.EXIT_MODBUS_REQUEST_FAILED):
            self.__error_handler.modbus_request_error()
        return retval

    def get_power_state(self):
        retval = self.__devices['Power'].get_state()
        if (retval == exit_codes.EXIT_MODBUS_REQUEST_FAILED):
            self.__error_handler.modbus_request_error()
        return retval

    def read_pressure(self):
        retval = self.__devices['Pressure Sensor'].read_pressure()
        if (retval == exit_codes.EXIT_MODBUS_REQUEST_FAILED):
            self.__error_handler.modbus_request_error()
        return retval

    def valve_control_enable(self,enable):
        if (enable):
            return self.__devices['Valve'].enable()
        return self.__devices['Valve'].disable()

    def valve_rotate(self,speed,position):
        return self.__devices['Valve'].rotate_until_angle_reached(speed,position)

    def valve_opening_rotation(self,speed):
        return self.__devices['Valve'].rotate_clockwise(speed)

    def valve_closing_rotation(self,speed):
        return self.__devices['Valve'].rotate_counterclockwise(speed)

    def vavle_stop(self):
        return self.__devices['Valve'].emergency_stop()

    def __reset_devices(self):
        for key in self.__devices.keys():
            self.__devices.get(key).reset()
