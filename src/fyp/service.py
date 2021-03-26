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
        # logger.debug(f"basic_payload:{payload}")
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
        action = {"file": (file_name, byteio.read(), "image/jpeg")} 
        # logger.info(f"created file payload {action}")
        r = requests.post(f'{self.__ENDPOINT}/device/aws/upload-img',
                        data=payload,files=action)
        return r 

    def update_photos_db(self, file_name): 
        payload = self.__create_payload()
        payload["file_name"] = file_name 
        r = requests.post(f'{self.__ENDPOINT}/device/add-img',data=payload)
        return r 

    # function to detect number of person in the image 
    def count_persons(self, file_name): 
        payload = self.__create_payload()
        payload["fileName"] = file_name
        r = requests.post(f'{self.__ENDPOINT}/device/aws/count-persons',data=payload)
        return r

    def count_faces(self, file_name): 
        payload = self.__create_payload()
        payload["fileName"] = file_name 
        r = requests.post(f'{self.__ENDPOINT}/device/aws/count-faces',data=payload)
        return r 

    def search_faces(self, file_name):
        payload = self.__create_payload()
        payload["fileName"] = file_name
        r = request.post(f'{self.__ENDPOINT}/device/aws/search-faces',data=payload)
        return r 
    
