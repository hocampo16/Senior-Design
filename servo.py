import time
import RPi.GPIO as GPIO


def setAngle(pin, angle):
    #servo setup
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    pwm = GPIO.PWM(8, 50)
    pwm.start(0)
    
    duty = angle / 18 + 2
    GPIO.output(pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(pin, False)
    pwm.ChangeDutyCycle(0)
    time.sleep(0.5)
    
    GPIO.cleanup()