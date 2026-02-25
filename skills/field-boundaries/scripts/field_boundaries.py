"""Field Boundaries Skill.

High-level skill for accessing and visualizing USDA field boundary data.
Wraps the FieldBoundaryDownloader with additional visualization capabilities.

Output Formats:
    - GeoJSON (.geojson) - Default, human-readable
    - GeoParquet (.parquet) - Cloud-optimized, efficient for large datasets

Filenames include CRS information: fields_EPSG4326.geojson
"""

from pathlib import Path
from typing import Any

import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

import logging as _logging
import sys as _sys
import os as _os

_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from _downloader import FieldBoundaryDownloader


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


class FieldBoundariesSkill:
    """Skill for accessing and visualizing field boundary data.

    This skill provides a simplified interface to the USDA Crop Sequence
    Boundaries dataset with built-in visualization capabilities.

    Example:
        >>> skill = FieldBoundariesSkill()
        >>> fields = skill.download(count=50, regions=['corn_belt'])
        >>> skill.plot_fields(fields, title="Iowa Corn Fields")
    """

    def __init__(self, config: Config | None = None) -> None:
        """Initialize the field boundaries skill.

        Args:
            config: Optional configuration object.
        """
        self.config = config or Config()
        self.downloader = FieldBoundaryDownloader(config)

    def download(
        self,
        count: int = 200,
        regions: list[str] | None = None,
        crops: list[str] | None = None,
        output_path: str | None = None,
    ) -> gpd.GeoDataFrame:
        """Download field boundaries from USDA Crop Sequence Boundaries.

        Downloads a SUBSET of fields (not entire dataset) for efficient
        local processing. Optimized for small machines.

        Args:
            count: Number of fields to download (default: 200).
                Keep small (50-500) for efficient local processing.
            regions: List of regions to sample from.
                Options: 'corn_belt', 'great_plains', 'southeast'.
                Default: ['corn_belt'].
            crops: List of crop types to include.
                Options: 'corn', 'soybeans', 'wheat', 'cotton'.
                Default: ['corn', 'soybeans'].
            output_path: Optional output file path. If None, saves to
                default location with CRS in filename.
                Format: fields_EPSG4326.geojson

        Returns:
            GeoDataFrame with field boundaries in EPSG:4326.

        Example:
            >>> skill = FieldBoundariesSkill()
            >>> # Download small subset for testing
            >>> fields = skill.download(
            ...     count=50,  # Small for local machine
            ...     regions=['corn_belt'],
            ...     crops=['corn', 'soybeans'],
            ...     output_path='data/fields_EPSG4326.geojson'
            ... )
        """
        fields = self.downloader.download(
            count=count,
            regions=regions,
            crops=crops,
            output_format="geojson",
        )

        # Auto-save if output_path provided
        if output_path:
            self.export(fields, output_path)

        return fields

    def plot_fields(
        self,
        fields: gpd.GeoDataFrame,
        title: str = "Field Boundaries",
        color_by: str = "crop_name",
        figsize: tuple[int, int] = (12, 8),
        save_path: str | None = None,
    ) -> None:
        """Plot field boundaries on a map.

        Args:
            fields: GeoDataFrame with field boundaries.
            title: Plot title.
            color_by: Column to color fields by ('crop_name', 'region', etc.).
            figsize: Figure size (width, height).
            save_path: Optional path to save the figure.

        Example:
            >>> skill = FieldBoundariesSkill()
            >>> fields = skill.download(count=50)
            >>> skill.plot_fields(fields, title="Sample Fields")
        """
        fig, ax = plt.subplots(figsize=figsize)

        if color_by in fields.columns:
            fields.plot(column=color_by, legend=True, ax=ax, alpha=0.7, edgecolor="black")
        else:
            fields.plot(ax=ax, alpha=0.7, edgecolor="black")

        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")

        # Add grid
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
            print(f"Saved map to: {save_path}")

        plt.show()

    def get_summary(self, fields: gpd.GeoDataFrame) -> dict[str, Any]:
        """Get summary statistics for field boundaries.

        Args:
            fields: GeoDataFrame with field boundaries.

        Returns:
            Dictionary with summary statistics.

        Example:
            >>> skill = FieldBoundariesSkill()
            >>> fields = skill.download(count=50)
            >>> summary = skill.get_summary(fields)
            >>> print(f"Total fields: {summary['total_fields']}")
        """
        return {
            "total_fields": len(fields),
            "total_area_acres": fields["area_acres"].sum(),
            "avg_field_size": fields["area_acres"].mean(),
            "median_field_size": fields["area_acres"].median(),
            "size_range": (fields["area_acres"].min(), fields["area_acres"].max()),
            "regions": fields["region"].value_counts().to_dict(),
            "crops": fields["crop_name"].value_counts().to_dict()
            if "crop_name" in fields.columns
            else {},
        }

    def filter_by_size(
        self,
        fields: gpd.GeoDataFrame,
        min_acres: float = 0,
        max_acres: float = float("inf"),
    ) -> gpd.GeoDataFrame:
        """Filter fields by size.

        Args:
            fields: GeoDataFrame with field boundaries.
            min_acres: Minimum field size in acres.
            max_acres: Maximum field size in acres.

        Returns:
            Filtered GeoDataFrame.

        Example:
            >>> skill = FieldBoundariesSkill()
            >>> fields = skill.download(count=100)
            >>> large_fields = skill.filter_by_size(fields, min_acres=200)
        """
        return fields[(fields["area_acres"] >= min_acres) & (fields["area_acres"] <= max_acres)]

    def export(
        self,
        fields: gpd.GeoDataFrame,
        output_path: str | None = None,
        format: str = "geojson",
    ) -> Path:
        """Export fields to file.

        Output formats:
            - GeoJSON (.geojson) - Human-readable, good for small datasets
            - GeoParquet (.parquet) - Cloud-optimized, efficient for large datasets

        NO SHAPEFILES - use GeoJSON or GeoParquet instead.

        Filenames should include CRS: fields_EPSG4326.geojson

        Args:
            fields: GeoDataFrame with field boundaries.
            output_path: Output file path. If None, auto-generates with CRS.
            format: Export format ('geojson' or 'geoparquet').

        Returns:
            Path to exported file.

        Example:
            >>> skill = FieldBoundariesSkill()
            >>> fields = skill.download(count=50)
            >>> # CRS automatically included in filename
            >>> skill.export(fields, 'data/fields_EPSG4326.geojson')
        """
        # Get CRS info for filename
        crs = fields.crs.to_string() if fields.crs else "EPSG4326"
        epsg_code = crs.split(":")[-1] if ":" in crs else "4326"

        if output_path is None:
            # Auto-generate filename with CRS
            output_path = (
                self.config.raw_data_path / f"field_boundaries/fields_EPSG{epsg_code}.{format}"
            )

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if format == "geojson":
            fields.to_file(output_path, driver="GeoJSON")
        elif format == "geoparquet":
            fields.to_parquet(output_path)
        else:
            raise ValueError(f"Unsupported format: {format}. Use 'geojson' or 'geoparquet'.")

        return output_path
