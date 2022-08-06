import sys
#import matplotlib.pyplot as plt
import fileinput
mem = []
inp = []
for line in fileinput.input():
    mem.append(line)
    line = line.strip('\n')
    inp.append(line)

for i in range(len(mem),256):
    mem.append("0000000000000000\n")

# for i in range(len(mem)):
#     print(mem[i])

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
reg = {"1":"000",
    "2":"001",
    "3":"010",
    "4":"011",
    "5":"100",
    "6":"101",
    "7":"110",
    "8":"111", }

Reg = ("R0","R1","R2","R3","R4","R5","R6","FLAGS")

A1 = ('add','sub','mul','xor','or','and')
B1 = ('rs','ls')
C1 = ('not','cmp','div')
D1 = ('ld','st')
E1 = ('jmp','jlt','jgt','je')

#flags
ovrflw = False          #add sub mul
lssThan = False         #cmp
GrtrThan = False        #cmp
Equal = False           #cmp

def key(val):
    for key, value in reg.items():
        if val == value:
            return key

def base2(x):
    return bin(x).replace('0b','')

def complement2(x):
    n = ''
    for i in x:
        if i == '0':
            n = n + '1'
        else:
            n = n + '0'
    return n

def base10(x):
    return int(x, 2)

format = ['00000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000']

PC = 0
cd = 0
halted = False

bonus = {}
inst = {}
ins_clk = 0

#i
clk = 0


