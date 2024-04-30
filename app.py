from flask import Flask, send_from_directory, request, jsonify, redirect
import os
import requests
from flask_cors import CORS
import psycopg2
import boto3
from datetime import datetime
import uuid

app = Flask(__name__, static_folder='.')
CORS(app)

API_KEY = '8600f8cf4b9c8244a4d2eacf7c7ca399'

session = boto3.Session(
    aws_access_key_id='AKIA6GBMF4I4QCV5LOZX',
    aws_secret_access_key='qEOiz3R3E5Ku4vnxXrV3R/Q7Cj8bOmthXhtCPmPl',
    region_name='us-east-1'  # e.g., 'us-west-2'
)

# Initialize a DynamoDB client
dynamodb = session.resource('dynamodb')
# Reference your DynamoDB table
table = dynamodb.Table('backend-logging')

def add_log(city):
    # Create a unique ID for each log entry
    log_id = str(uuid.uuid4())
    # Current timestamp
    timestamp = datetime.utcnow().isoformat()

    # Put the log entry into the DynamoDB table
    table.put_item(
        Item={
            'log_id': log_id,
            'city': city,
            'timestamp': timestamp
        }
    )
    print(f"Log added for {city} at {timestamp}")


def create_connection():
    return psycopg2.connect(
        dbname="logs",
        user="mrinmoy",
        password="RsA%9V27",
        host="backend-logging.postgres.database.azure.com",
        port='5432',
        sslmode='require'
    )

def insert_data(city_name, temperature, description):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO weather (city_name, temperature, description)
        VALUES (%s, %s, %s);
    """, (city_name, temperature, description))
    conn.commit()
    cur.close()
    conn.close()


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
    insert_data(city,data['main']['temp'],data['weather'][0]['description']);
    print(city)
    print(data['main']['temp'])
    print(data['weather'][0]['description'])
    add_log(city)
    return jsonify(weather)

if __name__ == '__main__':
    app.run(debug=True)
