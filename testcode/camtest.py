from picamzero import Camera
from PIL import Image
import cv2
import numpy as np

cam = Camera()
cam.take_photo("helloworld.jpg")
im = cv2.imread("helloworld.jpg")
im = im[:,:,2]
im = im[600:2100,700:4000]
print(np.max(im))
print(np.min(im))
#Image.fromarray(im).show()

#norm = (cv2.normalize(im, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX,dtype=cv2.CV_32F)*255).astype(np.uint8)
norm = (np.cbrt(cv2.normalize(im, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX,dtype=cv2.CV_32F))*255).astype(np.uint8)
Image.fromarray(norm).show()

diff = cv2.subtract(norm,im)
#Image.fromarray(diff).show()