while(not halted):
    ins = inp[cd]
    inst[PC] = clk
    opc = ins[0:5]

    #addf subf movf
    if opc == '00000':
        format[-1] = '0000000000000000'
        r1 = ins[7:10]
        r2 = ins[10:13]
        r1 = int(key(r1))
        r2 = int(key(r2))
        r3 = ins[13:16]
        r3 = int(key(r3))
        a = base10(format[r1])
        b = base10(format[r2])
        c = base10(format[r3])

        a = b + c

        if a > (2**8-1):
            a = 65535
            format[-1] = '0000000000001000'
            ovrflw = True

        a = '0000000000000000' + base2(a)
        format[r1] = a[len(a)-16:len(a)]
        print(' '.join(format))

        i = base10(format[0])
        i = i + 1
        i = '00000000' + base2(i)

        format[0] = i[len(i)-8:len(i)]
        clk+=1

    elif opc == "00001":
        format[-1] = '0000000000000000'
        r1 = ins[7:10]
        r1 = int(key(r1))
        r2 = ins[10:13]
        r2 = int(key(r2))
        r3 = ins[13:16]
        r3 = int(key(r3))
        a = base10(format[r1])
        b = base10(format[r2])
        c = base10(format[r3])

        if c - b < -(2**8 - 1):
            a = 0
            ovrflw = True
            format[-1] = '0000000000001000'
        else:
            a = b - c

        a = '0000000000000000' + base2(a)
        format[r1] = a[len(a)-16:len(a)]
        print(' '.join(format))

        i = base10(format[0])
        i = i + 1
        i = '00000000' + base2(i)

        format[0] = i[len(i)-8:len(i)]
        clk+=1

    elif opc == "00010":
        format[-1] = '0000000000000000'
        r1 = ins[5:8]
        r1 = int(key(r1))
        format[r1] = '00000000' + ins[8:16]
        print(' '.join(format))
        i = base10(format[0])
        i = i + 1
        i = '00000000' + base2(i)
        format[0] = i[len(i)-8:len(i)]
        clk+=1

    #add sub mul xor or and 
    if opc == '10000':
        format[-1] = '0000000000000000'
        r1 = ins[7:10]
        r2 = ins[10:13]
        r1 = int(key(r1))
        r2 = int(key(r2))
        r3 = ins[13:16]
        r3 = int(key(r3))
        a = base10(format[r1])
        b = base10(format[r2])
        c = base10(format[r3])

        a = b + c

        if a > (2**16-1):
            a = 65535
            format[-1] = '0000000000001000'
            ovrflw = True

        a = '0000000000000000' + base2(a)
        format[r1] = a[len(a)-16:len(a)]
        print(' '.join(format))

        i = base10(format[0])
        i = i + 1
        i = '00000000' + base2(i)

        format[0] = i[len(i)-8:len(i)]
        clk+=1

    elif opc == "10001":
        format[-1] = '0000000000000000'
        r1 = ins[7:10]
        r1 = int(key(r1))
        r2 = ins[10:13]
        r2 = int(key(r2))
        r3 = ins[13:16]
        r3 = int(key(r3))
        a = base10(format[r1])
        b = base10(format[r2])
        c = base10(format[r3])

        if c > b:
            a = 0
            ovrflw = True
            format[-1] = '0000000000001000'
        else:
            a = b - c

        a = '0000000000000000' + base2(a)
        format[r1] = a[len(a)-16:len(a)]
        print(' '.join(format))

        i = base10(format[0])
        i = i + 1
        i = '00000000' + base2(i)

        format[0] = i[len(i)-8:len(i)]
        clk+=1

    elif opc == "10110":
        format[-1] = '0000000000000000'
        r1 = ins[7:10]
        r1 = int(key(r1))
        r2 = ins[10:13]
        r2 = int(key(r2))
        r3 = ins[13:16]
        r3 = int(key(r3))
        a = base10(format[r1])
        b = base10(format[r2])
        c = base10(format[r3])

        a = b * c

        if a > (2**16-1):
            a = 65535
            format[-1] = '0000000000001000'
            ovrflw = True

        a = '0000000000000000' + base2(a)
        format[r1] = a[len(a)-16:len(a)]
        print(' '.join(format))

        i = base10(format[0])
        i = i + 1
        i = '00000000' + base2(i)

        format[0] = i[len(i)-8:len(i)]
        clk+=1

    elif opc == "11010":
        format[-1] = '0000000000000000'
        r1 = ins[7:10]
        r1 = int(key(r1))
        r2 = ins[10:13]
        r2 = int(key(r2))
        r3 = ins[13:16]
        r3 = int(key(r3))
        a = base10(format[r1])
        b = base10(format[r2])
        c = base10(format[r3])

        a = b ^ c

        # if a > (2**16-1):
        #     a = 65535
        #     format[-1] = '0000000000001000'

        a = '0000000000000000' + base2(a)
        format[r1] = a[len(a)-16:len(a)]
        print(' '.join(format))

        i = base10(format[0])
        i = i + 1
        i = '00000000' + base2(i)

        format[0] = i[len(i)-8:len(i)]
        clk+=1

    elif opc == "11011":
        format[-1] = '0000000000000000'
        r1 = ins[7:10]
        r1 = int(key(r1))
        r2 = ins[10:13]
        r2 = int(key(r2))
        r3 = ins[13:16]
        r3 = int(key(r3))
        a = base10(format[r1])
        b = base10(format[r2])
        c = base10(format[r3])

        a = b | c

        # if a > (2**16-1):
        #     a = 65535
        #     format[-1] = '0000000000001000'

        a = '0000000000000000' + base2(a)
        format[r1] = a[len(a)-16:len(a)]
        print(' '.join(format))

        i = base10(format[0])
        i = i + 1
        i = '00000000' + base2(i)

        format[0] = i[len(i)-8:len(i)]
        clk+=1

    elif opc == "11100":
        format[-1] = '0000000000000000'
        r1 = ins[7:10]
        r1 = int(key(r1))
        r2 = ins[10:13]
        r2 = int(key(r2))
        r3 = ins[13:16]
        r3 = int(key(r3))
        a = base10(format[r1])
        b = base10(format[r2])
        c = base10(format[r3])

        a = b & c

        # if a > (2**16-1):
        #     a = 65535
        #     format[-1] = '0000000000001000'

        a = '0000000000000000' + base2(a)
        format[r1] = a[len(a)-16:len(a)]
        print(' '.join(format))

        i = base10(format[0])
        i = i + 1
        i = '00000000' + base2(i)

        format[0] = i[len(i)-8:len(i)]
        clk+=1

