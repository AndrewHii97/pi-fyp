from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import time 
import logging 
import setting

class IoTShadow:
	def __init__(self,configuration):
			# declare private variable 
			self.__config = None 
			self.__logger = None 
			self.__config = None 
			self.__shadow_client = None 
			self.__device_shadow_handler = None 
			self.__is_connected = False
			# constructor 
			self.__logger = self.__create_logger()
			self.__config = configuration 
		 
	def __create_logger(self):
		logger = logging.getLogger("AWSIoTPythonSDK.core")
		logger.setLevel(logging.DEBUG)
		streamHandler = logging.StreamHandler()
		formatter = logging.Formatter(
			'%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		streamHandler.setFormatter(formatter)
		logger.addHandler(streamHandler)
		return logger 
	
	# init using private key, rootCA and certificate 
	def __setup_mqtt_shadow_client(self):
		# Init AWSIoTMQTTShadowClient 
		shadow_client = AWSIoTMQTTShadowClient(self.__config.get_client_id())
		shadow_client.configureEndpoint(
			self.__config.get_endpoint()
			, self.__config.get_port()
		)
		shadow_client.configureCredentials(
			self.__config.get_rootCA_path()
			, self.__config.get_private_key_path()
			, self.__config.get_certifcate_path()
		)
		# AWSIoTMQTTShadowClient configuration
		shadow_client.configureAutoReconnectBackoffTime(1,32,20)
		shadow_client.configureConnectDisconnectTimeout(10) # 10sec 
		shadow_client.configureMQTTOperationTimeout(5) # 5sec 
		
		self.__shadow_client = shadow_client
	
	def __create_shadow_handler(self,thing_name): 
		# Create a device Shadow with persistent subscription
		self.__device_shadow_handler \
			= self.__device_shadow.createShadowHandlerWithName(self.__config.get_thing_name(),True)
	
	def connect_shadow_client(self):
		self.__setup_mqtt_shadow_client()
		# Connect to AWS IoT 
		self.__shadow_client.connect()
		self.__create_shadow_handler(self.__config.get_thing_name())
		self.__is_connected = True
		
	def is_connected(self):
		return self.__is_connected
	
	def get_device_shadow_handler(self):
		if self.__is_connected:
			return self.__device_shadow_handler
		else:
			return None
	
	def update_shadow(self):
		def customShadowCallback_Delta(payload, responseStatus, token):
			print(responseStatus)
			payloadDict = json.loads(payload)
			print("++++++++DELTA++++++++++")
			print("property: " + str(payloadDict["state"]["property"]))
			print("version: " + str(payloadDict["version"]))
			print("+++++++++++++++++++++++\n\n")
			
		def customShadowCallback_Delete(payload, responseStatus, token):
			if responseStatus == "timeout":
				print("Delete request " + token + " time out!")
			if responseStatus == "accepted":
				print("~~~~~~~~~~~~~~~~~~~~~~~")
				print("Delete request with token: " + token + " accepted!")
				print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
			if responseStatus == "rejected":
				print("Delete request " + token + " rejected!")
				
		def customShadowCallback_Update(payload, responseStatus, token):
			if responseStatus == "timeout":
				print("Update request " + token + " time out!")
			if responseStatus == "accepted":
				payloadDict = json.loads(payload)
				print("~~~~~~~~~~~~~~~~~~~~~~~")
				print("Update request with token: " + token + " accepted!")
				print("property: " + str(payloadDict["state"]["desired"]["property"]))
				print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
			if responseStatus == "rejected":
				print("Update request " + token + " rejected!")		
		
                # function to delete the shadow of the devices
		deviceShadowHandler.shadowDelete(customShadowCallback_Delete, 5) 
                # function to register the deltat of the devices
		deviceShadowHandler.shadowRegisterDeltaCallback(customShadowCallback_Delta)
		
		while True:
			print("this is running") 
			JSONPayload = '{"state":{"desired":{"property":' + str(loopCount) + '}}}'
			deviceShadowHandler.shadowUpdate(JSONPayload, customShadowCallback_Update, 5)
			loopCount += 1
			time.sleep(1)
		

		
	


		
		
		
		
		

	
	
