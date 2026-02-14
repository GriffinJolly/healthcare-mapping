# Healthcare Mapping & Accessibility Analysis Project

A comprehensive Python project for collecting, cleaning, analyzing, and visualizing healthcare facility data from OpenStreetMap (OSM) with advanced spatial accessibility analysis for Chennai, India.

## Project Overview

This project demonstrates a complete data pipeline from raw OpenStreetMap data collection to sophisticated spatial accessibility analysis, including:
- Healthcare facility mapping and categorization
- Spatial accessibility analysis using grid-based distance calculations
- Identification of underserved areas
- Interactive heatmaps and visualizations
- Comprehensive reporting with actionable recommendations

## Key Features

### Data Pipeline
- **Data Collection**: Fetches healthcare facility data from OpenStreetMap using Overpass API with retry logic
- **Data Cleaning**: Processes raw data, removes duplicates, and categorizes facilities
- **Spatial Analysis**: Advanced accessibility analysis using KDTree algorithms for efficient distance calculations
- **Visualization**: Interactive maps, heatmaps, and statistical charts
- **Reporting**: Automated generation of comprehensive reports with recommendations

### Analysis Capabilities
- **Distance Metrics**: Calculate average, median, and maximum distances to healthcare facilities
- **Coverage Analysis**: Percentage of area within 1km, 2km, 5km, and 10km of facilities
- **Underserved Area Identification**: Pinpoint locations lacking adequate healthcare access
- **Facility Type Analysis**: Compare accessibility between hospitals, clinics, and pharmacies
- **Heatmap Generation**: Visual representation of healthcare accessibility across the city

## Project Structure

```
healthcare_mapping/
├── data_collection.py              # Fetches data from OpenStreetMap with retry logic
├── data_cleaning.py               # Cleans, categorizes, and visualizes data
├── create_map.py                  # Original interactive map generator
├── create_fixed_map.py            # Improved map with better error handling
├── ultra_simple_map.py            # Simple test map for debugging
├── debub_map.py                  # Debug map with limited markers
├── acessibility_analysis.py        # Core spatial accessibility analysis
├── create_heatmap.py             # Generates accessibility heatmaps
├── generate_final_report.py       # Creates comprehensive analysis reports
├── data/
│   ├── raw/                      # Raw OSM data (CSV, JSON)
│   └── processed/                # Cleaned data and analysis results
├── outputs/                      # Generated maps, charts, and reports
└── README.md                     # This file
```

## Installation

Install required packages:

```bash
pip install pandas folium overpy matplotlib seaborn scipy geopy numpy
```

### Package Details
- **pandas**: Data manipulation and analysis
- **folium**: Interactive map creation
- **overpy**: OpenStreetMap Overpass API client
- **matplotlib/seaborn**: Data visualization
- **scipy**: Scientific computing (KDTree for spatial analysis)
- **geopy**: Geodesic distance calculations
- **numpy**: Numerical computing

## Usage

### Complete Analysis Pipeline

Run the full analysis pipeline in order:

```bash
# 1. Collect healthcare facility data
python data_collection.py

# 2. Clean and categorize data
python data_cleaning.py

# 3. Perform accessibility analysis
python acessibility_analysis.py

# 4. Generate accessibility heatmap
python create_heatmap.py

# 5. Generate final report
python generate_final_report.py
```

### Individual Components

#### 1. Data Collection
```bash
python data_collection.py
```
- Queries Overpass API for healthcare facilities
- Handles API timeouts with exponential backoff retries
- Saves raw data to `data/raw/`
- Supports hospitals, clinics, pharmacies, and specialized facilities

#### 2. Data Cleaning & Visualization
```bash
python data_cleaning.py
```
- Removes duplicate facilities based on coordinates
- Categorizes facilities into 9 types
- Generates data quality reports and visualizations
- Creates facility distribution charts

#### 3. Accessibility Analysis
```bash
python acessibility_analysis.py
```
- Creates 100x100 analysis grid (10,000 points)
- Calculates distances using efficient KDTree algorithm
- Identifies underserved areas (>5km from facilities)
- Generates comprehensive accessibility metrics

#### 4. Interactive Heatmap
```bash
python create_heatmap.py
```
- Creates accessibility heatmap with color gradients
- Red areas = Poor access, Green areas = Good access
- Includes facility markers and interactive legends
- Saves as interactive HTML map

#### 5. Final Report Generation
```bash
python generate_final_report.py
```
- Generates comprehensive analysis report
- Includes executive summary and recommendations
- Identifies top underserved locations
- Creates both detailed and summary reports

## Data Categories

The project categorizes healthcare facilities into:

- **Hospitals** - Major medical centers and hospitals
- **Clinics** - Medical clinics and doctor offices
- **Pharmacies** - Medicine stores and pharmacies
- **Health Centers** - Community health centers
- **Dental** - Dental clinics and hospitals
- **Laboratory** - Medical laboratories and diagnostic centers
- **Therapy** - Physical therapy and rehabilitation centers
- **Specialized Care** - Specialized medical facilities
- **Alternative/Mental Health** - Alternative medicine and mental health facilities

