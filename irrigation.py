#valve control

import RPi.GPIO as GPIO
import time 
  
def init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(16,GPIO.OUT)
    GPIO.setup(10,GPIO.OUT)

def off():
    init()
    GPIO.output(16,False)
    GPIO.output(10,False)
  
#open valve
def open(sec):
    init()
    GPIO.output(16,True)
    GPIO.output(10,False)
    time.sleep(sec)
    off()

#close valve
def close(sec):
    init()
    GPIO.output(16,False)
    GPIO.output(10,True)
    time.sleep(sec)
    off()
    

# print("opening")
# open(3)
# time.sleep(60)
# print("closing")
# close(3)
 

        