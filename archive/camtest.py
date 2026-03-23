from picamera2 import Picamera2, Preview, MappedArray
import time
import RPi.GPIO as GPIO
import cv2
import matplotlib.pyplot as plt
import numpy as np
import servo
import camera

def setAngle(pin, angle):
    duty = angle / 18 + 2
    GPIO.output(pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)  # Time in seconds
    GPIO.output(pin, False)
    pwm.ChangeDutyCycle(0)
    time.sleep(0.5)

pin = 8 #servo gpio pin

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)
pwm = GPIO.PWM(8, 50)
pwm.start(0)

#amera.config("imx708_noir.json", False, False, 0, 66666, 0.42)
tuningFile = "imx708_noir.json"
tuning = Picamera2.load_tuning_file(tuningFile)
picam2 = Picamera2(tuning=tuning)
#image is converted to red in tuning file above (/usr/share/libcamera/ipa/rpi/pisp/imx7008_noir.json) by changing black_level values for green and blue to max     
picam2.configure(picam2.create_preview_configuration())

#control configurations
picam2.set_controls({"AwbEnable": False})
picam2.set_controls({"AeEnable": False})
picam2.set_controls({"Saturation": 0}) #turns image from mono red to b&w
picam2.set_controls({"ExposureTime": 66666, "Brightness":0.42}) #exposuretime = 66666, brightness = 0.42 (brightness = 0.42 is to ensure that the max brightness value is 255


wavelengthSelect = 1 # 0 = Red, 1 = NIR
if wavelengthSelect == 0: #Red
    picam2.set_controls({"Contrast": 2, "AnalogueGain": 3})
    setAngle(pin,10)
    time.sleep(0.5)
elif wavelengthSelect == 1: #NIR
    picam2.set_controls({"Contrast": 3, "AnalogueGain": 12})
    setAngle(pin,180)
    time.sleep(0.5)


picam2.start_preview(Preview.QT)
picam2.start()

time.sleep(0.5)  

picam2.capture_file("test.jpg")
img = cv2.imread("test.jpg")
assert img is not None, "file could not be read, check with os.path.exists()"

img = img[:,:,2] 

mask = np.zeros(img.shape[:2], np.uint8)
mask[700:2050, 580:3400] = 255 

masked_img = cv2.bitwise_and(img,img,mask = mask)
masked_img = masked_img[700:2050, 580:3400]
cv2.imwrite("masktest.jpg", masked_img) 

histr = cv2.calcHist([img],[0],mask,[256],[0,256])
plt.plot(histr)
plt.xlim([0,256])
plt.show()