## 🎯 Key Insights & Recommendations

### Identified Issues
1. **Access Inequality**: 14.2% of Chennai area >5km from healthcare
2. **Hospital Concentration**: Hospitals more centrally located than clinics/pharmacies
3. **Peripheral Gaps**: Outer areas have significantly worse access
4. **Distance Barriers**: Some areas face 10km+ travel for basic healthcare

### Strategic Recommendations
1. **Targeted Facility Placement**: Focus on identified underserved grid points
2. **Peripheral Expansion**: Extend clinic/pharmacy coverage in outer areas
3. **Mobile Health Solutions**: Consider mobile clinics for extremely remote areas
4. **Data Integration**: Combine with population density for prioritization

## 🗺️ Generated Outputs

### Maps & Visualizations
- `healthcare_facilities_map.html` - Interactive facility map
- `healthcare_facilities_map_fixed.html` - Improved map with better rendering
- `accessibility_heatmap.html` - Accessibility heatmap with color gradients
- `01_data_quality_overview.png` - Data quality charts
- `accessibility_analysis.png` - Comprehensive analysis visualizations

### Reports & Data
- `FINAL_REPORT.txt` - Comprehensive analysis report with recommendations
- `SUMMARY.txt` - Quick summary for sharing
- `accessibility_summary.csv` - Key metrics spreadsheet
- `accessibility_grid.csv` - Detailed grid analysis data
- `healthcare_facilities_clean.csv` - Cleaned facility dataset

## 📈 Key Findings (Chennai Analysis)

### Facility Distribution
- **Total facilities**: 1,385
- **Hospitals**: 600 (43.3%)
- **Clinics**: 400 (28.9%)
- **Pharmacies**: 213 (15.4%)
- **Health Centers**: 53 (3.8%)
- **Dental facilities**: 80 (5.8%)
- **Laboratories**: 21 (1.5%)

### Accessibility Metrics
- **Median distance to healthcare**: 1.47 km
- **Average distance**: 1.82 km
- **Maximum distance**: 10.37 km
- **Areas within 2km**: 78.3%
- **Areas within 5km**: 85.8%
- **Underserved areas (>5km)**: 14.2%

### Hospital-Specific Access
- **Median distance to hospital**: 2.31 km
- **Areas within 5km of hospital**: 72.1%
- **Hospital access gap**: 13.7% worse than overall facility access

## 🔧 Technical Details

### Spatial Analysis Methodology
- **Grid Resolution**: 100x100 grid (10,000 analysis points)
- **Distance Calculation**: KDTree algorithm for efficient nearest-neighbor searches
- **Coordinate System**: WGS84 (latitude/longitude)
- **Distance Metric**: Geodesic distances (great circle distances)

### Performance Optimizations
- **KDTree indexing**: O(n log n) vs O(n²) for distance calculations
- **Vectorized operations**: NumPy for efficient numerical computations
- **Memory management**: Chunked processing for large datasets
- **Error handling**: Comprehensive exception handling and data validation

### Data Sources
- **Primary**: OpenStreetMap via Overpass API
- **Facility types**: amenity=hospital, clinic, doctors, pharmacy
- **Additional**: healthcare=* tags for specialized facilities
- **Metadata**: name, address, phone, operator where available

## 🔍 Error Handling & Robustness

### API Resilience
- **Exponential backoff**: 5, 10, 20 second retries for timeouts
- **Graceful degradation**: Continue analysis with partial data
- **Rate limiting**: Respect Overpass API usage limits

### Data Validation
- **Coordinate validation**: Check for valid latitude/longitude ranges
- **Duplicate detection**: Remove facilities with identical coordinates
- **Category validation**: Ensure facility types are properly classified
- **Missing data handling**: Graceful handling of incomplete OSM entries

### Visualization Robustness
- **HTML escaping**: Prevent XSS attacks in map popups
- **Responsive design**: Maps work on different screen sizes
- **Fallback rendering**: Multiple map generation options
- **Browser compatibility**: Tested across modern browsers

## 🛠️ Technologies Used

### Core Technologies
- **Python 3.x** - Main programming language
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing and array operations
- **SciPy** - Scientific computing and spatial algorithms

### Geospatial & Mapping
- **Folium** - Interactive map creation
- **Leaflet.js** - Web mapping library (via Folium)
- **Geopy** - Geodesic distance calculations
- **OpenStreetMap** - Source of healthcare facility data

### Data Visualization
- **Matplotlib** - Static plotting and charts
- **Seaborn** - Statistical data visualization
- **HTML/CSS/JavaScript** - Interactive map components

### Data Sources
- **Overpass API** - OpenStreetMap data access
- **OpenStreetMap** - Crowdsourced mapping data
- **Healthcare tags** - OSM amenity and healthcare classifications

