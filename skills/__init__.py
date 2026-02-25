"""Agricultural Data Skills.

Skills provide high-level, reusable interfaces for accessing and analyzing
agricultural data sources. Each skill wraps a specific data source with
consistent download, analysis, and visualization capabilities.

Key Features:
    - Field-centric downloads (subset only, not full datasets)
    - CRS in all filenames (e.g., fields_EPSG4326.geojson)
    - GeoJSON/GeoParquet/CSV/GeoTIFF only (NO shapefiles)
    - Optimized for small machines

Skills:
    - FieldBoundariesSkill: Access USDA field boundary data
    - SSURGOSoilSkill: Access USDA NRCS SSURGO soil data
    - NASAPowerWeatherSkill: Access NASA POWER weather data
    - CDLCroplandSkill: Access USDA Cropland Data Layer
    - Sentinel2ImagerySkill: Access Sentinel-2 satellite imagery
    - LandsatImagerySkill: Access Landsat 8/9 satellite imagery

Workflow Pattern:
    1. Download field boundaries (small subset)
    2. Use field file to query other data sources
    3. All data linked by field_id

Example:
    >>> from agri_toolkit.skills import (
    ...     FieldBoundariesSkill,
    ...     SSURGOSoilSkill,
    ...     NASAPowerWeatherSkill
    ... )

    >>> # Step 1: Get field subset
    >>> field_skill = FieldBoundariesSkill()
    >>> fields = field_skill.download(
    ...     count=20,  # Small for local machine
    ...     output_path='data/fields_EPSG4326.geojson'
    ... )

    >>> # Step 2: Chain to soil data
    >>> soil_skill = SSURGOSoilSkill()
    >>> soil = soil_skill.download_for_fields(
    ...     'data/fields_EPSG4326.geojson',
    ...     output_path='data/soil_EPSG4326.csv'
    ... )

    >>> # Step 3: Chain to weather data
    >>> weather_skill = NASAPowerWeatherSkill()
    >>> weather = weather_skill.download_for_fields(
    ...     'data/fields_EPSG4326.geojson',
    ...     start_date='2020-01-01',
    ...     end_date='2024-12-31',
    ...     output_path='data/weather.csv'
    ... )
"""

from agri_toolkit.skills.cdl_cropland import CDLCroplandSkill
from agri_toolkit.skills.field_boundaries import FieldBoundariesSkill
from agri_toolkit.skills.landsat_imagery import LandsatImagerySkill
from agri_toolkit.skills.nasa_power_weather import NASAPowerWeatherSkill
from agri_toolkit.skills.sentinel2_imagery import Sentinel2ImagerySkill
from agri_toolkit.skills.ssurgo_soil import SSURGOSoilSkill

__all__ = [
    "CDLCroplandSkill",
    "FieldBoundariesSkill",
    "LandsatImagerySkill",
    "NASAPowerWeatherSkill",
    "Sentinel2ImagerySkill",
    "SSURGOSoilSkill",
]
