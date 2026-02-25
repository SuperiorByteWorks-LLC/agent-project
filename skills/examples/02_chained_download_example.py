"""Example 02: Chained Data Download Workflow

This example demonstrates the field-centric workflow:
1. Download field boundaries (small subset)
2. Use field file to query soil data
3. Use field file to query weather data
4. Use field file to query crop data
5. Combine all data sources

All downloads are SUBSET only - optimized for small machines.
Output files include CRS in filenames.
"""

import sys
from pathlib import Path

_skills_root = Path(__file__).resolve().parent.parent
for _d in ["field-boundaries", "ssurgo-soil", "nasa-power-weather", "cdl-cropland"]:
    sys.path.insert(0, str(_skills_root / _d / "scripts"))

import pandas as pd

    from cdl_cropland import CDLCroplandSkill
    from field_boundaries import FieldBoundariesSkill
    from nasa_power_weather import NASAPowerWeatherSkill
from ssurgo_soil import SSURGOSoilSkill


def main():
    """Demonstrate chained field-centric data workflow."""
    print("=" * 70)
    print("Example 02: Chained Data Download Workflow")
    print("=" * 70)

    # Common field file (used throughout)
    fields_file = "data/examples/fields_EPSG4326.geojson"

    # Step 1: Download field boundaries
    print("\n" + "-" * 70)
    print("Step 1: Download Field Boundaries")
    print("-" * 70)

    field_skill = FieldBoundariesSkill()
    fields = field_skill.download(
        count=20,  # SMALL for local machine
        regions=["corn_belt"],
        crops=["corn", "soybeans"],
        output_path=fields_file,
    )
    print(f"Downloaded {len(fields)} fields")
    print(f"Saved to: {fields_file}")

    # Step 2: Get soil data for fields
    print("\n" + "-" * 70)
    print("Step 2: Download SSURGO Soil Data for Fields")
    print("-" * 70)

    soil_skill = SSURGOSoilSkill()
    soil = soil_skill.download_for_fields(
        fields_geojson=fields_file,
        attributes=["om_pct", "ph_water", "awc_r", "drainagecl"],
        output_path="data/examples/soil_EPSG4326.csv",
    )
    print(f"Retrieved soil data for {len(soil)} fields")
    print(f"Columns: {list(soil.columns)}")

    # Step 3: Get weather data for fields
    print("\n" + "-" * 70)
    print("Step 3: Download NASA POWER Weather Data for Fields")
    print("-" * 70)

    weather_skill = NASAPowerWeatherSkill()
    weather = weather_skill.download_for_fields(
        fields_geojson=fields_file,
        start_date="2023-01-01",
        end_date="2023-12-31",
        parameters=["T2M_MIN", "T2M_MAX", "PRECTOTCORR"],
        output_path="data/examples/weather.csv",  # No CRS - time series
    )
    print(f"Retrieved {len(weather)} daily weather records")
    print(f"Fields covered: {weather['field_id'].nunique()}")
    print(f"Date range: {weather['date'].min()} to {weather['date'].max()}")

    # Step 4: Get crop data for fields
    print("\n" + "-" * 70)
    print("Step 4: Download CDL Cropland Data for Fields")
    print("-" * 70)

    cdl_skill = CDLCroplandSkill()
    cdl = cdl_skill.download_for_fields(
        fields_geojson=fields_file,
        years=[2020, 2021, 2022, 2023],
        output_path="data/examples/cdl_EPSG4326.csv",
    )
    print(f"Retrieved crop data for {len(cdl)} field-years")
    print(f"Crop distribution:")
    print(cdl["crop_name"].value_counts())

    # Step 5: Combine data sources
    print("\n" + "-" * 70)
    print("Step 5: Combine All Data Sources")
    print("-" * 70)

    # Load all datasets
    fields_df = fields[["field_id", "area_acres", "region", "crop_name"]].copy()
    soil_df = soil[["field_id", "om_pct", "ph_water", "awc_r"]].copy()

    # Get seasonal weather summary
    weather_summary = weather_skill.get_seasonal_summary(weather, season="growing")
    weather_summary.columns = [
        "field_id",
        "tmin_min",
        "tmin_mean",
        "tmin_max",
        "tmax_min",
        "tmax_mean",
        "tmax_max",
        "total_precip",
        "total_solar",
    ]

    # Get latest crop data
    cdl_latest = cdl.sort_values("year").groupby("field_id").last().reset_index()
    cdl_latest = cdl_latest[["field_id", "crop_name", "year"]]
    cdl_latest.columns = ["field_id", "current_crop", "crop_year"]

    # Merge all datasets on field_id
    combined = fields_df.merge(soil_df, on="field_id", how="left")
    combined = combined.merge(weather_summary, on="field_id", how="left")
    combined = combined.merge(cdl_latest, on="field_id", how="left")

    # Save combined dataset
    output_file = "data/examples/combined_data_EPSG4326.csv"
    combined.to_csv(output_file, index=False)

    print(f"\nCombined dataset:")
    print(f"  Fields: {len(combined)}")
    print(f"  Columns: {list(combined.columns)}")
    print(f"  Saved to: {output_file}")

    # Summary
    print("\n" + "=" * 70)
    print("Complete! Output files:")
    print("-" * 70)
    print(f"  Fields:     {fields_file}")
    print(f"  Soil:       data/examples/soil_EPSG4326.csv")
    print(f"  Weather:    data/examples/weather.csv")
    print(f"  Crops:      data/examples/cdl_EPSG4326.csv")
    print(f"  Combined:   {output_file}")
    print("=" * 70)

    return combined


if __name__ == "__main__":
    main()
