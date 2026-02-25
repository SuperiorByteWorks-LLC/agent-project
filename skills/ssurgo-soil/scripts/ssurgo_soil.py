"""SSURGO Soil Skill.

High-level skill for accessing USDA NRCS SSURGO soil data.
Provides soil property data for agricultural fields including organic matter,
pH, texture, drainage class, and available water capacity.
"""

import io
from pathlib import Path
from typing import Any

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import requests
from matplotlib.patches import Patch
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


class SSURGOSoilSkill:
    """Skill for accessing USDA NRCS SSURGO soil data.

    SSURGO (Soil Survey Geographic Database) provides detailed soil property
    data at the map unit level from the USDA Natural Resources Conservation
    Service.

    Key Attributes:
        - Organic Matter (om_pct): Percentage, 0-20%
        - pH (ph_water): pH in water, 3.5-10.0
        - Texture: Sand/Silt/Clay percentages
        - Drainage Class: Well drained, moderately well drained, etc.
        - Available Water Capacity (awc): inches/inch, 0-0.25
        - Bulk Density: g/cm³
        - Cation Exchange Capacity: meq/100g

    Data Source:
        - Web Soil Survey: https://websoilsurvey.sc.egov.usda.gov/
        - Bulk Download: https://nrcs.app.box.com/v/soils
        - Soil Data Access API: SOAP/REST endpoints

    Example:
        >>> skill = SSURGOSoilSkill()
        >>> # Get soil data for specific fields
        >>> soil_data = skill.download_for_fields(fields_geojson='fields.geojson')
        >>> skill.plot_soil_map(soil_data, attribute='om_pct')
    """

    # NRCS Soil Data Access (SDA) API endpoint
    SDA_URL = "https://sdmdataaccess.sc.egov.usda.gov/Tabular/SDMTabularService.asmx"

    # Key attributes for agricultural analysis
    KEY_ATTRIBUTES = [
        "om_pct",  # Organic matter percentage
        "ph_water",  # pH in water
        "awc_r",  # Available water capacity
        "drainagecl",  # Drainage class
        "claytotal_r",  # Clay percentage
        "sandtotal_r",  # Sand percentage
        "silttotal_r",  # Silt percentage
        "dbthirdbar_r",  # Bulk density
        "cec7_r",  # Cation exchange capacity
        "ec_r",  # Electrical conductivity
    ]

    def __init__(self, config: Config | None = None) -> None:
        """Initialize the SSURGO soil skill.

        Args:
            config: Optional configuration object.
        """
        self.config = config or Config()
        self.logger = self.config.logger

    def download_for_fields(
        self,
        fields_geojson: str,
        attributes: list[str] | None = None,
        output_path: str | None = None,
    ) -> pd.DataFrame:
        """Download SSURGO soil data for field boundaries.

        This method queries the NRCS Soil Data Access (SDA) API to retrieve
        soil properties for the map units that intersect with the provided
        field boundaries.

        Args:
            fields_geojson: Path to GeoJSON file with field boundaries.
            attributes: List of soil attributes to retrieve. If None,
                retrieves all key agricultural attributes.
            output_path: Optional path to save results.

        Returns:
            DataFrame with soil data for each field.

        Example:
            >>> skill = SSURGOSoilSkill()
            >>> soil = skill.download_for_fields(
            ...     fields_geojson='data/fields.geojson',
            ...     attributes=['om_pct', 'ph_water', 'awc_r']
            ... )
        """
        fields = gpd.read_file(fields_geojson)
        attributes = attributes or self.KEY_ATTRIBUTES

        results = []

        for idx, field in fields.iterrows():
            field_id = field.get("field_id", f"field_{idx}")
            centroid = field.geometry.centroid

            # Query soil data at field centroid
            soil_data = self._query_soil_at_point(
                lat=centroid.y,
                lon=centroid.x,
                attributes=attributes,
            )

            if soil_data:
                soil_data["field_id"] = field_id
                results.append(soil_data)

        df = pd.DataFrame(results)

        if output_path:
            df.to_csv(output_path, index=False)
            self.logger.info("Soil data saved to: %s", output_path)

        return df

    def _query_soil_at_point(
        self,
        lat: float,
        lon: float,
        attributes: list[str],
    ) -> dict[str, Any] | None:
        """Query SSURGO soil data at a specific point.

        Args:
            lat: Latitude of query point.
            lon: Longitude of query point.
            attributes: List of soil attributes to retrieve.

        Returns:
            Dictionary with soil attributes, or None if no data found.
        """
        # Build SDA query
        attr_str = ", ".join([f"chorizon.{attr}" for attr in attributes])

        query = f"""
        SELECT {attr_str}, component.mukey
        FROM chorizon
        INNER JOIN component ON chorizon.cokey = component.cokey
        INNER JOIN mapunit ON component.mukey = mapunit.mukey
        INNER JOIN legend ON mapunit.lkey = legend.lkey
        WHERE mapunit.mukey IN (
            SELECT mukey FROM SDA_Get_Mukey_From_LatLong({lat}, {lon})
        )
        AND chorizon.hzdept_r <= 20 AND chorizon.hzdepb_r >= 10
        ORDER BY chorizon.hzdept_r
        """

        try:
            response = requests.post(
                self.SDA_URL,
                data={"query": query},
                timeout=30,
            )
            response.raise_for_status()

            # Parse response (SDA returns XML)
            # This is a simplified parser - full implementation would parse XML
            return {"mukey": None}  # Placeholder

        except requests.RequestException as e:
            self.logger.warning("Failed to query soil data at %s, %s: %s", lat, lon, e)
            return None

    def calculate_area_weighted_average(
        self,
        soil_data: pd.DataFrame,
        attribute: str,
    ) -> float:
        """Calculate area-weighted average for multi-unit fields.

        When multiple soil map units intersect a field, this method
        calculates the area-weighted average of the specified attribute.

        Args:
            soil_data: DataFrame with soil data including area fractions.
            attribute: Attribute to average (e.g., 'om_pct', 'ph_water').

        Returns:
            Area-weighted average value.

        Example:
            >>> avg_ph = skill.calculate_area_weighted_average(
            ...     soil_data, attribute='ph_water'
            ... )
        """
        if attribute not in soil_data.columns:
            raise ValueError(f"Attribute '{attribute}' not found in data")

        if "area_fraction" in soil_data.columns:
            return (soil_data[attribute] * soil_data["area_fraction"]).sum()

        return soil_data[attribute].mean()

    def plot_soil_map(
        self,
        soil_data: pd.DataFrame,
        fields: gpd.GeoDataFrame | None = None,
        attribute: str = "om_pct",
        title: str = "Soil Properties",
        figsize: tuple[int, int] = (12, 8),
        save_path: str | None = None,
    ) -> None:
        """Plot soil data on a map.

        Args:
            soil_data: DataFrame with soil data.
            fields: Optional GeoDataFrame with field boundaries for spatial plot.
            attribute: Soil attribute to visualize.
            title: Plot title.
            figsize: Figure size.
            save_path: Optional path to save figure.

        Example:
            >>> skill = SSURGOSoilSkill()
            >>> soil = skill.download_for_fields('fields.geojson')
            >>> skill.plot_soil_map(soil, attribute='ph_water')
        """
        if attribute not in soil_data.columns:
            raise ValueError(f"Attribute '{attribute}' not in soil data")

        if fields is not None:
            # Spatial plot with field boundaries
            fig, ax = plt.subplots(figsize=figsize)

            # Join soil data to fields
            merged = fields.merge(soil_data, on="field_id", how="left")
            merged.plot(column=attribute, legend=True, ax=ax, alpha=0.7)

            ax.set_title(f"{title}: {attribute}")
        else:
            # Bar plot of soil values
            fig, ax = plt.subplots(figsize=figsize)
            soil_data.plot(x="field_id", y=attribute, kind="bar", ax=ax)
            ax.set_title(f"{title}: {attribute}")
            ax.tick_params(axis="x", rotation=45)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")

        plt.show()

    def get_soil_health_score(
        self,
        soil_data: pd.DataFrame,
        weights: dict[str, float] | None = None,
    ) -> pd.DataFrame:
        """Calculate a composite soil health score.

        Combines multiple soil attributes into a single health score
        using weighted averaging.

        Args:
            soil_data: DataFrame with soil data.
            weights: Dictionary of attribute weights. If None, uses
                default agricultural weights.

        Returns:
            DataFrame with added 'soil_health_score' column.

        Example:
            >>> soil_with_score = skill.get_soil_health_score(soil_data)
        """
        if weights is None:
            weights = {
                "om_pct": 0.3,
                "awc_r": 0.25,
                "ph_water": 0.2,
                "drainagecl": 0.15,
                "claytotal_r": 0.1,
            }

        # Normalize each attribute to 0-1 scale
        normalized = pd.DataFrame(index=soil_data.index)

        for attr, weight in weights.items():
            if attr in soil_data.columns:
                min_val = soil_data[attr].min()
                max_val = soil_data[attr].max()
                if max_val > min_val:
                    normalized[attr] = (soil_data[attr] - min_val) / (max_val - min_val)
                else:
                    normalized[attr] = 0.5

        # Calculate weighted score
        soil_data = soil_data.copy()
        soil_data["soil_health_score"] = 0
        total_weight = 0

        for attr, weight in weights.items():
            if attr in normalized.columns:
                soil_data["soil_health_score"] += normalized[attr] * weight
                total_weight += weight

        if total_weight > 0:
            soil_data["soil_health_score"] /= total_weight

        return soil_data

    def classify_drainage(self, soil_data: pd.DataFrame) -> pd.DataFrame:
        """Classify drainage classes into simple categories.

        Args:
            soil_data: DataFrame with 'drainagecl' column.

        Returns:
            DataFrame with added 'drainage_category' column.
        """
        drainage_map = {
            "Excessively drained": "excessive",
            "Somewhat excessively drained": "excessive",
            "Well drained": "good",
            "Moderately well drained": "good",
            "Somewhat poorly drained": "poor",
            "Poorly drained": "poor",
            "Very poorly drained": "poor",
        }

        if "drainagecl" in soil_data.columns:
            soil_data = soil_data.copy()
            soil_data["drainage_category"] = soil_data["drainagecl"].map(drainage_map)

        return soil_data

    def export(
        self,
        soil_data: pd.DataFrame,
        output_path: str,
        format: str = "csv",
    ) -> Path:
        """Export soil data to file.

        Args:
            soil_data: DataFrame with soil data.
            output_path: Output file path.
            format: Export format ('csv', 'json', 'excel').

        Returns:
            Path to exported file.
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if format == "csv":
            soil_data.to_csv(output_path, index=False)
        elif format == "json":
            soil_data.to_json(output_path, orient="records")
        elif format == "excel":
            soil_data.to_excel(output_path, index=False)
        else:
            raise ValueError(f"Unsupported format: {format}")

        return output_path
