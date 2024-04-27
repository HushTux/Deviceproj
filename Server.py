from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    # Replace 'your_api_key' with the actual API key and 'Your_Location' with your location.
    api_url = "http://api.weatherapi.com/v1/current.json"
    api_key = ""
    location = ""
    params = {
        'key': api_key,
        'q': location
    }
    weather_response = requests.get(api_url, params=params)
    weather_data = weather_response.json()

    # Here you would actually integrate with your sensor to get these readings.
    # This is placeholder data.
    temperature = 25
    humidity = 50

    return render_template('index.html',
                           temperature=temperature,
                           humidity=humidity,
                           weather=weather_data)

if __name__ == '__main__':
    app.run(debug=True)
