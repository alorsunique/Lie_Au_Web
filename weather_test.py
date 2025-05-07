import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

from datetime import datetime


import matplotlib.pyplot as plt

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)


#9.30, 123.31 Dumaguete
#14.65, 121.07 UPD


# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": 9.30,
	"longitude": 123.21,
	"daily": ["weather_code", "sunrise", "sunset"],
	"hourly": ["temperature_2m", "weather_code", "relative_humidity_2m", "apparent_temperature", "rain", "precipitation_probability"],
	"current": ["temperature_2m", "weather_code"],
	"timezone": "auto",
	"forecast_days": 3
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()}{response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

# Current values. The order of variables needs to be the same as requested.
current = response.Current()
current_temperature_2m = current.Variables(0).Value()
current_weather_code = current.Variables(1).Value()

print(f"Current time {current.Time()}")

print(f"Formatted Time: {datetime.fromtimestamp(current.Time())}")

print(f"Current temperature_2m {current_temperature_2m}")
print(f"Current weather_code {current_weather_code}")

# Process hourly data. The order of variables needs to be the same as requested.
hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_weather_code = hourly.Variables(1).ValuesAsNumpy()
hourly_relative_humidity_2m = hourly.Variables(2).ValuesAsNumpy()
hourly_apparent_temperature = hourly.Variables(3).ValuesAsNumpy()
hourly_rain = hourly.Variables(4).ValuesAsNumpy()
hourly_precipitation_probability = hourly.Variables(5).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
)}

hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["weather_code"] = hourly_weather_code
hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
hourly_data["apparent_temperature"] = hourly_apparent_temperature
hourly_data["rain"] = hourly_rain
hourly_data["precipitation_probability"] = hourly_precipitation_probability

hourly_dataframe = pd.DataFrame(data = hourly_data)
print(hourly_dataframe)

# Process daily data. The order of variables needs to be the same as requested.
daily = response.Daily()
daily_weather_code = daily.Variables(0).ValuesAsNumpy()
daily_sunrise = daily.Variables(1).ValuesInt64AsNumpy()
daily_sunset = daily.Variables(2).ValuesInt64AsNumpy()

daily_data = {"date": pd.date_range(
	start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
	end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = daily.Interval()),
	inclusive = "left"
)}

daily_data["weather_code"] = daily_weather_code
daily_data["sunrise"] = daily_sunrise
daily_data["sunset"] = daily_sunset

daily_dataframe = pd.DataFrame(data = daily_data)
print(daily_dataframe)





date_list = []
temp_list = []
humid_list = []
apparent_temp_list = []
rain_prob_list = []

for index, row in hourly_dataframe.iterrows():
	print(row)

	date_time = row['date']
	date_list.append(date_time)



	current_temperature = row['temperature_2m']
	temp_list.append(current_temperature)


	current_humidity = row['relative_humidity_2m']
	humid_list.append(current_humidity)



	apparent_temperature = row['apparent_temperature']
	apparent_temp_list.append(apparent_temperature)

	rain_prob = row['precipitation_probability']
	rain_prob_list.append(rain_prob)

plt.ylim(0,100)
plt.plot(date_list, temp_list, label="Temp")
plt.plot(date_list, humid_list, label="Humid")
plt.plot(date_list, apparent_temp_list, label="App Temp")
plt.plot(date_list, rain_prob_list, label="rain_prob")
plt.legend()
plt.show()

weather_codes = {
    0: "Clear sky",
    1: "Mainly clear, partly cloudy, and overcast",
    2: "Mainly clear, partly cloudy, and overcast",
    3: "Mainly clear, partly cloudy, and overcast",
    45: "Fog and depositing rime fog",
    48: "Fog and depositing rime fog",
    51: "Drizzle: Light, moderate, and dense intensity",
    53: "Drizzle: Light, moderate, and dense intensity",
    55: "Drizzle: Light, moderate, and dense intensity",
    56: "Freezing Drizzle: Light and dense intensity",
    57: "Freezing Drizzle: Light and dense intensity",
    61: "Rain: Slight, moderate and heavy intensity",
    63: "Rain: Slight, moderate and heavy intensity",
    65: "Rain: Slight, moderate and heavy intensity",
    66: "Freezing Rain: Light and heavy intensity",
    67: "Freezing Rain: Light and heavy intensity",
    71: "Snow fall: Slight, moderate, and heavy intensity",
    73: "Snow fall: Slight, moderate, and heavy intensity",
    75: "Snow fall: Slight, moderate, and heavy intensity",
    77: "Snow grains",
    80: "Rain showers: Slight, moderate, and violent",
    81: "Rain showers: Slight, moderate, and violent",
    82: "Rain showers: Slight, moderate, and violent",
    85: "Snow showers slight and heavy",
    86: "Snow showers slight and heavy",
    95: "Thunderstorm: Slight or moderate",
    96: "Thunderstorm with slight and heavy hail",
    99: "Thunderstorm with slight and heavy hail"
}

daily_code_list = []

for index, row in daily_dataframe.iterrows():
	print(row)
	daily_code_list.append(row['weather_code'])

print(daily_code_list)

print(weather_codes[daily_code_list[0]])

formatted_string = (f"Weather for today: {weather_codes[daily_code_list[0]]}\n"
					f"Weather for tomorrow: {weather_codes[daily_code_list[1]]}\n"
					f"Weather for the day after: {weather_codes[daily_code_list[2]]}\n")

print(formatted_string)

with open("outputweather.txt", "w") as file:
    file.write(formatted_string)