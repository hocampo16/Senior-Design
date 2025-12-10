import time
import RPi.GPIO as GPIO

def setAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(8, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)  # Time in seconds
    GPIO.output(8, False)
    pwm.ChangeDutyCycle(0)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.OUT)
pwm = GPIO.PWM(8, 50)
pwm.start(0)

#servo goes from 10 to 180

setAngle(10)
time.sleep(1)

# setAngle(180)
# time.sleep(1)