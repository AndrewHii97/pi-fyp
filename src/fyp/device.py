import sys
import RPi.GPIO as GPIO 
import time
from mfrc522 import SimpleMFRC522
from obsvr_pttn import Publisher

class DeviceQueue: 
	
	def __init__(self,config): 
		devices = config.get_devices()
		self.dev_q = []	
		# create device & put in List
		for device in devices: 
			new_device = None
			device_type = device["type"]
			if device_type == "motor" :
				new_device = Motor(device["input"][0]
					,device["input"][1]
					,device["input"][2]
					,device["input"][3]
					,device["id"])
			elif device_type == "rfid":
				new_device = RfidReader(device["id"])
			elif device_type == "gate_lock":
				new_device = DoorLock(
					device["input"][0]
					,device["output"][0]
					,device["id"])
			elif device_type == "ultra_sonic" : 
				new_device = USonicSensor(
					device["output"][0]
					,device["input"][0] 
					,device["id"])
			self.dev_q.append(new_device)
			print(self.dev_q)
	
	def get_device_using_id(self,device_id): 
		for device in self.dev_q:
			if device.get_device_id() == device_id.value:
				return device 

class Device(Publisher): 
	def __init__(self,device_id):
		super().__init__()
		self.__id =  device_id

	def set_device_id(self,device_id): 
		self.__id = device_id 
		
	def get_device_id(self): 
		return self.__id 

	def set_device_meta(self,meta : str) : 
		self.__meta = meta 

	def get_device_meta(self) :
		return self.__meta

	def __del__(self): 
		super().__del__() 

class Motor(Device): 
	def __init__(self,pin1,pin2,pin3,pin4,device_id):
		super().__init__(device_id)
		# initiate pin number as constant 
		self.__PIN1 = pin1 
		self.__PIN2 = pin2 
		self.__PIN3 = pin3 
		self.__PIN4 = pin4
		GPIO.setmode(GPIO.BOARD)
		# set the pins connected to output pin
		GPIO.setup(pin1,GPIO.OUT)
		GPIO.setup(pin2,GPIO.OUT)
		GPIO.setup(pin3,GPIO.OUT)
		GPIO.setup(pin4,GPIO.OUT)
		# motor sequence table 
		self.__STEP_COUNT = 8
		self.__SEQ = [ 
				 [0,0,0,1],
				 [0,0,1,1], 
				 [0,0,1,0], 
				 [0,1,1,0],
				 [0,1,0,0], 
				 [1,1,0,0],
				 [1,0,0,0],
				 [1,0,0,1]
		]
		# motor idle state
		self.__IDLE = [0,0,0,0]

	def setStep(self,s1,s2,s3,s4): 
		GPIO.output(self.__PIN1,s1)
		GPIO.output(self.__PIN2,s2)		
		GPIO.output(self.__PIN3,s3)
		GPIO.output(self.__PIN4,s4)

	# angle per stride = 5.625 
	# 64 steps/ revolution
	def forwards(self,delay,steps=0):
		for i in range(steps):
			# range() function start the iterator at 0,1,2,...,7
			for ii in range(self.__STEP_COUNT):
				self.setStep(self.__SEQ[ii][0],self.__SEQ[ii][1],self.__SEQ[ii][2]
					,self.__SEQ[ii][3])
				time.sleep(delay)
	
	# go through sequence table once
	def forward(self,delay): 
		# range() function start the iterator at 0,1,2,...,7
		for ii in range(self.__STEP_COUNT):
				self.setStep(self.__SEQ[ii][0],self.__SEQ[ii][1],self.__SEQ[ii][2]
								,self.__SEQ[ii][3])
				time.sleep(delay)
	

	def backwards(self,delay,steps=0): 
		for i in range(steps):
			# range() function start the iterator at 7,6,5,...,0
			for ii in reversed(range(self.__STEP_COUNT)):
				self.setStep(self.__SEQ[ii][0],self.__SEQ[ii][1],self.__SEQ[ii][2]
								,self.__SEQ[ii][3])
				time.sleep(delay)

	# go throuhg sequence table once in reverse order 
	def backward(self,delay,steps=0): 
		# range() function start the iterator at 7,6,5,...,0
		for ii in reversed(range(self.__STEP_COUNT)):
			self.setStep(self.__SEQ[ii][0],self.__SEQ[ii][1],self.__SEQ[ii][2]
							,self.__SEQ[ii][3])
			time.sleep(delay)


	def go_idle(self):
		self.setStep(self.__IDLE[0],self.__IDLE[1],self.__IDLE[2],self.__IDLE[3]) 

	def __del__(self):
		GPIO.cleanup([self.__PIN1,self.__PIN2,self.__PIN3,self.__PIN4])


