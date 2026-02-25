---
name: cdl-cropland
description: Access USDA Cropland Data Layer (CDL) for annual crop type classifications. Retrieve crop classifications for agricultural fields across the US, analyze crop rotations, and visualize crop distributions. Use when identifying crop types, analyzing land use, or studying crop patterns over time.
metadata:
  author: boreal-bytes
  version: '1.0'
  source: https://github.com/SuperiorByteWorks-LLC/agent-project
---

# CDL Cropland Skill

Access USDA Cropland Data Layer (CDL) for annual crop type classifications.

## Overview

The Cropland Data Layer (CDL) is an annual raster classification of crop types and land cover for the contiguous United States, produced by USDA NASS.

## Major Crop Classes

| Code | Crop                 |
| ---- | -------------------- |
| 1    | Corn                 |
| 2    | Cotton               |
| 3    | Rice                 |
| 4    | Sorghum              |
| 5    | Soybeans             |
| 6    | Sunflower            |
| 10   | Peanuts              |
| 21   | Barley               |
| 22   | Durum Wheat          |
| 23   | Spring Wheat         |
| 24   | Winter Wheat         |
| 36   | Alfalfa              |
| 61   | Fallow/Idle Cropland |

## Usage

### Download CDL Data

```python
from skills.cdl-cropland.scripts.cdl_cropland import CDLCroplandSkill

skill = CDLCroplandSkill()
cdl = skill.download_for_fields(
    fields_geojson='data/fields_EPSG4326.geojson',
    years=[2020, 2021, 2022, 2023, 2024],
    output_path='data/cdl.csv'
)
```

### Plot Crop Map

```python
skill.plot_crop_map(cdl, year=2024, title='Crop Distribution')
```

### Analyze Crop Rotation

```python
rotation = skill.analyze_crop_rotation(cdl)
```

### Get Crop Summary

```python
summary = skill.get_crop_summary(cdl)
```

## Data Source

- **USDA CropScape**: https://croplandcros.scinet.usda.gov/
- **Direct Download**: https://www.nass.usda.gov/Research_and_science/Cropland/Release/

## Dependencies

- geopandas
- matplotlib
- numpy
- pandas
- rasterio

## References

- See [scripts/cdl_cropland.py](scripts/cdl_cropland.py) for full implementation
