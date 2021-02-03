def main(args):
	try:
		I = 40
		O = 3
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(O,GPIO.OUT)
		GPIO.setup(I,GPIO.IN,GPIO.PUD_DOWN)
		GPIO.output(O,GPIO.HIGH)
		while True:
			time.sleep(2)
			print(GPIO.input(I))
	finally:
		GPIO.cleanup()
	return 0 
if __name__ == '__main__':
    import sys
    import  RPi.GPIO as GPIO 
    import time
    sys.exit(main(sys.argv))

