import requests
import json

data = {
    'Password': 'Njkfesbhd',
}

url = 'http://influencerhiring.com/convertrates/'

try:
    response = requests.post(url=url, data=json.dumps(data))
except:
    print("Rates not exchanged from api.")
