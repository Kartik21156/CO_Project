import os
path = "C:/Users/kartik/Desktop/test.txt"
f = open(path,"a")

i=0
while True:
    line = input(f"{i} ")
    line = line + "\n"
    f.write(line)
    i = i + 1
    if line == 'hlt\n':
        break

f.close()

os.system(f"python ./asm.py test.txt")
