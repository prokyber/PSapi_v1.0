import modbus_api
import time
import exit_codes

REQUEST_DELAY = 0.006
COIL_OFFSET = 0
DISCRETE_INPUT_OFFSET = 10000
INPUT_OFFSET = 30000
HOLDING_OFFSET = 40000

def modbus_delay():
    time.sleep(REQUEST_DELAY)

class Coil:
    def __init__(self,reg_number,slave_ID):
        self.__offset = COIL_OFFSET
        self.__reg_number = reg_number + self.__offset
        self.__slave_ID = slave_ID

    def write_fcn(self,reg_number,val,slave_ID):
        modbus_api.writeCoils(reg_number,[val],slave_ID)

    def write(self,val):
        modbus_delay()
        try:
            self.write_fcn(self.__reg_number,val,self.__slave_ID)
        except:
            return exit_codes.EXIT_MODBUS_REQUEST_FAILED
        return exit_codes.EXIT_SUCCESS

    def read_fcn(self,reg_number,slave_id):
        return modbus_api.readCoils(reg_number,1,slave_id)[0]

    def read(self):
        modbus_delay()
        try:
            retval = self.read_fcn(self.__reg_number,self.__slave_ID)
        except:
            return exit_codes.EXIT_MODBUS_REQUEST_FAILED
        return retval

    def reset(self):
        self.disable()


class Discrete_Input:
    def __init__(self,reg_number,slave_ID):
        self.__offset = DISCRETE_INPUT_OFFSET
        self.__reg_number = reg_number + self.__offset
        self.__slave_ID = slave_ID        

    def write(self,val):
        return exit_codes.EXIT_WRITE_OPERATION_NOT_PERMITTED

    def read_fcn(self,reg_number,slave_id):
        return modbus_api.readDiscreteInputs(reg_number,1,slave_id)[0]

    def read(self):
        modbus_delay()
        try:
            retval = self.read_fcn(self.__reg_number,self.__slave_ID)[0]    
        except:
            return exit_codes.EXIT_MODBUS_REQUEST_FAILED
        return retval

    def reset(self):
        return exit_codes.EXIT_SUCCESS


class Input:
    __offset = INPUT_OFFSET
    def __init__(self,slave_ID):
        self.slave_ID = slave_ID

    def write(self,val):
        return exit_codes.EXIT_WRITE_OPERATION_NOT_PERMITTED
        
    def read_fcn(self):
        pass

    def read(self):
        modbus_delay()
        try:
            retval = self.read_fcn()
        except:
            return exit_codes.EXIT_MODBUS_REQUEST_FAILED
        return retval

    def reset(self):
        return exit_codes.EXIT_SUCCESS

class Input_16Bit_Unsigned(Input):
    def __init__(self,reg_number,slave_ID):
        Input.__init__(Input,slave_ID)
        self.__reg_number = reg_number + self._Input__offset

    def read_fcn(self):
        return modbus_api.read16BitUnsignedInputs(self.reg_number,1,self.slave_ID)[0]

class Input_16Bit_Signed(Input):
    def __init__(self,reg_number,slave_ID):
        Input.__init__(Input,slave_ID)
        self.reg_number = reg_number + self._Input__offset

    def read_fcn(self):
        return modbus_api.read16BitSignedInputs(self.reg_number,1,self.slave_ID)[0]

class Input_32Bit_Unsigned(Input):
    def __init__(self,reg_number,slave_ID):
        Input.__init__(Input,slave_ID)
        self.reg_number = reg_number + self._Input__offset

    def read_fcn(self):
        return modbus_api.read32BitUnsignedInputs(self.reg_number,1,self.slave_ID)[0]

class Input_32Bit_Signed(Input):
    def __init__(self,reg_number,slave_ID):
        Input.__init__(Input,slave_ID)
        self.reg_number = reg_number + self._Input__offset

    def read_fcn(self):
        return modbus_api.read32BitSignedInputs(self.reg_number,1,self.slave_ID)[0]

class Input_Float(Input):
    def __init__(self,reg_number,slave_ID):
        Input.__init__(Input,slave_ID)
        self.reg_number = reg_number + self._Input__offset

    def read_fcn(self):
        return modbus_api.readFloatInputs(self.reg_number,1,self.slave_ID)[0]