class USonicSensor(Device): 
	
	def __init__(self,trig_pin,echo_pin,device_id):
		super().__init__(device_id)
		# initialize trig and echo pin for Ultrasonic sensor 
		self.__TRIG = trig_pin
		self.__ECHO = echo_pin
		# set input output mode for the raspberry pi pin 
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.__TRIG,GPIO.OUT)
		GPIO.setup(self.__ECHO,GPIO.IN)
		GPIO.output(self.__TRIG,False)
		self.__trig_dist = 0 
		
	def calibrate(self): 
		print("calibrating")
		GPIO.output(self.__TRIG,False)
		time.sleep(2)
		print("get distance in calibrating")
		self.__trig_dist = self.get_distance()

	def get_distance(self): 
		pulse_start = 0 
		pulse_end = 0 
		GPIO.output(self.__TRIG,True)
		time.sleep(0.00001)
		GPIO.output(self.__TRIG,False) 
		while GPIO.input(self.__ECHO) == 0:
				# print(f"\r{GPIO.input(self.__ECHO)}",end="")
				pulse_start = time.time()
		print("start 2nd loop")
		while GPIO.input(self.__ECHO) == 1:
				# print(f"\r{GPIO.input(self.__ECHO)}",end="")
				pulse_end = time.time()
		print(f'pulse_start:{pulse_start}')
		print(f'pulse_end:{pulse_end}')
		pulse_duration = pulse_end - pulse_start 
		distance = pulse_duration * 17150
		distance = round(distance, 2)
		return distance 

	def __del__(self):
		GPIO.cleanup([self.__TRIG,self.__ECHO])

	def get_trig_dist(self): 
		return self.__trig_dist

	def run(self):
		print("start running ultrasonic sensor") 
		while True : 
			dist = self.get_distance() 
			print(f"Distance:{dist}")
			if dist > 10 : 
				super().notify_all_observer()
				time.sleep(5)	

class RfidReader(Device): 

	def __init__(self,device_id): 
		super().__init__(device_id)
		# 3.3V => Pin 1
		# GND => Pin 6 
		# pin allocation 
		self.__SCK = 24 # serial clock
		self.__MOSI = 19 # Master out Slave In (data line) 
		self.__MISO = 21 # Master in Slave out (data line) 
		self.__RST = 22 # Reset 
		self.__reader = SimpleMFRC522()
		self.__rfid_id = None 
		self.__rfid_text = None 

	def read(self): 
		self.__rfid_id,self.__rfid_text = self.__reader.read() 
	
	def get_id(self):
		return self.__rfid_id

	def get_text(self):
		return self.__rfid_text 

	def get_SCK_pin_no(self):
		return self.__SCK

	def get_MOSI_pin_no(self):
		return self.__MOSI

	def get_MISO_pin_no(self): 
		return self.__MISO

	def get_RST_pin_no(self):
		return self.__RST

	def __del__(self): 
		GPIO.cleanup([self.__SCK,self.__MOSI,self.__MOSI,self.__MISO,self.__RST])


class DoorLock(Device):
	
	def __init__(self, in_pin, out_pin,device_id): 
		super().__init__(device_id)
		GPIO.setmode(GPIO.BOARD)
		self.__OUT_PIN = out_pin 
		self.__IN_PIN = in_pin 
		GPIO.setup(self.__OUT_PIN,GPIO.OUT)
		GPIO.setup(self.__IN_PIN,GPIO.IN,GPIO.PUD_DOWN) # pull-down resistor
		GPIO.output(self.__OUT_PIN,True)
			
	def __del__(self): 
		GPIO.cleanup([self.__OUT_PIN,self.__IN_PIN])
	
	def get_status(self): 
		return GPIO.input(self.__IN_PIN)

