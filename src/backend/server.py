import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.backend.routers import weather
print("Starting FastAPI server...", file=sys.stderr)
app:FastAPI = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(weather.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the ML models backend!"}


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))  # Use Render's default port
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)
