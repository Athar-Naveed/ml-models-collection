import os
import requests
from dotenv import load_dotenv
from ..models.weather_prediction import WeatherPrediction
class Weather:
    def __init__(self):
        load_dotenv()   
        self.rapid_api_key = os.getenv("RAPID_API_KEY")
        
        
        if not self.rapid_api_key:
            raise ValueError("RAPID_API_KEY environment variable is not set")
        self.lat = 0.0
        self.lon = 0.0
        self.city = ""
        self.weather = WeatherPrediction()
        
    def getLocation(self, ip):
        try:
            url = f"https://ip-to-location-geolocation-by-ip.p.rapidapi.com/{ip}"
            print(f"self rapid api key: {self.rapid_api_key}")
            headers = {
                "x-rapidapi-key": self.rapid_api_key,
                "x-rapidapi-host": "ip-to-location-geolocation-by-ip.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers)

            print(response.json())
            location_data = response.json()
            if 'lat' not in location_data or 'lon' not in location_data or 'city' not in location_data:
                raise ValueError("Missing required location data in API response")
                
            self.lat = location_data['lat']
            self.lon = location_data['lon']
            self.city = location_data['city']
            
            condition_code = self.get_current_weather(self.lat, self.lon)
            
            self.weather.get_weather_history(self.lat,self.lon)
            
            
            return {"condition": condition_code, "city": self.city}
            
        except requests.RequestException as e:
            raise Exception(f"Error fetching location data: {str(e)}")
        except ValueError as e:
            raise Exception(f"Error processing location data: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error in getLocation: {str(e)}")

    def get_current_weather(self, lat, lon):
        try:
            url = "https://easy-weather1.p.rapidapi.com/current/basic"

            querystring = {"latitude": lat, "longitude": lon}

            headers = {
                "x-rapidapi-key": self.rapid_api_key,
                "x-rapidapi-host": "easy-weather1.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers, params=querystring)
            response.raise_for_status()  # Raises exception for 4XX/5XX responses
            
            weather_data = response.json()
            if 'currentWeather' not in weather_data or 'conditionCode' not in weather_data['currentWeather']:
                raise ValueError("Missing weather condition code in API response")
                
            condition_code = weather_data['currentWeather']['conditionCode']
            
            return condition_code
            
        except requests.RequestException as e:
            raise Exception(f"Error fetching weather data: {str(e)}")
        except ValueError as e:
            raise Exception(f"Error processing weather data: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error in get_current_weather: {str(e)}")