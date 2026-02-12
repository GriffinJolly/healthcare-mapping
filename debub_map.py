import pandas as pd
import folium

# Load data
df = pd.read_csv('data/processed/healthcare_facilities_clean.csv')

print(f"Total facilities: {len(df)}")
print(f"\nFirst 5 facilities:")
print(df[['name', 'latitude', 'longitude', 'category']].head())

# Create simple map with just 10 markers for testing
center_lat = df['latitude'].mean()
center_lon = df['longitude'].mean()

m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

# Add just the first 10 markers
for idx, row in df.head(10).iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=row['name'],
        icon=folium.Icon(color='red', icon='plus', prefix='fa')
    ).add_to(m)
    print(f"Added marker: {row['name']} at {row['latitude']}, {row['longitude']}")

m.save('outputs/test_map.html')
print("\nTest map saved to: outputs/test_map.html")
print("If you can see 10 markers, the data is fine!")