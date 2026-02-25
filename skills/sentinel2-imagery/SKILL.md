---
name: sentinel2-imagery
description: Access Sentinel-2 satellite imagery for agricultural fields. Download multispectral imagery with specific bands (Red, NIR, SWIR) for vegetation analysis, NDVI calculation, and crop monitoring. Optimized for field-based AOI queries, not full scenes. Use when analyzing crop health, vegetation indices, or field-level satellite data.
metadata:
  author: boreal-bytes
  version: '1.0'
  source: https://github.com/SuperiorByteWorks-LLC/agent-project
---

# Sentinel-2 Imagery Skill

Access Sentinel-2 satellite imagery for agricultural fields.

## Overview

This skill downloads Sentinel-2 multispectral imagery ONLY for field boundaries (AOI queries), never full scenes. Optimized for small machines.

## Key Bands

| Band | Name       | Wavelength | Use                    |
| ---- | ---------- | ---------- | ---------------------- |
| B2   | Blue       | 490 nm     | Water, soil moisture   |
| B3   | Green      | 560 nm     | Vegetation vigor       |
| B4   | Red        | 665 nm     | Chlorophyll absorption |
| B5   | Red Edge 1 | 705 nm     | Vegetation stress      |
| B6   | Red Edge 2 | 740 nm     | Vegetation stress      |
| B7   | Red Edge 3 | 783 nm     | Vegetation stress      |
| B8   | NIR        | 842 nm     | Vegetation biomass     |
| B8A  | Narrow NIR | 865 nm     | Vegetation biomass     |
| B11  | SWIR 1     | 1610 nm    | Moisture content       |
| B12  | SWIR 2     | 2190 nm    | Moisture content       |

## Usage

### Download Imagery

```python
from skills.sentinel2-imagery.scripts.sentinel2_imagery import Sentinel2ImagerySkill

skill = Sentinel2ImagerySkill()
imagery = skill.download_for_fields(
    fields_geojson='data/fields_EPSG4326.geojson',
    start_date='2024-06-01',
    end_date='2024-08-31',
    bands=['B4', 'B8', 'B11'],
    cloud_cover_max=20,
    output_dir='data/imagery'
)
```

### Calculate NDVI

```python
ndvi = skill.calculate_ndvi(imagery)
```

### Plot Bands

```python
skill.plot_rgb(imagery, field_id='field_001')
skill.plot_ndvi(ndvi, field_id='field_001')
```

## Output Formats

- GeoTIFF (.tif) with CRS in filename (e.g., `sentinel2_field_001_20240615_EPSG4326.tif`)
- Cloud-Optimized GeoTIFF (COG) for efficient access

## Data Source

- **Copernicus Data Space**: https://dataspace.copernicus.eu/
- **AWS Open Data**: s3://sentinel-s2-l2a/

## Dependencies

- geopandas
- matplotlib
- numpy
- pandas
- rasterio
- requests
- shapely

## References

- See [scripts/sentinel2_imagery.py](scripts/sentinel2_imagery.py) for full implementation
