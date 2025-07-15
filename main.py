from picamzero import Camera
import time
import RPi.GPIO as GPIO
import numpy as np
import cv2
import os
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
matplotlib.use('Agg')
from PIL import Image
import threading

import motor
import ndvi
import maskingNDVI
import irrigation

refreshRate = 4*60*60 #how often code should run (in seconds) [CURRENTLY RUNS EVERY 6HRS]

def mainCode():

    #USER VARIABLES ==========================================================================================================================

    #NOTE: all defaults can still be tweaked if better values work! They are just the best that I could find as of May 1st

    #flat gain values for images
    nirGain = 2.5 #default 1.75
    rgbGain = 0.5 #default 1

    #exponential boost to lower values of red band image
    #this fixes problem where soil is too dark
    boostThresholdRedBand = 1 #default 63
    boostGainRedBand = 1 #default 1 (or 30)

    #threshold values for determining what is is a plant, and how stressed they are from NDVI values (should be 0-1)
    plantThreshold = 0.1 #default 0.1
    stressThreshold = 0.25 #default 0.1

    #TAKE PHOTOS ===================================================================================================================

    LED_PIN = 11
    cam = Camera()
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LED_PIN,GPIO.OUT)

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
    cv2.imwrite("NDVI_time_data/ndvi_result_"+timeStr+".jpg",ndvi_norm)

    #turn into heatmap with collors corresponding to NDVI value refs
    
#     colors = ["#0017ff","#d5a22b","#2aff00"]
#     custom_cmap = LinearSegmentedColormap.from_list("custom_cmap",colors)
#     plt.imshow(ndvi_image, cmap = custom_cmap, vmin = -1, vmax = 1)
#     plt.colorbar()
#     plt.savefig("NDVI_time_data/ndvi_result_"+timeStr+".jpg",bbox_inches = "tight", dpi = 1000)
#     plt.close('all')

    #MASK IMAGES ===================================================================================================================

    dir_name = "/home/senior-design/Senior-Design/NDVI_results"
    output_folder = "/home/senior-design/Senior-Design/Masking_Images"
    txt_path = "Masking_%.txt"

    mask = maskingNDVI.mask(ndvi_image, plantThreshold, stressThreshold, dir_name, output_folder, timeStr)


    #IRRIGTION CODE==================================================================================================

    # print(mask)
    # if mask > 50:
    #     print("Irrigation needed")
    #     irrigation.open(3)
    #     time.sleep(5)
    #     irrigation.close(3)
    # else:
    #     print("Irrigation not needed")
    # GPIO.cleanup()

    #FINISHING CODE =================================================================================================================

    # plantImg = Image.open("Masking_Images/plant_mask_result_"+ timeStr +".jpg")
    # stressImg = Image.open("Masking_Images/stressed_plant_mask_result_"+ timeStr +".jpg")
    # 
    # print("done")
    # 
    # plt.show()
    # stressImg.show()
    # plantImg.show()
    
def run_threaded(func):
    job_thread = threading.Thread(target = func)
    job_thread.start()
    

while 1:
    run_threaded(mainCode)
    time.sleep(refreshRate)

# mainCode()


