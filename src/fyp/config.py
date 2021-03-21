import json
import sys
from pathlib import Path


class ConfigParser:

	class Configuration:
		def __init__(self,config_obj): 
			self.__endpoint = config_obj['endpoint']
			self.__certificate_path = config_obj['certificate_path']
			self.__private_key = config_obj['private_key']
			self.__rootCA = config_obj['rootCA']
			self.__port = int(config_obj['port'])
			self.__client_id = config_obj['client_id']
			self.__thing_name = config_obj['thing_name']
			self.__devices = config_obj['devices']

		def get_endpoint(self):
			return self.__endpoint
					
		def get_certifcate_path(self):
			return self.__certificate_path 

		def get_private_key_path(self):
			return self.__private_key

		def get_rootCA_path(self):
			return self.__rootCA

		def get_port(self):
			return self.__port

		def get_client_id(self):
			return self.__client_id

		def get_thing_name(self):
			return self.__thing_name
		# return an array of devices inforamtion
		def get_devices(self):
			return self.__devices 

	def __init__(self, file_path='config.json'):
		file_content = self.__get_file_txt(file_path)
		self.__configuration = self.Configuration(
			self.__verify_json_format(self.__convert_txt(file_content)))

	def get_configuration(self):
		return self.__configuration 

	def __get_file_txt(self,file_path):
		# open the configuration file and check if file exists
		try:
			with open(file_path, 'r') as file:
				file_content = file.read()
		except FileNotFoundError:
			sys.exit(print('File Path cannot be found'))
		return file_content

	def __convert_txt(self,json_txt):
		# turn json txt into python obj
		try:
			self.json = json.loads(json_txt)
			return(self.json)
		except json.JSONDecodeError as e:
			error_msg = f'Error:\n{e.doc}\n{e.msg} Line:{e.lineno} Column:{e.colno}\n'
			sys.exit(print(error_msg))

	def __verify_json_format(self,config_obj):
		isEqual = True
		keys = [
			'endpoint',
			'certificate_path',
			'private_key',
			'rootCA',
			'port',
			'client_id',
			'thing_name',
			'devices'
		]

		dic_keys = list(config_obj.keys())
		for key in keys:
			if key not in dic_keys:
				isEqual = False
				break
		if isEqual:
			return config_obj
		else:
			sys.exit(print("wrong json format"))