#mov imm rs ls 
    elif opc == "10010":
        format[-1] = '0000000000000000'
        r1 = ins[5:8]
        r1 = int(key(r1))
        format[r1] = '00000000' + ins[8:16]
        print(' '.join(format))
        i = base10(format[0])
        i = i + 1
        i = '00000000' + base2(i)
        format[0] = i[len(i)-8:len(i)]
        clk+=1

    elif opc == "11000":
        format[-1] = '0000000000000000'
        r1 = ins[5:8]
        r1 = int(key(r1))
        r2 = base10(format[r1])
        r3 = base10(ins[8:16])
        a = '0000000000000000' + base2(r2 >> r3)
        a = a[len(a) - 16:len(a)]
        format[r1] = a
        print(' '.join(format))
        i = base10(format[0])
        i = i + 1
        i = '00000000' + base2(i)
        format[0] = i[len(i)-8:len(i)]
        clk+=1

    elif opc == "11001":
        format[-1] = '0000000000000000'
        r1 = ins[5:8]
        r1 = int(key(r1))
        r2 = base10(format[r1])
        r3 = base10(ins[8:16])
        a = '0000000000000000' + base2(r2 << r3)
        format[r1] = a[len(a) - 16:len(a)]
        print(' '.join(format))
        i = base10(format[0])
        i = i + 1
        i = '00000000' + base2(i)
        format[0] = i[len(i)-8:len(i)]
        clk+=1

