---
name: ssurgo-soil
description: Access USDA NRCS SSURGO soil data for agricultural fields. Query soil properties including organic matter, pH, texture, drainage class, and available water capacity. Use when analyzing soil conditions, crop suitability, or field-level soil characteristics.
metadata:
  author: boreal-bytes
  version: '1.0'
  source: https://github.com/SuperiorByteWorks-LLC/agent-project
---

# SSURGO Soil Skill

Access USDA NRCS SSURGO (Soil Survey Geographic Database) data for agricultural analysis.

## Overview

This skill queries the NRCS Soil Data Access (SDA) API to retrieve soil properties for map units intersecting with field boundaries.

## Key Soil Attributes

- **om_pct**: Organic matter percentage (0-20%)
- **ph_water**: pH in water (3.5-10.0)
- **awc_r**: Available water capacity (inches/inch, 0-0.25)
- **drainagecl**: Drainage class (well drained, moderately well drained, etc.)
- **claytotal_r**: Clay percentage
- **sandtotal_r**: Sand percentage
- **silttotal_r**: Silt percentage
- **dbthirdbar_r**: Bulk density (g/cm³)
- **cec7_r**: Cation exchange capacity (meq/100g)
- **ec_r**: Electrical conductivity

## Usage

### Download Soil Data for Fields

```python
from skills.ssurgo-soil.scripts.ssurgo_soil import SSURGOSoilSkill

skill = SSURGOSoilSkill()
soil = skill.download_for_fields(
    fields_geojson='data/fields_EPSG4326.geojson',
    attributes=['om_pct', 'ph_water', 'awc_r', 'drainagecl'],
    output_path='data/soil.csv'
)
```

### Plot Soil Maps

```python
skill.plot_soil_map(soil, attribute='om_pct', title='Organic Matter Content')
```

### Get Soil Summary

```python
summary = skill.get_soil_summary(soil)
```

## Data Source

- **Web Soil Survey**: https://websoilsurvey.sc.egov.usda.gov/
- **Soil Data Access API**: https://sdmdataaccess.sc.egov.usda.gov/

## Dependencies

- geopandas
- matplotlib
- pandas
- requests
- shapely

## References

- See [scripts/ssurgo_soil.py](scripts/ssurgo_soil.py) for full implementation
