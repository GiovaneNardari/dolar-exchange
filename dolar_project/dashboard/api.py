import requests
from datetime import datetime

r = requests.get('https://economia.awesomeapi.com.br/json/daily/USD-BRL/15')

for data in r.json():
    print(datetime.fromtimestamp(int(data['timestamp'])), float(data['bid']))