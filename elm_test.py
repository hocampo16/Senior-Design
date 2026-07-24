import numpy as np
import matplotlib as plt
import cv2

sensor_white = 140
sensor_gray = 45
sensor_black = 8.4

sensor = [sensor_white, sensor_gray, sensor_black]

#NOTE: all test images are taken in red band
photos = ["testing_white.jpg", "testing_gray.jpg", "testing_black.jpg"]
avg = np.zeros(3)
i = 0

for x in photos:
    
    img = cv2.imread(x)
    cropped_img = img[80:420, 60:580]
    cropped_img = cropped_img[:,:,0]
    avg[i] = np.average(cropped_img)
    i = i + 1

print(avg)

slope_intercept = np.polyfit(avg, sensor, 1)
#print(slope_intercept[0])
#print(slope_intercept[1])
output = cv2.imread(photos[2])
output = cv2.multiply(output, slope_intercept[0])
output = cv2.add(output, slope_intercept[1])
#cv2.imwrite("elm_test_output.jpg", output)



                 
cv2.imshow("Image", output)
cv2.waitKey(0)
#cv2.destroyAllWindows()