#reading the input file



#opcodes
from audioop import add
from multiprocessing.sharedctypes import Value


opcode = {"10000":"add",           #A
        "10001":"sub",             #A
        "10010":"mov",             #B mov imm
        "10011":"mov",             #C mov reg
        "10100":"ld",              #D
        "10101":"st",              #D
        "10110":"mul",             #A
        "10111":"div",             #C
        "11000":"rs",              #B
        "11001":"ls",              #B
        "11010":"xor",             #A
        "11011":"or",              #A
        "11100":"and",             #A
        "11101":"not",             #C
        "11110":"cmp",             #C
        "11111":"jmp",             #E
        "01100":"jlt",             #E
        "01101":"jgt",             #E
        "01111":"je",              #E
        "01010":"hlt"}             #F

#registors in bin
reg = {"R0":"000",
    "R1":"001",
    "R2":"010",
    "R3":"011",
    "R4":"100",
    "R5":"101",
    "R6":"110",
    "FLAGS":"111", }

#semantics for instructions

###

#A(add sub mul xor or and)
def A(opc,r1,r2,r3):
    return opc + "00" + r1 + r2 + r3       #5+3+3+3 = 14

#B(mov Imm rs ls)
def B(opc,r1,imm):
    return opc + r1 + imm                  #5+3+8 = 16

#C(mov reg div not cmp)
def C(opc,r1,r2):
    return opc + "00000" + r1 + r2          #5+3+3 = 11

#D(ld st)
def D(opc,r1,addr):
    return opc + r1 + addr                  #5+3+8 s= 16

#E(jmp jlt jgt je)
def E(opc,addr):
    return opc + "000" + addr               #5+8 = 13

#F(hlt)
def F():
    return "0101000000000000"               #5

###

#-#

def intToBi(x):
    bi = bin(x)
    bi = bi.replace("0b","")
    return x

def key(val):
    for key, Value in opcode.items():
        if val == Value:
            return key


####
def conversion(inp,reg,addr):
    if(inp[0]=="add"):
        opc = key("add")
        r1 = reg.get(inp[1])
        r2 = reg.get(inp[2])
        r3 = reg.get(inp[3])
        print(A(opc,r1,r2,r3))
    
    elif():
        pass

    elif (inp[0] == "sub"):
        opc = key("sub")
        r1 = reg.get(inp[1])
        r2 = reg.get(inp[2])
        r3 = reg.get(inp[3])
        print(A(opc, r1, r2, r3))

    elif():
        pass

    elif (inp[0] == "mul"):
        opc = key("mul")
        r1 = reg.get(inp[1])
        r2 = reg.get(inp[2])
        r3 = reg.get(inp[3])
        print(A(opc, r1, r2, r3))

    elif():
        pass

    elif (inp[0] == "xor"):
        opc = key("xor")
        r1 = reg.get(inp[1])
        r2 = reg.get(inp[2])
        r3 = reg.get(inp[3])
        print(A(opc, r1, r2, r3))

    elif():
        pass

    elif (inp[0] == "or"):
        opc = key("or")
        r1 = reg.get(inp[1])
        r2 = reg.get(inp[2])
        r3 = reg.get(inp[3])
        print(A(opc, r1, r2, r3))

    elif():
        pass

    elif (inp[0] == "and"):
        opc = key("and")
        r1 = reg.get(inp[1])
        r2 = reg.get(inp[2])
        r3 = reg.get(inp[3])
        print(A(opc, r1, r2, r3))

    elif():
        pass

    elif (inp[0] == "mov"):
        if ("$" in inp[2]):
            opc = "10010"
            r1 = reg.get(inp[1])
            imm = intToBi(int(inp[2][1:len(inp[2])]))
            pr = "00000000" + imm
            im1 = pr[len(pr) - 8:len(pr)]
            print(B(opc, r1, im1))

        else:
            op = "10011"
            r1 = reg.get(inp[1])
            r2 = reg.get(inp[2])
            print(C(op, r1, r2))

    elif():
        pass

    






