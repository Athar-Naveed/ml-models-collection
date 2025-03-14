from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import weather
import sys
print("Starting FastAPI server...", file=sys.stderr)
app:FastAPI = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(weather.app)

@app.get("/")
async def root():
    return {"message": "Welcome to the ML models backend!"}


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 10000))  # Use Render's default port
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)