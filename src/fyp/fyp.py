import sys
from iot_core import IoTShadow 
import device
import logging

logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger(__name__)
logger.info('Main Program Start')
logger.setLevel(logging.DEBUG)

def main(args):
	# configure connection to the shadow cloud 
    """
	iot_shadow = IoTShadow()
    iot_shadow.connect_shadow_client()
    print(iot_shadow.is_connected())
    iot_shadow.update_shadow()
    create devices read from configuration file  
	"""

	# initialize sensor and motor connected 
	motor = device.Motor(32,36,38,40)
	logger.info("motor initialized")
	rfid = device.RfidReader()
	logger.info("gate switch initialized")
	glock = device.DoorLock(35,37)
	logger.info("door lock initialized")
	usonic = device.UsonicSensor(10,8)
	logger.info("ultrasonic sensor initialized")
	# rfid wait for rfid scan 
	rfid.read()
	print(rfid.get_id())
	# the rfid need to be sent to web server for authentication 
	# motor will move to open the gate at this moment if rfid valid  
	while glock.get_status() == True : 
		print("motor moving",end="\r")
		motor.forward(0.2) 
	usonic.calibrate()
	# ultrasonic sensor try to detect if any perons run through 
	while usonic.get_distance() > 20: 
		print("no person detected yet") 
	print("usonicsensor detect something") 
	'''
	camera turn on to capture the scene
	the captured picture is sent to the cloud 
	the face recognition is carry out 
	the loop reset if no error detected 
	the machine turn into alarming state if intruders detected 
	'''

	return 0


if __name__ == '__main__':
	sys.exit(main(sys.argv))

