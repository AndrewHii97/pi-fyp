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


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('Main Program Start')
logger.setLevel(logging.INFO)

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
	motion_sensor = device.MotionSensor(8)
	glock = device.DoorLock(35, 37)
	camera = device.Camera()
	client = Client('http://192.168.0.137:3000',DEVICE_NAME, PASSWORD)
		
	def openGate():
		for counter in range(130):
			motor.forward(0.001)
		motor.go_idle()

	def closeGate(): 
		for counter in range(130): 
			motor.backward(0.001)
		motor.go_idle()

	def lockdoor_thread():	# thread lock gate upon gate closed
		while glock.get_status() == 0 : 
			time.sleep(0.1)
		closeGate()
		logger.info("gate locked") 
		
	while isActivated:
		rfid.read()
		beepy.beep(sound='coin') # generte a beep after rfid read 
		logger.info(f'RFID VALUE:{rfid.get_id()}')
		rfid_value = rfid.get_id() # rfid value read 
		r = client.check_rfid(rfid.get_id())
		res = r.json()
		logger.debug(f'Response:{res}') 
		rfid_owner = []
		rfid_owner = res['keyowner'] # key owner or key sharer list 
		openFlag = False
		
		if res['status'] == True and len(res['keyowner']) != 0: 
			openFlag = True 
		else: 
			logger.info("RFID not recognized") 
			openFlag = False
			beepy.beep(sound='wilhelm')
			continue 
			
		# timeout the gate 
		# isOpened = True 
		# counter = 0 
		# while glock.get_status() == 1: 
		#	time.sleep(1)
		#	counter = counter + 1 
		#	if counter >= 3: 
		#		logger.info("Gate Not Opened Timeout") 
		#		isOpened = False 
		#		break 

		# if isOpened == False : 
		#	continue 
			

		logger.info("start sensing for motion")	
		while motion_sensor.get_status() == 0 :
			print(motion_sensor.get_status())
			time.sleep(1)

		logger.info("motion sensor detect person")
		beepy.beep(sound='coin')	
		byte = camera.capture() # capture images after motion sensor trigger 
		file_name = str(uuid.uuid1()) + ".jpg" # uuid as filename from hostname and time 
		logger.info(f"UUID:{file_name}")

		# upload photo to s3 
		r = client.upload_images(file_name,byte)
		res = r.json() 
		logger.debug(res) 
		if res['status'] == False: 
			logger.info("Image Upload Fail: Restart Process") 
			continue

		logger.info("uploaded imaged to s3")
		image  = client.update_photos_db(file_name) # update database on photo information
		logger.info("done update photos table of database")

		r = client.count_persons(file_name)
		res = r.json()
		logger.debug(res)
		logger.info("done counting number of persons")
		person_count = res['PersonCount'] # Persons Count 
		logger.info(f"PersonCount:{person_count}")


		r = client.count_faces(file_name) 
		res = r.json()
		logger.debug(res)
		logger.info("done counting number of faces") 
		face_count = res['FaceCount'] # Face Count 
		logger.info(f"FaceCount:{face_count}")
		
		if face_count > person_count: 
			logger.info("face count > person_count")
			person_count = face_count
		elif face_count < person_count: 
			logger.info("face count < person count:file issue ")
			issue = client.create_issue("Some Face Undetected") # Issue! 
			client.link_issues_photo(issue['issueid'], image['photoid']) 
			logger.info("process reset") 
			beepy.sound('wilhelm')
			continue 
		elif face_count == person_count: 
			logger.info("face count = person count") 

		# lastly check if no person detected 
		if person_count == 0: 
			logger.info("Gate Open BUt No Person Detected: File Issues")
			logger.info("Process Reseted") 
			issue = client.create_issue('No Person Detected') # Issue!
			client.link_issues_photo(issue['issueid'], image['photoid'])
			beepy.sound('wilhelm')
			continue 

		# search for person in the image captured	
		r = client.search_faces(file_name)
		res = r.json() 
		logger.debug(res)
		
		# check if any error in searching process 
		if res['hasUnIndexed'] == True : 
			logger.error(f"some faces captured unclear")
			logger.warning("process reseted")
			continue
		if res['status'] == False: 
			logger.error(f"error searching faces:\n{res['error']}") 
			logger.warning("process reseted")
			continue 
	
		results = res['Result']
		faceIds = []
		for result in results: 
			faceMatches = result['FaceMatches']
			for face in faceMatches:
				faceIds.append(face['Face']['FaceId'])
		logger.info(f'All matching faces: {faceIds}')


		personsInPhoto = []	
		if len(faceIds) > 0: 
			# find the faceids belong to which person 
			personsInPhoto	= client.find_faceOwner(faceIds)
			logger.info(f"number of person rekognized :{len(personsInPhoto)}")
			logger.debug(personsInPhoto)
			logger.info("Done Searching FaceID Owner in DB") 
		else : 
			# when no any matching faces found 
			logger.info("no matching faces after search") 

		hasTailgaters = False
		if face_count > 1 :
			hasTailgaters = True  
		
		owner = findCommon(personsInPhoto, rfid_owner)
		ownerCount = len(owner)
		nonOwner = findDiff(personsInPhoto, owner) 
		nonOwnerCount = len(nonOwner)
		intruderCount = face_count - len(personsInPhoto)
		logger.info(f'KeyOwner:{owner}')
		logger.info(f'NonOwner:{nonOwner}')
		logger.info(f'Intruders:{intruderCount}')
		logger.info(f'HasTailgaters:{hasTailgaters}')
		
		if hasTailgaters: # when taigating occur  
			if len(personsInPhoto) == 0 : # no a single face recognized  
				logger.info("More than a single intruders")
				issue = client.create_issue(f"{intruderCount} Intruders") 
				client.link_issues_photo(issue['issueid'], image['photoid'])
				openFlag = False
				beepy.beep(sound='wilhelm')
			elif face_count == len(personsInPhoto): # when all face recognized 
				logger.info("the tailgater is another residents") 
				issue = client.create_issue("Tailgating by Resident")
				client.link_issues_photo(issue['issueid'], image['photoid'])
				for person in personsInPhoto : 
					client.create_entry(person['id'], image['photoid'],True)
				openFlag = True
				beepy.beep(sound='ping')
			elif face_count > len(personsInPhoto): # some face not recognized
				logger.info("have tailgater which is an outsider")
				issue = client.create_issue(f"Tailgated by {intruderCount} Intruders")
				client.link_issues_photo(issue['issueid'], image['photoid'])
				for person in personsInPhoto :
					client.create_entry(person['id'], image['photoid'],True)
				openFlag= False
				beepy.beep(sound='wilhelm')
		else: # when no tailgating	
			logger.info("Single Person Condition")
			if len(personsInPhoto) == 0: # if not a single face recognized	
				logger.info("Intruder detected using resident rfid") 
				issue = client.create_issue(f"Intrudres - RFID:{rfid_value} ") 
				client.link_issues_photo(issue['issueid'],image['photoid'])
				openFlag= False 
				beepy.beep(sound='wilhelm')
			else: # the only face is recognized  
				if isInList(personsInPhoto[0],rfid_owner ): 
					logger.info("Resident Keyowner Entering")
					client.create_entry(personsInPhoto[0]['id'], image['photoid'],False)
					openFlag = True
					beepy.beep(sound='ping')
				else: 
					logger.info('Resident Non key owner entering')
					issue = client.create_issue(
						f"Resident Non Key Owner - RFID:{rfid_value}")
					client.link_issues_photo(issue['issueid'], image['photoid'])
					client.create_entry(personsInPhoto[0]['id'], image['photoid'],True)
					openFlag = True
					beepy.beep(sound='ping')
		
		if openFlag == True: 
			logger.info("gate start to unlock")
			openGate()
			time.sleep(2)
		else:
			logger.info("gate does not unlock")
			continue;

		logger.info("start lock gate thread ")
		lock_door = threading.Thread(target=lockdoor_thread)
		lock_door.start()
					
		lock_door.join()

def isInList( person, personList): 
	for i in personList: 
		if person['id'] == i['id']:
			return True 
	return False

# work person id which is unique 
def findCommon(list1, list2): 
	common = []
	for i  in list1:
		for ii in list2: 
			if i['id'] == ii['id']: 
				common.append(i) 
	return common

def findDiff(list1,list2): 
	refList = []
	searchList = []
	if len(list1) > len(list2): 
		refList = list2.copy()
		searchList = list1.copy() 
	else: 
		refList = list1.copy() 
		searchList = list2.copy()

	for i in refList:
		counter = 0	
		for ii in searchList: 
			if i['id'] == ii['id']: 
				searchList.pop(counter)
			counter = counter + 1
	return searchList

def main(args):
	# ConnectToShadow 
	run()
	logger.info("main completed")
	return 0
	# the face recognition is carry out 
	# the loop reset if no error detected 

if __name__ == '__main__':
	sys.exit(main(sys.argv))
