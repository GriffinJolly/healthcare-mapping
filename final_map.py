import pandas as pd
import folium

print("Creating final map...")

# Load data
df = pd.read_csv('data/processed/healthcare_facilities_clean.csv')
print(f"Loaded {len(df)} facilities")

# Calculate center
center_lat = df['latitude'].mean()
center_lon = df['longitude'].mean()

# Create map
m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=11,
    tiles='OpenStreetMap'
)

# Simple color mapping
color_map = {
    'Hospital': 'red',
    'Clinic': 'blue',
    'Pharmacy': 'green',
    'Health Center': 'orange',
    'Dental': 'purple',
    'Laboratory': 'darkblue',
    'Therapy': 'pink',
    'Specialized Care': 'darkred',
    'Alternative/Mental Health': 'lightblue',
    'Other': 'gray'
}

print("Adding markers...")

# Add markers with proper escaping
added = 0
for idx, row in df.iterrows():
    if idx % 200 == 0:
        print(f"  Processing {idx}/{len(df)}...")
    
    # Clean the name - remove any problematic characters
    name = str(row['name']).replace("'", "").replace('"', '').replace('`', '')
    category = str(row['category'])
    
    # Simple popup text (avoid complex HTML)
    popup_text = f"{name}<br>Type: {category}"
    
    # Add circle marker
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=5,
        popup=popup_text,
        tooltip=name,
        color=color_map.get(category, 'gray'),
        fill=True,
        fillColor=color_map.get(category, 'gray'),
        fillOpacity=0.7,
        weight=2
    ).add_to(m)
    
    added += 1

print(f"Added {added} markers")

# Count facilities by category
category_counts = df['category'].value_counts().to_dict()

# Create a SIMPLE legend using basic HTML (no FontAwesome)
legend_items = []
for cat, color in color_map.items():
    count = category_counts.get(cat, 0)
    if count > 0:
        legend_items.append(f'<p style="margin:3px 0"><span style="color:{color};font-size:20px">●</span> {cat} ({count})</p>')

legend_html = f'''
<div style="position:fixed;bottom:50px;left:50px;width:200px;background-color:white;
            border:2px solid grey;z-index:9999;padding:10px;border-radius:5px">
<h4 style="margin:5px 0;text-align:center">Facility Types</h4>
{"".join(legend_items)}
<hr style="margin:8px 0">
<p style="text-align:center;font-weight:bold">Total: {added}</p>
</div>
'''

m.get_root().html.add_child(folium.Element(legend_html))

# Simple title
title_html = '''
<div style="position:fixed;top:10px;left:50%;transform:translateX(-50%);
            background-color:white;border:2px solid grey;z-index:9999;
            padding:10px;border-radius:5px;text-align:center">
<h3 style="margin:0">Chennai Healthcare Facilities</h3>
</div>
'''

m.get_root().html.add_child(folium.Element(title_html))

# Save
output_path = 'outputs/healthcare_map_final.html'
m.save(output_path)

print(f"\n{'='*60}")
print("SUCCESS!")
print(f"{'='*60}")
print(f"Map saved to: {output_path}")
print(f"Total markers: {added}")
print("\nOpen the file to see your map with:")
print("  - Color-coded markers by facility type")
print("  - Interactive legend")
print("  - Click markers to see facility names")