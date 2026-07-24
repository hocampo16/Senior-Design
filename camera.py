from picamera2 import Picamera2, Preview, MappedArray
import servo
import time
import cv2
import os

def config(tuningFile,AwB,Ae,Saturation,ExposureTime,Brightness):
    
    os.environ["LIBCAMERA_LOG_LEVELS"] = "3" #dusables log in shell unless there is an error
    
    tuning = Picamera2.load_tuning_file(tuningFile)
    picam2 = Picamera2(tuning=tuning)
    #image is converted to red in tuning file above (/usr/share/libcamera/ipa/rpi/pisp/imx7008_noir.json) by changing black_level values for green and blue to max     
    picam2.configure(picam2.create_preview_configuration())

    #control configurations
    picam2.set_controls({"AwbEnable": False})
    picam2.set_controls({"AeEnable": False})
    picam2.set_controls({"Saturation": 0}) #turns image from mono red to b&w
    picam2.set_controls({"ExposureTime": 66666})
    picam2.set_controls({"Brightness":0.42})#exposuretime = 66666, brightness = 0.42 (brightness = 0.42 is to ensure that the max brightness value is 255
    return picam2

def takePhoto(picam2, wavelengthSelect,showPreview, pin, output):
    
    
    # 0 = Red, 1 = NIR
    if wavelengthSelect == 0: #Red
        picam2.set_controls({"Contrast": 2})
        picam2.set_controls({"AnalogueGain": 3})
        servo.setAngle(pin,18)
        #wl = red
    elif wavelengthSelect == 1: #NIR
        picam2.set_controls({"Contrast": 2})
        picam2.set_controls({"AnalogueGain": 12})
        servo.setAngle(pin,180)
        #wl = nir
        
    
    
    if(showPreview):
        picam2.start_preview(Preview.QT)
        picam2.start()
        time.sleep(0.5)  

    
    picam2.capture_file(output)
    img = cv2.imread(output)
    assert img is not None, "file could not be read, check with os.path.exists()"

    '''img = img[:,:,2] 

    mask = np.zeros(img.shape[:2], np.uint8)
    mask[700:2050, 580:3400] = 255 

    masked_img = cv2.bitwise_and(img,img,mask = mask)
    masked_img = masked_img[700:2050, 580:3400]
    cv2.imwrite("masktest.jpg", masked_img) 

    histr = cv2.calcHist([img],[0],mask,[256],[0,256])
    plt.plot(histr)
    plt.xlim([0,256])
    plt.show()'''
