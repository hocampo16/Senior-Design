import cv2
from PIL import Image

img = cv2.imread("nir.jpg")
mono = img[:,:,2]

img = mono[800:2500,400:3700]
img = Image.fromarray(img)
img.show()