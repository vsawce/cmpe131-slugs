import requests
import json
import datetime
import pprint
general_data = {}
# Get weather forecast for next week.
# forecast  returns object that includes: temperature, weather, timestamp, weekday
WEATHER_URL = "https://api.openweathermap.org/data/3.0/onecall?lat=37.335480&lon=-121.893028&appid=eb584b1f51c58eeaf838fba4e2997f46&exclude=current,minutely,hourly,alerts"
WEEKDAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
weather_params = {
    "units": "imperial"
}

weather_data = requests.get(
    WEATHER_URL,
    params=weather_params
);

weather = json.loads(weather_data.content)

day = weather["daily"][0]
dt = datetime.datetime.fromtimestamp(day["dt"])
timestamp = dt.strftime("%m/%d/%Y, %H:%M:%S")
weekday = WEEKDAYS[dt.weekday()]
day_data = {
    "temperature": day["temp"]["day"],
    "condition": day["weather"][0]["main"],
}
general_data["weather"] = day_data

# Get nearby transit stop leaving times
# Returns array of nearby transit stops as objects, including their route #'s, and leaving times
TRANSIT_URL = "https://transit.hereapi.com/v8/departures?ids=401902823,718301021&maxPerBoard=1&apiKey=c6TZkG4BVXmMloUipnKq8GepDwFL2eNaGLzvywjeAPU"
transit_response = requests.get(TRANSIT_URL)
upcoming_stops = json.loads(transit_response.content)
transit_data = []
for board in upcoming_stops["boards"]:
    time_unformatted= board["departures"][0]["time"][0:-6]
    time = datetime.datetime.strptime(time_unformatted, '%Y-%m-%dT%H:%M:%S')
    difference_in_seconds = (time - datetime.datetime.now()).total_seconds()
    difference_in_minutes = divmod(difference_in_seconds, 60)
    display_minutes = ("99+", str(difference_in_minutes[0])[:-2]) [difference_in_minutes[0] < 99]
    transit_data.append(board["departures"][0]["transport"]["shortName"] + ": " + display_minutes)
general_data["transit"] = transit_data

print(json.dumps(general_data, indent=4))