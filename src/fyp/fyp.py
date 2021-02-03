import sys
import pathlib
from config import ConfigParser
from fyp_cli import create_fyp_cli



def main(args):
	# remove the first argument which specify the script name 
	if not isinstance(args,type([])):
		args = [args]
	args.pop(0)	
	parsed_args = create_fyp_cli(args)
	config_parser = ConfigParser(parsed_args.file_path)
	config_obj = config_parser.config_obj
	key_path = pathlib.Path(config_obj["private_key"])
	
	


	return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))

