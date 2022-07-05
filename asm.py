from audioop import add
import sys

#opcodes

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

A = ('add','sub','mul','xor','or','and')
B = ('rs','ls')
C = ('not','cmp','div')
D = ('ld','st')
E = ('jmp','jlt','jgt','je')

def key(val):
    for key, value in opcode.items():
        if val == value:
            return key

#semantics for instructions

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

def intToBi(x):
    bi = bin(x)
    bi = bi.replace("0b","")
    return x

def conversion(inp,reg,addr):
    ####        A
    if(inp[0]=="add"):
        print(A(key("add"),reg.get(inp[1]),reg.get(inp[2]),reg.get(inp[3])))
    
    elif (inp[0]=="sub"):
        print(A(key("sub"),reg.get(inp[1]),reg.get(inp[2]),reg.get(inp[3])))

    elif (inp[0]=="mul"):
        print(A(key("mul"),reg.get(inp[1]),reg.get(inp[2]),reg.get(inp[3])))

    elif (inp[0]=="xor"):
        print(A(key("xor"),reg.get(inp[1]),reg.get(inp[2]),reg.get(inp[3])))

    elif (inp[0]=="or"):
        print(A(key("or"),reg.get(inp[1]),reg.get(inp[2]),reg.get(inp[3])))

    elif (inp[0]=="and"):
        print(A(key("and"),reg.get(inp[1]),reg.get(inp[2]),reg.get(inp[3])))

    ####        mov Imm and mov Reg
    elif (inp[0]=="mov"):
        if ("$" in inp[2]):
            pr = "00000000" + intToBi(int(inp[2][1:len(inp[2])]))
            print(B("10010",reg.get(inp[1]),pr[len(pr) - 8:len(pr)]))

        else:
            print(C("10011",reg.get(inp[1]),reg.get(inp[2])))

    ###                 B
    elif (inp[0]=="rs"):
        oup = "00000000" + intToBi(int(inp[2][1:len(inp[2])]))
        print(B(key("rs"),reg.get(inp[1]),oup[len(oup) - 8:len(oup)]))

    elif (inp[0]=="ls"):
        oup = "00000000" + intToBi(int(oup[2][1:len(oup[2])]))
        print(B(key("ls"),reg.get(oup[1]),oup[len(oup) - 8:len(oup)]))
    
    ###             C
    elif(inp[0]=="div"):
        print(C(key("div"),reg.get(inp[1]),reg.get(inp[2])))

    elif (inp[0]=='not'):
        print(C(key('not'),reg.get(inp[1]),reg.get(inp[2])))

    elif (inp[0]=='cmp'):
        print(C(key('cmp'),reg.get(inp[1]),reg.get(inp[2])))

    ###         D
    elif (inp[0]=='ld'):
        oup = "00000000" + intToBi(int(addr.get(inp[2])))
        print(D(key('ld'),reg.get(inp[1]),oup[len(oup) - 8:len(oup)]))

    elif (inp[0]=='st'):
        oup = "00000000" + intToBi(int(addr.get(inp[2])))
        print(D(key('st'),reg.get(inp[1]),oup[len(oup) - 8:len(oup)]))

    ###         E
    elif (inp[0]=='jmp'):
        oup = "00000000" + intToBi(int(addr.get(inp[1])))
        print(E(key('jmp'),oup[len(oup) - 8:len(oup)]))

    elif (inp[0]=='jlt'):
        oup = "00000000" + intToBi(int(addr.get(inp[1])))
        print(E(key('jlt'),oup[len(oup) - 8:len(oup)]))

    elif (inp[0]=='jgt'):
        oup = "00000000" + intToBi(int(addr.get(inp[1])))
        print(E(key('jgt'),oup[len(oup) - 8:len(oup)]))

    elif (inp[0]=='je'):
        oup = "00000000" + intToBi(int(addr.get(inp[1])))
        print(E(key('je'),oup[len(oup) - 8:len(oup)]))

    ###         F
    elif (inp[0]=="hlt"):
        print(F())

    ###         FOR LABELS!!!

    ###             A
    elif (inp[0][-1]==":" and inp[1]=='add'):
        print(A(key("add"),reg.get(inp[2]),reg.get(inp[3]),reg.get(inp[4])))

    elif (inp[0][-1]==":" and inp[1]=='sub'):
        print(A(key("sub"),reg.get(inp[2]),reg.get(inp[3]),reg.get(inp[4])))

    elif (inp[0][-1]==":" and inp[1]=='mul'):
        print(A(key("mul"),reg.get(inp[2]),reg.get(inp[3]),reg.get(inp[4])))

    elif (inp[0][-1]==":" and inp[1]=='xor'):
        print(A(key("xor"),reg.get(inp[2]),reg.get(inp[3]),reg.get(inp[4])))

    elif (inp[0][-1]==":" and inp[1]=='or'):
        print(A(key("or"),reg.get(inp[2]),reg.get(inp[3]),reg.get(inp[4])))

    elif (inp[0][-1]==":" and inp[1]=='and'):
        print(A(key("and"),reg.get(inp[2]),reg.get(inp[3]),reg.get(inp[4])))

    ###         mov Imm & mov reg
    elif (inp[0][-1]==":" and inp[1]=="mov"):
        if ("$" in inp[3]):
            oup = "00000000" + intToBi(int(inp[3][1:len(inp[3])]))
            print(B("00010",reg.get(inp[2]), oup[len(oup) - 8:len(oup)]))

        else:
            print(C("00011",reg.get(inp[2]),reg.get(inp[3])))

    ###             B
    elif (inp[0][-1]==":" and inp[0]=="rs"):
        oup = "00000000" + intToBi(int(inp[3][1:len(inp[3])]))
        print(B(key("rs"),reg.get(inp[2]),oup[len(oup) - 8:len(oup)]))

    elif (inp[0][-1]==":" and inp[0]=="ls"):
        oup = "00000000" + intToBi(int(inp[3][1:len(inp[3])]))
        print(B(key("ls"),reg.get(inp[2]),oup[len(oup) - 8:len(oup)]))

    ###             C
    elif (inp[0][-1]==':' and inp[1]=="div"):
        print(C(key('div'),reg.get(inp[2]),reg.get(inp[3])))

    elif (inp[0][-1]==':' and inp[1]=="not"):
        print(C(key('not'),reg.get(inp[2]),reg.get(inp[3])))

    elif (inp[0][-1]==':' and inp[1]=="cmp"):
        print(C(key('cmp'),reg.get(inp[2]),reg.get(inp[3])))

    ###             D
    elif (inp[0][-1]==':' and inp[1]=="ld"):
        oup = "00000000" + intToBi(int(addr.get(inp[3])))
        print(D(key('ld'),reg.get(inp[2]),oup[len(oup) - 8:len(oup)]))

    elif (inp[0][-1]==':' and inp[1]=="st"):
        oup = "00000000" + intToBi(int(addr.get(inp[3])))
        print(D(key('st'),reg.get(inp[2]),oup[len(oup) - 8:len(oup)]))

    ###             E
    elif (inp[0][-1]==':' and inp[1]=='jmp'):
        oup = "00000000" + intToBi(int(addr.get(inp[2])))
        print(E(key('jmp'),oup[len(oup) - 8:len(oup)]))

    elif (inp[0][-1]==':' and inp[1]=='jlt'):
        oup = "00000000" + intToBi(int(addr.get(inp[2])))
        print(E(key('jlt'),oup[len(oup) - 8:len(oup)]))

    elif (inp[0][-1]==':' and inp[1]=='jgt'):
        oup = "00000000" + intToBi(int(addr.get(inp[2])))
        print(E(key('jgt'),oup[len(oup) - 8:len(oup)]))

    elif (inp[0][-1]==':' and inp[1]=='je'):
        oup = "00000000" + intToBi(int(addr.get(inp[2])))
        print(E(key('je'),oup[len(oup) - 8:len(oup)]))

    ###             F
    elif(inp[0][-1]==":" and inp[1]=="hlt"):
        print(F())

