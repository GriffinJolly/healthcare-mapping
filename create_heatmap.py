import pandas as pd
import folium
from folium import plugins
import numpy as np

print("="*60)
print("CREATING ACCESSIBILITY HEATMAP")
print("="*60)

# Load the data
facilities_df = pd.read_csv('data/processed/healthcare_facilities_clean.csv')
grid_df = pd.read_csv('data/processed/accessibility_grid.csv')

print(f"\nLoaded {len(facilities_df)} facilities")
print(f"Loaded {len(grid_df)} grid points")

# Calculate center
center_lat = facilities_df['latitude'].mean()
center_lon = facilities_df['longitude'].mean()

# Create map
m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=11,
    tiles='OpenStreetMap'
)

# Prepare heatmap data
# We want to show POOR accessibility as red (high values)
# So we invert the distances: high distance = hot spots (red)
print("\nPreparing heatmap data...")

# Use distance to any facility for the heatmap
heat_data = []
for idx, row in grid_df.iterrows():
    # The heatmap intensity represents distance (farther = more intense/red)
    heat_data.append([
        row['latitude'], 
        row['longitude'], 
        row['distance_to_any_km']  # Higher distance = redder
    ])

# Add heatmap layer
print("Adding heatmap layer...")
plugins.HeatMap(
    heat_data,
    min_opacity=0.4,
    max_zoom=18,
    radius=15,
    blur=20,
    gradient={
        0.0: 'green',    # Close to facilities (good access)
        0.4: 'yellow',   # Medium distance
        0.7: 'orange',   # Far from facilities
        1.0: 'red'       # Very far (poor access)
    }
).add_to(m)

# Add facility markers on top as small dots
print("Adding facility markers...")
for idx, row in facilities_df.iterrows():
    if idx % 100 == 0:
        print(f"  Adding marker {idx}/{len(facilities_df)}...")
    
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=3,
        popup=str(row['name']),
        color='blue',
        fill=True,
        fillColor='blue',
        fillOpacity=0.8,
        weight=1
    ).add_to(m)

# Add legend
legend_html = '''
<div style="position: fixed; 
            bottom: 50px; left: 50px; width: 250px; 
            background-color: white; z-index:9999; 
            border:2px solid grey; border-radius: 8px; 
            padding: 15px; box-shadow: 0 0 10px rgba(0,0,0,0.2);">
    <h4 style="margin-top: 0; text-align: center;">Healthcare Accessibility</h4>
    <div style="background: linear-gradient(to right, green, yellow, orange, red); 
                height: 20px; border-radius: 3px; margin: 10px 0;"></div>
    <div style="display: flex; justify-content: space-between; font-size: 11px;">
        <span>Good Access</span>
        <span>Poor Access</span>
    </div>
    <hr style="margin: 10px 0;">
    <p style="margin: 5px 0; font-size: 12px;">
        <span style="color:blue; font-size: 16px;">●</span> Healthcare Facility
    </p>
    <p style="margin: 5px 0; font-size: 11px; color: gray;">
        Red areas = Far from healthcare<br>
        Green areas = Close to healthcare
    </p>
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

# Add title
title_html = '''
<div style="position: fixed; 
            top: 10px; left: 50%; transform: translateX(-50%);
            background-color: white; z-index:9999; 
            border:2px solid grey; border-radius: 8px; 
            padding: 10px; text-align: center;
            box-shadow: 0 0 10px rgba(0,0,0,0.2);">
    <h3 style="margin: 0;">Chennai Healthcare Accessibility Heatmap</h3>
    <p style="margin: 5px 0; font-size: 12px; color: gray;">
        Red = Underserved Areas | Green = Good Access
    </p>
</div>
'''
m.get_root().html.add_child(folium.Element(title_html))

# Save map
output_path = 'outputs/accessibility_heatmap.html'
m.save(output_path)

print(f"\n{'='*60}")
print("HEATMAP CREATED!")
print(f"{'='*60}")
print(f"Saved to: {output_path}")
print("\nOpen the file to see:")
print("  - Red areas: Far from healthcare facilities (underserved)")
print("  - Green areas: Close to healthcare facilities (well-served)")
print("  - Blue dots: Individual healthcare facilities")