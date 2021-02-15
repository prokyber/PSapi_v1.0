import exit_codes
import macros
from modbus_registers import find_register_type


    
class Digital_Output:
    def __init__(self,reg_number,slave_ID):
        self.__coil = find_register_type('Coil','None')(reg_number,slave_ID)
        if (self.__coil==exit_codes.EXIT_INVALID_MODBUS_REGISTER_SPECIFICATION):
            exit(exit_codes.EXIT_INVALID_MODBUS_REGISTER_SPECIFICATION)
        
    def write(self,val):
        if (self.__coil.write(val)!=exit_codes.EXIT_MODBUS_REQUEST_FAILED):
            return exit_codes.EXIT_SUCCESS
        return exit_codes.EXIT_MODBUS_REQUEST_FAILED

    def read(self):
        return self.__coil.read()
        
    def reset(self):
        return self.__coil.reset()
    
class Digital_Input:
    def __init__(self,reg_number,slave_ID):
        self.__dicrete_input = find_register_type('DiscreteInput','None')(reg_number,slave_ID)
        if (self.__dicrete_input==exit_codes.EXIT_INVALID_MODBUS_REGISTER_SPECIFICATION):
            exit(exit_codes.EXIT_INVALID_MODBUS_REGISTER_SPECIFICATION)
        
    def read(self):
        return self.__dicrete_input.read()
        
    def reset(self):
        return self.__dicrete_input.reset()

class Analog_Input:
    def __init__(self,reg_number,slave_ID,voltage_multiplicator):
        self.__voltage_multiplicator = voltage_multiplicator
        self.__analog_input = find_register_type('Input','Input_Float')(reg_number,slave_ID)
        if (self.__analog_input==exit_codes.EXIT_INVALID_MODBUS_REGISTER_SPECIFICATION):
            exit(exit_codes.EXIT_INVALID_MODBUS_REGISTER_SPECIFICATION)
    
    def read(self):
        retval = self.__analog_input.read()
        if (retval!=exit_codes.EXIT_MODBUS_REQUEST_FAILED):
            return retval*self.__voltage_multiplicator
        return exit_codes.EXIT_MODBUS_REQUEST_FAILED

    def reset(self):
        return self.__analog_input.reset()

