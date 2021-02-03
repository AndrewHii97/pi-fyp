import json 
import pytest
import pathlib
from pathlib import Path
from src.fyp import config as cf 
from src.fyp import fyp_cli




# test ConfigParser Class 
class TestConfigParser:
	@pytest.fixture 
	def config_parser_valid(self,valid_path):
		return cf.ConfigParser(valid_path)
	
	@pytest.fixture 
	def valid_path(self):
		return Path("test/test_config/test_config.json")

	@pytest.fixture 
	def json_obj(self):
		return {'1':'hello json'}
		
	
	def test_init_e_path(self):
		with pytest.raises((FileNotFoundError,json.JSONDecodeError,SystemExit)):
			test_config_parser = cf.ConfigParser("test_path")
	
	def test_init_v_path_e_json(self):
		with pytest.raises((json.JSONDecodeError,SystemExit)):
			test_config_parser = cf.ConfigParser("test/test_config/error_config.json")

	def test_config_obj(self,config_parser_valid,json_obj):
		assert config_parser_valid.config_obj['1'] == json_obj['1']


class TestCli:
	@pytest.fixture 
	def file_path(self):
		return ["config.json"]
	
	def test_cli_return(self,file_path):
		cli_parser = fyp_cli.create_fyp_cli(file_path)
		assert cli_parser.file_path == pathlib.Path("config.json")
		
		
		
		
		
	
	

		

