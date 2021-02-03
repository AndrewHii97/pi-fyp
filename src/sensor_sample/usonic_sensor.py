def main(args):
    try: 
        TRIG = 3
        ECHO = 40
        pulse_start = 0
        pulse_end = 0 
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(TRIG,GPIO.OUT)
        GPIO.setup(ECHO,GPIO.IN)
        GPIO.output(TRIG,False)
        print("Waiting for Sensor to Settle")
        time.sleep(2)
        print("Sensor Settle")
        print("Emit wave for 10us")
        GPIO.output(TRIG,True)
        time.sleep(0.00001)
        GPIO.output(TRIG,False)
        pulse_End = time.time() 
        while True : 
            while GPIO.input(ECHO) == 0:
                pulse_start = time.time()
            while GPIO.input(ECHO) == 1:
                pulse_end = time.time()
            print(f"pulse_start:{pulse_start}")
            print(f"pulse_end:{pulse_end}")
            pulse_duration = pulse_end - pulse_start 
            distance = pulse_duration * 17150
            distance = round(distance, 2)
            print(distance)
    finally:
        GPIO.cleanup()
    
    
    return 0

if __name__ == '__main__':
    import sys
    import  RPi.GPIO as GPIO 
    import time
    sys.exit(main(sys.argv))
