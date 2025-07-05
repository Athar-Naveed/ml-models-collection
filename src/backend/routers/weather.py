from fastapi import APIRouter, HTTPException, status
from fastapi.responses import ORJSONResponse
from ..utils.weather_data import Weather

router = APIRouter(default_response_class=ORJSONResponse)

@router.post("/weather")
async def get_weather(region_data: dict):
    try:
        city = region_data.get("city")
        lat = region_data.get("lat")
        lon = region_data.get("lon")

        if not city or lat is None or lon is None:
            raise ValueError("Missing city, lat, or lon")

        weather_model = Weather()
        data = weather_model.getLocation(city, lat, lon)
        print(f"data{data}")
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))