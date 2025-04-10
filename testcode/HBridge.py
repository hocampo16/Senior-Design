import RPi.GPIO as GPIO
import time

def init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(13,GPIO.OUT)
    GPIO.setup(15,GPIO.OUT)

def off():
    init()
    GPIO.output(13,False)
    GPIO.output(15,False)
    GPIO.cleanup()
    
def forward(sec):
    init()
    GPIO.output(13,True)
    GPIO.output(15,False)
    time.sleep(sec)
    GPIO.cleanup()
    off()
    
def back(sec):
    init()
    GPIO.output(13,False)
    GPIO.output(15,True)
    time.sleep(sec)
    GPIO.cleanup()
    off()

off()
for i in range (100):
    back(0.5)
    time.sleep(0.5)
    forward(0.4)
    time.sleep(0.5)


# init()
# GPIO.output(15,True)
# print("forward")
# 
# time.sleep(3)
# GPIO.output(15,False)
# print("backward")