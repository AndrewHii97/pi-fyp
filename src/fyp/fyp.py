import sys
import pathlib
from config import ConfigParser
from cli import create_fyp_cli
from iot_core import IoTShadow 
from device import DeviceQueue 
import enum



class DeviceCode(enum.Enum):
	MOTOR = "1"
	RFID = "2"
	GLOCK = "3" 
	USONIC = "4" 

def main(args):
	# remove the first argument which specify the script name 
	if not isinstance(args,type([])):
		args = [args]
	args.pop(0)	
	parsed_args = create_fyp_cli(args)
	config_parser = ConfigParser(parsed_args.file_path)
	configuration = config_parser.get_configuration() 
	# configure connection to the shadow cloud 
        # iot_shadow = IoTShadow(configuration)
        # iot_shadow.connect_shadow_client()
        # print(iot_shadow.is_connected())
        # iot_shadow.update_shadow()
        # create devices read from configuration file  
	device_queue = DeviceQueue(configuration) 
	motor = device_queue.get_device_using_id(DeviceCode.MOTOR)
	rfid = device_queue.get_device_using_id(DeviceCode.RFID) 
	glock = device_queue.get_device_using_id(DeviceCode.GLOCK) 
	usonic = device_queue.get_device_using_id(DeviceCode.USONIC) 
	# device logic 
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
	# camera turn on to capture the scene

	# the captured picture is sent to the cloud 
        
	# the face recognition is carry out 

	# the loop reset if no error detected 

	# the machine turn into alarming state if intruders detected 

	return 0


if __name__ == '__main__':
	sys.exit(main(sys.argv))

