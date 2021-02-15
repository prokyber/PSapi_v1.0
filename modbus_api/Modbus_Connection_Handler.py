from colorama import Fore
import modbus_api
import exit_codes
import modbus_configs

class Modbus_Connection_Error_Handler:
    def __init__(self,debug):
        self.__modbus_error = exit_codes.EXIT_SUCCESS
        self.__logging = debug

    def ports_searching(self):
        if (self.__logging):
            print(Fore.BLUE + "Debug information: " + Fore.RESET + "Searching for active ports...")

    def modbus_init_no_error(self):
        if (self.__logging):
            print(Fore.BLUE + "Debug information: " + Fore.RESET + "Nodbus server: "+ Fore.GREEN + "Connection was successfully established." + Fore.RESET)

    def modbus_init_error(self):
        error_type = ""
        if (self.__modbus_error == exit_codes.EXIT_NO_ACTIVE_PORTS):
            error_type = "There is no active ports."
        elif (self.__modbus_error == exit_codes.EXIT_NO_ACTIVE_DEVICES):
            error_type = "There is no active devices."
        else:
            error_type = "Unknown reason."
        if (self.__logging):
            print(Fore.RED + "Error: " + Fore.RESET + "Modbus server: Connection can not be established.")
            print(Fore.YELLOW + "Possible reason: " + Fore.RESET + "Modbus server: " + error_type)
        self.__critical_error(self.__modbus_error)

    def modbus_no_ports_error(self):
        self.__modbus_error = exit_codes.EXIT_NO_ACTIVE_PORTS

    def modbus_no_devices_error(self):
        self.__modbus_error = exit_codes.EXIT_NO_ACTIVE_DEVICES

    def modbus_request_error(self):
        if (self.__logging):
            print(Fore.RED + "Error: " + Fore.RESET + "Modbus server: request failed.")

    def __critical_error(self,error):
        if (self.__logging):
            print(Fore.RED + "Critical error." + Fore.RESET + " Program will be terminated.")
        exit(error)
        
class Modbus_Connection_Handler:
    def __init__(self,debug):
        self.__stop_bits = modbus_configs.modbus_configs['stop_bits']
        self.__package_size = modbus_configs.modbus_configs['package_size']
        self.__parity = modbus_configs.modbus_configs['parity']
        self.__baud_rate = modbus_configs.modbus_configs['baud_rate']
        self.__slave_ID = modbus_configs.modbus_configs['slave_ID']
        self.__device_register = modbus_configs.modbus_configs['device_reg']
        self.__error_handler = Modbus_Connection_Error_Handler(debug)
        self.__init()
    
    def __init(self):
        if (self.__create_modbus()):
            self.__error_handler.modbus_init_no_error()
        else:
            self.__error_handler.modbus_init_error()

    def __create_modbus(self):
        is_connected = False
        self.__error_handler.ports_searching()
        ports = modbus_api.getPorts()
        if (len(ports) != 0):
            for port in ports:
                modbus_api.createModbusClient(port, self.__stop_bits, self.__package_size, self.__parity, self.__baud_rate)
                try:
                    modbus_api.write16BitUnsignedHoldings(
                        self.__device_register, [1], self.__slave_ID)
                    is_connected = True
                except:
                    is_connected = False
                if (is_connected):
                    break
            if (not is_connected):
                self.__error_handler.modbus_no_devices_error()
        else:
            self.__error_handler.modbus_no_ports_error()
        return (is_connected)