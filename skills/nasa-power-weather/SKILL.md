---
name: nasa-power-weather
description: Access NASA POWER weather and climate data for agricultural fields. Retrieve time-series meteorological data including temperature, precipitation, solar radiation, humidity, and wind. Calculate growing degree days and accumulated precipitation. Use when analyzing weather patterns, climate impacts, or crop growth conditions.
metadata:
  author: boreal-bytes
  version: '1.0'
  source: https://github.com/SuperiorByteWorks-LLC/agent-project
---

# NASA POWER Weather Skill

Access NASA POWER (Prediction Of Worldwide Energy Resources) weather data for agricultural analysis.

## Overview

This skill provides meteorological and solar data from NASA satellites and models, specifically designed for agricultural applications.

## Key Weather Parameters

- **T2M_MIN**: Daily minimum temperature (°C)
- **T2M_MAX**: Daily maximum temperature (°C)
- **T2M**: Daily mean temperature (°C)
- **PRECTOTCORR**: Precipitation (mm)
- **ALLSKY_SFC_SW_DWN**: Solar radiation (MJ/m²/day)
- **RH2M**: Relative humidity (%)
- **WS10M**: Wind speed at 10m (m/s)
- **WS10M_MAX**: Maximum wind speed at 10m (m/s)
- **PS**: Surface pressure (kPa)
- **T2MDEW**: Dew point temperature (°C)

## Usage

### Download Weather Data

```python
from skills.nasa-power-weather.scripts.nasa_power_weather import NASAPowerWeatherSkill

skill = NASAPowerWeatherSkill()
weather = skill.download_for_fields(
    fields_geojson='data/fields_EPSG4326.geojson',
    start_date='2020-01-01',
    end_date='2024-12-31',
    parameters=['T2M_MIN', 'T2M_MAX', 'PRECTOTCORR'],
    output_path='data/weather.csv'
)
```

### Calculate Growing Degree Days

```python
weather_with_gdd = skill.calculate_growing_degree_days(
    weather,
    base_temp=10.0,
    max_temp=30.0
)
```

### Calculate Accumulated Precipitation

```python
weather_with_precip = skill.calculate_accumulated_precipitation(
    weather,
    window_days=7
)
```

### Plot Weather Time Series

```python
skill.plot_weather_timeseries(weather, field_id='field_001')
skill.plot_temperature_comparison(weather)
```

### Get Seasonal Summary

```python
seasonal = skill.get_seasonal_summary(weather, season='growing')
```

## Data Source

- **NASA POWER API**: https://power.larc.nasa.gov/api/
- **Documentation**: https://power.larc.nasa.gov/docs/

## Dependencies

- geopandas
- matplotlib
- pandas
- requests
- shapely

## References

- See [scripts/nasa_power_weather.py](scripts/nasa_power_weather.py) for full implementation
