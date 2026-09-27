# Data source checklist

Use the official product pages/DOIs supplied by the problem statement.

## Inputs

SST
- OSTIA
- Daily
- Native ~0.05°
- Regrid to 0.25°

SSS
- SMAP / SMOS product
- Daily
- Native ~0.125° in the statement
- Regrid to 0.25°

SSH/SLA
- DUACS
- Daily
- 0.25°

Currents
- OSCAR L4
- Daily
- 0.25°

Winds
- ASCAT and/or CCMP
- Harmonize to daily 0.25°

## Target

GLORYS Global Ocean Reanalysis
- Temperature
- Regrid/extract to the requested grid/depths

## Independent validation

Gridded ARGO / INCOIS LAS
- Keep validation observations independent from the GLORYS training target.
- Match each observation to the nearest model grid/time carefully.
- Report coverage and sample count.

## Recommended split

Do NOT randomly split individual pixels from the same day across train/test if
the goal is to measure generalization in time.

A simple first split:
- Train: earlier dates
- Validation: following period
- Test: later unseen period

For a stronger study, also test spatial holdouts.
