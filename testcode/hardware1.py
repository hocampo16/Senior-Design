from picamera import PiCamera
import time
import RPi.GPIO as GPIO
from PIL import Image
import numpy as np

# Initialize camera
cam = PiCamera()
GPIO.setmode(GPIO.BOARD)

# Setup GPIO for servo control
GPIO.setup(3, GPIO.OUT)
pwm = GPIO.PWM(3, 50)
pwm.start(0)

# Function to set servo angle
def setAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(3, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)  # Time in seconds
    GPIO.output(3, False)
    pwm.ChangeDutyCycle(0)


    

# Take first photo and move servo
cam.capture("img1.jpg")
time.sleep(1)
setAngle(180)
time.sleep(2)

# Take second photo and reset servo
cam.capture("img2.jpg")
time.sleep(1)
setAngle(0)

# Cleanup GPIO
pwm.stop()
GPIO.cleanup()

# Image processing - convert images to red bands
img1 = Image.open("img1.jpg")
img1 = np.array(img1)
img1[:, :, 1] = 0  # Remove green channel
img1[:, :, 2] = 0  # Remove blue channel
img1 = Image.fromarray(img1)
img1.save("redimg1.jpg")

img2 = Image.open("img2.jpg")
img2 = np.array(img2)
img2[:, :, 1] = 0  # Remove green channel
img2[:, :, 2] = 0  # Remove blue channel
img2 = Image.fromarray(img2)
img2.save("redimg2.jpg")


from PIL import Image
import numpy as np
import cv2

# Save first image
img1 = Image.fromarray(img1)
img1.save('redimg1.jpg')

# Open and process second image
img2 = Image.open("img2.jpg")
img2 = np.array(img2)
img2[:, :, 1] *= 0  # Remove green channel
img2[:, :, 2] *= 0  # Remove blue channel
img2 = Image.fromarray(img2)
img2.save('redimg2.jpg')

# Calculating NDVI
def calcNDVI(nir, red):
    top = nir.astype(float) - red.astype(float)
    bottom = nir.astype(float) + red.astype(float)

    bottom[bottom == 0] = 0.00001  # Avoid division by zero

    ndvi = top / bottom
    return ndvi

# Load images using OpenCV
img1 = cv2.imread("img1.jpg")
img2 = cv2.imread("img2.jpg")

# Extract red and NIR channels
red = img1[:, :, 2]
nir = img2[:, :, 2]

# Compute NDVI
ndvi_image = calcNDVI(nir, red)

# Normalize NDVI to 8-bit scale
ndvi_norm = ((ndvi_image + 1) / 2 * 255).astype(np.uint8)

# Save and display result
cv2.imwrite("ndvi_result.jpg", ndvi_norm)
Image.fromarray(ndvi_norm).show()












