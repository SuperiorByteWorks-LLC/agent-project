---
name: field-boundaries
description: Access and visualize USDA field boundary data for agricultural analysis. Download field polygons, visualize coverage, filter by size, and export to GeoJSON or GeoParquet. Use when working with agricultural field data, crop boundaries, or field-level spatial analysis.
metadata:
  author: boreal-bytes
  version: '1.0'
  source: https://github.com/SuperiorByteWorks-LLC/agent-project
---

# Field Boundaries Skill

Access USDA Crop Sequence Boundaries data for agricultural fields across the US.

## Overview

This skill provides a high-level interface to the USDA Crop Sequence Boundaries dataset, optimized for efficient local processing with small machine footprints.

## Key Features

- **Field-centric downloads**: Subset only, not full datasets
- **CRS in filenames**: Automatic EPSG code inclusion (e.g., `fields_EPSG4326.geojson`)
- **Multiple formats**: GeoJSON, GeoParquet (NO shapefiles)
- **Visualization**: Built-in mapping with crop/region coloring
- **Filtering**: By size, region, and crop type

## Usage

### Download Field Boundaries

```python
from skills.field_boundaries.scripts.field_boundaries import FieldBoundariesSkill

skill = FieldBoundariesSkill()
fields = skill.download(
    count=50,  # Small for local machine
    regions=['corn_belt'],
    crops=['corn', 'soybeans'],
    output_path='data/fields_EPSG4326.geojson'
)
```

### Visualize Fields

```python
skill.plot_fields(fields, title="Iowa Corn Fields", color_by="crop_name")
```

### Filter by Size

```python
large_fields = skill.filter_by_size(fields, min_acres=200)
```

### Get Summary Statistics

```python
summary = skill.get_summary(fields)
print(f"Total fields: {summary['total_fields']}")
print(f"Total area: {summary['total_area_acres']} acres")
```

## Parameters

### Download

| Parameter     | Type      | Default              | Description                                       |
| ------------- | --------- | -------------------- | ------------------------------------------------- |
| `count`       | int       | 200                  | Number of fields to download (50-500 recommended) |
| `regions`     | list[str] | ['corn_belt']        | Options: 'corn_belt', 'great_plains', 'southeast' |
| `crops`       | list[str] | ['corn', 'soybeans'] | Options: 'corn', 'soybeans', 'wheat', 'cotton'    |
| `output_path` | str       | None                 | Output file path (CRS auto-included in filename)  |

## Output Formats

- **GeoJSON** (.geojson): Human-readable, good for small datasets
- **GeoParquet** (.parquet): Cloud-optimized, efficient for large datasets

## Dependencies

- geopandas
- matplotlib
- numpy
- pandas

## References

- See [scripts/field_boundaries.py](scripts/field_boundaries.py) for full implementation
