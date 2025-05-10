from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()
app = Flask(__name__)

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/weather')
def get_weather():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    city = request.args.get('city')
    forecast = request.args.get('forecast')
    history = request.args.get('history')

    if city:
        query = city
    elif lat and lon:
        query = f"{lat},{lon}"
    else:
        return jsonify({'error': 'Invalid request'}), 400

    # Current weather URL
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={query}"

    if forecast:
        # Forecast URL (up to 3 days)
        url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={query}&days=3"
        return get_forecast(url)

    if history:
        # Historical weather URL
        try:
            date = datetime.strptime(history, "%Y-%m-%d")
        except ValueError:
            return jsonify({'error': 'Invalid date format'}), 400
        url = f"http://api.weatherapi.com/v1/history.json?key={WEATHER_API_KEY}&q={query}&dt={date.strftime('%Y-%m-%d')}"
        return get_history(url)

    res = requests.get(url).json()

    try:
        city_name = res["location"]["name"]
        lat = res["location"]["lat"]
        lon = res["location"]["lon"]

        return jsonify({
            "name": city_name,
            "lat": lat,
            "lon": lon,
            "temp": res["current"]["temp_c"],
            "humidity": res["current"]["humidity"],
            "wind": res["current"]["wind_kph"],
            "description": res["current"]["condition"]["text"],
            "rain": res["current"].get("precip_mm", "No data"),
            "thunder": "thunder" in res["current"]["condition"]["text"].lower(),
            "storm": "storm" in res["current"]["condition"]["text"].lower()
        })
    except Exception as e:
        print(e)
        return jsonify({'error': 'Could not parse weather data'}), 500

def get_forecast(url):
    res = requests.get(url).json()
    try:
        city_name = res["location"]["name"]  # Get the city name
        forecast_data = []
        for day in res["forecast"]["forecastday"]:
            forecast_data.append({
                "date": day["date"],
                "temp": day["day"]["avgtemp_c"],
                "humidity": day["day"]["avghumidity"],
                "description": day["day"]["condition"]["text"],
                "rain": day["day"].get("totalprecip_mm", "No data"),
                "wind": day["day"]["maxwind_kph"]
            })
        return jsonify({
            "name": city_name,
            "forecast": forecast_data
        })
    except Exception as e:
        print(e)
        return jsonify({'error': 'Could not get forecast data'}), 500


def get_history(url):
    res = requests.get(url).json()
    try:
        city_name = res["location"]["name"]  # Get the city name
        history_data = {
            "date": res["forecast"]["forecastday"][0]["date"],
            "temp": res["forecast"]["forecastday"][0]["day"]["avgtemp_c"],
            "humidity": res["forecast"]["forecastday"][0]["day"]["avghumidity"],
            "description": res["forecast"]["forecastday"][0]["day"]["condition"]["text"],
            "rain": res["forecast"]["forecastday"][0]["day"].get("totalprecip_mm", "No data"),
            "wind": res["forecast"]["forecastday"][0]["day"]["maxwind_kph"]
        }
        return jsonify({
            "name": city_name,
            "history": history_data
        })
    except Exception as e:
        print(e)
        return jsonify({'error': 'Could not get historical data'}), 500


if __name__ == '__main__':
    app.run(debug=True)
