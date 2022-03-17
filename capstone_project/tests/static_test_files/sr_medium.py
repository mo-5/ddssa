""" tests contains any unit tests for backend files
"""
from pprint import pprint
import time
import warnings
from threading import Event
import os
import logging

# File contains 3 stall statements

print("before loop")

for i in range(8):
    if i == 7:
        warnings.warn("The loop is about to end!")  # Stall
# this is a random comment

    print("Hello, World!")  # Stall
    time.sleep(0.01)  # Stall

# # this is a random comment

    # # this is a random comment

    """Random 
    multi-line comment"""
    

    pprint("this is an object")
    

    os.system('echo "hello"')
    os.system('pause')
    logging.basicConfig(level=logging.INFO)

    logging.info("here is some info")
    
print("after loop")

k = 1

while(k < 5):
    pprint("inside while loop!")

print("outside loop")