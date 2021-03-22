import sys 
import device
import time
motor = device.Motor(32,36,38,40)
rfid = device.RfidReader()
# glock = device.DoorLock(35,37)
# usonic = device.USonicSensor(10,8)



# rfid.read() 
# print("RFID detect something")
# print(rfid.get_id())
# print(rfid.get_text())



time.sleep(5)
for counter in range(100):
    motor.backward(0.001)
for counter in range(100):
    motor.forward(0.001)

# while glock.get_status() == True : 
#     print("motor moving",end="\r")
#     motor.forward(0.1)
# usonic.calibrate()
# while usonic.get_distance() > 20: 
#     print("no person detected yet",end="\r")
# print("usonicsensor detect something")


