## Ncessary Imports
import os
import signal
import requests
import schedule
import time
import json
from pyairtable import Api
from shared_memory_dict import SharedMemoryDict

COINGECKO_BASE_URL = 'https://api.coingecko.com/api/v3'

# NOTE: The environment variable 'AIRTABLE_API_KEY' should contain
# the Personal Access Token for the base with the correct scopes
api = Api(os.environ['AIRTABLE_API_KEY'])

AIRTABLE_NAME = 'insert name of airtable base here'
AIRTABLE_BASE_KEY = 'insert base key here'
table = api.table(AIRTABLE_BASE_KEY, AIRTABLE_NAME)

neededIds = []

def deleteAllRecords():
    records = table.all()
    for record in records:
        table.delete(record['id'])

def updateCoinDetails():
    # Get the top 20 coins from the CoinGeckoAPI
    deleteAllRecords()
    data = requests.get(COINGECKO_BASE_URL + '/coins/markets?vs_currency=usd&per_page=20&page=1')
    # Update the coin details in the airtable database
    json_data = json.loads(data.text)
    total = []
    #emtpy neededIds
    neededIds.clear()
    for item in json_data:
        token_id = item['id']
        neededIds.append(token_id)
        price = item['current_price']
        total.append({'ID': token_id, 'Price': price})
    table.batch_create(total)
    
def updateCoinPrices():
    ids = neededIds
    data = requests.get(COINGECKO_BASE_URL + '/simple/price', params={'ids': ','.join(ids), 'vs_currencies': 'usd'})
    # Update the coin price details in the airtable database
    json_data = data.json()
    for record_id, price_data in json_data.items():
        update_data = {
            'Price': price_data.get('usd', 0),
        }
        table.update(record_id, update_data)

while True:
    #If you need to schedule for minutes, replace seconds with minutes
    schedule.every(10).seconds.do(updateCoinDetails)
    schedule.every(1).seconds.do(updateCoinPrices)

    
