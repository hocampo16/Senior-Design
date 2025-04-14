import cv2
import numpy as np
from PIL import Image

# Load the normalized NDVI image (0–255 grayscale)
ndvi_image = cv2.imread("/Users/hannahocampo/Desktop/OneDrive_1_4-6-2025/NDVI_Result_Trial.png", cv2.IMREAD_GRAYSCALE)

# Convert pixel values back to NDVI range (-1 to 1)
ndvi_scaled = (ndvi_image.astype(np.float32) / 255) * 2 - 1

# Thresholds
plant_threshold = 0.79       # NDVI above this is considered "plant"
stress_threshold = 0.7      # NDVI below this is considered "stressed"
#healthy_threshold = 0.7     # Optional: for defining super-healthy plants

# Create masks
plant_mask = (ndvi_scaled > plant_threshold).astype(np.uint8)
stress_mask = (ndvi_scaled < stress_threshold).astype(np.uint8)

# Combine masks to get stressed plants only
stressed_plant_mask = cv2.bitwise_and(plant_mask, stress_mask)

# Convert to displayable format (0 or 255)
plant_mask_display = plant_mask * 255
stressed_plant_display = stressed_plant_mask * 255

# Calculate percentages
total_pixels = ndvi_image.size
plant_pixels = np.count_nonzero(plant_mask)
stressed_plant_pixels = np.count_nonzero(stressed_plant_mask)

plant_percent = (plant_pixels / total_pixels) * 100
stress_percent_within_plants = (stressed_plant_pixels / plant_pixels) * 100 if plant_pixels > 0 else 0

# Print results
print(f"Total plant area: {plant_percent:.2f}%")
print(f"Stressed plant area (within plant regions): {stress_percent_within_plants:.2f}%")

# Save result images
cv2.imwrite("plant_mask_result.png", plant_mask_display)
cv2.imwrite("stressed_plant_mask_result.png", stressed_plant_display)

# Show the images
Image.fromarray(plant_mask_display).show()
Image.fromarray(stressed_plant_display).show()
