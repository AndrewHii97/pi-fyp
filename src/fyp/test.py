import sys 
import device
import time
motor = device.Motor(32,36,38,40)
rfid = device.RfidReader()
glock = device.DoorLock(35,37)
usonic = device.USonicSensor(8,10)



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
# while usonic.get_distance() > 20: 
#     print("no person detected yet",end="\r")
# print("usonicsensor detect something")

while True: 
    print(glock.get_status(),end="\r")


