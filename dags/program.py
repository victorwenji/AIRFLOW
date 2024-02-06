import requests
import json
from hdfs import InsecureClient
from datetime import datetime

current_date = datetime.now()
current_date_as_str_time = current_date.strftime('%Y-%m-%d')
heure_en_temps_reel = current_date.strftime('%H_%M_%S')

def meteo_data() : 
    # Fetch forecast data
    response_forecast = requests.get('https://api.openweathermap.org/data/2.5/forecast?q=limoges,FR1&appid=eea045ed57d81cb0b2ad92319810b8c6')

    if response_forecast.status_code == 200:
        data_forecast = response_forecast.json()

        json_file_path_forecast = f'/user/datalake/meteobrut/Datajours4/{current_date_as_str_time}.json'  # Adjust the HDFS path

        # Write to HDFS
        client_forecast = InsecureClient('http://localhost:9870', user='hadoop')
        with client_forecast.write(json_file_path_forecast, overwrite=True) as writer_forecast:
            json.dump(data_forecast, writer_forecast, indent=2)

        print(f"Forecast data has been saved to {json_file_path_forecast} on HDFS")
    else:
        print(f"Failed to fetch forecast data with status code: {response_forecast.status_code}")

    # Fetch current weather data
    response_current = requests.get('https://api.openweathermap.org/data/2.5/weather?q=limoges,FR&appid=a09da6bb2e938eeb1997fff56f6d14c2')

    if response_current.status_code == 200:
        data_current = response_current.json()

        json_file_path_current = f'/user/datalake/meteobrut/DataCurrent/{current_date_as_str_time}/{heure_en_temps_reel}.json'  # Adjust the HDFS path

        # Write to HDFS
        client_current = InsecureClient('http://localhost:9870', user='hadoop')
        with client_current.write(json_file_path_current, overwrite=True) as writer_current:
            json.dump(data_current, writer_current, indent=2)

        print(f"Current weather data has been saved to {json_file_path_current} on HDFS")
    else:
        print(f"Failed to fetch current weather data with status code: {response_current.status_code}")

def ingest_meteo():
    meteo_data()