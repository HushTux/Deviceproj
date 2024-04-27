from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

# Global variable to store sensor data
sensor_data = {'temperature': 'No data', 'humidity': 'No data'}

# Your weather API key and base URL
api_key = ""
weather_api_url = "http://api.weatherapi.com/v1/current.json"


@app.route('/')
def index():
    global sensor_data
    location = ""  # Set this to your desired location
    params = {'key': api_key, 'q': location}

    # Fetch weather data from the weather API
    weather_response = requests.get(weather_api_url, params=params)
    weather_data = weather_response.json()

    # Combine sensor data and weather data to pass to the template
    data = {'sensor': sensor_data, 'weather': weather_data}

    return render_template('index.html', data=data)


@app.route('/update', methods=['POST'])
def update_sensor_data():
    global sensor_data
    sensor_data = request.get_json()
    print(f"Received data: {sensor_data}")
    return jsonify({'status': 'success'}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
