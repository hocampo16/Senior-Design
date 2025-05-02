import cv2
import numpy as np

#NDVI calculation
def calcNDVI (nir, red):
     top = (nir.astype(float) - red.astype(float))
     bottom = (nir.astype(float) + red.astype(float))
    
     bottom[bottom == 0] = 0.000001
    
     ndvi = top/bottom 
     return ndvi

#turns images into usable data for NDVI
def monoImg (inputFile, gain = 1, outputName = "img", timeStr = "", doMask = False, boostThreshold = 0, boostGain = 1):
    img = cv2.imread(inputFile)

    monoImg = img[:,:,2] #gets only red band of photos
    monoImg = monoImg[800:2500,400:3700] #crops image
    
    #apply flat gain to image
    if gain != 1:
        monoImg = np.clip(monoImg * gain, 0, 255).astype(np.uint8)
    
    #boost lower values of image
    if(doMask):
        lessThan = ((monoImg < boostThreshold)).astype(np.uint8)
        greaterThan = (monoImg > boostThreshold).astype(np.uint8)
        lessThanMasked = (monoImg+(boostGain * np.exp(-6.9 / boostThreshold))) * lessThan
        greaterThanMasked = monoImg * greaterThan
        monoImg = lessThanMasked + greaterThanMasked
        
    cv2.imwrite(outputName + timeStr + ".jpg", monoImg) #create jpg from processed image
    return monoImg