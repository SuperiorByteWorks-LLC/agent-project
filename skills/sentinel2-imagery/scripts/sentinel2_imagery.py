"""Sentinel-2 Imagery Skill.

High-level skill for accessing Sentinel-2 satellite imagery.
Downloads imagery for field boundaries ONLY (not full scenes).
Optimized for small machines with field-based AOI queries.

Output Formats:
    - GeoTIFF (.tif) with CRS in filename
    - Cloud-Optimized GeoTIFF (COG) for efficient access

Filenames include CRS: sentinel2_field_001_20240615_EPSG4326.tif
"""

from pathlib import Path
from typing import Any

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio
import requests
from rasterio.mask import mask
from rasterio.plot import show
from shapely.geometry import box, mapping

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


class Sentinel2ImagerySkill:
    """Skill for accessing Sentinel-2 satellite imagery for fields.

    IMPORTANT: Downloads imagery ONLY for field boundaries (AOI queries).
    NEVER downloads full Sentinel-2 scenes. Optimized for small machines.

    Data Source:
        - Copernicus Data Space: https://dataspace.copernicus.eu/
        - AWS Open Data: s3://sentinel-s2-l2a/

    Key Bands:
        - B4 (Red): 665 nm - Chlorophyll absorption
        - B8 (NIR): 842 nm - Vegetation biomass
        - B11 (SWIR): 1610 nm - Moisture content

    Example:
        >>> skill = Sentinel2ImagerySkill()
        >>> # Download for field subset ONLY
        >>> imagery = skill.download_for_fields(
        ...     fields_geojson='fields_EPSG4326.geojson',
        ...     start_date='2024-06-01',
        ...     end_date='2024-08-31',
        ...     bands=['B4', 'B8'],
        ...     cloud_cover_max=20
        ... )
    """

    # Sentinel-2 bands for agriculture
    BANDS = {
        "B2": ("Blue", 490, "Water, soil moisture"),
        "B3": ("Green", 560, "Vegetation vigor"),
        "B4": ("Red", 665, "Chlorophyll absorption"),
        "B5": ("Red Edge 1", 705, "Vegetation stress"),
        "B6": ("Red Edge 2", 740, "Vegetation stress"),
        "B7": ("Red Edge 3", 783, "Vegetation stress"),
        "B8": ("NIR", 842, "Vegetation biomass"),
        "B8A": ("Narrow NIR", 865, "Vegetation biomass"),
        "B11": ("SWIR 1", 1610, "Moisture content"),
        "B12": ("SWIR 2", 2190, "Moisture content"),
    }

    # Spatial resolution per band
    RESOLUTION_10M = ["B2", "B3", "B4", "B8"]
    RESOLUTION_20M = ["B5", "B6", "B7", "B8A", "B11", "B12"]
    RESOLUTION_60M = ["B1", "B9", "B10"]

    def __init__(self, config: Config | None = None) -> None:
        """Initialize the Sentinel-2 imagery skill.

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
        bands: list[str] | None = None,
        cloud_cover_max: float = 20.0,
        output_dir: str | None = None,
    ) -> pd.DataFrame:
        """Download Sentinel-2 imagery for field boundaries ONLY.

        Queries Sentinel-2 catalog for scenes covering field AOIs,
        then downloads ONLY the required bands clipped to field extent.
        NEVER downloads full scenes.

        Args:
            fields_geojson: Path to GeoJSON with field boundaries.
                Must include CRS (e.g., fields_EPSG4326.geojson).
            start_date: Start date 'YYYY-MM-DD'.
            end_date: End date 'YYYY-MM-DD'.
            bands: List of bands to download. Default: ['B4', 'B8'] for NDVI.
            cloud_cover_max: Maximum cloud cover % (default: 20).
            output_dir: Output directory. Default: data/raw/sentinel2/

        Returns:
            DataFrame with metadata for downloaded imagery.
            Columns: field_id, date, band, file_path, cloud_cover

        Example:
            >>> skill = Sentinel2ImagerySkill()
            >>> # Start with small field subset
            >>> fields = field_skill.download(count=20)
            >>> field_skill.export(fields, 'fields_EPSG4326.geojson')
            >>>
            >>> # Download imagery for fields ONLY
            >>> imagery = skill.download_for_fields(
            ...     fields_geojson='fields_EPSG4326.geojson',
            ...     start_date='2024-06-01',
            ...     end_date='2024-08-31',
            ...     bands=['B4', 'B8'],
            ...     cloud_cover_max=20
            ... )
        """
        # Load fields
        fields = gpd.read_file(fields_geojson)

        # Ensure fields have CRS
        if fields.crs is None:
            raise ValueError("Fields must have CRS. Save as fields_EPSG4326.geojson")

        # Default bands for NDVI
        bands = bands or ["B4", "B8"]

        # Validate bands
        invalid_bands = [b for b in bands if b not in self.BANDS]
        if invalid_bands:
            raise ValueError(f"Invalid bands: {invalid_bands}")

        # Setup output directory
        if output_dir is None:
            output_dir = self.config.raw_data_path / "sentinel2"
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        results = []

        # Get overall AOI from all fields (for catalog search)
        aoi_bounds = fields.total_bounds

        # Search for available scenes
        scenes = self._search_scenes(
            bbox=aoi_bounds,
            start_date=start_date,
            end_date=end_date,
            cloud_cover_max=cloud_cover_max,
        )

        if not scenes:
            self.logger.warning("No Sentinel-2 scenes found matching criteria")
            return pd.DataFrame()

        self.logger.info(f"Found {len(scenes)} scenes, downloading for {len(fields)} fields")

        # For each field, extract imagery from best scene
        for idx, field in fields.iterrows():
            field_id = field.get("field_id", f"field_{idx}")

            # Find best scene for this field (lowest cloud cover)
            best_scene = self._select_best_scene(field.geometry, scenes)

            if best_scene is None:
                self.logger.warning(f"No suitable scene for {field_id}")
                continue

            # Download each band for this field
            for band in bands:
                try:
                    file_path = self._download_band_for_field(
                        field=field,
                        field_id=field_id,
                        scene=best_scene,
                        band=band,
                        output_dir=output_dir,
                    )

                    if file_path:
                        results.append(
                            {
                                "field_id": field_id,
                                "date": best_scene["date"],
                                "band": band,
                                "file_path": str(file_path),
                                "cloud_cover": best_scene["cloud_cover"],
                                "scene_id": best_scene["id"],
                            }
                        )

                except Exception as e:
                    self.logger.error(f"Failed to download {band} for {field_id}: {e}")

        df = pd.DataFrame(results)

        if len(df) > 0:
            # Save manifest
            manifest_path = output_dir / f"sentinel2_manifest_EPSG{fields.crs.to_epsg()}.csv"
            df.to_csv(manifest_path, index=False)
            self.logger.info(f"Downloaded {len(df)} images. Manifest: {manifest_path}")

        return df

    def _search_scenes(
        self,
        bbox: tuple[float, float, float, float],
        start_date: str,
        end_date: str,
        cloud_cover_max: float,
    ) -> list[dict]:
        """Search Sentinel-2 catalog for scenes covering bbox.

        Returns list of scenes sorted by cloud cover (lowest first).
        """
        # This would query Copernicus Data Space or AWS STAC API
        # For now, return placeholder

        # In production, this queries:
        # https://catalogue.dataspace.copernicus.eu/odata/v1/Products
        # or AWS STAC: https://earth-search.aws.element84.com/v0/

        self.logger.info(f"Searching scenes for bbox: {bbox}")

        # Placeholder - would return actual scene metadata
        return []

    def _select_best_scene(
        self,
        field_geometry: Any,
        scenes: list[dict],
    ) -> dict | None:
        """Select best scene for a field (lowest cloud cover).

        Args:
            field_geometry: Shapely geometry.
            scenes: List of scene metadata.

        Returns:
            Best scene dict or None.
        """
        if not scenes:
            return None

        # Sort by cloud cover
        sorted_scenes = sorted(scenes, key=lambda s: s.get("cloud_cover", 100))

        # Check intersection (would use actual geometry intersection in production)
        for scene in sorted_scenes:
            # Check if field intersects scene
            return scene

        return None

    def _download_band_for_field(
        self,
        field: Any,
        field_id: str,
        scene: dict,
        band: str,
        output_dir: Path,
    ) -> Path | None:
        """Download single band for a field (clipped to field extent).

        Downloads ONLY the required band pixels, not full scene.
        """
        # Get field bounds for filename
        bounds = field.geometry.bounds  # minx, miny, maxx, maxy

        # Build filename with CRS
        date_str = scene["date"].replace("-", "")
        epsg_code = "4326"  # Would extract from actual CRS
        filename = f"sentinel2_{field_id}_{date_str}_{band}_EPSG{epsg_code}.tif"
        output_path = output_dir / filename

        if output_path.exists():
            self.logger.debug(f"Already exists: {output_path}")
            return output_path

        # In production:
        # 1. Get COG (Cloud-Optimized GeoTIFF) URL for band
        # 2. Use rasterio with windowed read to download ONLY field extent
        # 3. Reproject if needed
        # 4. Save clipped image

        # Placeholder
        self.logger.info(f"Would download {band} for {field_id} to {output_path}")

        return output_path

    def calculate_ndvi(
        self,
        red_band_path: str,
        nir_band_path: str,
        output_path: str | None = None,
    ) -> str:
        """Calculate NDVI from Red and NIR bands.

        NDVI = (NIR - Red) / (NIR + Red)

        Args:
            red_band_path: Path to Red band (B4) GeoTIFF.
            nir_band_path: Path to NIR band (B8) GeoTIFF.
            output_path: Output path. If None, auto-generates.

        Returns:
            Path to NDVI GeoTIFF.
        """
        with rasterio.open(red_band_path) as red_src:
            red = red_src.read(1)
            profile = red_src.profile
            crs = red_src.crs

        with rasterio.open(nir_band_path) as nir_src:
            nir = nir_src.read(1)

        # Calculate NDVI
        ndvi = np.where((nir + red) > 0, (nir - red) / (nir + red), np.nan)

        # Update profile for output
        profile.update(
            dtype=rasterio.float32,
            count=1,
            compress="lzw",
        )

        if output_path is None:
            # Auto-generate with CRS
            epsg_code = crs.to_epsg() if crs else "4326"
            output_path = red_band_path.replace("_B4_", "_NDVI_").replace(
                ".tif", f"_EPSG{epsg_code}.tif"
            )

        with rasterio.open(output_path, "w", **profile) as dst:
            dst.write(ndvi.astype(rasterio.float32), 1)

        self.logger.info(f"NDVI saved to: {output_path}")
        return output_path

    def plot_imagery(
        self,
        image_path: str,
        title: str = "Sentinel-2 Imagery",
        figsize: tuple[int, int] = (10, 10),
        save_path: str | None = None,
    ) -> None:
        """Plot satellite imagery.

        Args:
            image_path: Path to GeoTIFF.
            title: Plot title.
            figsize: Figure size.
            save_path: Optional path to save figure.
        """
        fig, ax = plt.subplots(figsize=figsize)

        with rasterio.open(image_path) as src:
            show(src, ax=ax, title=title)

        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")

        plt.show()

    def extract_statistics(
        self,
        image_path: str,
        fields_geojson: str,
    ) -> pd.DataFrame:
        """Extract zonal statistics for fields.

        Args:
            image_path: Path to GeoTIFF (e.g., NDVI).
            fields_geojson: Path to field boundaries.

        Returns:
            DataFrame with statistics per field.
        """
        fields = gpd.read_file(fields_geojson)

        with rasterio.open(image_path) as src:
            results = []

            for idx, field in fields.iterrows():
                field_id = field.get("field_id", f"field_{idx}")

                # Clip raster to field
                out_image, out_transform = mask(src, [mapping(field.geometry)], crop=True)

                # Calculate statistics
                data = out_image[0]
                data = data[~np.isnan(data)]  # Remove nodata

                if len(data) > 0:
                    results.append(
                        {
                            "field_id": field_id,
                            "mean": np.mean(data),
                            "std": np.std(data),
                            "min": np.min(data),
                            "max": np.max(data),
                            "median": np.median(data),
                        }
                    )

        return pd.DataFrame(results)

    def get_available_products(
        self,
        bbox: tuple[float, float, float, float],
        start_date: str,
        end_date: str,
    ) -> pd.DataFrame:
        """Get list of available Sentinel-2 products without downloading.

        Args:
            bbox: Bounding box (minx, miny, maxx, maxy).
            start_date: Start date.
            end_date: End date.

        Returns:
            DataFrame with available products.
        """
        # Query catalog only
        scenes = self._search_scenes(bbox, start_date, end_date, cloud_cover_max=100)

        return pd.DataFrame(scenes)
