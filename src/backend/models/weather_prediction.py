import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from datetime import datetime, timedelta


class WeatherPrediction:
    def __init__(self):
        try:
            # Setup the Open-Meteo API client with cache and retry on error
            self.cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
            self.retry_session = retry(self.cache_session, retries=5, backoff_factor=0.2)
            self.openmeteo = openmeteo_requests.Client(session=self.retry_session)
            self.url = "https://archive-api.open-meteo.com/v1/archive"
        except Exception as e:
            raise Exception(f"Error initializing WeatherPrediction: {str(e)}")

    def get_weather_history(self, lat, lon):
            current_date = datetime.now()
            end_date = (current_date - timedelta(days=2)).strftime("%Y-%m-%d")  # Yesterday
            start_date = (current_date - timedelta(days=7)).strftime("%Y-%m-%d")  # 8 days ago
            params = {
    "latitude": lat,
    "longitude": lon,
    "start_date": start_date,
    "end_date": end_date,
    "daily": "temperature_2m_max",
    }
            responses = self.openmeteo.weather_api(self.url, params=params)

            # Process first location. Add a for-loop for multiple locations or weather models
            daily = responses[0].Daily()
            daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()

            daily_data = {
                "date": pd.date_range(
                    start=pd.to_datetime(daily.Time(), unit="s", utc=True).tz_localize(None),
                    end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True).tz_localize(None),
                    freq=pd.Timedelta(seconds=daily.Interval()),
                    inclusive="left"
                )
            }

            daily_data["temperature_2m_max"] = daily_temperature_2m_max.astype(int)

            daily_dataframe = pd.DataFrame(data=daily_data)
            
            self.weather_prediction_model(daily_dataframe)

    def weather_prediction_model(self,df):
         from sklearn.model_selection import train_test_split
         x = df['date']
         y = df['temperature_2m_max']
         x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
         print(x)
         print(y)