class Motor_Registers_Abstaction:
    def __init__(self,reg_number, slave_ID):
        self.__reg_number = reg_number
        self.__slave_ID = slave_ID
        self.__ppr = macros.motor.ppr.FULL
        self.__angle_quant = 0
        self.__enable = macros.motor.enable_values.DISABLE
        self.__speed = 0
        self.__angle = 0
        self.__angle_from_boot = 0
        self.__mode = macros.motor.modes.NONE
        self.__action = macros.motor.actions.STOP
        self.__init_registers()

    def __init_registers(self):
        self.__ppr_register = find_register_type('Holding','16BitUnsigned')(self.__reg_number+ macros.motor.offsets.PPR ,self.__slave_ID)
        self.__angle_quant_register = find_register_type('Holding','Float')(self.__reg_number+ macros.motor.offsets.ANGLE_QUANT,self.__slave_ID)
        self.__enable_register = find_register_type('Holding','16BitUnsigned')(self.__reg_number+ macros.motor.offsets.ENABLE,self.__slave_ID)
        self.__speed_register = find_register_type('Holding','16BitUnsigned')(self.__reg_number+ macros.motor.offsets.SPEED,self.__slave_ID)
        self.__angle_register = find_register_type('Holding','Float')(self.__reg_number+ macros.motor.offsets.ANGLE,self.__slave_ID)
        self.__mode_register = find_register_type('Holding','16BitUnsigned')(self.__reg_number+macros.motor.offsets.MODE,self.__slave_ID)
        self.__action_register = find_register_type('Holding','16BitUnsigned')(self.__reg_number+macros.motor.offsets.COMMAND,self.__slave_ID)
        self.__angle_from_boot_register = find_register_type('Holding','Float')(self.__reg_number+macros.motor.offsets.ANGLE_FROM_BOOT,self.__slave_ID)
        self.__reset_angle_from_boot_register = find_register_type('Holding','16BitUnsigned')(self.__reg_number+macros.motor.offsets.RESET_ANGLE_FROM_BOOT ,self.__slave_ID)

    def set_ppr(self,ppr):
        if (ppr in macros.motor.PPR_values.PPR_values_list):
            if(self.__ppr_register.write(ppr)!=exit_codes.EXIT_MODBUS_REQUEST_FAILED):
                self.__ppr = ppr
                self.__angle_quant = self.get_angle_quant()
                return exit_codes.EXIT_SUCCESS
            return exit_codes.EXIT_MODBUS_REQUEST_FAILED
        return exit_codes.EXIT_FAILURE

    def get_ppr(self):
        return self.__ppr

    def get_angle_quant(self):
        return self.__angle_quant

    def set_enable(self,enable):
        if (enable in macros.motor.enable_values.enable_values_list):
            if(self.__enable_register.write(enable)!=exit_codes.EXIT_MODBUS_REQUEST_FAILED):
                self.__enable = enable
                return exit_codes.EXIT_SUCCESS
            return exit_codes.EXIT_MODBUS_REQUEST_FAILED
        return exit_codes.EXIT_FAILURE

    def get_enable(self):
        return self.__enable

    def set_speed(self,speed):
        if (speed not in macros.motor.speed_values.speed_values_list):
            if (speed < macros.motor.speed_values.MIN):
                speed = macros.motor.speed_values.MIN
            else:
                speed = macros.motor.speed_values.MAX
        if(self.__speed_register.write(speed)!=exit_codes.EXIT_MODBUS_REQUEST_FAILED):
            self.__speed = speed
            return exit_codes.EXIT_SUCCESS
        return exit_codes.EXIT_MODBUS_REQUEST_FAILED

    def get_speed(self):
        return self.__speed

    def set_angle(self,angle):
        if(self.__angle_register.write(angle)!=exit_codes.EXIT_MODBUS_REQUEST_FAILED):
            self.__angle = angle
            updated_angle = self.__update_angle()
            if(self.__angle!=updated_angle):
                self.__angle = updated_angle
                return exit_codes.EXIT_ANGLE_WAS_UPDATED
            return exit_codes.EXIT_SUCCESS
        return exit_codes.EXIT_MODBUS_REQUEST_FAILED

    def __update_angle(self):
        return self.__angle_register.read()

    def get_angle(self):
        return self.__angle

    def get_angle_from_boot(self):
        self.__angle_from_boot = self.__angle_from_boot_register.read()
        return self.__angle_from_boot

    def reset_angle_from_boot(self):
        if(self.__angle_from_boot_register.write(1)!=exit_codes.EXIT_MODBUS_REQUEST_FAILED):
            self.__angle_from_boot = 0
            return exit_codes.EXIT_SUCCESS
        return exit_codes.EXIT_MODBUS_REQUEST_FAILED

    def set_mode(self,mode):
        if (mode in macros.motor.modes.motor_modes_list):
            if(self.__mode_register.write(mode)!=exit_codes.EXIT_MODBUS_REQUEST_FAILED):
                self.__mode = mode
                return exit_codes.EXIT_SUCCESS
            return exit_codes.EXIT_MODBUS_REQUEST_FAILED
        return exit_codes.EXIT_FAILURE

    def get_mode(self):
        return self.__mode

    def set_action(self,action):
        if (action in macros.motor.actions.actions_list):
            if(self.__action_register.write(action)!=exit_codes.EXIT_MODBUS_REQUEST_FAILED):
                self.__action = action
                return exit_codes.EXIT_SUCCESS
            return exit_codes.EXIT_MODBUS_REQUEST_FAILED
        return exit_codes.EXIT_FAILURE

    def get_action(self):
        return self.__action