#mov reg div not cmp
    elif opc == "10011":
        format[-1] = '0000000000000000'
        r1 = ins[10:13]
        r1 = int(key(r1))
        r2 = ins[13:16]
        r2 = int(key(r2))
        format[r1] = format[r2]

        if ins[13:16] == '111':
            format[-1] = '0000000000000000'
        
        print(' '.join(format))
        i = base10(format[0])
        i = i + 1
        i = '00000000' + base2(i)
        format[0] = i[len(i)-8:len(i)]
        clk+=1

    elif opc == "10111":
        format[-1] = '0000000000000000'
        r1 = ins[10:13]
        r1 = int(key(r1))
        r2 = ins[13:16]
        r2 = int(key(r2))
        a = base10(format[r1])
        b = base10(format[r2])

        q = "0000000000000000" + base2(a // b)
        r = "0000000000000000" + base2(a % b)

        format[2] = q[len(q) - 16:len(q)]
        format[1] = r[len(r) - 16:len(r)]

        print(' '.join(format))
        i = base10(format[0])
        i = i + 1
        i = '00000000' + base2(i)
        format[0] = i[len(i)-8:len(i)]
        clk+=1

    elif opc == "11101":
        format[-1] = '0000000000000000'
        r1 = ins[10:13]
        r1 = int(key(r1))
        r2 = ins[13:16]
        r2 = int(key(r2))
        
        format[r1] = complement2(format[r2])

        print(' '.join(format))
        i = base10(format[0])
        i = i + 1
        i = '00000000' + base2(i)
        format[0] = i[len(i)-8:len(i)]
        clk+=1

    elif opc == "11110":
        format[-1] = '0000000000000000'
        r1 = ins[10:13]
        r1 = int(key(r1))
        r2 = ins[13:16]
        r2 = int(key(r2))
        a = base10(format[r1])
        b = base10(format[r2])

        if a > b:
            format[-1] = '0000000000000010'
            GrtrThan = True
        elif a < b:
            format[-1] = '0000000000000100'
            lssThan = True
        elif a == b:
            format[-1] = '0000000000000001'
            Equal = True

        print(' '.join(format))
        i = base10(format[0])
        i = i + 1
        i = '00000000' + base2(i)
        format[0] = i[len(i)-8:len(i)]
        clk+=1

#ld st 
    elif opc == "10100":
        format[-1] = '0000000000000000'
        r1 = ins[5:8]
        r1 = int(key(r1))
        r2 = ins[8:16]
        membase10 = mem[base10(r2)].strip('\n')
        format[r1] = membase10
        print(' '.join(format))
        i = base10(format[0])
        i = i + 1
        i = '00000000' + base2(i)
        format[0] = i[len(i)-8:len(i)]
        bonus[PC] = clk
        clk+=1

    elif opc == "10101":
        format[-1] = '0000000000000000'
        r1 = ins[5:8]
        r2 = ins[8:16]
        r1 = int(key(r1))
        mem[base10(r2)] = format[r1]
        print(' '.join(format))
        i = base10(format[0])
        i = i + 1
        i = '00000000' + base2(i)
        format[0] = i[len(i)-8:len(i)]
        bonus[PC] = clk
        clk+=1

#jmp jlt jgt je
    elif opc == "11111":
        addr = ins[5:16]
        addr = base10(addr)
        format[-1] = '0000000000000000'
        print(' '.join(format))

        i = "00000000" + ins[8:16]
        format[0] = i[len(i) - 8:len(i)]
        cd = addr - 1
        
        bonus[PC] = clk
        PC = PC + 1
        bonus[PC] = cd
        clk = addr

    elif opc == "01100":
        if lssThan == True:
            addr = base10(ins[5:16])
            format[-1] = '0000000000000000'
            print(' '.join(format))
            r1 = "00000000" + ins[8:16]
            format[0] = r1[len(r1) - 8:len(r1)]
            bonus[PC] = clk
            PC = PC + 1
            cd = addr - 1
            bonus[PC] = cd
            clk = addr

        else:
            format[-1] = '0000000000000000'
            print(' '.join(format))
            a = base10(format[0])
            a = "00000000" + base2(a + 1)
            format[0] = a[len(a) - 8:len(a)]
            clk+=1

    elif opc == "01101":
        if GrtrThan == True:
            addr = base10(ins[5:16])
            format[-1] = '0000000000000000'
            print(' '.join(format))
            r1 = "00000000" + ins[8:16]
            format[0] = r1[len(r1) - 8:len(r1)]
            bonus[PC] = clk
            PC = PC + 1
            cd = addr - 1
            bonus[PC] = cd
            clk = addr

        else:
            format[-1] = '0000000000000000'
            print(' '.join(format))
            a = base10(format[0])
            a = "00000000" + base2(a + 1)
            format[0] = a[len(a) - 8:len(a)]
            clk+=1

    elif opc == "01111":
        if Equal == True:
            addr = base10(ins[5:16])
            format[-1] = '0000000000000000'
            print(' '.join(format))
            r1 = "00000000" + ins[8:16]
            format[0] = r1[len(r1) - 8:len(r1)]
            bonus[PC] = clk
            PC = PC + 1
            cd = addr - 1
            bonus[PC] = cd
            clk = addr

        else:
            format[-1] = '0000000000000000'
            print(' '.join(format))
            a = base10(format[0])
            a = "00000000" + base2(a + 1)
            format[0] = a[len(a) - 8:len(a)]
            clk+=1

#hlt
    elif opc == "01010":
        print(' '.join(format))
        break

    PC = PC + 1
    ins_clk = ins_clk + 1
    cd = cd + 1

# for i in mem:
#     print(i)   
# 
o = []

for i in range(len(mem)):
    if mem[i] != '':
        a=mem[i].strip('\n')
        o.append(a)
    # sys.stdout.write(mem[i]) 

b = list(filter(None,o))
for i in range(len(mem)):
    print(b[i])

# for k in inst.keys():
#     x = k
#     y = inst[k]
#     plt.scatter(x,y,color = 'm')
#     for j in bonus.keys():
#         if j == k:
#             q = bonus[j]
#             plt.scatter(x,q,color = 'm')
# plt.show()