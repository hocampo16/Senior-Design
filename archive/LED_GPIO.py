import RPi.GPIO as GPIO
import time

LED_PIN = 11;
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_PIN,GPIO.OUT)

GPIO.output(LED_PIN,True)
time.sleep(3)
GPIO.output(LED_PIN,False)
GPIO.cleanup()

print("done")