"""
Convert harmonized variables into model-ready NPZ files.

Expected standardized NetCDF variables:
sst, sss, ssh, current_u, current_v, wind_u, wind_v, temperature

All should share:
time, latitude, longitude

The target temperature should have:
time, depth, latitude, longitude

This script is intentionally conservative: it checks dimensions rather
than silently guessing variable names.
"""

import argparse
import numpy as np
import xarray as xr

DEPTHS = [0, 5, 10, 20, 30, 50, 75, 100, 125, 150, 200, 300, 500, 700, 1000]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, help="harmonized NetCDF")
    p.add_argument("--output", required=True, help="output NPZ")
    args = p.parse_args()

    ds = xr.open_dataset(args.input)

    names = ["sst", "sss", "ssh", "current_u", "current_v", "wind_u", "wind_v"]
    for n in names + ["temperature"]:
        if n not in ds:
            raise ValueError(f"Missing variable: {n}")

    X = np.stack([ds[n].values for n in names], axis=1)
    Y = ds["temperature"].values

    if Y.ndim != 4:
        raise ValueError("temperature must be [time, depth, lat, lon]")

    np.savez_compressed(args.output, X=X.astype("float32"), Y=Y.astype("float32"))
    print("Saved:", args.output, X.shape, Y.shape)

if __name__ == "__main__":
    main()
