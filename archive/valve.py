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
    GPIO.output(16,True)
    GPIO.output(18,False)
    time.sleep(sec)
    off()

#close valve
def close(sec):
    init()
    GPIO.output(16,False)
    GPIO.output(18,True)
    time.sleep(sec)
    off()
    

#print("open")
#open(2)
#print("close")
#close(2)
 
for i in range(0,30):
    #open(1)
    #time.sleep(0.1)
    close(0.9)
    open(0.9)
    #time.sleep(0.1) 
    GPIO.cleanup()
        