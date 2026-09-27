"""
Starter regridding utility.

For each source product:
1. Open NetCDF with xarray.
2. Normalize longitude convention.
3. Select North Indian Ocean.
4. Resample/regrid to 0.25°.
5. Convert timestamps to daily.
6. Save standardized arrays.

For production, use xarray.interp/reindex carefully and document
whether interpolation is linear, nearest-neighbour, conservative, etc.
"""

import xarray as xr
import numpy as np

LAT = np.arange(5.0, 30.0001, 0.25)
LON = np.arange(45.0, 105.0001, 0.25)

def subset_nio(ds):
    lat_name = "latitude" if "latitude" in ds.coords else "lat"
    lon_name = "longitude" if "longitude" in ds.coords else "lon"
    return ds.sel({lat_name: slice(5, 30), lon_name: slice(45, 105)})

def regrid_to_target(ds):
    lat_name = "latitude" if "latitude" in ds.coords else "lat"
    lon_name = "longitude" if "longitude" in ds.coords else "lon"
    return ds.interp({lat_name: LAT, lon_name: LON}, method="linear")
