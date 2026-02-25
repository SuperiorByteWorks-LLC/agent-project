# Agricultural Data Skills — Examples

This directory contains example scripts demonstrating how to use the agricultural data skills.

## Quick Start

All examples use the **field-centric workflow**:

1. Download field boundaries (small subset)
2. Use field file to query other data sources
3. All data is linked by `field_id`

## Examples

### 01_field_boundaries_example.py

Download and visualize field boundaries.

```bash
python skills/examples/01_field_boundaries_example.py
```

**Output:**

- `data/examples/fields_EPSG4326.geojson` - Field boundaries
- `data/examples/fields_map.png` - Visualization

### 02_chained_download_example.py

Demonstrate the full chained workflow.

```bash
python skills/examples/02_chained_download_example.py
```

**Output:**

- `data/examples/fields_EPSG4326.geojson` - Field boundaries
- `data/examples/soil_EPSG4326.csv` - SSURGO soil data
- `data/examples/weather.csv` - NASA POWER weather data
- `data/examples/cdl_EPSG4326.csv` - CDL crop data
- `data/examples/combined_data_EPSG4326.csv` - Combined dataset

### 03_visualization_example.py

Create professional visualizations.

```bash
python skills/examples/03_visualization_example.py
```

**Output:**

- `data/examples/fields_soil_ph.png` - Fields colored by soil pH
- `data/examples/weather_timeseries.png` - Temperature time series
- `data/examples/precipitation.png` - Precipitation chart
- `data/examples/summary_dashboard.png` - Multi-panel summary

## Key Principles

### 1. Field-Centric Downloads

All skills accept a `fields_geojson` parameter to download data ONLY for specific fields:

```python
import sys
from pathlib import Path

_skills_root = Path(__file__).resolve().parent.parent
for _d in ["field-boundaries", "ssurgo-soil"]:
    sys.path.insert(0, str(_skills_root / _d / "scripts"))

from field_boundaries import FieldBoundariesSkill
from ssurgo_soil import SSURGOSoilSkill

# Step 1: Get field boundaries (small subset)
field_skill = FieldBoundariesSkill()
fields = field_skill.download(
    count=20,  # SMALL for local machine
    output_path='data/fields_EPSG4326.geojson'
)

# Step 2: Chain to soil data
soil_skill = SSURGOSoilSkill()
soil = soil_skill.download_for_fields(
    fields_geojson='data/fields_EPSG4326.geojson',
    output_path='data/soil_EPSG4326.csv'
)
```

### 2. CRS in Filenames

All output files include the EPSG code:

- `fields_EPSG4326.geojson` (WGS84)
- `soil_EPSG4326.csv`
- `sentinel2_field001_20240615_EPSG4326.tif`

### 3. No Shapefiles

Use GeoJSON, GeoParquet, CSV, or GeoTIFF only.

### 4. Optimized for Small Machines

Keep field counts small (20-50) for efficient local processing.

## Available Skills

| Skill                 | Data Source                   | Output Format |
| --------------------- | ----------------------------- | ------------- |
| FieldBoundariesSkill  | USDA Crop Sequence Boundaries | GeoJSON       |
| SSURGOSoilSkill       | NRCS SSURGO                   | CSV           |
| NASAPowerWeatherSkill | NASA POWER                    | CSV           |
| CDLCroplandSkill      | USDA CDL                      | CSV           |
| Sentinel2ImagerySkill | Sentinel-2                    | GeoTIFF       |
| LandsatImagerySkill   | Landsat 8/9                   | GeoTIFF       |

## Data Flow

```
┌─────────────────┐
│ Field Boundaries│ ← Start here (20-50 fields)
└────────┬────────┘
         │
    ┌────┴────┬──────────┬──────────┐
    ▼         ▼          ▼          ▼
┌───────┐ ┌───────┐ ┌────────┐ ┌─────────┐
│ Soil  │ │Weather│ │Crops   │ │Imagery  │
└───────┘ └───────┘ └────────┘ └─────────┘
    │         │          │          │
    └─────────┴──────────┴──────────┘
              ▼
       ┌─────────────┐
       │ Combined    │
       │ Analysis    │
       └─────────────┘
```

## Troubleshooting

### No Data Found

- Check that fields have valid coordinates
- Verify date ranges are valid
- Try larger `count` or different regions

### Large Downloads

- Keep field count small (20-50)
- Use date ranges of 1-2 years
- Filter by cloud cover for satellite data

### Import Errors

All skills are standalone. No package install needed — just add the skill's `scripts/` dir to your path:

```bash
python skills/examples/01_field_boundaries_example.py
```
