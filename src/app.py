import requests
import configparser
from flask import Flask, render_template, request


app = Flask(__name__)

@app.route("/", methods=["GET"])
def weather_dashboard():
    return render_template("home.html")

@app.route("/results", methods=["POST"])
def render_results():
    zip_code = request.form["zipCode"] # obedece al "name" que se especifica en el html
    data = get_weather_results(zip_code)
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    weather = data["weather"][0]["main"]
    location = data["name"]
    return render_template("results.html", location=location,
                           weather=weather, temp=temp, feels_like=feels_like)

def get_api_key():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config["openweathermap"]["api"]

def get_weather_results(zip_code):
    api_key = get_api_key()
    api_url = f"https://api.openweathermap.org/data/2.5/weather?zip={zip_code}&units=metrics&appid={api_key}"
    req = requests.get(api_url)
    return req.json()

if __name__ == "__main__":
    app.run(debug=True)
    