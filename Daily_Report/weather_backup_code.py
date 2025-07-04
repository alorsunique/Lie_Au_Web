# just backup

time.sleep(10000)





#9.30, 123.31 Dumaguete
#14.65, 121.07 UPD




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

with open("../outputweather.txt", "w") as file:
    file.write(formatted_string)