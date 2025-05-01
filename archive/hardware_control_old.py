from picamzero import Camera
import time
import RPi.GPIO as GPIO
from PIL import Image
import numpy as np
import cv2
import time
import motor

#setup ==========================================================================================================================
cam = Camera()
    
timestr = time.strftime("%m-%d-%Y_%H%M%S")
LED_PIN = 11
BYPASS_PIN = 7


nirgain = 1 #gain value for NIR image, may not be necessary
rgbgain = 1


def calcNDVI (nir, red):
     top = (nir.astype(float) - red.astype(float))
     bottom = (nir.astype(float) + red.astype(float))
    
     bottom[bottom == 0] = 0.00001
    
     ndvi = top/bottom 
     return ndvi 

#take photos ===================================================================================================================
GPIO.setmode(GPIO.BOARD)    
GPIO.setup(LED_PIN,GPIO.OUT)
GPIO.output(LED_PIN,True)
time.sleep(0.5)
cam.take_photo("nir.jpg")
motor.forward(0.5)
time.sleep(0.5)
cam.take_photo("nirrgb.jpg")
motor.back(0.5)
GPIO.output(LED_PIN,False)

GPIO.cleanup()

#calculating NDVI ===============================================================================================================

#turns images into cv arrays
nir = cv2.imread("nir.jpg")
nirrgb = cv2.imread("nirrgb.jpg")

redband_nirrgb = nirrgb[:,:,2]
#redband_nirrgb = redband_nirrgb[600:2100,700:4000]
redband_nirrgb = (cv2.normalize(redband_nirrgb, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX,dtype=cv2.CV_32F)*255).astype(np.uint8)
cv2.imwrite("NIRRGB_redbands/redband_nirrgb_"+timestr+".jpg",redband_nirrgb)

redband_nir = nir[:,:,2]
#redband_nir = redband_nir[600:2100,700:4000]
redband_nir = (cv2.normalize(redband_nir, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX,dtype=cv2.CV_32F)*255).astype(np.uint8)
gained_nir = np.clip(redband_nir * nirgain, 0, 255).astype(np.uint8)
cv2.imwrite("NIR_redbands/redband_nir_"+timestr+".jpg",gained_nir)

remove_nir = (gained_nir * 1).astype(np.uint8)
redband_rgb = cv2.subtract(redband_nirrgb,remove_nir).astype(np.uint8)
gained_red = np.clip(redband_rgb * rgbgain, 0, 255).astype(np.uint8)
cv2.imwrite("RGB_redbands/redband_rgb_"+timestr+".jpg",redband_rgb) #diagnostic


ndvi_image = calcNDVI (gained_nir,gained_red)

# added code for contrasting set directly towards our image 
ndvi_min = np.min(ndvi_image)
ndvi_max = np.max(ndvi_image)
ndvi_norm = ((ndvi_image +1) /2 *255).astype(np.uint8) #normalizes for outputting images


cv2.imwrite("NDVI_results/ndvi_result"+timestr+".jpg", ndvi_norm)
Image.fromarray(ndvi_norm).show()