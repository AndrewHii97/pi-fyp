import RPi.GPIO as GPIO 
import sys 
import device
import time
# motor = device.Motor(32,36,38,40)
# rfid = device.RfidReader()
glock = device.DoorLock(35,37)
# usonic = device.USonicSensor(8,10)
# motion_sensor = device.MotionSensor(8) 


# while True: 
#         time.sleep(1)
#         print(glock.get_status());

def readSensor():
	motion_sensor = device.MotionSensor(8)
	while True:
		time.sleep(1)	
		print(motion_sensor.get_status())

# readSensor()
	

# camera = device.Camera()
# data = camera.capture()
# data.seek(0) move the pointer to the start of the byte so we can read the stream
# data.seek(0)
# print(data.read())

# rfid.read() 
# print("RFID detect something")
# print(rfid.get_id())
# print(rfid.get_text())


def unlockGate():
	motor = device.Motor(32,36,38,40)
	counter = 0 
	for x in range(5000): 
		# motor.forward(0.001)
		motor.backward(0.001) # backward is moving the screw towards the motor
		print(counter)
		counter = counter + 1 

# unlockGate()

def lockGate():
	motor = device.Motor(32,36,38,40)
	counter = 0
	for x in range(5000):
		motor.forward(0.001) 
		print(counter)
		counter = counter + 1 


input('Press to start')
motor = device.Motor(32,36,38,40)
counter = 0
while True: 
    motor.forward(0.01)
    print(counter)
    counter = counter + 1;


# lockGate()



# usonic.calibrate()
# print("finish calibrating") 
# while True :
#	  time.sleep(2)
#	  print(usonic.get_distance())

# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(8,GPIO.IN,GPIO.PUD_DOWN) 
# 
# time.sleep(5)
# print("start detection")
# while True: 
#	  time.sleep(1)
#	  sensor = GPIO.input(8)
#	  print(sensor)
# 
# GPIO.cleanup()

list1 = ['a','e','b','d']
list2 = ['a','b']

def findCommon(list1,list2): 
	common = [] 
	for i in list1: 
		for ii in list2: 
			if i == ii : 
				common.append(i)
	return common

def findDiff(list1,list2): 
	if len(list1) > len(list2): 
		refList = list2.copy()
		searchList = list1.copy() 
	else: 
		refList = list1.copy() 
		searchList = list2.copy()
	for i in refList:
		counter = 0	
		for ii in searchList: 
			if i == ii: 
				searchList.pop(counter)
			counter = counter + 1
	return searchList



