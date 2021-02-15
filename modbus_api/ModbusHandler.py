import pymodbus
import serial
from pymodbus.pdu import ModbusRequest,ModbusResponse,ModbusExceptions
from pymodbus.file_message import ReadFifoQueueRequest
from pymodbus.client.sync import ModbusSerialClient as ModbusClient #initialize a serial RTU client instance
from pymodbus.client.sync import ModbusTcpClient  
from pymodbus.transaction import ModbusRtuFramer
from pymodbus.exceptions import ModbusIOException
from ModbusHandlerExceptions import ModbusHandlerExceptions
from ModValConverter import ModValConverter
import struct
# import logging
# FORMAT = ('%(asctime)-15s %(threadName)-15s'
#           ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
# logging.basicConfig(format=FORMAT)
# log = logging.getLogger()
# log.setLevel(logging.DEBUG)
# import time
#4 43 75 46 0 2 3e 48
class modbusHandler:

    def __init__(self,type, tcpIp, tcpPort, Method, Port, Stopbits , Bytesize, Parity, Baudrate):
        self.modValConverter = ModValConverter()
        self.exceptionHandler = ModbusHandlerExceptions()
        self.tcpNumberOfRetries = 20

        if(type == "TCP"):
            self.ModbusClient = ModbusTcpClient(tcpIp,tcpPort,timeout = 0.5)
        else: 
            if(type == "RTU"):
                if(len(Port)==0):
                    self.exceptionHandler.generateException("NoPortSpecifiedError")
                self.ModbusClient = ModbusClient(method = Method, port = Port, stopbits = Stopbits , bytesize = Bytesize, parity = Parity, baudrate = Baudrate, timeout = 1)
        self.ModbusClient.register(self.ReadFifoRequest.ReadFifoResponse)
        self.ModbusClient.register(self.Read2FifosRequest.Read2FifosResponse)
        self.ModbusClient.register(self.ReadFifoAndTimeRequest.ReadFifoAndTimeResponse)

    def setNumberOfRetriesTCP(self,number):
        self.tcpNumberOfRetries = number

    class DataOut:
        registers = []

    class DataOutTwoRegs:
        registers0 = []
        registers1 = []

    class Read2FifosRequest(ModbusRequest):
        function_code = 66
        _rtu_frame_size = 8

        class Read2FifosResponse(ModbusResponse):
            function_code = 65
            _rtu_byte_count_pos = 3
            def __init__(self, values=None, **kwargs):
                ModbusResponse.__init__(self, **kwargs)
                self.values = values or []
            def encode(self):
                result = bytes([len(self.values) * 2])
                for register in self.values:
                    result += struct.pack('>H', register)
                return result
            def decode(self, data):
                byte_count = int(data[1])
                self.values = []
                for i in range(2, byte_count + 1, 2):
                    self.values.append(struct.unpack('>H', data[i:i + 2])[0])

        def __init__(self, address=None, **kwargs):
            ModbusRequest.__init__(self, **kwargs)
            self.address = address
            self.count = 2

        def encode(self):
            return struct.pack('>HH', self.address, self.count)

        def decode(self, data):
            self.address, self.count = struct.unpack('>HH', data)

        def execute(self, context):
            if not (1 <= self.count <= 0x7d0):
                return self.doException(ModbusExceptions.IllegalValue)
            if not context.validate(self.function_code, self.address, self.count):
                return self.doException(ModbusExceptions.IllegalAddress)
            values = context.getValues(self.function_code, self.address,
                                       self.count)
            return self.Read2FifosResponse(values)
    
    class ReadFifoRequest(ModbusRequest):
    
        function_code = 66
        _rtu_frame_size = 8

        class ReadFifoResponse(ModbusResponse):
            function_code = 24
            _rtu_byte_count_pos = 3

            def __init__(self, values=None, **kwargs):
                ModbusResponse.__init__(self, **kwargs)
                self.values = values or []

            def encode(self):
                """ Encodes response pdu

                :returns: The encoded packet message
                """
                # print(len(self.values))
                result = bytes([len(self.values) * 2])
                for register in self.values:
                    result += struct.pack('>H', register)
                return result

            def decode(self, data):
                """ Decodes response pdu

                :param data: The packet data to decode
                """
                # print(data)
                byte_count = int(data[1])
                self.values = []
                for i in range(2, byte_count + 1, 2):
                    self.values.append(struct.unpack('>H', data[i:i + 2])[0])

    class ReadFifoAndTimeRequest(ModbusRequest):
    
        function_code = 67
        # _rtu_frame_size = 8
        # fifoFreq = 100
        class ReadFifoAndTimeResponse(ModbusResponse):
            function_code = 67
            _rtu_double_byte_count_pos = 10

            def __init__(self, values=None, **kwargs):
                ModbusResponse.__init__(self, **kwargs)
                self.values = values or []
                # print(kwargs)

            def encode(self):
                """ Encodes response pdu

                :returns: The encoded packet message
                """
                return self.values

            def decode(self, data):
                """ Decodes response pdu

                :param data: The packet data to decode
                """
                timeFromStart = struct.unpack('>Q', data[0:8])[0]
                byte_count = struct.unpack('>H',data[8:10])[0]
                # print(data.hex())
                # print(timeFromStart)

                # print(byte_count)
                byteCounter = 10
                fifoAllRegs = []
                sampleFreqs = []

                while(byteCounter-6 < byte_count):
                    sampleFreqs.append(struct.unpack('>H', data[byteCounter:byteCounter + 2])[0])
                    byteCounter = byteCounter + 2
                    nextRegCount = struct.unpack('>H', data[byteCounter:byteCounter + 2])[0]
                    byteCounter = byteCounter + 2
                    fifoRegs = []

                    for i in range(nextRegCount):
                        fifoRegs.append(struct.unpack('>H', data[byteCounter + i*2:byteCounter + i*2 + 2])[0])
                        # fifoTimes.append(timeFromStart - (1/self.fifoFreq)*1000000*i)
                    byteCounter = byteCounter + nextRegCount*2

                    fifoAllRegs.append(fifoRegs)
                # print(fifoAllRegs)

                self.values = [timeFromStart,fifoAllRegs,sampleFreqs]

        def __init__(self,address=None,count = 1, **kwargs):
            ModbusRequest.__init__(self, **kwargs)
            self.address = address
            self.count = count
            # print(kwargs)
    
        def encode(self):
            return struct.pack('>HH', self.address, self.count)
    
        def decode(self, data):
            self.address, self.count = struct.unpack('>HH', data)
    
        def execute(self, context):
            if not (1 <= self.count <= 0x7d0):
                return self.doException(ModbusExceptions.IllegalValue)
            if not context.validate(self.function_code, self.address, self.count):
                return self.doException(ModbusExceptions.IllegalAddress)
            values = context.getValues(self.function_code, self.address,
                                       self.count)
            return self.ReadFifoResponse(values)

    def connect(self):
        self.ModbusClient.connect()

    def isSlaveIsNotResponding(self, result):
        if(type(result)==pymodbus.exceptions.ModbusIOException):
            return True
        return False

    def writeCoils(self,addresS,valuE,uniT):
        addresS = addresS - 1 # when I ask 30001, python sends request for 30002, why??? Bug???
        for x in range(self.tcpNumberOfRetries):
            try:
                result = self.ModbusClient.write_coils(address = addresS,values = valuE,unit = uniT)
                if (not self.isSlaveIsNotResponding(result)):
                    break
            except pymodbus.exceptions.ConnectionException:
                pass
        if(type(result)==pymodbus.exceptions.ModbusIOException):
            self.exceptionHandler.generateException("ModbusIOError")
        return result
    
    def write16BitUnsignedRegister(self,addresS,valuE,uniT):
        addresS = addresS - 1 # when I ask 30001, python sends request for 30002, why??? Bug???
        for x in range(self.tcpNumberOfRetries):
            try:
                result = self.ModbusClient.write_register(address = addresS,value = valuE,unit = uniT)
                if (not self.isSlaveIsNotResponding(result)):
                    break
            except pymodbus.exceptions.ConnectionException:
                pass
        if(type(result)==pymodbus.exceptions.ModbusIOException):
            self.exceptionHandler.generateException("ModbusIOError")
        return result

    def write16BitUnsignedRegisters(self,addresS,valuE,uniT):
        addresS = addresS - 1 # when I ask 30001, python sends request for 30002, why??? Bug???
        for x in range(self.tcpNumberOfRetries):
            try:
                result = self.ModbusClient.write_registers(address = addresS,values = valuE,unit = uniT)
                if (not self.isSlaveIsNotResponding(result)):
                    break
            except pymodbus.exceptions.ConnectionException:
                pass
        if(type(result)==pymodbus.exceptions.ModbusIOException):
            self.exceptionHandler.generateException("ModbusIOError")
        return result
    
    def readCoils(self,addresS,counT,uniT):
        addresS = addresS - 1 # when I ask 30001, python sends request for 30002, why??? Bug???
        for x in range(self.tcpNumberOfRetries):
            try:
                result = self.ModbusClient.read_coils(address = addresS,count = counT,unit = uniT)
                if (not self.isSlaveIsNotResponding(result)):
                    break
            except pymodbus.exceptions.ConnectionException:
                pass
        if(type(result)==pymodbus.exceptions.ModbusIOException):
            self.exceptionHandler.generateException("ModbusIOError")
        return result

    def readDiscreteInputs(self,addresS, counT, uniT):
        addresS = addresS - 1 # when I ask 30001, python sends request for 30002, why??? Bug???
        for x in range(self.tcpNumberOfRetries):
            try:
                result = self.ModbusClient.read_discrete_inputs(address = addresS,count = counT,unit = uniT)
                if (not self.isSlaveIsNotResponding(result)):
                    break
            except pymodbus.exceptions.ConnectionException:
                pass
        if(type(result)==pymodbus.exceptions.ModbusIOException):
            self.exceptionHandler.generateException("ModbusIOError")
        return result

    def readInputRegisters(self,addresS,counT,uniT):
        addresS = addresS - 1 # when I ask 30001, python sends request for 30002, why??? Bug???
        for x in range(self.tcpNumberOfRetries):
            try:
                result = self.ModbusClient.read_input_registers(address = addresS,count = counT,unit = uniT)
                if (not self.isSlaveIsNotResponding(result)):
                    break
            except pymodbus.exceptions.ConnectionException:
                pass
        if(type(result)==pymodbus.exceptions.ModbusIOException):
            self.exceptionHandler.generateException("ModbusIOError")
        return result
       
    def readHoldingRegisters(self,addresS,counT,uniT):
        addresS = addresS - 1 # when I ask 30001, python sends request for 30002, why??? Bug???
        for x in range(self.tcpNumberOfRetries):
            try:
                result = self.ModbusClient.read_holding_registers(address = addresS,count = counT,unit = uniT)
                if (not self.isSlaveIsNotResponding(result)):
                    break
            except pymodbus.exceptions.ConnectionException:
                pass
        if(type(result)==pymodbus.exceptions.ModbusIOException):
            self.exceptionHandler.generateException("ModbusIOError")
        return result

    def getFifoAndTime(self,addresS,number,uniT):
        addresS = addresS - 1 # when I ask 30001, python sends request for 30002, why??? Bug???

        for x in range(self.tcpNumberOfRetries):
            # print(x)
            try:
                request = self.ReadFifoAndTimeRequest(address=addresS,count = number, unit = uniT)
                result = self.ModbusClient.execute(request)
                if (not self.isSlaveIsNotResponding(result)):
                    break
            except pymodbus.exceptions.ConnectionException:
                pass
            
        if(type(result)==pymodbus.exceptions.ModbusIOException):
            self.exceptionHandler.generateException("ModbusIOError")

        try:
            encoded = result.encode()
        except AttributeError:
            self.exceptionHandler.generateException("EncodeError")
            return result

        if type(encoded) is not list:
            if(type(result)==pymodbus.pdu.ExceptionResponse):
                self.exceptionHandler.generateException(encoded)
            else:
                self.exceptionHandler.generateException("NotAListReturned")
        dataOut = []
        # encoded[0] = encoded[0]
        # print(encoded)
        for i in range(number):
            fifoLocal = []
            timeLineLocal = []
            rang = len(encoded[1][i])
            timeStep = (1/encoded[2][i])*1000
            for j in range(rang):
                fifoLocal.append(encoded[1][i][j])
                timeLineLocal.append(encoded[0] - (rang-j)*timeStep)
            newAr = [fifoLocal,timeLineLocal]
            dataOut.append(newAr)

        return dataOut

    def getFifoAndTime16BitUnsigned(self,addresS,number,uniT):
        result = self.getFifoAndTime(addresS,number,uniT)
        result = list(map(tuple,result))
        return result

    def getFifoAndTime16BitSigned(self,addresS,number,uniT):
        result = self.getFifoAndTime(addresS,number,uniT)
        for x in range(len(result)):
            result[x][0] = list(map(self.modValConverter.modTo16BitSigned,result[x][0]))
        result = list(map(tuple,result))
        return result

    def getFifoAndTime32BitUnsigned(self,addresS,number,uniT):
        result = self.getFifoAndTime(addresS,number*2,uniT)
        outData = []
        for x in range (number):
            timeLine = result[x*2][1]
            if(len(result[x*2][0]) != len(result[x*2][1])):
                self.exceptionHandler.generateException("RegsFIFOsHaveDifferentSizes")
            for i in range(len(result[x*2][0])):
                result[x*2][0][i] = self.modValConverter.modTo32BitUnsigned(result[x*2][0][i],result[x*2+1][0][i])
            dataLine = result[x*2][0]
            outData.append((dataLine,timeLine))
        return outData

    def getFifoAndTime32BitSigned(self,addresS,number,uniT):
        result = self.getFifoAndTime(addresS,number*2,uniT)
        outData = []
        for x in range (number):
            timeLine = result[x*2][1]
            if(len(result[x*2][0]) != len(result[x*2][1])):
                self.exceptionHandler.generateException("RegsFIFOsHaveDifferentSizes")
            for i in range(len(result[x*2][0])):
                result[x*2][0][i] = self.modValConverter.modTo32BitSigned(result[x*2][0][i],result[x*2+1][0][i])
            dataLine = result[x*2][0]
            outData.append((dataLine,timeLine))
        return outData

    def getFifoAndTimeFloat(self,addresS,number,uniT):
        result = self.getFifoAndTime(addresS,number*2,uniT)
        outData = []
        for x in range(number):
            timeLine = result[x*2][1]
            if(len(result[x*2][0]) != len(result[x*2][1])):
                self.exceptionHandler.generateException("RegsFIFOsHaveDifferentSizes")
            for i in range(len(result[x*2][0])):
                result[x*2][0][i] = self.modValConverter.modToFloat(result[x*2][0][i],result[x*2+1][0][i])
            dataLine = result[x*2][0]
            outData.append((dataLine,timeLine))
        return outData
