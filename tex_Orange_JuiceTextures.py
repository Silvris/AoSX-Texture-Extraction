from inc_noesis import *

def registerNoesisTypes():
    handle = noesis.register("Orange_Juice Decompressed Textures", ".ojt")
    noesis.setHandlerTypeCheck(handle, texCheckType)
    noesis.setHandlerLoadRGBA(handle, texLoadARGB)
    noesis.logPopup()
    return 1


def texCheckType(data):
    bs = NoeBitStream(data)
    fileMagic = bs.readUInt()
    if fileMagic in (0x47414c,0x4d474c):
        return 1
    else:
        print("Fatal Error: Unknown file magic: " + str(hex(fileMagic) + " expected 0x47414c!"))
        return 0

def texLoadARGB(data, texList):
    bs = NoeBitStream(data)
    magic = bs.readUInt()
    width = bs.readUInt()
    height = bs.readUInt()
    if(magic == 0x4d474c):
        length = width*height
        pix = rapi.imageDecodeDXT(bs.readBytes(length), width, height, noesis.NOESISTEX_DXT5)
    else:
        length = width*height*8
        pix = rapi.imageDecodeRaw(bs.readBytes(length), width, height, "b16g16r16a16")
    texList.append(NoeTexture("OJTex", width, height, pix, noesis.NOESISTEX_RGBA32))
    return 1