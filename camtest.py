from picamera2 import Picamera2, Preview, MappedArray
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


tuning = Picamera2.load_tuning_file("imx708_noir.json")
picam2 = Picamera2(tuning=tuning)
#image is converted to red in tuning file above (/usr/share/libcamera/ipa/rpi/pisp/imx7008_noir.json) by changing black_level values for green and blue to max     
picam2.configure(picam2.create_preview_configuration())

#control configurations
picam2.set_controls({"AwbEnable": False})
picam2.set_controls({"AeEnable": False})
picam2.set_controls({"Saturation": 0}) #turns image from mono red to b&w
picam2.set_controls({"ExposureTime": 66666, "Brightness":0.42}) #exposuretime = 66666, brightness = 0.42 (brightness = 0.42 is to ensure that the max brightness value is 255


wl = 1 # 0 = Red, 1 = NIR
if wl == 0: #Red
    picam2.set_controls({"Contrast": 2, "AnalogueGain": 1})
    setAngle(10)
    time.sleep(0.5)
elif wl == 1: #NIR
    picam2.set_controls({"Contrast": 3, "AnalogueGain": 5})
    setAngle(180)
    time.sleep(0.5)


picam2.start_preview(Preview.QT)
picam2.start()