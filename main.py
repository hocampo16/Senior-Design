from picamera2 import Picamera2, Preview, MappedArray
import time
import RPi.GPIO as GPIO
import cv2
import matplotlib.pyplot as plt
import numpy as np

import camera
import servo

pc2 = camera.config("imx708_noir.json", False, False, 0, 66666, 0.42)
camera.takePhoto(pc2, wavelengthSelect = 0, showPreview = True, pin = 8, output = "testing.jpg") # 0 = Red, 1 = NIR