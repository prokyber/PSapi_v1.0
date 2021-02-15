from ModbusHandler import modbusHandler
from datetime import datetime
import time
import psutil, os
import serial.tools.list_ports
import logging

# logging.basicConfig()
# log = logging.getLogger()
# log.setLevel(logging.DEBUG)

# mbClient = None
# mbTcpClient = None

#Creartes Serial modbus client
def createModbusClient(port, stopBits, bytesize, parity, baudrate):
    global mbClient 
    mbClient = modbusHandler(type = "RTU",tcpIp = "", tcpPort = 0,Method = "rtu", Port = port, Stopbits = stopBits , Bytesize = bytesize, Parity = parity, Baudrate = baudrate)


#Create Modbus TCP client
def createModbusTcpClient(ip, port):
    global mbClient 
    mbClient = modbusHandler(type = "TCP",tcpIp = ip, tcpPort = port,Method = "", Port = 0, Stopbits = 0 , Bytesize = 0, Parity = 0, Baudrate = 0)
    mbClient.connect()

#Modbus registers to Float value
def modToFloat(self,MSB,LSB):
    modBytesMsb = MSB.to_bytes(2, byteorder='big', signed=False)
    modBytesLsb = LSB.to_bytes(2, byteorder='big', signed=False)
    modBytes = modBytesMsb + modBytesLsb
    modBytesFloat = struct.unpack(">f",modBytes)
    return modBytesFloat[0]

#Functions for reading Input registers(30001 - 40000)
def read16BitUnsignedInputs(regNum,numOfReg,slaveNum):
    result = mbClient.readInputRegisters(regNum,numOfReg,slaveNum)
    return result.registers

def read16BitSignedInputs(regNum,numOfReg,slaveNum):
    result = mbClient.readInputRegisters(regNum,numOfReg,slaveNum)
    outputArray = []
    for x in range(numOfReg):
        outputArray.append(mbClient.modValConverter.modTo16BitSigned(result.registers[x]))
    return outputArray

def read32BitUnsignedInputs(regNum,numOfReg,slaveNum):
    result = mbClient.readInputRegisters(addresS = regNum, counT = numOfReg*2, uniT = slaveNum)
    outputArray = []
    for x in range(numOfReg):
        outputArray.append(mbClient.modValConverter.modTo32BitUnsigned(result.registers[x*2],result.registers[x*2+1]))
    return outputArray

def read32BitSignedInputs(regNum,numOfReg,slaveNum):
    result = mbClient.readInputRegisters(addresS = regNum, counT = numOfReg*2, uniT = slaveNum)
    outputArray = []
    for x in range(numOfReg):
        outputArray.append(mbClient.modValConverter.modTo32BitSigned(result.registers[x*2],result.registers[x*2+1]))
    return outputArray

def readFloatInputs(regNum,numOfReg,slaveNum):
    result = mbClient.readInputRegisters(addresS = regNum, counT = numOfReg*2, uniT = slaveNum)
    outputArray = []
    for x in range(numOfReg):
        outputArray.append(mbClient.modValConverter.modToFloat(result.registers[x*2],result.registers[x*2+1]))
    return outputArray

#Functions for reading Holding registers(40001 - 50000)
def read16BitUnsignedHoldings(regNum,numOfReg,slaveNum):
    result = mbClient.readHoldingRegisters(regNum,numOfReg,slaveNum)
    return result.registers

def read16BitSignedHoldings(regNum,numOfReg,slaveNum):
    result = mbClient.readHoldingRegisters(regNum,numOfReg,slaveNum)
    outputArray = []
    for x in range(numOfReg):
        outputArray.append(mbClient.modValConverter.modTo16BitSigned(result.registers[x]))
    return outputArray

def read32BitSignedHoldings(regNum,numOfReg,slaveNum):
    result = mbClient.readHoldingRegisters(addresS = regNum, counT = numOfReg*2, uniT = slaveNum)
    outputArray = []
    for x in range(numOfReg):
        outputArray.append(mbClient.modValConverter.modTo32BitSigned(result.registers[x*2],result.registers[x*2+1]))
    return outputArray

def read32BitUnsignedHoldings(regNum,numOfReg,slaveNum):
    result = mbClient.readHoldingRegisters(addresS = regNum, counT = numOfReg*2, uniT = slaveNum)
    outputArray = []
    for x in range(numOfReg):
        outputArray.append(mbClient.modValConverter.modTo32BitUnsigned(result.registers[x*2],result.registers[x*2+1]))
    return outputArray

