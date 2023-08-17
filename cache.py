import signal
import sys
import json
import requests
from shared_memory_dict import SharedMemoryDict
from airtable import Airtable
from pyairtable import Api
import os


# Creating shared memory dictionary
price_cache = SharedMemoryDict(name='tokens', size=1024)

# Signal handler function to clear shared memory on exit
def sigint_handler(signal, frame):
    del price_cache
    sys.exit(0)
signal.signal(signal.SIGINT, sigint_handler)

# Fetch data from the CoinGecko API 
data = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&per_page=20&page=1")
data = json.loads(data.text)

# Organize data from CoinGecko API and store it
organized_data = {}
for item in data:
    token_id = item['id']
    organized_data[token_id] = {
        'price': item['current_price'],
    }

# Update shared memory with organized data
price_cache.update(organized_data)
print(price_cache)
