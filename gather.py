import requests
import json
import datetime
api_url = "https://api.openweathermap.org/data/3.0/onecall?lat=37.335480&lon=-121.893028&appid=eb584b1f51c58eeaf838fba4e2997f46&exclude=current,minutely,hourly,alerts"
WEEKDAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
weather_params = {
    "units": "imperial"
}

weather_data = requests.get(
    api_url,
    params=weather_params
);

weather = json.loads(weather_data.content)
weather_str = json.dumps(weather, indent=4)

forecast = [];
for day in weather["daily"]:
    dt = datetime.datetime.fromtimestamp(day["dt"])
    timestamp = dt.strftime("%m/%d/%Y, %H:%M:%S")
    weekday = WEEKDAYS[dt.weekday()]
    day_data = {
        "temperature": day["temp"]["day"],
        "weather": day["weather"][0]["main"],
        "datetime_stamp": timestamp,
        "weekday": weekday
    }
    forecast.append(day_data);


