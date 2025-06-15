from fastapi import APIRouter, HTTPException, status
from fastapi.responses import ORJSONResponse
from ..utils.weather_data import Weather

router = APIRouter(default_response_class=ORJSONResponse)

@router.post("/weather")
async def get_weather(ip: dict):
    weather_model = Weather()
    try:
        data = weather_model.getLocation(ip['ip'])
        return {"data": data}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
