

def main(args):
    print("process start")
    camera = PiCamera()
    camera.resolution = (1024, 768)
    camera.start_preview()
    sleep(2)
    camera.capture('foo.jpg')
    camera.close()
    print("process end")
    return 0

if __name__ == '__main__':
    import sys
    from picamera import PiCamera
    from time import sleep 
    sys.exit(main(sys.argv))
