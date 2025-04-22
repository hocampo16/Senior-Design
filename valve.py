#valve control

import RPi.GPIO as GPIO
import time 
  
def init():
    GPIO.setmoode(GPIO.BOARD)
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

#close valve
def close():
    init()
    GPIO.output(16,False)
    GPIO.output(18,True)
    off()