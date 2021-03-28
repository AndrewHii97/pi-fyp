import sys
import uuid
from iot_core import IoTShadow 
import logging
import threading 
import time 
import device
import beepy # ceate beep sound 
from service import Client
from setting import DEVICE_NAME, PASSWORD 


logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger(__name__)
logger.info('Main Program Start')
logger.setLevel(logging.DEBUG)

# configure connection to cloud shadow 
def ConnectToShadow(): 
	iot_shadow = IoTShadow()
	iot_shadow.connect_shadow_client()
	print(iot_shadow.is_connected())
	iot_shadow.update_shadow()

def run(): 
	isActivated = True 
	# initialize sensor and motor connected 
	motor = device.Motor(32,36,38,40)
	rfid = device.RfidReader()
	glock = device.DoorLock(35,37)
	motion_sensor = device.MotionSensor(8)
	camera = device.Camera()
	client = Client('http://192.168.0.137:3000',DEVICE_NAME, PASSWORD)
		
	def openGate():
		for counter in range(100):
			motor.backward(0.001)

	def closeGate(): 
		for counter in range(100): 
			motor.forward(0.001)

	def lockdoor_thread():	# thread lock gate upon gate closed
		while glock.get_status() == 0 : 
			time.sleep(0.1)
		closeGate()
		logger.debug("gate locked") 
		
	while isActivated:
		rfid.read()
		beepy.beep(sound=1) # generte a beep after rfid read 
		logger.debug(f'RFID VALUE:{rfid.get_id()}')
		rfid_value = rfid.get_id() # rfid value read 
		r = client.check_rfid(rfid.get_id())
		res = r.json()
		logger.debug(f'Response:{res}') 
		rfid_owners = res # key owner or key sharer list 
		
		if res['status'] == True and len(res['keyowner']) != 0: 
			openGate()
		else: 
			logger.info("RFID not recognized") 
			continue 
			
		# timeout the gate 
		isOpened = True 
		counter = 0 
		while glock.get_status() == 1: 
			time.sleep(1)
			counter = counter + 1 
			if counter >= 3: 
				logger.info("Gate Not Opened Timeout") 
				isOpened = False 
				break 

		if isOpened == False : 
			continue 
			
		time.sleep(2)	
		logger.info("start lock gate thread ")
		lock_door = threading.Thread(target=lockdoor_thread)
		lock_door.start()

		logger.info("start sensing for motion")	
		while motion_sensor == 0 :
			time.sleep(1)
			logger.debug("no person") 
		logger.info("motion sensor detect person")
		beepy.beep(sound='coin')	

		byte = camera.capture() # capture images after motion sensor trigger 
		file_name = str(uuid.uuid1()) + ".jpg" # uuid as filename from hostname and time 
		logger.debug(f"UUID:{file_name}")

		# upload photo to s3 
		r = client.upload_images(file_name,byte)
		res = r.json() 
		logger.debug(res) 
		if res['status'] == False: 
			logger.info("Image Upload Fail: Restart Process") 
			continue

		logger.info("uploaded imaged to s3")
		image  = client.update_photos_db(file_name) # update database on photo information
		logger.debug(image) 	
		logger.info("done update photos table of database")

		r = client.count_persons(file_name)
		res = r.json()
		logger.debug(res)
		logger.info("done counting number of persons")
		person_count = res['PersonCount'] # Persons Count 


		r = client.count_faces(file_name) 
		res = r.json()
		logger.debug(res)
		logger.info("done counting number of faces") 
		face_count = res['FaceCount'] # Face Count 
		

		if face_count > person_count: 
			logger.info("face count > person_count")
			person_count = face_count
		elif face_count < person_count: 
			logger.info("face count < person count:file issue ")
			client.create_issues("Some Face Undetected") 
			logger.info("process reset") 
			continue 
		elif face_count = person_count: 
			logger.info("face count = person count") 

		# lastly check if no person detected 
		if person_count == 0: 
			logger.info("Gate Open BUt No Person Detected: File Issues")
			logger.info("Process Reseted") 
			client.create_issues('No Person Detected')
			continue 

		# search for person in the image captured 	
		r = client.search_faces(file_name)
		res = r.json() 
		logger.debug(res)
		
		# check if any error in searching process 
		if res['status'] == false: 
			logger.info("error searching faces") 
			logger.info("process reseted")
			continue 
	
		results = res['Result']
		faceIds = []
		for result in results: 
			faceMatches = result['FaceMatches']
			for face in faceMatches:
				faceIds.append(face['Face']['FaceId'])
		logger.debug(faceIds)

		# find the faceids belong to which person 
		r = client.find_faceOwner(faceIds)
		personsInPhoto = r.json() # array of persons data 
		logger.debug(res)
		logger.info("Done Searching FaceID Owner in DB") 

		hasTailgaters = False
		if face_count > 1 :
			hasTailgaters = True  

		if hasTailgaters: 
			if face_count == len(personsInPhoto): 
				logger.info("the tailgater is another residents") 
					
			elif face_count < len(personsInPhoto): 
				logger.info("the tailgater is an outsider")
		else: 
			
			pass
		lock_door.join()



def main(args):
	# ConnectToShadow 
	try:
		run()
	except: 
		logger.info("program manually stopped") 	
	
	logger.info("main completed")
	return 0
	# the face recognition is carry out 
	# the loop reset if no error detected 

if __name__ == '__main__':
	sys.exit(main(sys.argv))

