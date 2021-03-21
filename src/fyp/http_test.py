import requests 

r = requests.get('http://192.168.0.137:3000/')
print(r.text)
