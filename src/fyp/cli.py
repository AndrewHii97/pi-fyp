import argparse
import textwrap
import pathlib

def create_fyp_cli(args):
	parser = argparse.ArgumentParser(
		prog='FYP', 
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description=textwrap.dedent(
		"This service is used to:\
		\n \
		\t - Connect RaspberyPi to AWS Iot Core\n\
		\t - Control and manage sensors and devices connected\n"), 
		epilog=textwrap.dedent(
		"Created by: Andrew Hii \t Date: 1st Feb 2021\n")
	)
	parser.add_argument(
		'file_path', 
		metavar='f', 
		type=pathlib.Path, 
		nargs='?',
		default='config.json',
		help='Path to the configuration file'
	)
	return parser.parse_args(args)
