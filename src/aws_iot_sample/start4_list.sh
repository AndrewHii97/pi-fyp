set -e 
printf "\nRunning application...\n"
python3 aws-iot-device-sdk-python/samples/basicShadow/basicShadowDeltaListener.py -e a3iz7l1satteal-ats.iot.us-east-1.amazonaws.com  -r root-CA.crt -c my_raspi.cert.pem -k my_raspi.private.key
