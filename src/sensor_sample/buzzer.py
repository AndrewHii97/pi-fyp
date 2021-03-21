def main(args):
	try:
		BUZZ = 13
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(BUZZ,GPIO.OUT)
		p = GPIO.PWM(BUZZ, 60)
		p.start(50)
		sleep(10)
	finally:
		GPIO.cleanup()
		
if __name__ == '__main__':
    import sys
    import  RPi.GPIO as GPIO 
    from time import sleep
    sys.exit(main(sys.argv))
