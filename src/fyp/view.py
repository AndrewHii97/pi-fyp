from datetime import date,datetime
import time 
import sys

class TxtInterface:

	def __init__(self):
		# date/time
		self.date = date.today().strftime("%d/%m/%Y")
		self.time = datetime.now().strftime("%H:%M:%S") 
		# RFID Reader Status 
		self.id = 123456 
		self.id_owner = "HelloWorld" 
		# motor state
		self.motor_state = "Idle"
		# gate_state
		self.gate_state = "Lock" 
		# ultrasonic_sensor 
		self.threshold = 45 
		self.dist = 50
		# intruders/tailgaters alarm 
		self.alarm_state = "Off" 
		self.has_intruder = False 
		self.has_tailgater = False

	def print_tui(self):
		print(
		f"\t|===============================================|\n"
		f"\t| Devices Panel                                 |\n"
		f"\t|===============================================|\n"
		f"\t| DATE: {self.date:=<8}               TIME: {self.time:=<8} |\n"
		f"\t|===============================================|\n"
		f"\t| RFID_READER || USER_ID  > {self.id: <19} |\n"
		f"\t|             || ID_OWNER > {self.id_owner: <19} |\n"
		f"\t|===============================================|\n"
		f"\t| MOTOR_STATE || {self.motor_state: <30} |\n"
		f"\t|===============================================|\n"
		f"\t| GATE_STATE  || {self.gate_state: <30} |\n"
		f"\t|===============================================|\n"
		f"\t| USONIC      || THRESHOLD_DISTANCE > {self.threshold: <9} |\n"
		f"\t|             || CURRENT_READING    > {self.dist: <9} |\n"
		f"\t|===============================================|\n"
		f"\t| ALARM       || {self.alarm_state: <30} |\n"
		f"\t|===============================================|\n"
		f"\t| INTRUDERS   || {self.has_intruder: <30} |\n"
		f"\t|===============================================|\n"
		f"\t| TAILGATERS  || {self.has_tailgater: <30} |\n"
		f"\t|===============================================|\n"
		,end="")

	def update_tui(self):
		print(
		f"\n\n\n"
		f"\t\033[8C{self.date:=<8}\033[15CTIME: {self.time:=<8} |\n"
		f"\n"
		f"\t| RFID_READER || USER_ID  > {self.id: <19} |\n"
		f"\t|             || ID_OWNER > {self.id_owner: <19} |\n"
		f"\n"
		f"\t| MOTOR_STATE || {self.motor_state: <30} |\n"
		f"\n"
		f"\t| GATE_STATE  || {self.gate_state: <30} |\n"
		f"\n"
		f"\t| USONIC      || THRESHOLD_DISTANCE > {self.threshold: <9} |\n"
		f"\t|             || CURRENT_READING    > {self.dist: <9} |\n"
		f"\n"
		f"\t| ALARM       || {self.alarm_state: <30} |\n"
		f"\n"
		f"\t| INTRUDERS   || {self.has_intruder: <30} |\n"
		f"\n"
		f"\t| TAILGATERS  || {self.has_tailgater: <30} |\n"
		f"\n"
		,end="")

	def run_tui(self): 
		self.print_tui()
		while True : 
			try:
				for i in range(21):
					print("\033[A",end="")
				self.date = date.today().strftime("%d/%m/%Y")
				self.time = datetime.now().strftime("%H:%M:%S") 
				time.sleep(0.050)
				self.update_tui()
			except KeyboardInterrupt:
				for i in range(21): 
					print("")
				sys.exit(0)

