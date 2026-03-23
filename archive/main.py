from picamzero import Camera
import time
import RPi.GPIO as GPIO
import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

import motor
import ndvi
import maskingNDVI


#USER VARIABLES ==========================================================================================================================

#NOTE: all defaults can still be tweaked if better values work! They are just the best that I could find as of May 1st

#flat gain values for images
nirGain = 1.75 #default 1.75
rgbGain = 1 #default 1

#exponential boost to lower values of red band image
#this fixes problem where soil is too dark
boostThresholdRedBand = 63 #default 63
boostGainRedBand = 30 #default 1

#threshold values for determining what is is a plant, and how stressed they are from NDVI values (should be 0-1)
plantThreshold = 0.1 #default 0.1
stressThreshold = 0.2 #default 0.1

#TAKE PHOTOS ===================================================================================================================

LED_PIN = 11
cam = Camera()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_PIN,GPIO.OUT)

#everything below this comment should be included in a while(1) loop that runs once every hour
timeStr = time.strftime("%m-%d-%Y_%H%M%S")

#protocol for taking images
GPIO.output(LED_PIN,True)
time.sleep(0.2)
cam.take_photo("supplemental_files/nir.jpg")
GPIO.output(LED_PIN,False)
motor.forward(0.4)
time.sleep(4)
cam.take_photo("supplemental_files/rgb.jpg")
motor.back(0.4)

GPIO.cleanup()

#CALCULATE NDVI ===============================================================================================================

#image preprocessing
nir = ndvi.monoImg("supplemental_files/nir.jpg", nirGain, "nir_photos/nir_", timeStr)
red = ndvi.monoImg("supplemental_files/rgb.jpg", rgbGain, "red_photos/rgb_", timeStr, True, boostThresholdRedBand, boostGainRedBand)
#red = ndvi.monoImg("supplemental_files/rgb.jpg",True,"red_photos/rgb", timeStr)

#calculate NDVI for image
ndvi_image = ndvi.calcNDVI (nir,red)
ndvi_norm = ((ndvi_image +1) /2 *255).astype(np.uint8) #normalizes for outputting images

#turn into heatmap with collors corresponding to NDVI value refs
colors = ["#0017ff","#d5a22b","#2aff00"]
custom_cmap = LinearSegmentedColormap.from_list("custom_cmap",colors)
plt.imshow(ndvi_image, cmap = custom_cmap, vmin = -1, vmax = 1)
plt.colorbar()
plt.savefig("NDVI_results/ndvi_result_"+timeStr+".jpg",bbox_inches = "tight", dpi = 1000)

#MASK IMAGES ===================================================================================================================

dir_name = "/home/senior-design/Senior-Design/NDVI_results"
output_folder = "/home/senior-design/Senior-Design/Masking_Images"
txt_path = "Masking_%.txt"

maskingNDVI.mask(ndvi_image, plantThreshold, stressThreshold, dir_name, output_folder, timeStr)


#FINISHING CODE =================================================================================================================
print("done")
plt.show()