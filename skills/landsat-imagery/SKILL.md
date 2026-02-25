---
name: landsat-imagery
description: Access Landsat 8/9 satellite imagery for agricultural fields. Download multispectral imagery with bands for vegetation analysis, surface temperature, and land cover classification. Optimized for field-based AOI queries. Use when analyzing long-term crop trends, surface temperature, or historical field conditions.
metadata:
  author: boreal-bytes
  version: '1.0'
  source: https://github.com/SuperiorByteWorks-LLC/agent-project
---

# Landsat Imagery Skill

Access Landsat 8/9 satellite imagery for agricultural fields.

## Overview

This skill downloads Landsat 8/9 multispectral imagery ONLY for field boundaries (AOI queries), never full scenes. Provides long-term archive data back to 2013.

## Key Bands

| Band | Name            | Wavelength   | Resolution | Use                 |
| ---- | --------------- | ------------ | ---------- | ------------------- |
| B1   | Coastal Aerosol | 435-450 nm   | 30m        | Aerosol monitoring  |
| B2   | Blue            | 450-510 nm   | 30m        | Water penetration   |
| B3   | Green           | 530-590 nm   | 30m        | Vegetation vigor    |
| B4   | Red             | 640-670 nm   | 30m        | Vegetation health   |
| B5   | NIR             | 850-880 nm   | 30m        | Vegetation biomass  |
| B6   | SWIR1           | 1570-1650 nm | 30m        | Moisture content    |
| B7   | SWIR2           | 2110-2290 nm | 30m        | Mineral mapping     |
| B8   | Panchromatic    | 500-680 nm   | 15m        | Sharpening          |
| B9   | Cirrus          | 1360-1390 nm | 30m        | Cloud detection     |
| B10  | Thermal1        | 100m         | 100m       | Surface temperature |
| B11  | Thermal2        | 100m         | 100m       | Surface temperature |

## Usage

### Download Imagery

```python
from skills.landsat-imagery.scripts.landsat_imagery import LandsatImagerySkill

skill = LandsatImagerySkill()
imagery = skill.download_for_fields(
    fields_geojson='data/fields_EPSG4326.geojson',
    start_date='2020-06-01',
    end_date='2020-08-31',
    bands=['B4', 'B5', 'B6'],
    cloud_cover_max=20,
    output_dir='data/landsat'
)
```

### Calculate Indices

```python
ndvi = skill.calculate_ndvi(imagery)
evi = skill.calculate_evi(imagery)
```

### Plot Bands

```python
skill.plot_rgb(imagery, field_id='field_001')
skill.plot_index_timeseries(ndvi, field_id='field_001')
```

## Output Formats

- GeoTIFF (.tif) with CRS in filename (e.g., `landsat_field_001_20240615_EPSG4326.tif`)
- Cloud-Optimized GeoTIFF (COG) for efficient access

## Data Source

- **USGS EarthExplorer**: https://earthexplorer.usgs.gov/
- **Google Earth Engine**: LANDSAT/LC08/C02/T1_L2
- **AWS Open Data**: s3://usgs-landsat/

## Dependencies

- geopandas
- matplotlib
- numpy
- pandas
- rasterio
- requests
- shapely

## References

- See [scripts/landsat_imagery.py](scripts/landsat_imagery.py) for full implementation
