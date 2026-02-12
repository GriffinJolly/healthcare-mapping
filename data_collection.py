import overpy
import pandas as pd
import time
import json
import os

# Create directories if they don't exist
os.makedirs('data/raw', exist_ok=True)
os.makedirs('data/processed', exist_ok=True)
os.makedirs('outputs', exist_ok=True)

# Initialize Overpass API
api = overpy.Overpass()

# Retry function for API calls
def query_with_retry(api, query, max_retries=3, initial_delay=5):
    for attempt in range(max_retries):
        try:
            return api.query(query)
        except overpy.exception.OverpassGatewayTimeout as e:
            if attempt < max_retries - 1:
                delay = initial_delay * (2 ** attempt)  # Exponential backoff
                print(f"Server timeout (attempt {attempt + 1}/{max_retries}). Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                raise e
        except Exception as e:
            raise e

# Define your area of interest
city_name = "Chennai"
state_name = "Tamil Nadu"
country = "India"

print(f"Fetching data for {city_name}, {state_name}, {country}")

# Query to get all healthcare facilities
query = f"""
[out:json][timeout:180];
area["name"="{city_name}"]->.searchArea;
(
  node["amenity"="hospital"](area.searchArea);
  way["amenity"="hospital"](area.searchArea);
  node["amenity"="clinic"](area.searchArea);
  way["amenity"="clinic"](area.searchArea);
  node["amenity"="doctors"](area.searchArea);
  way["amenity"="doctors"](area.searchArea);
  node["amenity"="pharmacy"](area.searchArea);
  way["amenity"="pharmacy"](area.searchArea);
  node["healthcare"](area.searchArea);
  way["healthcare"](area.searchArea);
);
out center;
"""

try:
    result = query_with_retry(api, query)
    print(f"✓ Query successful!")
    
    # Initialize the facilities list HERE (this was missing!)
    facilities = []
    
    # Process nodes (point locations)
    print(f"Processing {len(result.nodes)} nodes...")
    for node in result.nodes:
        facility = {
            'id': node.id,
            'name': node.tags.get('name', 'Unnamed'),
            'type': node.tags.get('amenity') or node.tags.get('healthcare', 'unknown'),
            'latitude': float(node.lat),
            'longitude': float(node.lon),
            'address': node.tags.get('addr:street', ''),
            'phone': node.tags.get('phone', ''),
            'operator': node.tags.get('operator', ''),
            'emergency': node.tags.get('emergency', 'no'),
            'source': 'OSM'
        }
        facilities.append(facility)
    
    # Process ways (building outlines) - use center point
    print(f"Processing {len(result.ways)} ways...")
    for way in result.ways:
        facility = {
            'id': way.id,
            'name': way.tags.get('name', 'Unnamed'),
            'type': way.tags.get('amenity') or way.tags.get('healthcare', 'unknown'),
            'latitude': float(way.center_lat),
            'longitude': float(way.center_lon),
            'address': way.tags.get('addr:street', ''),
            'phone': way.tags.get('phone', ''),
            'operator': way.tags.get('operator', ''),
            'emergency': way.tags.get('emergency', 'no'),
            'source': 'OSM'
        }
        facilities.append(facility)
    
    # Check if we found anything
    if len(facilities) == 0:
        print("\n⚠ Warning: No facilities found!")
        print("This could mean:")
        print("1. The area name might be misspelled")
        print("2. The area is not well-mapped in OpenStreetMap")
        print("3. Try a different city or use bounding box method")
        exit()
    
    # Convert to DataFrame
    df = pd.DataFrame(facilities)
    
    print(f"\n{'='*60}")
    print(f"RESULTS SUMMARY")
    print(f"{'='*60}")
    print(f"Total facilities found: {len(df)}")
    print(f"\nBreakdown by type:")
    print(df['type'].value_counts())
    print(f"\nFacilities with names: {df['name'].ne('Unnamed').sum()}")
    print(f"Facilities with addresses: {df['address'].ne('').sum()}")
    
    # Display first few facilities
    print(f"\n{'='*60}")
    print("SAMPLE FACILITIES:")
    print(f"{'='*60}")
    print(df[['name', 'type', 'address']].head(10).to_string())
    
    # Save to CSV
    df.to_csv('data/raw/osm_healthcare_facilities.csv', index=False)
    print(f"\n✓ Data saved to: data/raw/osm_healthcare_facilities.csv")
    
    # Also save as JSON for backup
    with open('data/raw/osm_healthcare_facilities.json', 'w', encoding='utf-8') as f:
        json.dump(facilities, f, indent=2, ensure_ascii=False)
    print(f"✓ Backup saved to: data/raw/osm_healthcare_facilities.json")
    
    print(f"\n{'='*60}")
    print("SUCCESS! Data collection complete.")
    print(f"{'='*60}")
    print(f"\nNext steps:")
    print(f"1. Check the CSV file to verify the data looks good")
    print(f"2. Run the data cleaning script next")
    
except Exception as e:
    print(f"✗ Error: {e}")
    print(f"\nError type: {type(e).__name__}")
    import traceback
    print(f"\nFull traceback:")
    traceback.print_exc()
    print(f"\nTroubleshooting tips:")
    print("1. Check if the city name is spelled correctly")
    print("2. Try a larger city if data is sparse")
    print("3. The area might not be well-mapped in OSM")