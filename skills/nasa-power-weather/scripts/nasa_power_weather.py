"""NASA POWER Weather Skill.

High-level skill for accessing NASA POWER weather and climate data.
Provides meteorological time series for agricultural analysis.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import requests
from matplotlib.dates import DateFormatter
from shapely.geometry import Point

import logging as _logging


class Config:
    """Minimal standalone configuration for agricultural data skills."""

    def __init__(self, data_root: str = "data") -> None:
        _logging.basicConfig(level=_logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        self.logger = _logging.getLogger("agri_skills")
        self._data_root = Path(data_root)

    @property
    def raw_data_path(self) -> Path:
        return self._data_root / "raw"

    @property
    def processed_data_path(self) -> Path:
        return self._data_root / "processed"


class NASAPowerWeatherSkill:
    """Skill for accessing NASA POWER weather data.

    NASA POWER (Prediction Of Worldwide Energy Resources) provides
    meteorological and solar data from NASA satellites and models,
    specifically designed for agricultural applications.

    Data Source:
        - NASA POWER API: https://power.larc.nasa.gov/api/
        - Documentation: https://power.larc.nasa.gov/docs/

    Key Parameters:
        - T2M_MIN: Daily minimum temperature (°C)
        - T2M_MAX: Daily maximum temperature (°C)
        - PRECTOTCORR: Daily precipitation (mm)
        - ALLSKY_SFC_SW_DWN: All sky surface shortwave down (MJ/m²/day)
        - RH2M: Relative humidity at 2m (%)
        - WS10M: Wind speed at 10m (m/s)

    Example:
        >>> skill = NASAPowerWeatherSkill()
        >>> weather = skill.download_for_fields(
        ...     fields_geojson='fields.geojson',
        ...     start_date='2020-01-01',
        ...     end_date='2024-12-31'
        ... )
        >>> skill.plot_weather_timeseries(weather, field_id='field_001')
    """

    # NASA POWER API endpoint
    BASE_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"

    # Key parameters for agricultural analysis
    AGRICULTURAL_PARAMS = {
        "T2M_MIN": "Daily minimum temperature (°C)",
        "T2M_MAX": "Daily maximum temperature (°C)",
        "T2M": "Daily mean temperature (°C)",
        "PRECTOTCORR": "Precipitation (mm)",
        "ALLSKY_SFC_SW_DWN": "Solar radiation (MJ/m²/day)",
        "RH2M": "Relative humidity (%)",
        "WS10M": "Wind speed at 10m (m/s)",
        "WS10M_MAX": "Maximum wind speed at 10m (m/s)",
        "PS": "Surface pressure (kPa)",
        "T2MDEW": "Dew point temperature (°C)",
    }

    def __init__(self, config: Config | None = None) -> None:
        """Initialize the NASA POWER weather skill.

        Args:
            config: Optional configuration object.
        """
        self.config = config or Config()
        self.logger = self.config.logger

    def download_for_fields(
        self,
        fields_geojson: str,
        start_date: str,
        end_date: str,
        parameters: list[str] | None = None,
        output_path: str | None = None,
    ) -> pd.DataFrame:
        """Download NASA POWER weather data for field boundaries.

        Args:
            fields_geojson: Path to GeoJSON file with field boundaries.
            start_date: Start date in 'YYYY-MM-DD' format.
            end_date: End date in 'YYYY-MM-DD' format.
            parameters: List of weather parameters to retrieve.
                If None, uses default agricultural parameters.
            output_path: Optional path to save results.

        Returns:
            DataFrame with weather time series for each field.

        Example:
            >>> skill = NASAPowerWeatherSkill()
            >>> weather = skill.download_for_fields(
            ...     fields_geojson='fields.geojson',
            ...     start_date='2020-01-01',
            ...     end_date='2024-12-31',
            ...     parameters=['T2M_MIN', 'T2M_MAX', 'PRECTOTCORR']
            ... )
        """
        fields = gpd.read_file(fields_geojson)
        parameters = parameters or list(self.AGRICULTURAL_PARAMS.keys())[:6]

        all_weather = []

        for idx, field in fields.iterrows():
            field_id = field.get("field_id", f"field_{idx}")
            centroid = field.geometry.centroid

            # Query weather data at field centroid
            weather = self._query_weather(
                lat=centroid.y,
                lon=centroid.x,
                start_date=start_date,
                end_date=end_date,
                parameters=parameters,
            )

            if weather is not None:
                weather["field_id"] = field_id
                all_weather.append(weather)

        if not all_weather:
            raise RuntimeError("No weather data retrieved for any fields")

        combined = pd.concat(all_weather, ignore_index=True)

        if output_path:
            combined.to_csv(output_path, index=False)
            self.logger.info("Weather data saved to: %s", output_path)

        return combined

    def _query_weather(
        self,
        lat: float,
        lon: float,
        start_date: str,
        end_date: str,
        parameters: list[str],
    ) -> pd.DataFrame | None:
        """Query NASA POWER API for weather data.

        Args:
            lat: Latitude.
            lon: Longitude.
            start_date: Start date.
            end_date: End date.
            parameters: List of parameters.

        Returns:
            DataFrame with weather data, or None on failure.
        """
        params = {
            "parameters": ",".join(parameters),
            "community": "AG",
            "longitude": lon,
            "latitude": lat,
            "start": start_date.replace("-", ""),
            "end": end_date.replace("-", ""),
            "format": "JSON",
        }

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=60)
            response.raise_for_status()
            data = response.json()

            if "properties" not in data or "parameter" not in data["properties"]:
                self.logger.warning("No data returned for %s, %s", lat, lon)
                return None

            # Extract time series data
            param_data = data["properties"]["parameter"]

            # Build DataFrame from all parameters
            dates = None
            df_data = {}

            for param in parameters:
                if param in param_data:
                    param_values = param_data[param]
                    if dates is None:
                        dates = list(param_values.keys())
                    df_data[param] = list(param_values.values())

            if dates is None:
                return None

            df = pd.DataFrame(df_data)
            df["date"] = pd.to_datetime(dates, format="%Y%m%d")

            return df

        except requests.RequestException as e:
            self.logger.error("Failed to query weather data: %s", e)
            return None

    def calculate_growing_degree_days(
        self,
        weather: pd.DataFrame,
        base_temp: float = 10.0,
        max_temp: float = 30.0,
    ) -> pd.DataFrame:
        """Calculate Growing Degree Days (GDD).

        GDD = ((Tmin + Tmax) / 2) - Tbase
        Capped at Tmax.

        Args:
            weather: DataFrame with T2M_MIN and T2M_MAX columns.
            base_temp: Base temperature in °C (default: 10).
            max_temp: Maximum effective temperature in °C (default: 30).

        Returns:
            DataFrame with added 'gdd' column.
        """
        if "T2M_MIN" not in weather.columns or "T2M_MAX" not in weather.columns:
            raise ValueError("Weather data must contain T2M_MIN and T2M_MAX")

        df = weather.copy()

        # Calculate average daily temperature
        t_avg = (df["T2M_MIN"] + df["T2M_MAX"]) / 2

        # Cap at max_temp
        t_avg = t_avg.clip(upper=max_temp)

        # Calculate GDD
        df["gdd"] = (t_avg - base_temp).clip(lower=0)

        # Calculate cumulative GDD
        df["gdd_cumulative"] = df.groupby("field_id")["gdd"].cumsum()

        return df

    def calculate_accumulated_precipitation(
        self,
        weather: pd.DataFrame,
        window_days: int = 7,
    ) -> pd.DataFrame:
        """Calculate accumulated precipitation over rolling window.

        Args:
            weather: DataFrame with PRECTOTCORR column.
            window_days: Rolling window in days (default: 7).

        Returns:
            DataFrame with added 'precip_accum' column.
        """
        if "PRECTOTCORR" not in weather.columns:
            raise ValueError("Weather data must contain PRECTOTCORR")

        df = weather.copy()
        df["precip_accum"] = (
            df.groupby("field_id")["PRECTOTCORR"]
            .rolling(window=window_days, min_periods=1)
            .sum()
            .reset_index(0, drop=True)
        )

        return df

    def plot_weather_timeseries(
        self,
        weather: pd.DataFrame,
        field_id: str | None = None,
        parameters: list[str] | None = None,
        title: str = "Weather Time Series",
        figsize: tuple[int, int] = (14, 8),
        save_path: str | None = None,
    ) -> None:
        """Plot weather time series.

        Args:
            weather: DataFrame with weather data.
            field_id: Specific field to plot. If None, plots all fields.
            parameters: Parameters to plot. If None, plots all.
            title: Plot title.
            figsize: Figure size.
            save_path: Optional path to save figure.
        """
        if field_id:
            data = weather[weather["field_id"] == field_id]
        else:
            data = weather

        if parameters is None:
            parameters = [col for col in data.columns if col not in ["date", "field_id"]]

        # Create subplots
        n_params = len(parameters)
        fig, axes = plt.subplots(n_params, 1, figsize=figsize, sharex=True)

        if n_params == 1:
            axes = [axes]

        for ax, param in zip(axes, parameters):
            if param in data.columns:
                for field in data["field_id"].unique():
                    field_data = data[data["field_id"] == field]
                    ax.plot(field_data["date"], field_data[param], label=field, alpha=0.7)

                ax.set_ylabel(param)
                ax.grid(True, alpha=0.3)

        axes[-1].set_xlabel("Date")
        axes[-1].xaxis.set_major_formatter(DateFormatter("%Y-%m"))
        plt.xticks(rotation=45)

        plt.suptitle(title, fontsize=14, fontweight="bold")
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")

        plt.show()

    def plot_temperature_comparison(
        self,
        weather: pd.DataFrame,
        title: str = "Temperature Comparison",
        figsize: tuple[int, int] = (12, 6),
        save_path: str | None = None,
    ) -> None:
        """Plot temperature range comparison.

        Args:
            weather: DataFrame with T2M_MIN and T2M_MAX columns.
            title: Plot title.
            figsize: Figure size.
            save_path: Optional path to save figure.
        """
        if "T2M_MIN" not in weather.columns or "T2M_MAX" not in weather.columns:
            raise ValueError("Weather data must contain T2M_MIN and T2M_MAX")

        fig, ax = plt.subplots(figsize=figsize)

        for field_id in weather["field_id"].unique():
            field_data = weather[weather["field_id"] == field_id].sort_values("date")

            # Plot min/max range
            ax.fill_between(
                field_data["date"],
                field_data["T2M_MIN"],
                field_data["T2M_MAX"],
                alpha=0.3,
                label=f"{field_id} range",
            )

            # Plot mean
            if "T2M" in field_data.columns:
                ax.plot(field_data["date"], field_data["T2M"], label=f"{field_id} mean")

        ax.set_xlabel("Date")
        ax.set_ylabel("Temperature (°C)")
        ax.set_title(title)
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.xaxis.set_major_formatter(DateFormatter("%Y-%m"))
        plt.xticks(rotation=45)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")

        plt.show()

    def get_seasonal_summary(
        self,
        weather: pd.DataFrame,
        season: str = "growing",
    ) -> pd.DataFrame:
        """Get seasonal weather summary statistics.

        Args:
            weather: DataFrame with weather data.
            season: Season to analyze ('growing', 'spring', 'summer', 'fall', 'winter').

        Returns:
            DataFrame with seasonal summary by field.
        """
        df = weather.copy()
        df["month"] = df["date"].dt.month

        if season == "growing":
            # May-September growing season
            season_data = df[df["month"].isin([5, 6, 7, 8, 9])]
        elif season == "spring":
            season_data = df[df["month"].isin([3, 4, 5])]
        elif season == "summer":
            season_data = df[df["month"].isin([6, 7, 8])]
        elif season == "fall":
            season_data = df[df["month"].isin([9, 10, 11])]
        elif season == "winter":
            season_data = df[df["month"].isin([12, 1, 2])]
        else:
            season_data = df

        # Calculate summary statistics
        summary = (
            season_data.groupby("field_id")
            .agg(
                {
                    "T2M_MIN": ["min", "mean", "max"],
                    "T2M_MAX": ["min", "mean", "max"],
                    "PRECTOTCORR": "sum",
                    "ALLSKY_SFC_SW_DWN": "sum",
                }
            )
            .reset_index()
        )

        return summary

    def export(
        self,
        weather: pd.DataFrame,
        output_path: str,
        format: str = "csv",
    ) -> Path:
        """Export weather data to file.

        Args:
            weather: DataFrame with weather data.
            output_path: Output file path.
            format: Export format ('csv', 'json', 'excel', 'parquet').

        Returns:
            Path to exported file.
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if format == "csv":
            weather.to_csv(output_path, index=False)
        elif format == "json":
            weather.to_json(output_path, orient="records", date_format="iso")
        elif format == "excel":
            weather.to_excel(output_path, index=False)
        elif format == "parquet":
            weather.to_parquet(output_path, index=False)
        else:
            raise ValueError(f"Unsupported format: {format}")

        return output_path
