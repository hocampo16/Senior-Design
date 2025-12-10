import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os
from glob import glob

image_folder = "/home/plant-phenotyping/Senior-Design/EmpCorrect_App"
graph_folder= "/home/plant-phenotyping/Senior-Design/EmpCorrect_App/output_EMP"
os.makedirs(graph_folder, exist_ok=True)



output_file = "DN_ELM_results.txt"

# ROIs (same clockwise rectangles)
polygons = [
    [(25, 25), (250, 25), (250, 250), (25, 250)],        # ROI 1
    [(320, 25), (550, 25), (550, 250), (320, 250)],      # ROI 2
    [(620, 25), (850, 25), (850, 250), (620, 250)],      # ROI 3
    [(25, 300), (250, 300), (250, 550), (25, 550)],      # ROI 4
    [(300, 300), (550, 300), (550, 550), (300, 550)],    # ROI 5
    [(620, 300), (850, 300), (850, 550), (620, 550)],    # ROI 6
]

# Known reflectances
reflectance_values = [63.59, 66.72, 25.53, 92.69, 16.29, 4.9]


def extract_dn(img, pts):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mask = np.zeros(gray.shape, dtype=np.uint8)
    pts = np.array([pts], dtype=np.int32)
    cv2.fillPoly(mask, pts, 255)
    mean_dn = float(np.mean(gray[mask == 255]))
    return mean_dn


def line(x, a, b):
    return a * x + b


# Clear previous file
open(output_file, "w").close()

# Process all images in folder
image_list = glob(os.path.join(image_folder, "*.jpg")) + \
             glob(os.path.join(image_folder, "*.jpeg")) + \
             glob(os.path.join(image_folder, "*.png"))

for image_path in image_list:
    img_name = os.path.basename(image_path)
    img = cv2.imread(image_path)

    if img is None:
        print(f"Could not read {img_name}, skipping...")
        continue

    print(f"\nProcessing {img_name}...")

    # Extract DN values
    DN_values = [extract_dn(img, poly) for poly in polygons]

    # Fit linear regression (ELM)
    popt, _ = curve_fit(line, DN_values, reflectance_values)
    a, b = popt

    residuals = np.array(reflectance_values) - line(np.array(DN_values), a, b)
    ss_res = np.sum(residuals ** 2)
    ss_tot = np.sum((reflectance_values - np.mean(reflectance_values)) ** 2)
    R2 = 1 - (ss_res / ss_tot)

    # Save calibration graph 
    plt.figure(figsize=(6, 4))
    plt.scatter(DN_values, reflectance_values, label="Calibration Targets")

    x_line = np.linspace(min(DN_values), max(DN_values), 200)
    y_line = line(x_line, a, b)
    plt.plot(x_line, y_line,
             label=f"Linear Regression: y = {a:.4f}x + {b:.4f}\nR² = {R2:.4f}")

    plt.xlabel("DN")
    plt.ylabel("Reflectance")
    plt.grid(True)
    plt.legend()

    plot_filename = os.path.join(graph_folder, f"calibration_graph_{img_name}.png")
    plt.savefig(plot_filename, dpi=300)
    plt.close()

    #Save results to TXT
    with open(output_file, "a") as f:
        f.write(f"\n=== {img_name} ===\n")
        f.write("ROI, Mean DN, Reflectance\n")
        for i, (dn, refl) in enumerate(zip(DN_values, reflectance_values), start=1):
            f.write(f"ROI {i}, {dn:.3f}, {refl:.3f}\n")
        f.write(f"\nLinear Regression: y = {a:.6f}x + {b:.6f}\n")
        f.write(f"R² = {R2:.6f}\n")
        f.write("\n-----------------------------------------\n")

print("\nProcessing complete. All results saved!")
