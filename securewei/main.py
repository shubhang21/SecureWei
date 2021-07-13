import sys
import os
os.system('rm -rf input.sol')
file_i=open("input.sol","w")
file_i.write(sys.argv[1])
file_i.close()
file_i=open("input.sol","r")

lines=[]
lines=file_i.readlines()
file_i.close()
new_file = open("input.sol", "w")
for  line in lines:
    if len(line.split())!=0:
        if  line.split()[0]=="pragma":
            
            new_file.write("pragma solidity ^0.8; \n")
        else:
            new_file.write(line)
new_file.close()
            
            

        
os.system('rm -rf output.txt')
file_o=open("output.txt","w")
os.system('slither input.sol 2>&1 | tee output.txt >/dev/null 2>&1')


file_o.close()
file_o=open("output.txt","r")
file_r=open("result.txt","w")
file_r.close()
file_r=open("result.txt","a")
#apply operation on file_o and store reslut in file_r
lines=[]
prag="Pragma version^0.8 (input.sol#1) is too complex"
lines=file_o.readlines()

for line in lines:
    #logic-true
    
    if line.find(prag)!=-1:
        file_r.write("Pragma version is too complex\n")
        
    
    else:
        if len(line.split())!=0:
            if  line.split()[0]!="INFO:Slither:input.sol":
                if  line.split()[0]!="Reference:"and line.split()[0]!="Warning:"and line.split()[0][0:4]!="INFO" and  line.split()[0]!="-->" and line.split()[0]!="Compilation"  and line.split()[0]!="solc-0.8.5":
                    file_r.write(line)
            else:
                print("******************"+line.split()[7]+" Vulnerabilities Found ******************")
    
file_o.close()
file_r.close()
file_r=open("result.txt","r")
print(file_r.read())
file_r.close()