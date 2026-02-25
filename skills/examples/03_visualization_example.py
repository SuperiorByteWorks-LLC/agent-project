"""Example 03: Create Professional Visualizations

This example shows how to create publication-quality visualizations
using the downloaded field data.

Creates:
    - Field boundaries map with soil properties
    - Weather time series plots
    - NDVI satellite imagery plots
    - Multi-panel combined figure
"""

import sys
from pathlib import Path

_skills_root = Path(__file__).resolve().parent.parent
for _d in ["field-boundaries", "nasa-power-weather"]:
    sys.path.insert(0, str(_skills_root / _d / "scripts"))

import matplotlib.pyplot as plt
import pandas as pd

from field_boundaries import FieldBoundariesSkill
from nasa_power_weather import NASAPowerWeatherSkill


def main():
    """Create professional visualizations."""
    print("=" * 70)
    print("Example 03: Create Professional Visualizations")
    print("=" * 70)

    # Load previously downloaded data
    print("\nLoading data...")

    fields_file = "data/examples/fields_EPSG4326.geojson"
    soil_file = "data/examples/soil_EPSG4326.csv"
    weather_file = "data/examples/weather.csv"

    # Check if files exist
    for f in [fields_file, soil_file, weather_file]:
        if not Path(f).exists():
            print(f"Error: {f} not found. Run Example 02 first.")
            return

    # Initialize skills
    field_skill = FieldBoundariesSkill()
    weather_skill = NASAPowerWeatherSkill()

    # Load data
    fields = field_skill.download(count=20)  # Load or get cached
    soil = pd.read_csv(soil_file)
    weather = pd.read_csv(weather_file, parse_dates=["date"])

    # Visualization 1: Fields with soil pH
    print("\n1. Creating field boundaries + soil map...")

    # Merge fields with soil data
    import geopandas as gpd

    fields_gdf = gpd.read_file(fields_file)
    fields_with_soil = fields_gdf.merge(soil, on="field_id", how="left")

    fig, ax = plt.subplots(figsize=(12, 8))
    fields_with_soil.plot(
        column="ph_water",
        legend=True,
        ax=ax,
        alpha=0.7,
        edgecolor="black",
        legend_kwds={"label": "Soil pH"},
    )
    ax.set_title("Field Boundaries Colored by Soil pH", fontsize=14, fontweight="bold")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    plt.tight_layout()
    plt.savefig("data/examples/fields_soil_ph.png", dpi=300, bbox_inches="tight")
    print("   Saved: data/examples/fields_soil_ph.png")
    plt.close()

    # Visualization 2: Weather time series for one field
    print("\n2. Creating weather time series plot...")

    field_id = weather["field_id"].unique()[0]
    field_weather = weather[weather["field_id"] == field_id]

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(
        field_weather["date"], field_weather["T2M_MAX"], label="Max Temp", color="red", alpha=0.7
    )
    ax.plot(
        field_weather["date"], field_weather["T2M_MIN"], label="Min Temp", color="blue", alpha=0.7
    )
    ax.fill_between(
        field_weather["date"],
        field_weather["T2M_MIN"],
        field_weather["T2M_MAX"],
        alpha=0.2,
        color="gray",
    )
    ax.set_xlabel("Date")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title(f"Temperature Range: {field_id}", fontsize=14, fontweight="bold")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("data/examples/weather_timeseries.png", dpi=300, bbox_inches="tight")
    print("   Saved: data/examples/weather_timeseries.png")
    plt.close()

    # Visualization 3: Precipitation cumulative
    print("\n3. Creating precipitation plot...")

    weather_with_accum = weather_skill.calculate_accumulated_precipitation(weather, window_days=30)
    field_precip = weather_with_accum[weather_with_accum["field_id"] == field_id]

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.bar(
        field_precip["date"],
        field_precip["PRECTOTCORR"],
        label="Daily Precip",
        alpha=0.5,
        color="blue",
    )
    ax.plot(
        field_precip["date"],
        field_precip["precip_accum"],
        label="30-day Accumulated",
        color="red",
        linewidth=2,
    )
    ax.set_xlabel("Date")
    ax.set_ylabel("Precipitation (mm)")
    ax.set_title(f"Precipitation: {field_id}", fontsize=14, fontweight="bold")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("data/examples/precipitation.png", dpi=300, bbox_inches="tight")
    print("   Saved: data/examples/precipitation.png")
    plt.close()

    # Visualization 4: Multi-panel summary
    print("\n4. Creating multi-panel summary figure...")

    fig = plt.figure(figsize=(16, 12))

    # Panel 1: Fields map
    ax1 = plt.subplot(2, 2, 1)
    fields_with_soil.plot(column="om_pct", legend=True, ax=ax1, alpha=0.7)
    ax1.set_title("Organic Matter (%)")

    # Panel 2: Soil properties
    ax2 = plt.subplot(2, 2, 2)
    soil[["ph_water", "om_pct"]].boxplot(ax=ax2)
    ax2.set_title("Soil Properties Distribution")
    ax2.set_ylabel("Value")

    # Panel 3: Temperature
    ax3 = plt.subplot(2, 2, 3)
    ax3.plot(field_weather["date"], field_weather["T2M_MAX"], "r-", label="Max")
    ax3.plot(field_weather["date"], field_weather["T2M_MIN"], "b-", label="Min")
    ax3.fill_between(
        field_weather["date"], field_weather["T2M_MIN"], field_weather["T2M_MAX"], alpha=0.2
    )
    ax3.set_title(f"Temperature: {field_id}")
    ax3.set_ylabel("Temperature (°C)")
    ax3.legend()

    # Panel 4: Precipitation
    ax4 = plt.subplot(2, 2, 4)
    monthly_precip = field_weather.set_index("date").resample("M")["PRECTOTCORR"].sum()
    ax4.bar(range(len(monthly_precip)), monthly_precip.values, color="blue", alpha=0.6)
    ax4.set_title(f"Monthly Precipitation: {field_id}")
    ax4.set_ylabel("Precipitation (mm)")
    ax4.set_xticks(range(len(monthly_precip)))
    ax4.set_xticklabels([d.strftime("%b") for d in monthly_precip.index], rotation=45)

    plt.suptitle("Agricultural Data Summary", fontsize=16, fontweight="bold")
    plt.tight_layout()
    plt.savefig("data/examples/summary_dashboard.png", dpi=300, bbox_inches="tight")
    print("   Saved: data/examples/summary_dashboard.png")
    plt.close()

    print("\n" + "=" * 70)
    print("Visualization complete! Output files:")
    print("-" * 70)
    print("  - data/examples/fields_soil_ph.png")
    print("  - data/examples/weather_timeseries.png")
    print("  - data/examples/precipitation.png")
    print("  - data/examples/summary_dashboard.png")
    print("=" * 70)


if __name__ == "__main__":
    main()
