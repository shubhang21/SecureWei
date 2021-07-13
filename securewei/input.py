import sys
import os
os.system('rm -rf input.sol')
file=open("input.sol","w")
file.write(sys.argv[1])
file.close()
os.system('rm -rf output.txt')
file=open("output.txt","w")
os.system('slither input.sol 2>&1 | tee output.txt')
file=open("output.txt","r")
print(file.read())
file.close()

