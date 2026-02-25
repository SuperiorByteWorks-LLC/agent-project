"""Agricultural Data Skills for OpenCode.

Skills provide high-level, reusable interfaces for accessing and analyzing
agricultural data sources. Each skill wraps a specific data source with
consistent download, analysis, and visualization capabilities.

Key Features:
    - Field-centric downloads (subset only, not full datasets)
    - CRS in all filenames (e.g., fields_EPSG4326.geojson)
    - GeoJSON/GeoParquet/CSV/GeoTIFF only (NO shapefiles)
    - Optimized for small machines
    - Fully standalone — no agri_toolkit dependency

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
    >>> import sys, os
    >>> sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'field-boundaries', 'scripts'))
    >>> sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ssurgo-soil', 'scripts'))
    >>> sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'nasa-power-weather', 'scripts'))
    >>> from field_boundaries import FieldBoundariesSkill
    >>> from ssurgo_soil import SSURGOSoilSkill
    >>> from nasa_power_weather import NASAPowerWeatherSkill

    >>> # Step 1: Get field subset
    >>> field_skill = FieldBoundariesSkill()
    >>> fields = field_skill.download(
    ...     count=20,
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

import os as _os
import sys as _sys

# Add each skill's scripts directory to path so classes are importable
_skills_root = _os.path.dirname(_os.path.abspath(__file__))
for _skill_dir in [
    "field-boundaries",
    "ssurgo-soil",
    "nasa-power-weather",
    "cdl-cropland",
    "sentinel2-imagery",
    "landsat-imagery",
]:
    _scripts_path = _os.path.join(_skills_root, _skill_dir, "scripts")
    if _scripts_path not in _sys.path:
        _sys.path.insert(0, _scripts_path)

from cdl_cropland import CDLCroplandSkill  # noqa: E402
from field_boundaries import FieldBoundariesSkill  # noqa: E402
from landsat_imagery import LandsatImagerySkill  # noqa: E402
from nasa_power_weather import NASAPowerWeatherSkill  # noqa: E402
from sentinel2_imagery import Sentinel2ImagerySkill  # noqa: E402
from ssurgo_soil import SSURGOSoilSkill  # noqa: E402

__all__ = [
    "CDLCroplandSkill",
    "FieldBoundariesSkill",
    "LandsatImagerySkill",
    "NASAPowerWeatherSkill",
    "Sentinel2ImagerySkill",
    "SSURGOSoilSkill",
]
