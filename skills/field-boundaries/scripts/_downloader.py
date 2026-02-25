"""Standalone field boundary downloader using USDA Crop Sequence Boundaries.

Self-contained — no agri_toolkit dependency. Queries USDA NASS Crop Sequence
Boundaries (CSB) from Source Cooperative via DuckDB.

Data Source:
    USDA NASS Crop Sequence Boundaries (2023)
    https://source.coop/fiboa/us-usda-cropland

Coverage:
    Entire contiguous United States, 16+ million field boundaries
"""

import logging
from pathlib import Path
from typing import Any

import duckdb
import geopandas as gpd

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
_logger = logging.getLogger("agri_skills.field_boundaries")


class FieldBoundaryDownloader:
    """Download field boundary polygons from USDA Crop Sequence Boundaries.

    Accesses USDA NASS CSB data hosted on Source Cooperative in
    cloud-optimized GeoParquet format via DuckDB with server-side filtering.

    Regions:
        - corn_belt:   IL, IA, IN, OH, MN (major corn and soybean production)
        - great_plains: KS, NE, SD, ND, TX (wheat and diverse crops)
        - southeast:   AR, MS, LA, GA (cotton, rice, soybeans)

    Crops: Corn (1), soybeans (5), wheat (various), cotton (2) — CDL codes
    """

    SOURCE_COOP_URL = "https://data.source.coop/fiboa/us-usda-cropland/us_usda_cropland.parquet"

    REGION_STATE_FIPS = {
        "corn_belt": ["17", "19", "18", "39", "27"],  # IL, IA, IN, OH, MN
        "great_plains": ["20", "31", "46", "38", "48"],  # KS, NE, SD, ND, TX
        "southeast": ["05", "28", "22", "13"],  # AR, MS, LA, GA
    }

    CROP_TYPES = {
        "corn": ["1"],
        "soybeans": ["5"],
        "wheat": ["23", "24", "25", "26", "27"],
        "cotton": ["2"],
    }

    def __init__(
        self,
        data_root: str = "data",
        data_source_url: str | None = None,
    ) -> None:
        self.logger = _logger
        self._data_root = Path(data_root)
        self.raw_data_path = self._data_root / "raw"
        self.output_subdir = "field_boundaries"
        self.data_source_url = data_source_url or self.SOURCE_COOP_URL
        self._duckdb_conn: duckdb.DuckDBPyConnection | None = None
        self.raw_data_path.mkdir(parents=True, exist_ok=True)

    def _get_duckdb_connection(self) -> duckdb.DuckDBPyConnection:
        if self._duckdb_conn is None:
            self._duckdb_conn = duckdb.connect()
            self._duckdb_conn.execute("INSTALL spatial;")
            self._duckdb_conn.execute("LOAD spatial;")
            self._duckdb_conn.execute("INSTALL httpfs;")
            self._duckdb_conn.execute("LOAD httpfs;")
            self.logger.debug("DuckDB connection initialized with spatial extensions")
        return self._duckdb_conn

    def download(
        self,
        count: int = 200,
        regions: list[str] | None = None,
        crops: list[str] | None = None,
        output_format: str = "geojson",
    ) -> gpd.GeoDataFrame:
        """Download field boundaries from Source Cooperative.

        Args:
            count: Number of fields to download (default: 200).
            regions: Regions to sample from. Options: 'corn_belt',
                'great_plains', 'southeast'. Default: ['corn_belt'].
            crops: Crop types to include. Options: 'corn', 'soybeans',
                'wheat', 'cotton'. Default: ['corn', 'soybeans'].
            output_format: Output format ('geojson' or 'geoparquet').

        Returns:
            GeoDataFrame with field boundaries in EPSG:4326.
        """
        if count < 1:
            raise ValueError("count must be at least 1")

        regions = regions or ["corn_belt"]
        crops = crops or ["corn", "soybeans"]

        invalid_regions = [r for r in regions if r not in self.REGION_STATE_FIPS]
        if invalid_regions:
            raise ValueError(
                f"Invalid regions: {invalid_regions}. "
                f"Valid options: {list(self.REGION_STATE_FIPS.keys())}"
            )

        invalid_crops = [c for c in crops if c not in self.CROP_TYPES]
        if invalid_crops:
            raise ValueError(
                f"Invalid crops: {invalid_crops}. Valid options: {list(self.CROP_TYPES.keys())}"
            )

        self.logger.info("Downloading %d fields — regions: %s, crops: %s", count, regions, crops)
        fields_gdf = self._query_source_cooperative(count=count, regions=regions, crops=crops)

        if not self._validate(fields_gdf):
            raise RuntimeError("Downloaded field data failed validation")

        output_path = self._save_fields(fields_gdf, output_format)
        self.logger.info("Fields saved to: %s", output_path)
        return fields_gdf

    def _query_source_cooperative(
        self,
        count: int,
        regions: list[str],
        crops: list[str],
    ) -> gpd.GeoDataFrame:
        try:
            con = self._get_duckdb_connection()

            state_fips: list[str] = []
            for region in regions:
                state_fips.extend(self.REGION_STATE_FIPS[region])
            state_filter = ", ".join(f"'{f}'" for f in state_fips)

            crop_codes: list[str] = []
            for crop in crops:
                crop_codes.extend(self.CROP_TYPES[crop])
            crop_filter = ", ".join(f"'{c}'" for c in crop_codes)

            request_count = max(count * 2, count + 10)

            query = f"""
            SELECT
                id as field_id,
                substr(id, 1, 2) as state_fips,
                "crop:code" as crop_code,
                "crop:name" as crop_name,
                "crop:code_list" as crop_code_list,
                ST_AsWKB(geometry) as geometry
            FROM read_parquet('{self.data_source_url}')
            WHERE substr(id, 1, 2) IN ({state_filter})
            AND "crop:code" IN ({crop_filter})
            ORDER BY random()
            LIMIT {request_count}
            """

            self.logger.info("Querying Source Cooperative (10-30 seconds)...")
            result_df = con.execute(query).df()

            if len(result_df) == 0:
                raise RuntimeError(
                    "No fields found matching criteria. Try different regions/crops."
                )

            self.logger.info("Retrieved %d rows from Source Cooperative", len(result_df))

            # Convert WKB geometry
            if "geometry" in result_df.columns and len(result_df) > 0:
                first_geom = result_df["geometry"].iloc[0]
                if not isinstance(first_geom, bytes) and hasattr(first_geom, "__iter__"):
                    result_df["geometry"] = result_df["geometry"].apply(bytes)
                result_df["geometry"] = gpd.GeoSeries.from_wkb(result_df["geometry"])

            # Data is EPSG:5070 — calculate area before reprojecting
            gdf = gpd.GeoDataFrame(result_df, geometry="geometry", crs="EPSG:5070")
            gdf["area_acres"] = gdf.geometry.area / 4046.86

            # Reproject to EPSG:4326
            gdf = gdf.to_crs("EPSG:4326")

            # Filter zero-area fields
            gdf = gdf[gdf["area_acres"] > 0]

            # Limit to requested count
            if len(gdf) > count:
                gdf = gdf.iloc[:count]

            # Map state FIPS → region
            state_to_region: dict[str, str] = {}
            for region, fips_list in self.REGION_STATE_FIPS.items():
                for fips in fips_list:
                    state_to_region[fips] = region
            gdf["region"] = gdf["state_fips"].map(state_to_region).fillna(regions[0])

            return gdf[
                [
                    "field_id",
                    "region",
                    "state_fips",
                    "area_acres",
                    "crop_code",
                    "crop_name",
                    "crop_code_list",
                    "geometry",
                ]
            ]

        except Exception as e:
            self.logger.error("Failed to query Source Cooperative: %s", e)
            raise RuntimeError(f"Data download failed: {e}") from e

    def _validate(self, data: gpd.GeoDataFrame) -> bool:
        if data is None or len(data) == 0:
            self.logger.error("No fields in dataset")
            return False
        for col in ["field_id", "region", "geometry"]:
            if col not in data.columns:
                self.logger.error("Missing required column: %s", col)
                return False
        if data.crs is None:
            self.logger.error("GeoDataFrame has no CRS defined")
            return False
        return True

    def _save_fields(self, gdf: gpd.GeoDataFrame, output_format: str) -> Path:
        output_dir = self.raw_data_path / self.output_subdir
        output_dir.mkdir(parents=True, exist_ok=True)

        if output_format == "geojson":
            output_path = output_dir / "fields.geojson"
            gdf.to_file(output_path, driver="GeoJSON")
        elif output_format == "geoparquet":
            output_path = output_dir / "fields.parquet"
            gdf.to_parquet(output_path)
        else:
            raise ValueError(f"Unsupported format: {output_format}. Use 'geojson' or 'geoparquet'.")

        self.logger.info("Saved %d fields to %s", len(gdf), output_path)
        return output_path

    def __del__(self) -> None:
        if self._duckdb_conn is not None:
            self._duckdb_conn.close()
