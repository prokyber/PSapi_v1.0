import struct

class ModValConverter:
    def val16BitSignedToMod(self,regVal):
        modBytes = regVal.to_bytes(2, byteorder='big', signed=True)
        modBytes = struct.unpack(">H",modBytes)
        return modBytes[0]

    def val32BitUnsignedToMod(self,regVal):
        ba = bytearray(struct.pack(">L", regVal)) 
        msb = struct.unpack(">H",ba[0:2])
        lsb = struct.unpack(">H",ba[2:4])
        return [msb[0],lsb[0]]

    def val32BitSignedToMod(self,regVal):
        ba = bytearray(struct.pack(">l", regVal)) 
        msb = struct.unpack(">H",ba[0:2])
        lsb = struct.unpack(">H",ba[2:4])
        return [msb[0],lsb[0]]

    def valFloatToMod(self,regVal):
        ba = bytearray(struct.pack(">f", regVal)) 
        msb = struct.unpack(">H",ba[0:2])
        lsb = struct.unpack(">H",ba[2:4])
        return [msb[0],lsb[0]]

    def modTo16BitSigned(self,regVal):
        modBytes = regVal.to_bytes(2, byteorder='big', signed=False)
        modBytes = struct.unpack(">h",modBytes)
        return modBytes[0]

    def modTo32BitUnsigned(self,MSB,LSB):
        modBytesMsb = MSB.to_bytes(2, byteorder='big', signed=False)
        modBytesLsb = LSB.to_bytes(2, byteorder='big', signed=False)
        modBytes = modBytesMsb + modBytesLsb
        modBytes = struct.unpack(">L",modBytes)
        return modBytes[0]

    def modTo32BitSigned(self,MSB,LSB):
        modBytesMsb = MSB.to_bytes(2, byteorder='big', signed=False)
        modBytesLsb = LSB.to_bytes(2, byteorder='big', signed=False)
        modBytes = modBytesMsb + modBytesLsb
        modBytes = struct.unpack(">l",modBytes)
        return modBytes[0]

    def modToFloat(self,MSB,LSB):
        modBytesMsb = MSB.to_bytes(2, byteorder='big', signed=False)
        modBytesLsb = LSB.to_bytes(2, byteorder='big', signed=False)
        modBytes = modBytesMsb + modBytesLsb
        modBytesFloat = struct.unpack(">f",modBytes)
        return modBytesFloat[0]
