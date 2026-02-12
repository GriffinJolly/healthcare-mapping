# Healthcare Mapping Project

A comprehensive Python project for collecting, cleaning, and visualizing healthcare facility data from OpenStreetMap (OSM) for Chennai, India.

## Project Overview

This project demonstrates the complete data pipeline from raw OpenStreetMap data collection to interactive visualization of healthcare facilities including hospitals, clinics, pharmacies, and specialized care centers.

## Features

- **Data Collection**: Fetches healthcare facility data from OpenStreetMap using Overpass API
- **Data Cleaning**: Processes raw data, removes duplicates, and categorizes facilities
- **Interactive Mapping**: Creates beautiful, interactive maps with Folium
- **Data Visualization**: Generates charts and statistics about healthcare facility distribution
- **Error Handling**: Robust retry logic for API timeouts and data validation

## Project Structure

```
healthcare_mapping/
├── data_collection.py          # Fetches data from OpenStreetMap
├── data_cleaning.py           # Cleans and processes the data
├── create_map.py              # Creates interactive maps
├── create_fixed_map.py        # Improved map generator with error handling
├── ultra_simple_map.py        # Simple map for testing
├── debub_map.py              # Debug map with limited markers
├── data/
│   ├── raw/                   # Raw OSM data (CSV, JSON)
│   └── processed/             # Cleaned data
├── outputs/                   # Generated maps and visualizations
└── README.md                  # This file
```

## Installation

Install the required packages:

```bash
pip install pandas folium overpy matplotlib
```

## Usage

### 1. Data Collection

Fetch healthcare facilities for Chennai from OpenStreetMap:

```bash
python data_collection.py
```

This will:
- Query the Overpass API for healthcare facilities
- Handle API timeouts with automatic retries
- Save raw data to `data/raw/`
- Display statistics about the collected data

### 2. Data Cleaning

Process and clean the collected data:

```bash
python data_cleaning.py
```

This will:
- Remove duplicate facilities
- Categorize facilities by type
- Generate data quality reports
- Create visualization charts
- Save cleaned data to `data/processed/`

### 3. Map Creation

Generate interactive maps:

```bash
# Original map (may have rendering issues)
python create_map.py

# Fixed map with better error handling
python create_fixed_map.py

# Simple test map
python ultra_simple_map.py
```

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

## Map Features

The interactive maps include:

- **Color-coded markers** by facility type
- **Interactive popups** with facility details
- **Legend** showing facility categories and counts
- **Zoom and pan** functionality
- **Responsive design** for different screen sizes

## Sample Results

For Chennai, Tamil Nadu, the project found:
- **Total facilities**: 1,385
- **Hospitals**: 600
- **Clinics**: 400
- **Pharmacies**: 213
- **Health Centers**: 53
- **Dental facilities**: 80
- **Laboratories**: 21

## Error Handling

The project includes robust error handling for:
- **API timeouts** with exponential backoff retries
- **Data validation** and cleaning
- **Missing coordinates** and invalid data
- **HTML escaping** for safe map rendering

## Technologies Used

- **Python** - Core programming language
- **Pandas** - Data manipulation and analysis
- **Folium** - Interactive map creation
- **Overpy** - OpenStreetMap Overpass API client
- **Matplotlib** - Data visualization
- **Leaflet** - Interactive mapping library (via Folium)
- **OpenStreetMap** - Source of healthcare facility data

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Acknowledgments

- **OpenStreetMap** contributors for the healthcare facility data
- **Overpass API** for providing efficient data access
- **Folium** team for the excellent Python mapping library

## Future Enhancements

- [ ] Support for multiple cities
- [ ] Real-time data updates
- [ ] Advanced spatial analysis
- [ ] Facility density heatmaps
- [ ] Route planning to nearest facilities
- [ ] Integration with other healthcare datasets
