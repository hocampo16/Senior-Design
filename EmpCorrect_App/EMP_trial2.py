import cv2 
import numpy as np 
import matplotlib.pyplot as plt 
from scipy.optimize import curve_fit 



image_path = "/home/plant-phenotyping/Senior-Design/EmpCorrect_App/CT3.jpeg"
img = cv2.imread(image_path)




#clockwise direction 
polygons = [ [(25, 25), (250, 25), (250, 250),(25, 250)],#ROI 1
             [(320, 25), (550, 25), (550, 250), (320, 250)], # ROI 2
             [(620, 25), (850, 25), (850, 250), (620, 250)], # ROI 3
             [(25, 300), (250, 300), (250, 550), (25, 550)], # ROI 4
             [(300, 300), (550, 300), (550, 550), (300, 550)], # ROI 5
             [(620, 300), (850, 300), (850, 550), (620, 550)], # ROI 6
             ] 


reflectance_values = [63.59, 66.72, 25.53, 92.69, 16.29, 4.9] 



def extract_roi_and_dn(gray_img, pts):
    mask = np.zeros(img.shape [:2], dtype=np.uint8)
    pts = np.array([pts],dtype=np.int32)
    cv2.fillPoly(mask, pts, 255) 
    masked = cv2.bitwise_and(img, img, mask=mask) 
    mean_dn = float(np.mean(gray_img[mask == 255])) 
    return masked, mean_dn 
 


DN_values = [] 

for i, poly in enumerate(polygons):
    masked,mean_dn = extract_roi_and_dn(img, poly)
    DN_values.append(mean_dn)

    plt.figure(figsize=(3, 3)) 
    plt.title(f"ROI {i+1} Mask") 
    plt.imshow(cv2.cvtColor(masked, cv2.COLOR_BGR2RGB))
    plt.axis("off") 
    plt.show() 
 

print("\nMean DN values:")
print(DN_values) 
 

def line(x, a, b): return a * x + b 

popt, _ = curve_fit(line, DN_values, reflectance_values)
a, b = popt


residuals = np.array(reflectance_values) - line(np.array(DN_values), a, b)
ss_res = np.sum(residuals ** 2)
ss_tot = np.sum((reflectance_values - np.mean(reflectance_values)) ** 2)
R2 = 1 - (ss_res / ss_tot) 

print(f"\nSlope: {a}")
print(f"Intercept: {b}")
print(f"R²: {R2}") 


plt.figure(figsize=(6, 4))
plt.scatter(DN_values, reflectance_values, label="Calibration Targets")
x_line = np.linspace(min(DN_values), max(DN_values), 200)
y_line = line(x_line, a, b)
line_label= f"Linear Regression: y = ({a:.4f})x +({b:.4f}),\nR²={R2:.4f}"

plt.plot(x_line,y_line, label=line_label) 

plt.xlabel("DN (Digital Number)")
plt.ylabel("Reflectance")
#plt.title("Empirical Line Method Calibration")
plt.grid(True)
plt.legend()
plt.show() 

output_file= "DN_ELM_results.txt"

with open (output_file, "w") as f:
    f.write("ROI, Mean DN, Reflectance\n")
    for i, (dn,refls) in enumerate(zip(DN_values, reflectance_values), start =1):
                                   f.write(f"ROI {i}, {dn:.2f},{refls:.3f}\n")
    f.write("\nLinear Regression Line:\n")
    f.write(f"y= {a:.6f}*x +{b:6f}\n")
    f.write(f"R^2 = {R2:.4f}\n")
print(f"Results saved")
                                
 