import json
import sys 

class ConfigParser:	
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
	
	def get_config_obj():
		return self.config_obj
				
	def __init__(self, file_path='config.json'):
		file_content = self.__get_file_txt(file_path)
		self.config_obj = self.__convert_txt(file_content)


	
	
