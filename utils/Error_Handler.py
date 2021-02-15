from sys import exit
from colorama import Fore
import exit_codes

class Error_Handler:
    def __init__(self,debug):
        self.__modbus_error = exit_codes.EXIT_SUCCESS
        self.__logging = debug

    def __input_error(self):
        if (self.__logging):  
            print(Fore.RED + "Error: " + Fore.RESET + "invalid input.")

    def pwm_number_error(self,pwm_number,FIRST,SECOND):
        self.__input_error()
        if (self.__logging):
            print(Fore.YELLOW + "Possible reason: " + Fore.RESET + str(pwm_number) + ": incorrect PWM identificator.\nAllowed PWM identificator are: " + FIRST + ", " + SECOND + ".")
        return exit_codes.EXIT_INVALID_PWM_NUMBER

    def pressure_number_error(self,pressure_number,FIRST,SECOND):
        self.__input_error()
        if (self.__logging):
            print(Fore.YELLOW + "Possible reason: " + Fore.RESET + str(pressure_number) + ": incorrect Pressure identificator.\nAllowed Pressure identificator are: " + FIRST + ", " + SECOND + ".")
        return exit_codes.EXIT_INVALID_PRESSURE_NUMBER

    def __critical_error(self,error):
        if (self.__logging):
            print(Fore.RED + "Critical error." + Fore.RESET + " Program will be terminated.")
        exit(error)

    def period_error(self,period_ms):
        self.__input_error()
        if (self.__logging):
            print(Fore.YELLOW + "Possible reason: " + Fore.RESET + str(period_ms) + " is not positive integers.")
        return exit_codes.EXIT_INVALID_INPUT

    def polarity_error(self,polarity):
        self.__input_error()
        if (self.__logging):
            print(Fore.YELLOW + "Possible reason: " + Fore.RESET + str(polarity) + " is invalid value for polarity.\nAllowed values are:\n\tNormal: " + str(True) + "\n\tReversed: " + str(False))
        return exit_codes.EXIT_INVALID_INPUT

    def duty_cycle_error(self,duty_cycle):
        self.__input_error()
        if (self.__logging):
            print(Fore.YELLOW + "Possible reason: " + Fore.RESET + str(duty_cycle) + " is invalid value for duty cycle.\nAllowed value must be from interval <0;1>.")
        return exit_codes.EXIT_INVALID_INPUT

    def power_enable_error(sefl,enable):
        self.__input_error()
        if (self.__logging):
            print(Fore.YELLOW + "Possible reason: " + Fore.RESET + str(enable) + " is invalid value for power regulation.\nAllowed value must be false(disable) or true(enable).")
        return exit_codes.EXIT_INVALID_INPUT

    def compressor_enable_error(self,enable):
        self.__input_error()
        if (self.__logging):
            print(Fore.YELLOW + "Possible reason: " + Fore.RESET + str(enable) + " is invalid value for compressor regulation.\nAllowed value must be false(disable) or true(enable).")
        return exit_codes.EXIT_INVALID_INPUT

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
