import sys 
import device


motor = device.Motor(32.36,38,40)
rfid = device.RfidReader()
glock = device.DoorLock(35,37)
usonic = device.USonicSensor(10,8)



rfid.read() 
print(rfid.get_id())
while glock.get_status() == True : 
    print("motor moving",end="\r")
    motor.forward(0.2)
usonic.calibrate()
while usonic.get_distance() > 20: 
    print("no person detected yet",end="\r")
print("usonicsensor detect something")


