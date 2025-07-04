import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

from datetime import datetime, timedelta
from datetime import timezone

import matplotlib.pyplot as plt


from pathlib import Path
import yaml

import os

import json

import time



def find_project_root(script_path, marker):
    current_path = script_path
    while not (current_path / marker).exists():
        # If block checks for parent of current path
        # If it cannot go up any further, base directory is reached
        if current_path.parent == current_path:
            raise FileNotFoundError(f"Could not find '{marker}' in any parent directories.")

        current_path = current_path.parent

    # If it exits the while loop, marker was found
    return current_path








def get_current_values(response, weather_code_dict):
	current = response.Current()
	current_temperature_2m = current.Variables(0).Value()
	current_weather_code = current.Variables(1).Value()

	string_weather_code = weather_code_dict[current_weather_code]

	return current_temperature_2m,string_weather_code






def quarter_day_forecast(response, current_datetime_object):

	current_datetime_object = current_datetime_object.astimezone(timezone.utc)

	hourly = response.Hourly()
	hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
	hourly_weather_code = hourly.Variables(1).ValuesAsNumpy()
	hourly_relative_humidity_2m = hourly.Variables(2).ValuesAsNumpy()
	hourly_apparent_temperature = hourly.Variables(3).ValuesAsNumpy()
	hourly_rain = hourly.Variables(4).ValuesAsNumpy()
	hourly_precipitation_probability = hourly.Variables(5).ValuesAsNumpy()

	hourly_data = {"date": pd.date_range(
		start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
		end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
		freq=pd.Timedelta(seconds=hourly.Interval()),
		inclusive="left"
	)}

	hourly_data["temperature_2m"] = hourly_temperature_2m
	hourly_data["weather_code"] = hourly_weather_code
	hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
	hourly_data["apparent_temperature"] = hourly_apparent_temperature
	hourly_data["rain"] = hourly_rain
	hourly_data["precipitation_probability"] = hourly_precipitation_probability

	hourly_dataframe = pd.DataFrame(data=hourly_data)

	base_hour = current_datetime_object.replace(minute=0, second=0, microsecond=0)

	count = 0
	max_hours = 6

	hour_list = []

	while count <= max_hours:
		hour_list.append(base_hour + timedelta(hours=count))
		count += 1

	mask_time = (hourly_dataframe['date'] >= hour_list[0]) & (hourly_dataframe['date'] <= hour_list[-1])
	filtered_df = hourly_dataframe.loc[mask_time]

	print(filtered_df)

	for index, row in filtered_df.iterrows():
		print(row)

	return filtered_df


# Main
def main():
	config_file_name = 'Lie_Au_Web_config.yaml'
	script_path = Path(__file__).resolve()
	project_dir = find_project_root(script_path, config_file_name)

	config_file_path = project_dir / config_file_name

	with open(config_file_path, "r") as open_config:
		config_content = yaml.safe_load(open_config)

	resources_dir = Path(config_content['resources_dir'])
	daily_report_dir = resources_dir / "Daily Report"

	weather_code = {
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

	location_dict = {
		'Dumaguete': {
			'latitude': 9.30,
			'longitude': 123.21,
		},
		'UPD': {
			'latitude': 14.65,
			'longitude': 121.07,
		},
	}


	# Setup the Open-Meteo API client with cache and retry on error
	cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
	retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
	openmeteo = openmeteo_requests.Client(session=retry_session)




	location_value = 'Dumaguete'

	# Make sure all required weather variables are listed here
	# The order of variables in hourly or daily is important to assign them correctly below
	url = "https://api.open-meteo.com/v1/forecast"
	params = {
		"latitude": location_dict[location_value]['latitude'],
		"longitude": location_dict[location_value]['longitude'],
		"daily": ["weather_code", "sunrise", "sunset"],
		"hourly": ["temperature_2m", "weather_code", "relative_humidity_2m", "apparent_temperature", "rain",
				   "precipitation_probability"],
		"current": ["temperature_2m", "weather_code"],
		"timezone": "auto",
		"forecast_days": 3
	}
	responses = openmeteo.weather_api(url, params=params)
	response = responses[0]


	print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
	print(f"Elevation {response.Elevation()} m asl")


	current_temp, expected_weather = get_current_values(response,weather_code)

	output_dict = {
		'Temperature': current_temp,
		'Expected Weather': expected_weather,
	}

	print(output_dict)

	output_json_path = daily_report_dir / "Output_JSON.json"

	if output_json_path.exists():
		os.remove(output_json_path)

	with open(output_json_path, "w") as output_json:
		json.dump(output_dict, output_json)



	current_datetime_object = datetime.fromtimestamp(time.time())

	day_df = quarter_day_forecast(response,current_datetime_object)

	day_temp_list = []

	for index, row in day_df.iterrows():
		print(row)

		day_time = str(row['date'])
		day_app_temp = str(row['apparent_temperature'])
		day_rel_humid = str(row['relative_humidity_2m'])
		day_rain_change = str(row['precipitation_probability'])

		day_pack = [day_time, day_app_temp, day_rel_humid, day_rain_change]
		day_temp_list.append(day_pack)

	output_json_path = daily_report_dir / "quarter_Output_JSON.json"

	if output_json_path.exists():
		os.remove(output_json_path)

	with open(output_json_path, "w") as output_json:
		json.dump(day_temp_list, output_json)




	# Process hourly data. The order of variables needs to be the same as requested.
	hourly = response.Hourly()
	hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
	hourly_weather_code = hourly.Variables(1).ValuesAsNumpy()
	hourly_relative_humidity_2m = hourly.Variables(2).ValuesAsNumpy()
	hourly_apparent_temperature = hourly.Variables(3).ValuesAsNumpy()
	hourly_rain = hourly.Variables(4).ValuesAsNumpy()
	hourly_precipitation_probability = hourly.Variables(5).ValuesAsNumpy()

	hourly_data = {"date": pd.date_range(
		start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
		end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
		freq=pd.Timedelta(seconds=hourly.Interval()),
		inclusive="left"
	)}

	hourly_data["temperature_2m"] = hourly_temperature_2m
	hourly_data["weather_code"] = hourly_weather_code
	hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
	hourly_data["apparent_temperature"] = hourly_apparent_temperature
	hourly_data["rain"] = hourly_rain
	hourly_data["precipitation_probability"] = hourly_precipitation_probability

	hourly_dataframe = pd.DataFrame(data=hourly_data)
	print(hourly_dataframe)







if __name__ == "__main__":
	main()

