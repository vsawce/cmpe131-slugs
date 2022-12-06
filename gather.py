import requests
import json
import datetime
import random

general_data = []
# Get weather forecast for next week.
# forecast  returns object that includes: temperature, weather, timestamp, weekday
WEATHER_URL = "https://api.openweathermap.org/data/3.0/onecall?lat=37.335480&lon=-121.893028&appid=eb584b1f51c58eeaf838fba4e2997f46&exclude=minutely,hourly,daily,alerts"
WEEKDAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
weather_params = {
    "units": "imperial"
}

weather_data = requests.get(
    WEATHER_URL,
    params=weather_params
);

weather = json.loads(weather_data.content)
general_data.append(str(weather["current"]["feels_like"])+"F");
general_data.append(weather["current"]["weather"][0]["main"]);

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
    general_data.append(board["departures"][0]["transport"]["shortName"] + ":" + display_minutes)

# Get food of the day
# Will eventually update to datacrawl
dc_menu = ["C.KATSU", "BBQ CHKN", "BEEF STW", "PORK BUN"]
dc_item = dc_menu[random.randint(0, 3)]
general_data.append(dc_item)

# Get parking garage info
general_data.append("N:99%")
general_data.append("S:85%")
general_data.append("SW:79%")

data = "|".join(general_data)
req = requests.put("https://cmpe-led-server.herokuapp.com/update/?data=" + data)
print(req + data)