from picamzero import Camera
import time
import RPi.GPIO as GPIO
from PIL import Image
import numpy as np
import cv2
import os

import motor
import ndvi
import maskingNDVI

#user Variables ==========================================================================================================================

#only used when 
boostThresholdRedBand = 63
boostGainRedBand = 30

#take photos ===================================================================================================================
LED_PIN = 11
timeStr = time.strftime("%m-%d-%Y_%H%M%S")
cam = Camera()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_PIN,GPIO.OUT)

GPIO.output(LED_PIN,True)
time.sleep(0.2)
cam.take_photo("nir.jpg")
GPIO.output(LED_PIN,False)
print("motor forward")
motor.forward(0.5)
time.sleep(4)
cam.take_photo("rgb.jpg")
print("motor back")
motor.back(0.5)

GPIO.cleanup()

#calculating NDVI ===============================================================================================================

#turns images into cv arrays

nir = ndvi.monoImg("supplementalCodeFiles/nir.jpg",True,"nir_photos/nir", timeStr)
red = ndvi.monoImg("supplementalCodeFiles/rgb.jpg",True,"red_photos/rgb", timeStr, True,boostThresholdRedBand,boostGainRedBand)
#monoRGB = ndvi.monoImg("supplementalCodeFiles/rgb.jpg",True,"RGB_mono/RGB_mono", timeStr)

ndvi_image = ndvi.calcNDVI (nir,red)
ndvi_norm = ((ndvi_image +1) /2 *255).astype(np.uint8) #normalizes for outputting images

cv2.imwrite("NDVI_results/ndvi_result"+timeStr+".jpg", ndvi_norm)
Image.fromarray(ndvi_norm).show()

#masking images===================================================================================================================

dir_name = "/home/senior-design/Senior-Design/NDVI_results"
output_folder = "/home/senior-design/Senior-Design/Masking_Images"
txt_path = os.path(output_folder,"Masking_%.txt")

maskingNDVI.masking_ndvi(dir_name, output_folder, txt_path) 