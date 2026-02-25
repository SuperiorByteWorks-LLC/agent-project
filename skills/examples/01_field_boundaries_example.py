"""Example 01: Field Boundaries Download and Visualization

This example shows how to download a small subset of field boundaries
and visualize them. Optimized for small machines.

Output:
    - fields_EPSG4326.geojson - Field boundaries with CRS in filename
    - fields_map.png - Visualization map
"""

import sys
from pathlib import Path

# Add skills root to path
_skills_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_skills_root / "field-boundaries" / "scripts"))

from field_boundaries import FieldBoundariesSkill
def main():
    """Download and visualize field boundaries."""
    print("=" * 60)
    print("Example 01: Field Boundaries Download")
    print("=" * 60)

    # Initialize skill
    skill = FieldBoundariesSkill()

    # Step 1: Download small subset of fields
    # Keep count small (20-50) for efficient local processing
    print("\n1. Downloading field boundaries (small subset)...")
    fields = skill.download(
        count=20,  # Small for local machine
        regions=["corn_belt", "great_plains"],
        crops=["corn", "soybeans"],
        output_path="data/examples/fields_EPSG4326.geojson",
    )
    print(f"   Downloaded {len(fields)} fields")

    # Step 2: Get summary statistics
    print("\n2. Field summary:")
    summary = skill.get_summary(fields)
    print(f"   Total fields: {summary['total_fields']}")
    print(f"   Total area: {summary['total_area_acres']:.1f} acres")
    print(f"   Average size: {summary['avg_field_size']:.1f} acres")
    print(f"   Size range: {summary['size_range'][0]:.1f} - {summary['size_range'][1]:.1f} acres")

    # Step 3: Filter by size (optional)
    print("\n3. Filtering large fields (>100 acres)...")
    large_fields = skill.filter_by_size(fields, min_acres=100)
    print(f"   Found {len(large_fields)} large fields")

    # Step 4: Visualize
    print("\n4. Creating visualization...")
    skill.plot_fields(
        fields,
        title="Agricultural Field Boundaries",
        color_by="crop_name",
        save_path="data/examples/fields_map.png",
    )

    print("\n" + "=" * 60)
    print("Complete! Output files:")
    print("  - data/examples/fields_EPSG4326.geojson")
    print("  - data/examples/fields_map.png")
    print("=" * 60)

    return fields


if __name__ == "__main__":
    main()
