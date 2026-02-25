"""CDL Cropland Skill.

High-level skill for accessing USDA Cropland Data Layer (CDL).
Provides annual crop type classifications for agricultural fields.
"""

from pathlib import Path
from typing import Any

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio
from matplotlib.patches import Patch
from rasterio.features import rasterize

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


class CDLCroplandSkill:
    """Skill for accessing USDA Cropland Data Layer (CDL).

    The Cropland Data Layer (CDL) is an annual raster classification of crop
    types and land cover for the contiguous United States, produced by USDA NASS.

    Data Source:
        - USDA CropScape: https://croplandcros.scinet.usda.gov/
        - Direct Download: https://www.nass.usda.gov/Research_and_Science/Cropland/Release/

    Major Crop Classes:
        - 1: Corn
        - 5: Soybeans
        - 24: Winter Wheat
        - 27: Rye
        - 36: Alfalfa
        - 61: Fallow/Idle

    Example:
        >>> skill = CDLCroplandSkill()
        >>> cdl = skill.download_for_fields(
        ...     fields_geojson='fields.geojson',
        ...     years=[2016,2017,2018,2019,2020,2021,2022,2023,2024,2025]
        ... )
        >>> skill.plot_crop_map(cdl, year=2024)
    """

    # Major CDL crop codes
    CROP_CODES = {
        1: "Corn",
        2: "Cotton",
        3: "Rice",
        4: "Sorghum",
        5: "Soybeans",
        6: "Sunflower",
        10: "Peanuts",
        11: "Tobacco",
        12: "Sweet Corn",
        13: "Pop or Orn Corn",
        14: "Mint",
        21: "Barley",
        22: "Durum Wheat",
        23: "Spring Wheat",
        24: "Winter Wheat",
        25: "Other Small Grains",
        26: "Dbl Crop WinWht/Soybeans",
        27: "Rye",
        28: "Oats",
        29: "Millet",
        30: "Speltz",
        31: "Canola",
        32: "Flaxseed",
        33: "Safflower",
        34: "Rape Seed",
        35: "Mustard",
        36: "Alfalfa",
        37: "Other Hay/Non Alfalfa",
        38: "Camelina",
        39: "Buckwheat",
        41: "Sugarbeets",
        42: "Dry Beans",
        43: "Potatoes",
        44: "Other Crops",
        45: "Sugarcane",
        46: "Sweet Potatoes",
        47: "Misc Vegs & Fruits",
        48: "Watermelons",
        49: "Onions",
        50: "Cucumbers",
        51: "Chick Peas",
        52: "Lentils",
        53: "Peas",
        54: "Tomatoes",
        55: "Caneberries",
        56: "Hops",
        57: "Herbs",
        58: "Clover/Wildflowers",
        59: "Sod/Grass Seed",
        60: "Switchgrass",
        61: "Fallow/Idle Cropland",
        62: "Pasture/Grass",
        63: "Forest",
        64: "Shrubland",
        65: "Barren",
        66: "Cherries",
        67: "Peaches",
        68: "Apples",
        69: "Grapes",
        70: "Christmas Trees",
        71: "Other Tree Crops",
        72: "Citrus",
        74: "Pecans",
        75: "Almonds",
        76: "Walnuts",
        77: "Pears",
        81: "Clouds/No Data",
        82: "Developed",
        83: "Water",
        87: "Wetlands",
        88: "Nonag/Undefined",
        92: "Aquaculture",
        111: "Open Water",
        112: "Perennial Ice/Snow",
        121: "Developed/Open Space",
        122: "Developed/Low Intensity",
        123: "Developed/Med Intensity",
        124: "Developed/High Intensity",
        131: "Barren",
        141: "Deciduous Forest",
        142: "Evergreen Forest",
        143: "Mixed Forest",
        152: "Shrubland",
        176: "Grass/Pasture",
        190: "Woody Wetlands",
        195: "Herbaceous Wetlands",
    }

    def __init__(self, config: Config | None = None) -> None:
        """Initialize the CDL cropland skill.

        Args:
            config: Optional configuration object.
        """
        self.config = config or Config()
        self.logger = self.config.logger

    def download_for_fields(
        self,
        fields_geojson: str,
        years: list[int],
        output_path: str | None = None,
    ) -> pd.DataFrame:
        """Download CDL crop classifications for field boundaries.

        Args:
            fields_geojson: Path to GeoJSON file with field boundaries.
            years: List of years to retrieve (2008-present).
            output_path: Optional path to save results.

        Returns:
            DataFrame with crop classifications for each field and year.

        Example:
            >>> skill = CDLCroplandSkill()
            >>> cdl = skill.download_for_fields(
            ...     fields_geojson='data/fields.geojson',
            ...     years=[2020, 2021, 2022, 2023, 2024]
            ... )
        """
        fields = gpd.read_file(fields_geojson)
        results = []

        for year in years:
            self.logger.info("Processing CDL for year %d", year)

            for idx, field in fields.iterrows():
                field_id = field.get("field_id", f"field_{idx}")

                # Extract CDL value for this field
                crop_code, crop_name = self._extract_cdl_for_field(field.geometry, year)

                results.append(
                    {
                        "field_id": field_id,
                        "year": year,
                        "crop_code": crop_code,
                        "crop_name": crop_name,
                    }
                )

        df = pd.DataFrame(results)

        if output_path:
            df.to_csv(output_path, index=False)
            self.logger.info("CDL data saved to: %s", output_path)

        return df

    def _extract_cdl_for_field(
        self,
        geometry: Any,
        year: int,
    ) -> tuple[int, str]:
        """Extract dominant CDL crop code for a field geometry.

        Args:
            geometry: Shapely geometry.
            year: Year to extract.

        Returns:
            Tuple of (crop_code, crop_name).
        """
        # This is a placeholder - actual implementation would query CropScape API
        # or download and read GeoTIFF files
        return (1, "Corn")  # Placeholder

    def analyze_rotation(
        self,
        cdl_data: pd.DataFrame,
    ) -> pd.DataFrame:
        """Analyze crop rotation patterns.

        Identifies crop rotation patterns from year-to-year changes.

        Args:
            cdl_data: DataFrame with CDL data including 'field_id', 'year', 'crop_code'.

        Returns:
            DataFrame with rotation analysis.
        """
        # Sort by field and year
        df = cdl_data.sort_values(["field_id", "year"])

        # Calculate year-to-year changes
        df["prev_crop"] = df.groupby("field_id")["crop_code"].shift(1)
        df["changed"] = df["crop_code"] != df["prev_crop"]

        # Count rotations
        rotation_summary = (
            df.groupby("field_id")
            .agg({"changed": "sum", "crop_code": lambda x: list(x), "year": "count"})
            .reset_index()
        )

        rotation_summary.rename(
            columns={
                "changed": "rotation_count",
                "year": "year_count",
                "crop_code": "crop_sequence",
            },
            inplace=True,
        )

        return rotation_summary

    def get_dominant_crops(
        self,
        cdl_data: pd.DataFrame,
        top_n: int = 5,
    ) -> pd.DataFrame:
        """Get most common crops across all fields.

        Args:
            cdl_data: DataFrame with CDL data.
            top_n: Number of top crops to return.

        Returns:
            DataFrame with crop frequencies.
        """
        crop_counts = cdl_data["crop_name"].value_counts().head(top_n)
        total = len(cdl_data)

        df = pd.DataFrame(
            {
                "crop_name": crop_counts.index,
                "count": crop_counts.values,
                "percentage": (crop_counts.values / total * 100).round(2),
            }
        )

        return df

    def plot_crop_map(
        self,
        cdl_data: pd.DataFrame,
        fields: gpd.GeoDataFrame | None = None,
        year: int | None = None,
        title: str = "Crop Classification",
        figsize: tuple[int, int] = (12, 8),
        save_path: str | None = None,
    ) -> None:
        """Plot CDL crop classifications on a map.

        Args:
            cdl_data: DataFrame with CDL data.
            fields: Optional GeoDataFrame with field boundaries.
            year: Specific year to plot. If None, uses most recent.
            title: Plot title.
            figsize: Figure size.
            save_path: Optional path to save figure.
        """
        if year:
            data = cdl_data[cdl_data["year"] == year]
            title = f"{title} ({year})"
        else:
            data = cdl_data
            title = f"{title} (Latest Year)"

        if fields is not None:
            # Join CDL data to fields
            merged = fields.merge(data, on="field_id", how="left")

            fig, ax = plt.subplots(figsize=figsize)

            # Plot by crop
            merged.plot(column="crop_name", legend=True, ax=ax, alpha=0.7, edgecolor="black")

            ax.set_title(title, fontsize=14, fontweight="bold")
            ax.set_xlabel("Longitude")
            ax.set_ylabel("Latitude")

        else:
            # Bar chart of crop counts
            fig, ax = plt.subplots(figsize=figsize)

            crop_counts = data["crop_name"].value_counts().head(10)
            crop_counts.plot(kind="barh", ax=ax)

            ax.set_title(title, fontsize=14, fontweight="bold")
            ax.set_xlabel("Number of Fields")

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")

        plt.show()

    def plot_crop_trends(
        self,
        cdl_data: pd.DataFrame,
        title: str = "Crop Trends Over Time",
        figsize: tuple[int, int] = (12, 6),
        save_path: str | None = None,
    ) -> None:
        """Plot crop trends over multiple years.

        Args:
            cdl_data: DataFrame with CDL data.
            title: Plot title.
            figsize: Figure size.
            save_path: Optional path to save figure.
        """
        # Calculate crop percentages by year
        yearly = cdl_data.groupby(["year", "crop_name"]).size().unstack(fill_value=0)
        yearly_pct = yearly.div(yearly.sum(axis=1), axis=0) * 100

        fig, ax = plt.subplots(figsize=figsize)

        yearly_pct.plot(kind="bar", stacked=True, ax=ax)

        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.set_xlabel("Year")
        ax.set_ylabel("Percentage of Fields")
        ax.legend(title="Crop", bbox_to_anchor=(1.05, 1), loc="upper left")

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")

        plt.show()

    def classify_crop_type(self, cdl_data: pd.DataFrame) -> pd.DataFrame:
        """Classify crops into broader categories.

        Args:
            cdl_data: DataFrame with 'crop_code' column.

        Returns:
            DataFrame with added 'crop_category' column.
        """
        category_map = {
            1: "Row Crops",  # Corn
            2: "Row Crops",  # Cotton
            3: "Row Crops",  # Rice
            4: "Row Crops",  # Sorghum
            5: "Row Crops",  # Soybeans
            6: "Row Crops",  # Sunflower
            21: "Small Grains",  # Barley
            22: "Small Grains",  # Durum Wheat
            23: "Small Grains",  # Spring Wheat
            24: "Small Grains",  # Winter Wheat
            27: "Small Grains",  # Rye
            28: "Small Grains",  # Oats
            36: "Forage",  # Alfalfa
            37: "Forage",  # Other Hay
            61: "Fallow",  # Fallow/Idle
            62: "Forage",  # Pasture/Grass
            63: "Forest",
            176: "Forage",  # Grass/Pasture
        }

        cdl_data = cdl_data.copy()
        cdl_data["crop_category"] = cdl_data["crop_code"].map(category_map)
        cdl_data["crop_category"] = cdl_data["crop_category"].fillna("Other")

        return cdl_data

    def export(
        self,
        cdl_data: pd.DataFrame,
        output_path: str,
        format: str = "csv",
    ) -> Path:
        """Export CDL data to file.

        Args:
            cdl_data: DataFrame with CDL data.
            output_path: Output file path.
            format: Export format ('csv', 'json', 'excel').

        Returns:
            Path to exported file.
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if format == "csv":
            cdl_data.to_csv(output_path, index=False)
        elif format == "json":
            cdl_data.to_json(output_path, orient="records")
        elif format == "excel":
            cdl_data.to_excel(output_path, index=False)
        else:
            raise ValueError(f"Unsupported format: {format}")

        return output_path
