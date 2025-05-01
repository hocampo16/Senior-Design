import cv2
import numpy as np
from PIL import Image


boostThreshold = 63
boostGain = 30

img = cv2.imread("/home/senior-design/Senior-Design/rgb.jpg")
img = img[:,:,2]
cv2.imwrite("testRGBinput.jpg",img)

#create mask
lessThan = ((img < boostThreshold)).astype(np.uint8)
greaterThan = (img > boostThreshold).astype(np.uint8)

#apply mask
lessThanMasked = (img+(boostGain*np.exp(-6.9/boostThreshold)))*lessThan
greaterThanMasked = img*greaterThan

output = lessThanMasked+greaterThanMasked

cv2.imwrite("testRGBoutput.jpg",output)
Image.fromarray(output).show()

print("done")