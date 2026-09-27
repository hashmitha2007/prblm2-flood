from pathlib import Path
import numpy as np
import torch
from .model import SatelliteEmbeddingNet, DEPTHS

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "best.pt"

_model = None

def _get_model():
    global _model
    if _model is None and MODEL_PATH.exists():
        from .model import load_checkpoint
        _model = load_checkpoint(MODEL_PATH)
    return _model

def demo_profile(sst, sss, ssh, current_u, current_v, wind_u, wind_v):
    """
    Demonstration-only profile.
    It provides a smooth ocean-like temperature decay with depth.
    Replace this path with a trained checkpoint for real reconstruction.
    """
    surface = float(sst)
    salinity = float(sss)
    dynamic = 0.25 * float(ssh) + 0.15 * (current_u - current_v) - 0.01 * (wind_u + wind_v)
    values = []
    for d in DEPTHS:
        thermocline = 1.0 / (1.0 + np.exp(-(d - 80.0) / 35.0))
        temp = surface - 1.5 * thermocline - 0.0065 * d + dynamic
        temp -= max(0, salinity - 35.0) * 0.04
        values.append(round(float(temp), 3))
    return values

def predict_surface_features(features):
    model = _get_model()
    if model is None:
        return None
    x = torch.tensor(features, dtype=torch.float32)
    with torch.no_grad():
        y = model(x)
    return y.numpy()
