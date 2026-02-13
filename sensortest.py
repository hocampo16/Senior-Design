import AS7263_Pi as spec

#Reboot the spectrometer, just in case
spec.soft_reset()

#Set the gain of the device between 0 and 3.  Higher gain = higher readings
spec.set_gain(3)

#Set the integration time between 1 and 255.  Higher means longer readings
spec.set_integration_time(50)

#Set the board to continuously measure all colours
spec.set_measurement_mode(2)

try:
	#Turn on the main LED
	spec.enable_main_led()
	#Do this until the script is stopped:
	while True:
		#Store the list of readings in the variable "results"
		results = spec.get_calibrated_values()
		#Print the results!
		#print("610    :" + str(results[0]))
		print("680 :" + str(results[1]))
		#print("730 :" + str(results[2]))
		#print("760  :" + str(results[3]))
		#print("810   :" + str(results[4]))
		print("860 :" + str(results[5]) + "\n")
		
#When the script is stopped with control-C
except KeyboardInterrupt:
	#Set the board to measure just once (it stops after that)
	spec.set_measurement_mode(3)
	#Turn off the main LED
	spec.disable_main_led()
	#Notify the user
	print("Manually stopped")	