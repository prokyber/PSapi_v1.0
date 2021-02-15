import Periferials
import exit_codes
import macros

# EXAMPLE
#
# from Modbus_Connection_Handler import Modbus_Connection_Handler
# from Devices import Switch
# import device_configurations
# import time
# 
# modbus = Modbus_Connection_Handler(True)
# switch = Switch(device_configurations.POWER_CONTROL_REG,device_configurations.DEVICE_SLAVE_ID)
# switch.enable()
# time.sleep(1)
# switch.disable()
#
class Switch:
    def __init__(self,reg_number,slave_ID):
        self.__DI = Periferials.Digital_Output(reg_number,slave_ID)
        self.__val = False

    def enable(self):
        if (self.__DI.write(True)!=exit_codes.EXIT_MODBUS_REQUEST_FAILED):
            self.__val = True
            return exit_codes.EXIT_SUCCESS
        return exit_codes.EXIT_MODBUS_REQUEST_FAILED

    def disable(self):
        if (self.__DI.write(False)!=exit_codes.EXIT_MODBUS_REQUEST_FAILED):
            self.__val = False
            return exit_codes.EXIT_SUCCESS
        return exit_codes.EXIT_MODBUS_REQUEST_FAILED

    def get_state(self):
        old_val = self.__val 
        self.__val = self.__DI.read()
        if (self.__val!=exit_codes.EXIT_MODBUS_REQUEST_FAILED):
            return self.__val
        self.__val = old_val
        return exit_codes.EXIT_MODBUS_REQUEST_FAILED

    def reset(self):
        self.disable()

# EXAMPLE_1
# 
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
class Pressure_Sencor:
    def __init__(self,reg_number,slave_ID,voltage_multiplicator):
        self.__AI = Periferials.Analog_Input(reg_number,slave_ID,voltage_multiplicator)
        self.__reset_buffer()

    def __reset_buffer(self):
        self.__buffer = []
        self.__buffer_size = 100
        self.__buffer_cnt = 0

    def read_pressure(self):
        self.__reset_buffer()
        while(self.__buffer_cnt!=self.__buffer_size):
            tmp = self.__AI.read()
            if (tmp==exit_codes.EXIT_MODBUS_REQUEST_FAILED):
                self.__reset_buffer()
                return self.__buffer
            self.__buffer.append(tmp)
        return sum(self.__buffer)/(self.__buffer_size)

    def reset(self):
        self.__reset_buffer()

###########
# EXAMPLE_1
#
# from Modbus_Connection_Handler import Modbus_Connection_Handler
# from Devices import Step_Motor
# import device_configurations
#
# modbus = Modbus_Connection_Handler(True)
# motor = Step_Motor(device_configurations.MOTOR_REG,device_configurations.slave_ID,device_configurations.MOTOR_PPR_VALUE,device_configurations.MOTOR_DIRECTION_MULTIPLIER)
# motor.enable()
# motor.rotate_until_angle_reached(10,180)
# 
###########
# EXAMPLE_2
#
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
class Step_Motor:
    def __init__(self,reg_number,slave_ID,ppr,direction_multiplier):
        self.__motor = Periferials.Motor_Registers_Abstaction(reg_number,slave_ID)
        self.__direction_multiplier = direction_multiplier
        self.__preset(ppr)

    def __preset(self,ppr):
        self.__motor.set_ppr

    def enable(self):
        return self.__motor.set_enable(True)

    def disable(self):
        return self.__motor.set_enable(False)
    
    def rotate_clockwise(self,speed):
        retval = exit_codes.EXIT_SUCCESS
        retval = retval + self.__motor.set_mode(macros.motor.modes.CONTINIOUS)
        retval = retval + self.__motor.set_speed(speed)
        retval = retval + self.__motor.set_angle(10*self.__direction_multiplier)
        retval = retval + self.__motor.set_action(True)
        return retval

    def rotate_counter_clock_wise(self,speed):
        retval = exit_codes.EXIT_SUCCESS
        retval = retval + self.__motor.set_mode(macros.motor.modes.CONTINIOUS)
        retval = retval + self.__motor.set_speed(speed)
        retval = retval + self.__motor.set_angle(-10*self.__direction_multiplier)
        retval = retval + self.__motor.set_action(True)
        return retval

    def rotate_until_angle_reached(self,speed,angle):
        retval = exit_codes.EXIT_SUCCESS
        retval = retval + self.__motor.set_mode(macros.motor.modes.ANGULAR)
        retval = retval + self.__motor.set_speed(speed)
        retval = retval + self.__motor.set_angle(angle*self.__direction_multiplier)
        retval = retval + self.__motor.set_action(True)
        return retval

    def emergency_stop(self):
        return self.__motor.set_action(False)

    def reset(self):
        retval = exit_codes.EXIT_SUCCESS
        retval = retval + self.__motor.set_enable(False)
        retval = retval + self.__motor.set_mode(macros.motor.modes.NONE)
        retval = retval + self.__motor.set_speed(0)
        retval = retval + self.__motor.set_angle(0)
        retval = retval + self.__motor.set_action(False)
        return retval
