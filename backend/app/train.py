import argparse
from pathlib import Path
import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset
from .model import SatelliteEmbeddingNet

def load_npz(path):
    d = np.load(path)
    X = d["X"].astype("float32")
    Y = d["Y"].astype("float32")
    return torch.from_numpy(X), torch.from_numpy(Y)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--train", required=True)
    p.add_argument("--val", required=True)
    p.add_argument("--epochs", type=int, default=20)
    p.add_argument("--batch-size", type=int, default=8)
    p.add_argument("--lr", type=float, default=1e-3)
    p.add_argument("--output", default="models")
    args = p.parse_args()

    Xtr, Ytr = load_npz(args.train)
    Xva, Yva = load_npz(args.val)

    train_loader = DataLoader(TensorDataset(Xtr, Ytr), batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(TensorDataset(Xva, Yva), batch_size=args.batch_size)

    model = SatelliteEmbeddingNet()
    opt = torch.optim.AdamW(model.parameters(), lr=args.lr)
    loss_fn = nn.HuberLoss()

    best = float("inf")
    Path(args.output).mkdir(parents=True, exist_ok=True)

    for epoch in range(1, args.epochs + 1):
        model.train()
        tr_loss = 0
        for xb, yb in train_loader:
            opt.zero_grad()
            pred = model(xb)
            loss = loss_fn(pred, yb)
            loss.backward()
            opt.step()
            tr_loss += loss.item() * len(xb)

        model.eval()
        va_loss = 0
        with torch.no_grad():
            for xb, yb in val_loader:
                va_loss += loss_fn(model(xb), yb).item() * len(xb)

        tr_loss /= len(Xtr)
        va_loss /= len(Xva)
        print(f"Epoch {epoch:03d} | train={tr_loss:.5f} | val={va_loss:.5f}")

        if va_loss < best:
            best = va_loss
            torch.save({"model_state": model.state_dict(), "val_loss": best}, Path(args.output) / "best.pt")

if __name__ == "__main__":
    main()
