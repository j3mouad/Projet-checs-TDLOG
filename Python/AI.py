import os
import sys
new_dir = '/home/hassene/Desktop/Projet-echecs-TDLOG/build'
os.chdir(new_dir)
# Add to sys.path
if new_dir not in sys.path:
    sys.path.append(new_dir)
import libAI

a,b = libAI.generator() 
print(a,b)
def AI() : 
    return a,b 

