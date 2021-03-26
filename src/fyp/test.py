import RPi.GPIO as GPIO 
import sys 
import device
import time
# motor = device.Motor(32,36,38,40)
# rfid = device.RfidReader()
# glock = device.DoorLock(35,37)
# usonic = device.USonicSensor(8,10)

camera = device.Camera()
data = camera.capture()
# data.seek(0) move the pointer to the start of the byte so we can read the stream
data.seek(0)
print(data.read())

# rfid.read() 
# print("RFID detect something")
# print(rfid.get_id())
# print(rfid.get_text())


# time.sleep(5)
# for counter in range(100):
#     motor.backward(0.001)
# for counter in range(100):
#     motor.forward(0.001)

# usonic.calibrate()
# print("finish calibrating") 
# while True :
#     time.sleep(2)
#     print(usonic.get_distance())

# while True: 
#     print(glock.get_status(),end="\r")
# GPIO.cleanup()
# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(8,GPIO.IN,GPIO.PUD_DOWN) 
# 
# time.sleep(5)
# print("start detection")
# while True: 
#     time.sleep(1)
#     sensor = GPIO.input(8)
#     print(sensor)
# 
# GPIO.cleanup()

