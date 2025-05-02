from PIL import Image
import numpy as np
import cv2
import time
import ndvi

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

timeStr = time.strftime("%m-%d-%Y_%H%M%S")

boostThresholdRedBand = 63
boostGainRedBand = 30

nir = ndvi.monoImg("supplemental_files/nir.jpg",True,"nir_photos/nir_", timeStr)
red = ndvi.monoImg("supplemental_files/rgb.jpg",True,"red_photos/rgb_", timeStr, True,boostThresholdRedBand,boostGainRedBand)

ndvi_image = ndvi.calcNDVI (nir,red)


colors = ["#0017ff","#d5a22b","#2aff00"]
custom_cmap = LinearSegmentedColormap.from_list("custom_cmap",colors)

plt.imshow(ndvi_image, cmap = custom_cmap)
plt.colorbar()
plt.show()