def readFloatHoldings(regNum,numOfReg,slaveNum):
    result = mbClient.readHoldingRegisters(addresS = regNum, counT = numOfReg*2, uniT = slaveNum)
    outputArray = []
    # print(result)
    for x in range(numOfReg):
        outputArray.append(mbClient.modValConverter.modToFloat(result.registers[x*2],result.registers[x*2+1]))
    return outputArray


#Functions for reading Fifo queues of Input registers(30001 - 40000) and chip internal time(for synch)
def read16BitUnsignedFifoAndTime(regNum,numOfReg,slaveNum):
    result = mbClient.getFifoAndTime16BitUnsigned(regNum,numOfReg,slaveNum)
    return result 

def read16BitSignedFifoAndTime(regNum,numOfReg,slaveNum):
    result = mbClient.getFifoAndTime16BitSigned(regNum,numOfReg,slaveNum)
    return result 

def read32BitUnsignedFifoAndTime(regNum,numOfReg,slaveNum):
    result = mbClient.getFifoAndTime32BitUnsigned(regNum,numOfReg,slaveNum)
    return result 

def read32BitSignedFifoAndTime(regNum,numOfReg,slaveNum):
    result = mbClient.getFifoAndTime32BitSigned(regNum,numOfReg,slaveNum)
    return result 

def readFloatFifoAndTime(regNum,numOfReg,slaveNum):
    result = mbClient.getFifoAndTimeFloat(regNum,numOfReg,slaveNum)
    return result

#Functions for reading discrete inputs(10001 - 20000)
def readDiscreteInputs(regNum,numOfReg, slaveNum):
    result=mbClient.readDiscreteInputs(addresS = regNum, counT = numOfReg, uniT = slaveNum)
    return result.bits

#Functions for reading coils(1-10000)
def readCoils(regNum,numOfReg, slaveNum):
    result = mbClient.readCoils(regNum,numOfReg, slaveNum)
    return result.bits

#Functions for wiriting coils(1-10000)
def writeCoils(regNum,value,slaveNum):
    result=mbClient.writeCoils(regNum, value, slaveNum)
    return result

#Functions for wiriting holding registers(40001 - 50000)
def write16BitUnsignedHoldingRegister(regNum,value,slaveNum):
    result=mbClient.write16BitUnsignedRegister(regNum, value, slaveNum)
    return result

def write16BitUnsignedHoldings(regNum,value,slaveNum):
    result=mbClient.write16BitUnsignedRegisters(regNum, value, slaveNum)
    return result

def write16BitSignedHoldings(regNum,value,slaveNum):
    value = list(map(mbClient.modValConverter.val16BitSignedToMod,value))
    result=mbClient.write16BitUnsignedRegisters(regNum, value, slaveNum)
    return result

def write32BitUnsignedHoldings(regNum,value,slaveNum):
    arrayToSet = []
    for i in range(len(value)):
        vals = mbClient.modValConverter.val32BitUnsignedToMod(value[i])
        arrayToSet.append(vals[0])
        arrayToSet.append(vals[1])    
    result=mbClient.write16BitUnsignedRegisters(regNum, arrayToSet, slaveNum)
    return result

def write32BitSignedHoldings(regNum,value,slaveNum):
    arrayToSet = []
    for i in range(len(value)):
        vals = mbClient.modValConverter.val32BitSignedToMod(value[i])
        arrayToSet.append(vals[0])
        arrayToSet.append(vals[1])    
    result=mbClient.write16BitUnsignedRegisters(regNum, arrayToSet, slaveNum)
    return result

def writeFloatHoldings(regNum,value,slaveNum):
    arrayToSet = []
    for i in range(len(value)):
        vals = mbClient.modValConverter.valFloatToMod(value[i])
        arrayToSet.append(vals[0])
        arrayToSet.append(vals[1])    
    result=mbClient.write16BitUnsignedRegisters(regNum, arrayToSet, slaveNum)
    return result

#Returns names of available serial ports
def getPorts():
    try:
        comPorts = list(serial.tools.list_ports.comports())    # get list of all devices connected through serial port
    except TypeError:
        return []
    portNames = []
    for cp in comPorts:
        portNames.append(cp.device)
    return portNames

# while(1):
#     readFloatFifoAndTime(30023,3,4)
    # time.sleep(1)
