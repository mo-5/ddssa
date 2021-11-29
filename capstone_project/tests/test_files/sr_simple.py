import time
import warnings
# File contains 3 stall statements

for i in range(8):
    if i == 7:
        warnings.warn("The loop is about to end!") #Stall

    print("Hello, World!") #Stall
    time.sleep(0.01) #Stall
