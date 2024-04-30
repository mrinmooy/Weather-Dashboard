from flask import Flask, send_from_directory, request, jsonify, redirect
import os
import requests
# from flask_cors import CORS


app = Flask(__name__, static_folder='.')

API_KEY = '8600f8cf4b9c8244a4d2eacf7c7ca399'

@app.route('/')
def index():
    # return send_from_directory('.', 'index.html')
    return redirect("http://18.215.182.190/")

@app.route('/<path:path>')
def send_files(path):
    return send_from_directory('.', path)

@app.route('/weather', methods=['GET'])
def weather():
    city = request.args.get('city')
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    if data.get('cod') != 200:
        return jsonify({'error': 'City not found'}), 404
    weather = {
        'city': city,
        'temperature': data['main']['temp'],
        'description': data['weather'][0]['description'],
        'icon': data['weather'][0]['icon']
    }
    return jsonify(weather)

if __name__ == '__main__':
    app.run(debug=True)
