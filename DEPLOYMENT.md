# Deployment checklist

## 1. GitHub

Push this project to a GitHub repository.

Do not push:
- raw NetCDF/GRIB datasets
- trained model checkpoints if they are large
- secrets/API keys

## 2. Backend

Recommended first deployment: Render Docker service.

Root directory:
backend

Dockerfile:
backend/Dockerfile

Environment:
PORT is supplied by the platform.

After deployment test:
https://YOUR-BACKEND/health
https://YOUR-BACKEND/docs

## 3. Frontend

Deploy frontend as a static Vite site.

Build:
npm install && npm run build

Output:
dist

Environment:
VITE_API_URL=https://YOUR-BACKEND

## 4. CORS

The PoC backend currently allows all origins.
For a final deployment, restrict allow_origins to your actual frontend URL.

## 5. Real model deployment

The application should only be called a trained reconstruction system after:
- preprocessing all required surface products
- creating aligned daily 0.25° samples
- training against GLORYS target profiles
- evaluating on a temporally independent test period
- validating independently with ARGO

For large-scale inference, do not send an entire 0.25° basin grid through a browser request.
Run inference server-side and expose selected location/day queries through the API.
