import json

from flask import Flask, jsonify, request

from LocationDetector import LocationDetector


application = Flask(__name__)
location_detector = LocationDetector()


@application.route('/api/v1.0/predictions', methods=['POST'])
def create_prediction():
    data = request.data or '{}'
    body = json.loads(data)
    print(f'Service received request with payload: {body}')
    
    input_text = body['data']['ndarray']
    result = location_detector.predict(input_text, 'text')
    print(f'Model returned prediction: {result}')
    
    return jsonify(result)
