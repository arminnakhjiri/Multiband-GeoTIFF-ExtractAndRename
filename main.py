
from pathlib import Path
import rasterio

# =====================================================
# Sentinel-5P: Extract Monthly Bands and Rename Files
# January 2025 - October 2026 (22 months)
# =====================================================

# 1. Settings
INPUT_DIR = Path(
    ...
)

OUTPUT_DIR = Path(
    ...
)

DATA_SOURCE = "Sentinel5P"
PROCESSING_LEVEL = "OFFL_L3"
REGION = "Iran"

START_YEAR = 2025
START_MONTH = 1
NUMBER_OF_MONTHS = 22

PARAMETERS = ["NO2", "SO2", "HCHO", "UVAI", "CO", "CH4", "O3"]
STATISTICS = ["Mean", "Min", "Max"]

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# 2. Generate monthly date labels
def generate_months(year, month, count):
    dates = []

    for _ in range(count):
        dates.append(f"{year:04d}{month:02d}")

        month += 1
        if month > 12:
            month = 1
            year += 1

    return dates


months = generate_months(
    START_YEAR,
    START_MONTH,
    NUMBER_OF_MONTHS
)


# 3. Determine raster resolution from metadata
def get_resolution(src):

    if src.crs is None:
        raise ValueError("Raster CRS is missing.")

    x_res, y_res = src.res

    if src.crs.is_projected:
        unit_factor = src.crs.linear_units_factor[1]
        resolution_m = max(abs(x_res), abs(y_res)) * unit_factor

    elif src.crs.is_geographic:
        # Approximate pixel size at the equator
        resolution_m = max(abs(x_res), abs(y_res)) * 111319.4908

    else:
        raise ValueError("Unsupported CRS units.")

    return f"R{round(resolution_m)}m"


# 4. Process input files
input_files = sorted(
    p for p in INPUT_DIR.iterdir()
    if p.is_file() and p.suffix.lower() in [".tif", ".tiff"]
)

total_outputs = 0

for input_file in input_files:

    # Extract pollutant and statistic from source filename
    parts = input_file.stem.split("_")

    if len(parts) < 2:
        print(f"Skipped: {input_file.name} (invalid filename)")
        continue

    parameter = parts[0].upper()
    statistic = parts[1].capitalize()

    if parameter not in PARAMETERS or statistic not in STATISTICS:
        print(f"Skipped: {input_file.name} (unrecognized product)")
        continue

    try:
        with rasterio.open(input_file) as src:

            # Validate band count
            if src.count != NUMBER_OF_MONTHS:
                print(
                    f"Skipped: {input_file.name} "
                    f"({src.count} bands; expected {NUMBER_OF_MONTHS})"
                )
                continue

            resolution = get_resolution(src)

            print(f"\nProcessing: {input_file.name}")
            print(f"Resolution: {resolution}")
            print(f"Number of bands: {src.count}")

            # Prepare output raster profile
            profile = src.profile.copy()
            profile.update(
                driver="GTiff",
                count=1,
                compress="LZW",
                BIGTIFF="IF_SAFER"
            )

            # Extract individual monthly bands
            for band_index, date in enumerate(months, start=1):

                product_type = f"{parameter}_{statistic}"

                output_name = (
                    f"{DATA_SOURCE}_{product_type}_"
                    f"{PROCESSING_LEVEL}_{REGION}_"
                    f"{date}_{resolution}.tif"
                )

                output_path = OUTPUT_DIR / output_name

                # Read the selected band and its validity mask
                band = src.read(band_index)
                band_mask = src.read_masks(band_index)

                with rasterio.open(output_path, "w", **profile) as dst:

                    dst.write(band, 1)
                    dst.write_mask(band_mask)

                    # Preserve band description and add metadata
                    dst.set_band_description(
                        1, f"{product_type}_{date}"
                    )

                    dst.update_tags(
                        DataSource=DATA_SOURCE,
                        ProductType=product_type,
                        ProcessingLevel=PROCESSING_LEVEL,
                        Region=REGION,
                        Date=date,
                        Resolution=resolution,
                        SourceFile=input_file.name,
                        SourceBand=band_index
                    )

                total_outputs += 1

                print(f"  Saved: {output_name}")

    except Exception as error:
        print(f"Error processing {input_file.name}: {error}")


# 5. Summary
print("\n" + "=" * 55)
print("PROCESSING COMPLETED")
print("=" * 55)
print(f"Input files: {len(input_files)}")
print(f"Output files: {total_outputs}")
print(f"Output directory: {OUTPUT_DIR}")
