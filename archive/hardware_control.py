from picamzero import Camera
import time
import RPi.GPIO as GPIO
from PIL import Image
import numpy as np
import cv2

import motor
import ndvi

#setup ==========================================================================================================================

cam = Camera()
timestr = time.strftime("%m-%d-%Y_%H%M%S")
LED_PIN = 11
nirgain = 1
rgbgain = 1

boostThreshold = 63
boostGain = 30

#take photos ===================================================================================================================

GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_PIN,GPIO.OUT)

GPIO.output(LED_PIN,True)
time.sleep(0.2)
cam.take_photo("nir.jpg")
GPIO.output(LED_PIN,False)
motor.forward(0.5)
time.sleep(4)
cam.take_photo("rgb.jpg")
motor.back(0.5)

GPIO.cleanup()

#calculating NDVI ===============================================================================================================

#turns images into cv arrays
nir = cv2.imread("nir.jpg")
rgb = cv2.imread("rgb.jpg")

redband_rgb = rgb[:,:,2]
gained_red = np.clip(redband_rgb * rgbgain, 0, 255).astype(np.uint8)
lessThan = ((gained_red < boostThreshold)).astype(np.uint8)
greaterThan = (gained_red > boostThreshold).astype(np.uint8)
lessThanMasked = (gained_red+(boostGain*np.exp(-6.9/boostThreshold)))*lessThan
greaterThanMasked = gained_red*greaterThan
gained_red = lessThanMasked+greaterThanMasked
cv2.imwrite("RGB_redbands/redband_rgb_"+timestr+".jpg",gained_red)

redband_nir = nir[:,:,2]
gained_nir = np.clip(redband_nir * nirgain, 0, 255).astype(np.uint8)
cv2.imwrite("NIR_redbands/redband_nir_"+timestr+".jpg",gained_nir)

ndvi_image = ndvi.calcNDVI (gained_nir,gained_red)

# added code for contrasting set directly towards our image 
ndvi_min = np.min(ndvi_image)
ndvi_max = np.max(ndvi_image)
ndvi_norm = ((ndvi_image +1) /2 *255).astype(np.uint8) #normalizes for outputting images

cv2.imwrite("NDVI_results/ndvi_result"+timestr+".jpg", ndvi_norm)
Image.fromarray(ndvi_norm).show()