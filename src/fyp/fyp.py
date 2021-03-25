import sys
import uuid
from iot_core import IoTShadow 
import logging
import threading 
import time 
import device
from service import Client
from setting import DEVICE_NAME, PASSWORD 


logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger(__name__)
logger.info('Main Program Start')
logger.setLevel(logging.DEBUG)

def main(args):
	# configure connection to the shadow cloud 
	# iot_shadow = IoTShadow()
	# iot_shadow.connect_shadow_client()
	# print(iot_shadow.is_connected())
	# iot_shadow.update_shadow()
	# create devices read from configuration file  
	# initialize sensor and motor connected 
	motor = device.Motor(32,36,38,40)
	logger.info("motor initialized")
	rfid = device.RfidReader()
	logger.info("gate switch initialized")
	glock = device.DoorLock(35,37)
	logger.info("door lock initialized")
	motion_sensor = device.MotionSensor(8)
	logger.info("motion sensor initialized")
	camera = device.Camera()
	logger.info("camera initialized")
	client = Client('http://192.168.0.137:3000',DEVICE_NAME, PASSWORD) 
	logger.info("Create HTTP Client to handle requests to server") 
	# rfid wait for rfid scan 
	rfid.read()
	logger.debug(f'RFID VALUE:{rfid.get_id()}')
	r = client.check_rfid(rfid.get_id())
	res = r.json()
	logger.debug(f'Response:{res}') 

	if res['status'] == True and len(res['keyowner']): 
		for counter in range(100):
			# open the gate lock 
			motor.backward(0.001)

	logger.debug('wait for gate to be open') 
	while glock.get_status() == 1: 
		time.sleep(0.1)
		
	def lockdoor_thread():  # thread lock gate upon gate closed
		while glock.get_status() == 0 : 
			time.sleep(0.1)
		logger.info("door return to original position")
		logger.info("motor rotate to close the door")
		for counter in range(100): 
			time.sleep(0.001)
			motor.forward(0.001)
		logger.info("door is locked")
		
	time.sleep(2)	
	logger.info("lock door thread started")
	lock_door = threading.Thread(target=lockdoor_thread)
	lock_door.start()
	logger.info("start sensing for motion")	
	while motion_sensor == 0 :
		time.sleep(1)
		logger.debug("no person") 
	logger.info("motion sensor detect person")
	byte = camera.capture() # capture images after motion sensor trigger 
	file_name = str(uuid.uuid1()) # generate uuid from hostname and time 
	logger.debug("UUID:{file_name}")
	r = client.upload_images(file_name,byte)
	logger.debug(r)

	lock_door.join()
	logger.info("main completed")
	return 0
	# motor will move to open the gate at this moment if rfid valid  
	# while glock.get_status() == True : 
	#	print("motor moving",end="\r")
	#	motor.forward(0.2) 
	# usonic.calibrate()
	# # ultrasonic sensor try to detect if any perons run through 
	# while usonic.get_distance() > 20: 
	#	print("no person detected yet") 
	# print("usonicsensor detect something") 
	# camera turn on to capture the scene
	# the captured picture is sent to the cloud 
	# the face recognition is carry out 
	# the loop reset if no error detected 


if __name__ == '__main__':
	sys.exit(main(sys.argv))

