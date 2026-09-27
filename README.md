# Satellite Embedding-Based Subsurface Ocean Temperature Reconstruction

Full-stack Proof-of-Concept for the SIH-style problem statement:
- North Indian Ocean: 5°N–30°N, 45°E–105°E
- Target grid: 0.25° × 0.25°
- Daily surface inputs: SST, SSS, SSH/SLA, current U/V, wind U/V
- Target depths: 0, 5, 10, 20, 30, 50, 75, 100, 125, 150, 200, 300, 500, 700, 1000 m
- Target: depth-wise subsurface temperature reconstruction

## Architecture

React + Vite frontend
        |
        | REST API
        v
FastAPI backend
   |              |
   |              +--> trained PyTorch model (optional)
   |
   +--> NetCDF/NumPy preprocessing + demo inference

For deployment:
- Frontend can be deployed on Vercel/Netlify.
- Backend can be deployed on Render/Railway/Fly.io or any Docker host.
- For one-service deployment, the backend can also serve the built React frontend.

## Important

The public ocean datasets are very large. They are NOT included in this ZIP.

This repository contains:
1. Full-stack application
2. Data preprocessing skeleton
3. PyTorch embedding/reconstruction model
4. Training script
5. Evaluation script
6. Demo mode with physically plausible synthetic profiles
7. Docker deployment files
8. Dataset download/placement guide

The demo profile is NOT a scientific reconstruction. For scientific results, train the model using the recommended datasets and validate against independent ARGO observations.

## Quick start - backend

Windows PowerShell:

cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload

Backend:
http://127.0.0.1:8000
Swagger:
http://127.0.0.1:8000/docs

## Quick start - frontend

Open a second PowerShell:

cd frontend
npm install
npm run dev

Frontend:
http://localhost:5173

The frontend expects the backend at:
http://127.0.0.1:8000

Set VITE_API_URL if the backend is deployed elsewhere.

## Training

Install backend dependencies first.

Expected training data format:
data/processed/train.npz
data/processed/val.npz
data/processed/test.npz

Each NPZ should contain:
X: [N, 7, H, W]
Y: [N, 15, H, W]

Channels:
0 SST
1 SSS
2 SSH/SLA
3 current U
4 current V
5 wind U
6 wind V

Target channels:
15 standard depths.

Run:
python -m app.train --train data/processed/train.npz --val data/processed/val.npz --epochs 20 --output models

The resulting checkpoint is used automatically when present.

## Data preparation

Recommended raw products:
- OSTIA SST
- SMAP/SMOS SSS
- DUACS SSH/SLA
- OSCAR currents
- ASCAT/CCMP winds
- GLORYS temperature target
- Gridded ARGO / INCOIS LAS for independent validation

Use the scripts under backend/app/data_pipeline/.

## Deployment

### Backend with Docker

docker build -t ocean-temp-api ./backend
docker run -p 8000:8000 ocean-temp-api

### Frontend

cd frontend
npm install
npm run build

Set:
VITE_API_URL=https://YOUR-BACKEND-DOMAIN

Then deploy the frontend build using your preferred static host.

### Render

Backend:
- Root directory: backend
- Build: docker build is supported, or pip install -r requirements.txt
- Start: uvicorn app.main:app --host 0.0.0.0 --port $PORT

Frontend:
- Root directory: frontend
- Build: npm install && npm run build
- Publish: dist
- Environment variable:
  VITE_API_URL=https://YOUR-BACKEND-URL

## API endpoints

GET /health
GET /config
GET /demo/profile?latitude=15&longitude=80
POST /predict

POST /predict body:
{
  "latitude": 15.0,
  "longitude": 80.0,
  "sst": 28.5,
  "sss": 34.5,
  "ssh": 0.2,
  "current_u": 0.1,
  "current_v": -0.05,
  "wind_u": 4.0,
  "wind_v": 2.0
}

## Scientific caveat

A model trained on GLORYS is learning to approximate the GLORYS target distribution. Independent ARGO evaluation is therefore essential before claiming observational skill. Regridding and interpolation must also be documented because they affect the learned relationships.
