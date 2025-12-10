import cv2 
import numpy as np 
import matplotlib.pyplot as plt 
from scipy.optimize import curve_fit 

image_path= "/home/plant-phenotyping/Senior-Design/EmpCorrect_App/CT3.jpeg"
img= cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

polygons = [
	[(50,60),(80,60),(80,90),(50,90)],
	[(120,40),(160,40),(160,80),(120,80)],
	[(200,100),(240,100),(240,140),(200,140)],
	[(300,150),(340,150),(340,190),(300,190)],
	[(400,200),(440,200),(440,240),(400,240)],
	[(500,250),(540,250),(540,290),(500,290)]]

ref_vals= [0.03,0.12,0.25,0.35,0.50,0.80] 

def ext_mean_dn(gray_img,pts):
	mask = (np.zeros(gray_img.shape, dtype=np.uint8))
	pts = np.array([pts], dtype=np.int32)
	cv2.fillPoly(mask, pts,255)
	return float (np.mean(gray_img[mask == 255]))

DN_vals= [ext_mean_dn(img, poly) for poly in polygons]

print ("Mean DN values:", DN_vals)

def line (x,a,b):
	return a*x+b

popt, _ = curve_fit(line, DN_vals, ref_vals)
a, b = popt

res= np.array(ref_vals - line(np.array(DN_vals), a,b))
ss_res= np.sum(res**2)
ss_tot = np.sum(ref_vals - np.mean(ref_vals))**2
R2= 1 -(ss_res / ss_tot) 

print (f"\nGain (slope): {a}")
print ( f"Offest (intercept): {b} ")
print (f"R^2:{R2}")


plt.scatter (DN_vals, ref_vals, label ="Data")
x_line = np.linspace(min(DN_vals), max (DN_vals), 100)
plt.plot(x_line,line(x_line, a,b) , label = f"Fit (R^2={R2:.4f}0")
plt.xlabel("DN")
plt.ylabel("Reflectance")
plt.title("ELM Calibration Curve")
plt.legend()
plt.grid(True)
plt.show 



