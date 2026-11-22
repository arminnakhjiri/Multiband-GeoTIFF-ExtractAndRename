# Multiband GeoTIFF Extractor

A Python utility for extracting individual bands from multiband GeoTIFF files and exporting them as separate single-band rasters with **standardized, metadata-based filenames**.

The script automatically identifies the input product and statistic, extracts individual bands, assigns corresponding monthly timestamps, derives the nominal spatial resolution from raster metadata, and generates consistently named GeoTIFF files.

## 📌 Overview

- **Language**: Python
- **Library**: Rasterio
- **Input Format**: Multiband GeoTIFF (`.tif`, `.tiff`)
- **Output Format**: Single-band GeoTIFF
- **Temporal Coverage**: Configurable (default: January 2025–October 2026)
- **Number of Bands**: Configurable (default: 22)
- **Processing**: Individual band extraction and file renaming
- **Metadata Handling**: Preserves geospatial information, band descriptions, and raster validity masks
- **Resolution**: Automatically derived from raster geospatial metadata
- **Output Organization**: Separate output directory

## 🚀 How to Use

### 1. Install Dependencies

Install Rasterio using pip:

```bash
pip install rasterio
```

### 2. Configure Input and Output Directories

Specify the directory containing your input GeoTIFF files:

```python
INPUT_DIR = Path(r"D:\your\input\directory")
```

The script automatically creates a `monthly_bands` subdirectory for the extracted files.

### 3. Prepare Input Files

Input filenames should follow this convention:

```text
{Parameter}_{Statistic}.tif
```

Examples:

```text
NO2_Mean.tif
NO2_Min.tif
NO2_Max.tif
SO2_Mean.tif
SO2_Min.tif
SO2_Max.tif
```

The script supports the following parameter identifiers:

`NO2`, `SO2`, `HCHO`, `UVAI`, `CO`, `CH4`, `O3`

Supported statistics:

`Mean`, `Min`, `Max`

Each input raster must contain the expected number of bands, corresponding to the specified temporal coverage.

### 4. Configure Temporal Settings

Modify the following parameters according to your data:

```python
START_YEAR = 2025
START_MONTH = 1
NUMBER_OF_MONTHS = 22
```

The script automatically generates the corresponding monthly timestamps.

### 5. Run the Script

Execute the Python script:

```bash
python split_geotiff_bands.py
```

The script processes all recognized `.tif` and `.tiff` files in the input directory and exports the extracted bands to the output directory.

### 6. Check the Outputs

The Console displays the processing status, generated filenames, raster resolution, and total number of exported files.

## 📂 Processing Workflow

The script follows these steps:

1. **Input identification:** Scans the specified directory for GeoTIFF files.
2. **Product identification:** Extracts the parameter and statistic identifiers from the input filenames.
3. **Band validation:** Checks whether the input raster contains the expected number of bands.
4. **Temporal indexing:** Assigns a monthly timestamp to each band based on the configured starting date.
5. **Resolution detection:** Derives the nominal pixel resolution from the raster's CRS and spatial resolution.
6. **Band extraction:** Reads and exports each band as an independent single-band GeoTIFF.
7. **Metadata preservation:** Retains the spatial reference, geotransform, raster dimensions, data type, and validity mask.
8. **Filename generation:** Creates standardized filenames using the extracted product information and temporal and spatial metadata.

## 🏷️ Output Naming Convention

All output files follow this naming structure:

```text
Sentinel5P_{ProductType}_{ProcessingLevel}_{Region}_{Date}_{Resolution}.tif
```

Where:

| Component | Description | Example |
|---|---|---|
| DataSource | Data provider/platform identifier | `Sentinel5P` |
| ProductType | Parameter and statistical measure | `NO2_Mean` |
| ProcessingLevel | Processing product identifier | `OFFL_L3` |
| Region | Geographic region | `Iran` |
| Date | Monthly timestamp (YYYYMM) | `202501` |
| Resolution | Nominal spatial resolution | `R1113m` |
| Format | Output raster format | `.tif` |

**Example filenames:**

```text
Sentinel5P_NO2_Mean_OFFL_L3_Iran_202501_R1113m.tif
Sentinel5P_NO2_Mean_OFFL_L3_Iran_202502_R1113m.tif
Sentinel5P_NO2_Min_OFFL_L3_Iran_202501_R1113m.tif
Sentinel5P_SO2_Max_OFFL_L3_Iran_202510_R1113m.tif
```

## 📁 Directory Structure

```text
project/
│
├── split_geotiff_bands.py
│
├── README.md
│
└── data/
    │
    ├── input/
    │   ├── NO2_Mean.tif
    │   ├── NO2_Min.tif
    │   ├── NO2_Max.tif
    │   └── ...
    │
    └── monthly_bands/
        ├── Sentinel5P_NO2_Mean_OFFL_L3_Iran_202501_R1113m.tif
        ├── Sentinel5P_NO2_Mean_OFFL_L3_Iran_202502_R1113m.tif
        ├── Sentinel5P_NO2_Min_OFFL_L3_Iran_202501_R1113m.tif
        └── ...
```

## ⚙️ Technical Notes

- Original multiband GeoTIFF files remain unchanged.
- Each output file contains exactly one raster band.
- Spatial reference information and georeferencing are preserved.
- Raster validity masks are retained during extraction.
- The nominal resolution is derived from raster metadata rather than assigned as a fixed value.
- Files with unrecognized naming conventions or unexpected band counts are skipped.
- The output directory is created automatically if it does not exist.
- The temporal configuration must match the actual chronological ordering of bands in the input rasters.

**Note:** Resolution labels derived from geographic coordinate systems are approximate conversions to meters at the equator. For accurate spatial resolution reporting, projected coordinate systems are preferable.

## 📦 Requirements

| Package | Purpose |
|---|---|
| Python 3 | Scripting environment |
| Rasterio | GeoTIFF reading, writing, and metadata handling |
| pathlib | File and directory management |

---

## Author

**Armin Nakhjiri**  
Remote Sensing Scientist  
✉️ Nakhjiri.Armin@gmail.com

---

*Empowering the next generation of geospatial analysts, one script at a time.*