# # createModbusClient("/dev/ttyACM0",1,8,'E',230400)
# # # # # print(readFloatFifoAndFloat(30040,2,4))
# # # # # print(mbClient)\

# write16BitUnsignedHoldings(40462,1,4)
# write16BitUnsignedHoldings(40353,[400,1,60,0,0,49440,0,1,1],4)
# write16BitUnsignedHoldings(40360,0,4)


# write16BitUnsignedHoldings(40462,1,4)
# write16BitUnsignedHoldings(40363,[400,1,60,0,0,16672,0,1,1],4)
# write16BitUnsignedHoldings(40360,0,4)


# write16BitUnsignedHoldings(40355,0,4)
# write16BitUnsignedHoldings(40356,0,4)
# write16BitUnsignedHoldings(40357,0,4)
# write16BitUnsignedHoldingRegister(40358,16672,4)
# write16BitUnsignedHoldingRegister(40359,0,4)
# write16BitUnsignedHoldings(40360,1,4)

# createModbusTcpClient("10.42.0.18",80)
# createModbusTcpClient("192.168.0.108",80)
# createModbusClient("/dev/ttyACM0",1,8,"E",2000000)
# write32BitUnsignedHoldings(40020,[2000],4)
# time.sleep(0.005)
# writeFloatHoldings(40022,[0.1],4)
# time.sleep(0.005)
# write16BitUnsignedHoldings(40024,[0],4)
# time.sleep(0.005)
# writeFloatHoldings(40025,[0.1],4)
# time.sleep(0.005)
# write16BitUnsignedHoldings(40027,[1],4)
# time.sleep(0.005)
# writeCoils(1,[1],4)
# while(1):
    # time.sleep(0.010)
    # timeBefore = time.time()
    # result = read16BitUnsignedFifoAndTime(30001,8,4)

    # result = read32BitUnsignedHoldings(40001,1,4)
    # print(time.time()-timeBefore)

# write16BitUnsignedHoldings(40020,[400,1,60,0,0,49440,0,1,1],4)
# write16BitUnsignedHoldingRegister(40020,400,4)
# write16BitUnsignedHoldingRegister(40023,1,4)
# write16BitUnsignedHoldingRegister(40024,1,4)
# write16BitUnsignedHoldingRegister(40025,16754,4)
# write16BitUnsignedHoldingRegister(40027,1,4)
# write16BitUnsignedHoldingRegister(40028,1,4)
# write16BitUnsignedHoldings(40002,1,4)
# write32BitUnsignedHoldings(40010,[1000000],4)
# writeFloatHoldings(40012,[0.5],4)
# write32BitUnsignedHoldings(40014,[100000],4)
# writeFloatHoldings(40016,[0.2],4)

# createModbusTcpClient("192.168.0.114",80)
#     print(result[1])
    # read16BitUnsignedFifoAndTime(30001,4,4)
    # read16BitUnsignedFifoAndTime(30001,4,4)
    # print((time.perf_counter()-d)*1000)
    # print(len(readFloatFifoAndTime(30009,4,4)))
    # # print(read16BitUnsignedHoldings(40353,10,3))
    # print(readFloatInputs(30001,4,4))
    # print(read32BitUnsignedHoldings(40002,4,4))
    # print(read16BitUnsignedHoldings(40020,14,4))
    # time.sleep(0.1)
    # print(write16BitUnsignedHoldingReg
    # isters(40001,[12,11],4))
    # 
    # print("data")
    # print(readFloatFifoAndTime(30027,4,4))
    # time.sleep(0.01)
    # print((time.perf_counter()-d)*1000)

# import matplotlib.pyplot as plt
# import requests
# from drawnow import drawnow
# import numpy as np
# x=[]
# y=[]
# def make_fig():
#     plt.scatter(x, y,marker=".")  # I think you meant this

# plt.ion()  # enable interactivity
# fig = plt.figure()  # make a figure

# createModbusTcpClient("192.168.0.114",80)
# # createModbusTcpClient("192.168.0.103",80)
# # createModbusTcpClient("192.168.1.11",80)
# #     result = readFloatFifoAndTime(30001,2,4)

# while(1):
#     result = readFloatFifoAndTime(30007,1,4)
#     y = result[0][0]
#     x = result[0][1]
#     drawnow(make_fig)
#     print(readFloatHoldings(40100,10,4))