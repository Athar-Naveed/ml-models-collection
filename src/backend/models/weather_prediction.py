import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from datetime import datetime, timedelta
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
import math

class WeatherPrediction:
    def __init__(self):
        try:
            self.cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
            self.retry_session = retry(self.cache_session, retries=5, backoff_factor=0.2)
            self.openmeteo = openmeteo_requests.Client(session=self.retry_session)
            self.url = "https://archive-api.open-meteo.com/v1/archive"
        except Exception as e:
            raise Exception(f"Error initializing WeatherPrediction: {str(e)}")

    def get_weather_history(self, lat, lon):
        current_date = datetime.now()
        end_date = (current_date - timedelta(days=2)).strftime("%Y-%m-%d")
        start_date = (current_date - timedelta(days=7)).strftime("%Y-%m-%d")
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": start_date,
            "end_date": end_date,
            "daily": "temperature_2m_max",
        }
        responses = self.openmeteo.weather_api(self.url, params=params)

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

        responce=self.weather_prediction_model(daily_dataframe)
        print(f"responce{responce}")
        return responce

    def weather_prediction_model(self, df):
        df['date_ordinal'] = df['date'].map(pd.Timestamp.toordinal)

        X = df['date_ordinal'].values.reshape(-1, 1).astype(np.float32)
        y = df['temperature_2m_max'].values.astype(np.float32)

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        X_tensor = torch.tensor(X_scaled)
        y_tensor = torch.tensor(y).view(-1, 1)

        model = nn.Sequential(
            nn.Linear(1, 16),
            nn.ReLU(),
            nn.Linear(16, 1)
        )

        criterion = nn.MSELoss()
        optimizer = optim.Adam(model.parameters(), lr=0.01)

        epochs = 200
        for epoch in range(epochs):
            model.train()
            optimizer.zero_grad()
            outputs = model(X_tensor)
            loss = criterion(outputs, y_tensor)
            loss.backward()
            optimizer.step()

            if (epoch+1) % 50 == 0:
                print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}')

        model.eval()
        predicted = model(X_tensor).detach().numpy()

        # Calculate Accuracy Metrics
        mae = mean_absolute_error(y, predicted)
        mse = mean_squared_error(y, predicted)
        rmse = math.sqrt(mse)

        # Display Results
        print("\n✅ Training Complete")
        print("📊 Actual temperatures:", y)
        print("🤖 Predicted temperatures:", predicted.flatten())
        print(f"📈 MAE: {mae:.2f}")
        print(f"📉 MSE: {mse:.2f}")
        print(f"📊 RMSE: {rmse:.2f}")
        print(f"working")

        return {
            "actual_temps":y.tolist(),
            "predicted_temps":predicted.flatten().tolist()
        }
        # Save Model
        torch.save(model.state_dict(), "weather_model.pth")

# 🔽 Run this if script is called directly
if __name__ == "__main__":
    wp = WeatherPrediction()
    wp.get_weather_history(lat=31.5497, lon=74.3436)