inpt = []
variables = []
c_start = 0
addr = {}
max_val = 255
min_val = 0
code = True

#reading the input file
temp = sys.stdin.read().splitlines()
for i in range(len(temp)):
    inpt.append(temp[i].split(" "))

for i in range(len(inpt)):          #appending and skipping to variables
    if inpt[i][0] == "var":
        if len(inpt[i]) == 2:
            addr[inpt[i][1]] = len(inpt)-c_start+i
            variables.append(inpt[i][1])

    if inpt[i][0] != "var":
        c_start = i
        break

    if inpt[i][0][-1] == ":":       #appending labels for chk
        addr[inpt[0][0:-1]] = i - c_start
        variables.append(inpt[i][0][0:-1])

# codeChk(inpt,opcode,reg,addr)

if code == True:
    for i in range(len(inpt)):
        conversion(inpt[i],opcode,reg,addr)




def codeChk(inp,opcode,reg,addr,i):
    if inp[0][-1] != ":":
        #variables
        if inp[0] not in opcode.values():
            if inp[0] == "var":
                if len(inp) == "2":
                    if (inp[1] >= max_val):
                        print("Variable value greater than supported val on line : ",i+1)
                        return False
                    elif (inp[1] <= min_val):
                        print("Variable value smaller than supported val on line : ",i+1)
                        return False
                    return True
                else:
                    print("Error in Variable declaration on line : ",i+1)
                    return False

        #Flags
        elif ("FLAGS" in inp):
            if (inp[0] == "mov"):
                if len(inp) == 3:
                    if inp[2] in reg.keys():
                        return True
            else:
                print("ILLEGAL USE OF FLAG REGISTOR ON LINE : ",i+1)
                return False

        #               A
        elif (inp[0] in A):
            if len(inp) != 4:
                print("SYNTAX ERROR : ",i+1)
                return False
            elif len(inp) == 4:
                if inp[1] not in reg.keys():
                    print("INVALID REGISTER",i+1)
                    return False
                if inp[2] not in reg.keys():
                    print("INVALID REGISTER",i+1)
                    return False
                if inp[3] not in reg.keys():
                    print("INVALID REGISTER",i+1)
                    return False
            else:
                return True

        #               mov
        elif (inp[0] == 'mov'):
            if len(inp) != 3:
                print("SNYTAX ERROR",i+1)
                return False
            else:
                if inp[2][0] == '$':
                    if (int(inp[2][1:len(inp[2])]) > 255):
                        print("IMMEDIATE VALUE SURPASSED")
                        return False
                    elif (int(inp[2][1:len(inp[2])]) < 0):
                        print("IMMEDIATE VALUE SUBCEEDED")
                        return False
                    elif inp[1] not in reg.keys():
                        print("INVALID REGISTER",i+1)
                        return False
                    else:
                        return True
                    
                elif inp[1] in reg.keys():
                    if inp[2] not in reg.keys():
                        print("INVALID REGISTER",i+1)
                        return False
                    else:
                        return True
                
                else:
                    print("ERROR ON LINE : ",i+1)
                    return False
                
        #               B
        elif (inp[0] in B):
            if len(inp) != 3:
                print("SYNTAX ERROR", i+1)
                return False
            elif inp[1] not in reg.keys():
                print("INVALID REGISTER")
                return False
            elif inp[2][0] != '$':
                print("INVALID IMMEDIATE VALUE")
                return False
            elif (int(inp[2][1:len(inp[2])]) > 255):
                print("IMMEDIATE VALUE SURPASSED")
                return False
            elif (int(inp[2][1:len(inp[2])]) < 0):
                print("IMMEDIATE VALUE SUBCEEDED")
                return False
            else:
                return True

        #               C
        elif (inp[0] in C):
            if len(inp) != 3:
                print("SYNTAX ERROR",i+1)
                return False
            elif inp[1] not in reg.keys():
                print("INVALID REGISTER")
                return False
            elif inp[2] not in reg.keys():
                print("INVALID REGISTER")
                return False
            else:
                return True

        #               D
        elif (inp[0] in D):
            if len(inp) != 3:
                print("SYNTAX ERROR",i+1)
                return False
            elif inp[1] not in reg.keys():
                print("INVALID REGISTER",i+1)
                return False
            elif inp[2] not in reg.keys():
                print("INVALID REGISTER",i+1)
            
            else:
                return True
        
        #               E
        elif (inp[0] in E):
            if len[inp] != 2:
                print("SYNTAX ERROR",i+1)
                return False
            elif inp[1] not in addr.keys():
                print("INVALID MEM ADDR",i+1)
                return False
            else:
                return True
            
        #               F
        elif (inp[0] == "hlt"):
            if len(inp) != 1:
                print("SYNTAX ERROR ",i+1)
                return False
            else:
                return True
        
        else:
            return False

        #               LABELS
    else:
        
