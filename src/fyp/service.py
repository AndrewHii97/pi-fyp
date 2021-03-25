import logging 
import requests 

logging.basicConfig(level=logging.NOTSET) 
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Client(): 
    def __init__(self,endpoint,device_name,password):
        self.__ENDPOINT = endpoint
        self.__DEVICE_NAME = device_name 
        self.__PASSWORD = password
    
    def __create_payload(self): 
        payload = {'device_name':self.__DEVICE_NAME,
            'password':self.__PASSWORD} 
        logger.debug(f"basic_payload:{payload}")
        return payload

    # return list of person owning the key 
    def check_rfid(self,rfid): 
        payload = self.__create_payload() 
        payload["rfid"]= rfid 
        logger.info("include RFID in payload")
        logger.debug(f"updated_payload{payload}") 
        r = requests.post(f'{self.__ENDPOINT}/device/rfid-check',data=payload)
        return r

    # function upload images to aws storage
    def upload_images(self, file_name, byteio):
        payload = self.__create_payload()
        file_name = file_name + ".jpg"
        action = {"file": (file_name, byteio.read(), "image/jpeg")} 
        logger.info(f"created file payload {action}")
        r = requests.post(f'{self.__ENDPOINT}/device/aws/upload-img',
                data=payload,files=action)
        return r 