class Holding:
    
    __offset = HOLDING_OFFSET
    
    def __init__(self,slave_ID):
        self.slave_ID = slave_ID
        
    def write_fcn(self,val):
        pass

    def write(self,val):
        modbus_delay()
        try:
            self.write_fcn(val)    
        except:
            return exit_codes.EXIT_MODBUS_REQUEST_FAILED
        return exit_codes.EXIT_SUCCESS

    def read_fcn(self):
        pass

    def read(self):
        modbus_delay()
        try:
            retval = self.read_fcn()
        except:
            return exit_codes.EXIT_MODBUS_REQUEST_FAILED
        return retval

    def reset(self):
        self.write(0)

class Holding_16Bit_Unsigned(Holding):
    def __init__(self,reg_number,slave_ID):
        Holding.__init__(Holding,slave_ID)
        self.reg_number = reg_number + self._Holding__offset

    def write_fcn(self,val):
        modbus_api.write16BitUnsignedHoldings(self.reg_number,[val],self.slave_ID)

    def read_fcn(self):
        return modbus_api.read16BitUnsignedHoldings(self.reg_number,1,self.slave_ID)[0]

class Holding_16Bit_Signed(Holding):
    def __init__(self,reg_number,slave_ID):
        Holding.__init__(Holding,slave_ID)
        self.reg_number = reg_number + self._Holding__offset

    def write_fcn(self,val):
        modbus_api.write16BitSignedHoldings(self.reg_number,[val],self.slave_ID)

    def read_fcn(self):
        return modbus_api.read16BitSignedHoldings(self.reg_number,1,self.slave_ID)[0]

class Holding_32Bit_Unsigned(Holding):
    def __init__(self,reg_number,slave_ID):
        Holding.__init__(Holding,slave_ID)
        self.reg_number = reg_number + self._Holding__offset

    def write_fcn(self,val):
        modbus_api.write32BitUnsignedHoldings(self.reg_number,[val],self.slave_ID)

    def read_fcn(self):
        return modbus_api.read32BitUnsignedHoldings(self.reg_number,1,self.slave_ID)[0]

class Holding_32Bit_Signed(Holding):
    def __init__(self,reg_number,slave_ID):
        Holding.__init__(Holding,slave_ID)
        self.reg_number = reg_number + self._Holding__offset

    def write_fcn(self,val):
        modbus_api.write32BitSignedHoldings(self.reg_number,[val],self.slave_ID)

    def read_fcn(self):
        return modbus_api.read32BitSignedHoldings(self.reg_number,1,self.slave_ID)[0]

class Holding_Float(Holding):
    def __init__(self,reg_number,slave_ID):
        Holding.__init__(Holding,slave_ID)
        self.reg_number = reg_number + self._Holding__offset
        
    def write_fcn(self,val):
        modbus_api.writeFloatHoldings(self.reg_number,[val],self.slave_ID)

    def read_fcn(self):
        return modbus_api.readFloatHoldings(self.reg_number,1,self.slave_ID)[0]


registers_dictionary = {
    'Coil' : {
        'None' : Coil
    },'DiscreteInput' : {
        'None' : Discrete_Input
    },
    'Input' : {
        '16BitUnsigned' : Input_16Bit_Unsigned,
        '16BitSigned' : Input_16Bit_Signed,
        '32BitUnsigned' : Input_32Bit_Unsigned,
        '32BitSigned' : Input_32Bit_Signed,
        'Float' : Input_Float
    },
    'Holding' : {
        '16BitUnsigned' : Holding_16Bit_Unsigned,
        '16BitSigned' : Holding_16Bit_Signed,
        '32BitUnsigned' : Holding_32Bit_Unsigned,
        '32BitSigned' : Holding_32Bit_Signed,
        'Float' : Holding_Float
    }
}

def find_register_type(group,subgroup):
    retval = exit_codes.EXIT_INVALID_MODBUS_REGISTER_SPECIFICATION
    if (registers_dictionary.get(group)!=None):
        if (registers_dictionary.get(group).get(subgroup)!=None):
            return registers_dictionary.get(group).get(subgroup)
    return retval
