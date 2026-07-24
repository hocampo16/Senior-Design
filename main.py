import camera
import servo


pc2 = camera.config("imx708_noir.json", False, False, 0, 66666, 0.42)
camera.takePhoto(pc2, wavelengthSelect = 0, showPreview = True, pin = 8, output = "testing.jpg") #for wl select, 0 = Red, 1 = NIR