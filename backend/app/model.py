import torch
from torch import nn

DEPTHS = [0, 5, 10, 20, 30, 50, 75, 100, 125, 150, 200, 300, 500, 700, 1000]

class SatelliteEmbeddingNet(nn.Module):
    """
    CNN encoder-decoder PoC.
    Input: 7 surface variables.
    Output: 15 depth-wise temperatures.
    """

    def __init__(self, in_channels=7, out_channels=15):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Conv2d(in_channels, 32, 3, padding=1),
            nn.BatchNorm2d(32),
            nn.GELU(),
            nn.Conv2d(32, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.GELU(),
            nn.Conv2d(64, 128, 3, padding=1),
            nn.BatchNorm2d(128),
            nn.GELU(),
        )
        self.embedding = nn.Sequential(
            nn.Conv2d(128, 128, 1),
            nn.GELU(),
        )
        self.decoder = nn.Sequential(
            nn.Conv2d(128, 64, 3, padding=1),
            nn.GELU(),
            nn.Conv2d(64, 32, 3, padding=1),
            nn.GELU(),
            nn.Conv2d(32, out_channels, 1),
        )

    def forward(self, x):
        z = self.embedding(self.encoder(x))
        return self.decoder(z)

def load_checkpoint(path):
    model = SatelliteEmbeddingNet()
    state = torch.load(path, map_location="cpu")
    if "model_state" in state:
        model.load_state_dict(state["model_state"])
    else:
        model.load_state_dict(state)
    model.eval()
    return model
