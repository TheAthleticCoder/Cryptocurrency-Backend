from flask import Flask, json, jsonify
import subprocess
from shared_memory_dict import SharedMemoryDict
import os

import signal
import time
import sys

app = Flask(__name__)

price_cache = SharedMemoryDict(name='tokens', size=1024)

@app.route('/coins', methods=['GET'])
def getCoins():
    print(price_cache)
    response = jsonify(list(price_cache.keys()))
    response.status_code = 200
    return response

@app.route('/coins/price/<coinID>', methods=['GET'])
def getCoinPrice(coinID):
    try:
        price = price_cache[str(coinID)]
    except KeyError:
        response = jsonify("Error: Invalid coinID!")
        response.status_code = 404
        return response

    response = jsonify(price)
    response.status_code = 200

    return response

if __name__ == "__main__":
    app.run(debug=True)
