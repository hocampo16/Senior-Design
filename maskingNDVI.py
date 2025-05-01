import cv2
import numpy as np
from PIL import Image
import time
import pandas as pd
import os

def masking_ndvi(dir_name, output_folder, txt_path):
    
    extension = ('.png', '.jpg', '.jpeg')

    # If txt file doesn't exist, create it with headers
    if not os.path.exists(txt_path):
        with open(txt_path, "w") as f:
            f.write("Filename\tPlant Coverage (%)\tStressed Area (%)\n")

    # Scanning the directory to get required files
    for files in os.scandir(dir_name):
        if files.path.lower().endswith(extension):
            image_path = files.path

        # Load the normalized NDVI image (0–255 grayscale)
            ndvi_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        
            if ndvi_image is None:
                print(f"Warning:Could not read path {image_path}. Skipping")
                continue 
            base_filename = os.path.splitext(os.path.basename(image_path))[0]

            # Convert pixel values back to NDVI range (-1 to 1)
            ndvi_scaled = (ndvi_image.astype(np.float32) / 255) * 2 - 1

            # Thresholds
            plant_threshold = 0.4  # "plant"
            stress_threshold = 0.6  # "stressed"

            # Create masks
            plant_mask = (ndvi_scaled > plant_threshold).astype(np.uint8)
            stress_mask = (ndvi_scaled < stress_threshold).astype(np.uint8)

            # Combine masks to get stressed plants only
            stressed_plant_mask = cv2.bitwise_and(plant_mask, stress_mask)

            # Convert to displayable format (black or white)
            plant_mask_display = plant_mask * 255
            stressed_plant_display = stressed_plant_mask * 255

            # Calculate percentages
            total_pixels = ndvi_image.size
            plant_pixels = np.count_nonzero(plant_mask)
            stressed_plant_pixels = np.count_nonzero(stressed_plant_mask)

            plant_percent = (plant_pixels / total_pixels) * 100
            stress_percent_within_plants = (stressed_plant_pixels / plant_pixels) * 100 if plant_pixels > 0 else 0

            # Save mask images
            cv2.imwrite(os.path.join(output_folder, base_filename + "_plant_mask_result.png"), plant_mask_display)
            cv2.imwrite(os.path.join(output_folder, base_filename + "_stressed_plant_mask_result.png"), stressed_plant_display)

            # Save the results to the txt file
            with open(txt_path, "a") as f:
                f.write(f"{base_filename}\t{plant_percent:.2f}\t{stress_percent_within_plants:.2f}\n")

dir_name = "/home/senior-design/Senior-Design/NDVI_results"
output_folder = "/home/senior-design/Senior-Design/Masking_Images"
txt_path = os.path(output_folder,"Masking_%.txt")

maskingNDVI.masking_ndvi(dir_name, output_folder, txt_path) 