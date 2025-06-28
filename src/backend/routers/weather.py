from fastapi import APIRouter, HTTPException, status
from fastapi.responses import ORJSONResponse
from ..utils.weather_data import Weather

router = APIRouter(default_response_class=ORJSONResponse)

@router.post("/weather")
async def get_weather(region_data: dict):
    try:
        region = region_data.get("region")
        lat = region_data.get("lat")
        lon = region_data.get("lon")

        if not region or lat is None or lon is None:
            raise ValueError("Missing region, lat, or lon")

        weather_model = Weather()
        data = weather_model.getLocation(region, lat, lon)

        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
