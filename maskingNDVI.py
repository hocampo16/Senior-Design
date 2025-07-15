import cv2
import numpy as np
from PIL import Image
import os

def mask(ndvi, plant_threshold, stress_threshold, dir_name, output_folder, time_str):

    txt_path = "supplemental_files/Masking_%.txt"
    # If txt file doesn't exist, create it with headers
    if not os.path.exists(txt_path):
        with open(txt_path, "w") as f:
            f.write("Filename\tPlant Coverage (%)\tStressed Area (%)\n")
    
    # Create masks
    plant_mask = (ndvi > plant_threshold).astype(np.uint8)
    stress_mask = (ndvi < stress_threshold).astype(np.uint8)

    # Combine masks to get stressed plants only
    stressed_plant_mask = cv2.bitwise_and(plant_mask, stress_mask)

    # Convert to displayable format (black or white)
    plant_mask_display = (plant_mask * 255).astype(np.uint8)
    stressed_plant_display = (stressed_plant_mask * 255).astype(np.uint8)

    # Calculate percentages
    total_pixels = ndvi.size
    plant_pixels = np.count_nonzero(plant_mask)
    stressed_plant_pixels = np.count_nonzero(stressed_plant_mask)
    
    plant_percent = (plant_pixels / total_pixels) * 100
    stress_percent_within_plants = (stressed_plant_pixels / plant_pixels) * 100 if plant_pixels > 0 else 0
    
    # Save mask images
    cv2.imwrite(os.path.join("Masking_Images/plant_mask_result_"+ time_str +".jpg"), plant_mask_display)
    cv2.imwrite(os.path.join("Masking_Images/stressed_plant_mask_result_"+ time_str +".jpg"), stressed_plant_display)

    # Save the results to the txt file
    with open(txt_path, "a") as f:
        f.write(f"ndvi_result_{time_str}\t{plant_percent:.2f}\t{stress_percent_within_plants:.2f}\n")

    return stress_percent_within_plants
