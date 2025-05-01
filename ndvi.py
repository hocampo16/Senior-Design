import cv2
import numpy as np


def calcNDVI (nir, red):
     top = (nir.astype(float) - red.astype(float))
     bottom = (nir.astype(float) + red.astype(float))
    
     bottom[bottom == 0] = 0.000001
    
     ndvi = top/bottom 
     return ndvi

def monoImg (inputFile, createOutput = False, outputName = "monoImg", timeStr = "", doMask = False, boostThreshold = 255, boostGain = 1):
    img = cv2.imread(inputFile)

    monoImg = img[:,:,2]
    if(doMask):
        lessThan = ((monoImg < boostThreshold)).astype(np.uint8)
        greaterThan = (monoImg > boostThreshold).astype(np.uint8)
        lessThanMasked = (monoImg+(boostGain*np.exp(-6.9/boostThreshold)))*lessThan
        greaterThanMasked = monoImg*greaterThan
        monoImg = lessThanMasked+greaterThanMasked
    cv2.imwrite(outputName+timeStr+".jpg",monoImg)
    return monoImg