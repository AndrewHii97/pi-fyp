def main(args):
    print("process start")
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(32,GPIO.OUT)
    GPIO.setup(36,GPIO.OUT)
    GPIO.setup(38,GPIO.OUT)
    GPIO.setup(40,GPIO.OUT)
    for x in range(1):
        GPIO.output(32,GPIO.HIGH)
        GPIO.output(36,GPIO.LOW)
        GPIO.output(38,GPIO.LOW)
        GPIO.output(40,GPIO.LOW)
        sleep(0.2)
    
        GPIO.output(32,GPIO.LOW)
        GPIO.output(36,GPIO.HIGH)
        GPIO.output(38,GPIO.LOW)
        GPIO.output(40,GPIO.LOW)
        sleep(0.2)
    
        GPIO.output(32,GPIO.LOW)
        GPIO.output(36,GPIO.LOW)
        GPIO.output(38,GPIO.HIGH)
        GPIO.output(40,GPIO.LOW)
        sleep(0.2)
    
        GPIO.output(32,GPIO.LOW)
        GPIO.output(36,GPIO.LOW)
        GPIO.output(38,GPIO.LOW)
        GPIO.output(40,GPIO.HIGH)
        sleep(0.2)
        
    GPIO.cleanup()
    print("process end")
    return 0
    
if __name__ == '__main__':
    import sys
    import  RPi.GPIO as GPIO 
    sys.exit(main(sys.argv))
