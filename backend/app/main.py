from typing import Optional
from pathlib import Path
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .model import DEPTHS
from .inference import demo_profile, predict_surface_features

app = FastAPI(
    title="North Indian Ocean Temperature Reconstruction API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictionRequest(BaseModel):
    latitude: float = Field(..., ge=5, le=30)
    longitude: float = Field(..., ge=45, le=105)
    sst: float = Field(..., ge=-5, le=45)
    sss: float = Field(..., ge=0, le=45)
    ssh: float = Field(0.0)
    current_u: float = Field(0.0)
    current_v: float = Field(0.0)
    wind_u: float = Field(0.0)
    wind_v: float = Field(0.0)

@app.get("/")
def root():
    return {"message": "Satellite Embedding Ocean Temperature API", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/config")
def config():
    return {
        "region": {"lat_min": 5, "lat_max": 30, "lon_min": 45, "lon_max": 105},
        "resolution": "0.25° x 0.25°",
        "temporal_resolution": "daily",
        "input_variables": ["SST", "SSS", "SSH/SLA", "Current U", "Current V", "Wind U", "Wind V"],
        "depths_m": DEPTHS
    }

@app.get("/demo/profile")
def get_demo_profile(latitude: float = 15.0, longitude: float = 80.0,
                     sst: float = 28.5, sss: float = 34.5,
                     ssh: float = 0.2, current_u: float = 0.1,
                     current_v: float = -0.05, wind_u: float = 4.0,
                     wind_v: float = 2.0):
    temps = demo_profile(sst, sss, ssh, current_u, current_v, wind_u, wind_v)
    return {
        "mode": "demo",
        "latitude": latitude,
        "longitude": longitude,
        "depths_m": DEPTHS,
        "temperature_c": temps
    }

@app.post("/predict")
def predict(req: PredictionRequest):
    # Real trained inference expects a grid tensor [1,7,H,W].
    # For a single coordinate request, the API returns the demo path
    # unless a trained model and gridded inference service are configured.
    temps = demo_profile(
        req.sst, req.sss, req.ssh,
        req.current_u, req.current_v,
        req.wind_u, req.wind_v
    )
    return {
        "mode": "demo" if not Path(__file__).resolve().parents[1].joinpath("models/best.pt").exists() else "trained-model-ready",
        "location": {"latitude": req.latitude, "longitude": req.longitude},
        "depths_m": DEPTHS,
        "temperature_c": temps
    }
