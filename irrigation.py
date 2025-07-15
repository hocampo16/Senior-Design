#valve control

import RPi.GPIO as GPIO
import time 
  
def init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(16,GPIO.OUT)
    GPIO.setup(18,GPIO.OUT)

def off():
    init()
    GPIO.output(16,False)
    GPIO.output(18,False)
  
#open valve
def open(sec):
    init()
    print("valve open")
    GPIO.output(16,True)
    GPIO.output(18,False)
    time.sleep(sec)
    off()

#close valve
def close(sec):
    init()
    print("valve closed")
    GPIO.output(16,False)
    GPIO.output(18,True)
    time.sleep(sec)
    off()  

# print("opening")
# open(3)
# time.sleep(30)
# print("closing")
# close(3)


        