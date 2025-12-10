from picamera2 import Picamera2, Preview, MappedArray
import time
import RPi.GPIO as GPIO
import numpy as np
import cv2
from matplotlib import pyplot as plt


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
#camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
picam2.configure(picam2.create_still_configuration())
picam2.start()

#control configurations
picam2.set_controls({"AwbEnable": False})
picam2.set_controls({"AeEnable": False})
picam2.set_controls({"Saturation": 0}) #turns image from mono red to b&w
picam2.set_controls({"Contrast": 2, "Brightness":0.42}) #Brightness = 0.42 ensures that image can go up to 255


wl = 1 # 0 = Red, 1 = NIR
if wl == 0: #Red
    picam2.set_controls({"ExposureTime": 66666, "AnalogueGain": 5})
    setAngle(10)
    time.sleep(0.5)
elif wl == 1: #NIR
    picam2.set_controls({"ExposureTime": 66666, "AnalogueGain": 30})
    setAngle(180)
    time.sleep(0.5)

picam2.capture_file("test.jpg")
img = cv2.imread("test.jpg")
assert img is not None, "file could not be read, check with os.path.exists()"
img = img[:,:,2] #gets only red band of photos


mask = np.zeros(img.shape[:2], np.uint8)
mask[700:2050, 580:3400] = 255 #defining pixels mask will effect here
masked_img = cv2.bitwise_and(img,img,mask = mask)
masked_img = masked_img[700:2050, 580:3400]
cv2.imwrite("masktest.jpg", masked_img) #diagnostic image of mask

histr = cv2.calcHist([img],[0],mask,[256],[0,256])
plt.plot(histr)
plt.xlim([0,256])

plt.show()