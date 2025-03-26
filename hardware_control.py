from picamzero import Camera
import time
import RPi.GPIO as GPIO
from PIL import Image
import numpy as np
import cv2
import time

#setup ==========================================================================================================================
cam = Camera()
    
timestr = time.strftime("%m-%d-%Y_%H%M%S")

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT)
pwm=GPIO.PWM(3,50)
pwm.start(0)
nirgain = 1 #gain value for NIR image, may not be necessary
rgbgain = 1

def setAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(3,True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1) #time in seconds
    GPIO.output(3,False)
    pwm.ChangeDutyCycle(0)

def calcNDVI (nir, red):
     top = (nir.astype(float) - red.astype(float))
     bottom = (nir.astype(float) + red.astype(float))
    
     bottom[bottom == 0] = 0.00001
    
     ndvi = top/bottom 
     return ndvi 

#take photos ===================================================================================================================
setAngle(0)
time.sleep(1)
cam.take_photo("nir.jpg")
setAngle(150)
time.sleep(4)
cam.take_photo("nirrgb.jpg")
setAngle(0)

#GPIO cleaning, put this after you are done using GPIO code
pwm.stop()
GPIO.cleanup()


#calculating NDVI ===============================================================================================================

#turns images into cv arrays
nir = cv2.imread("nir.jpg")
nirrgb = cv2.imread("nirrgb.jpg")

redband_nirrgb = nirrgb[:,:,2]
redband_nirrgb = (cv2.normalize(redband_nirrgb, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX,dtype=cv2.CV_32F)*255).astype(np.uint8)
cv2.imwrite("NIRRGB_redbands/redband_nirrgb_"+timestr+".jpg",redband_nirrgb)

redband_nir = nir[:,:,2]
redband_nir = (cv2.normalize(redband_nir, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX,dtype=cv2.CV_32F)*255).astype(np.uint8)
#redband_nir = (np.sqrt(cv2.normalize(redband_nir, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX,dtype=cv2.CV_32F))*255).astype(np.uint8)
gained_nir = np.clip(redband_nir * nirgain, 0, 255).astype(np.uint8)
cv2.imwrite("NIR_redbands/redband_nir_"+timestr+".jpg",gained_nir)

remove_nir = (gained_nir * 1).astype(np.uint8)
redband_rgb = cv2.subtract(redband_nirrgb,remove_nir)
gained_red = np.clip(redband_rgb * rgbgain, 0, 255).astype(np.uint8)
cv2.imwrite("RGB_redbands/redband_rgb_"+timestr+".jpg",redband_rgb) #diagnostic


ndvi_image = calcNDVI (gained_nir,gained_red)

# added code for contrasting set directly towards our image 
ndvi_min = np.min(ndvi_image)
ndvi_max = np.max(ndvi_image)
#ndvi_norm = ((ndvi_image - ndvi_min) / (ndvi_max - ndvi_min) * 255).astype(np.uint8)
ndvi_norm = ((ndvi_image +1) /2 *255).astype(np.uint8) #normalizes for outputting images

## could also try the code below if we want to clip our image to the general min and max of -1 and 1 
##Define expected NDVI range (typically -1 to 1)
#ndvi_min_expected = -1
#ndvi_max_expected = 1

## Clip NDVI values 
#ndvi_clipped = np.clip(ndvi_image, ndvi_min_expected, ndvi_max_expected)
#ndvi_norm = ((ndvi_clipped - ndvi_min_expected) / (ndvi_max_expected - ndvi_min_expected) * 255).astype(np.uint8)

cv2.imwrite("NDVI_results/ndvi_result"+timestr+".jpg", ndvi_norm)
Image.fromarray(ndvi_norm).show()