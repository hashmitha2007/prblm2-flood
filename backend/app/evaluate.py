import argparse
import numpy as np
import torch
from .model import SatelliteEmbeddingNet

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--test", required=True)
    p.add_argument("--model", default="models/best.pt")
    args = p.parse_args()

    d = np.load(args.test)
    X = torch.tensor(d["X"], dtype=torch.float32)
    Y = torch.tensor(d["Y"], dtype=torch.float32)

    model = SatelliteEmbeddingNet()
    state = torch.load(args.model, map_location="cpu")
    model.load_state_dict(state["model_state"] if "model_state" in state else state)
    model.eval()

    with torch.no_grad():
        P = model(X)

    diff = P - Y
    rmse = torch.sqrt(torch.mean(diff ** 2)).item()
    bias = torch.mean(diff).item()

    a = P.flatten().numpy()
    b = Y.flatten().numpy()
    corr = float(np.corrcoef(a, b)[0, 1])

    print(f"RMSE: {rmse:.4f} °C")
    print(f"Bias: {bias:.4f} °C")
    print(f"Correlation: {corr:.4f}")

if __name__ == "__main__":
    main()
