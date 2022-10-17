import json
import os
import random

from flask import Flask, request
from geopy.geocoders import Nominatim
from requests import post


app = Flask(__name__)
endpoint = os.environ.get('LOCATION_DETECTOR_ENDPOINT')
prediction_url = f'http://{endpoint}/api/v1.0/predictions'


@app.route('/')
def home():
    return 'use /get_loc?text="...." to use this service'


def to_request_body(text):
    payload = {'data': {'names': [], 'ndarray': [text]}}
    print(f'Prepared detection request payload: {payload}')
    return payload


def get_locations(request_body):
    try:
        response = post(prediction_url, json=request_body)
    except:
        print(f'Error: Failed to send request to location detector at {prediction_url}')
        return None
    try:
        response_body = response.json()
        print(f'Received response body: {response_body}')
    except:
        print(f'Error: Failed to read response body.')
        return None
    locations = response_body['data']['ndarray']
    print(f'Extracted locations from text: {locations}')
    return locations


def detect_locations(text):
    request_body = to_request_body(text)
    locations = get_locations(request_body)
    return locations


@app.route('/get_loc')
def get_coords():
    text = request.args.get('text')
    locations = detect_locations(text)
    locs_dict = {}
    if locations:
        geolocator = Nominatim(user_agent='my_app')
        for idx, location in enumerate(locations):
            try:
                loc = geolocator.geocode(location)
                lat = loc.latitude
                long = loc.longitude
                locs_dict[idx+1] = {
                    'extracted location': location,
                    'generated address': loc.address,
                    'latitude': lat - random.uniform(0.05, 2),
                    'longitude': long + random.uniform(0.05, 2)
                }
                print(f'found lat & long for this location: {location}', flush=True)
            except:
                print(f'not found lat & long for this location: {location}', flush=True)
        jsonDict = json.dumps(locs_dict)
    else:
        print('Not found any location in this text', flush=True)
        jsonDict = {
            '1': {
                'extracted location': 'none',
                'generated address': 'Brisbane City, Queensland, Australia',
                'latitude': 0.4689682 - random.uniform(0.1, 5),
                'longitude': -30.0234991 + random.uniform(0.1, 5)
            }
        }

    return jsonDict, 200, {'Content-Type': 'application/json; charset=utf-8'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)