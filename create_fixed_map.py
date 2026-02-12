import pandas as pd
import folium
import html

print("="*60)
print("FIXED MAP CREATOR")
print("="*60)

# Load cleaned data
df = pd.read_csv('data/processed/healthcare_facilities_clean.csv')

print(f"\nLoaded {len(df)} facilities")

# Remove any rows with missing coordinates
df_valid = df.dropna(subset=['latitude', 'longitude'])
print(f"Facilities with valid coordinates: {len(df_valid)}")

# Calculate center point
center_lat = df_valid['latitude'].mean()
center_lon = df_valid['longitude'].mean()

print(f"Map center: {center_lat:.4f}, {center_lon:.4f}")

# Create base map with proper sizing
m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=11,
    tiles='OpenStreetMap',
    width='100%',
    height='100%'
)

# Define colors for different facility categories
colors = {
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

print("\nAdding markers to map...")

# Add markers with error handling
added = 0
errors = 0

for idx, row in df_valid.iterrows():
    if idx % 200 == 0:
        print(f"  Processing {idx}/{len(df_valid)}...")
    
    try:
        # Clean and escape data
        name = html.escape(str(row['name']))
        category = html.escape(str(row['category']))
        address = html.escape(str(row['address'])) if pd.notna(row['address']) and str(row['address']) != '' else 'N/A'
        phone = html.escape(str(row['phone'])) if pd.notna(row['phone']) and str(row['phone']) != '' else 'N/A'
        
        # Create popup HTML
        popup_html = f"""
        <div style="width: 200px; font-family: Arial;">
            <h4 style="margin-bottom: 5px;">{name}</h4>
            <p style="margin: 3px 0;"><b>Type:</b> {category}</p>
            <p style="margin: 3px 0;"><b>Address:</b> {address}</p>
            <p style="margin: 3px 0;"><b>Phone:</b> {phone}</p>
        </div>
        """
        
        # Add marker
        folium.CircleMarker(
            location=[float(row['latitude']), float(row['longitude'])],
            radius=5,
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=name,
            color=colors.get(row['category'], 'gray'),
            fill=True,
            fillColor=colors.get(row['category'], 'gray'),
            fillOpacity=0.7,
            weight=2
        ).add_to(m)
        
        added += 1
        
    except Exception as e:
        errors += 1
        if errors <= 5:  # Only show first 5 errors
            print(f"  Error with row {idx}: {e}")

print(f"\n✓ Added {added} markers to map")
if errors > 0:
    print(f"⚠ {errors} errors encountered")

# Count by category
category_counts = df_valid['category'].value_counts()

# Add legend
legend_html = f'''
<div style="position: fixed; 
            bottom: 50px; left: 50px; width: 220px; 
            background-color: white; z-index:9999; 
            border:2px solid grey; border-radius: 8px; 
            padding: 15px; box-shadow: 0 0 10px rgba(0,0,0,0.2);">
    <h4 style="margin-top: 0; text-align: center;">Facility Types</h4>
'''

for category, count in category_counts.items():
    color = colors.get(category, 'gray')
    legend_html += f'    <p style="margin: 5px 0;"><span style="color:{color}; font-size: 20px;">●</span> {category} ({count})</p>\n'

legend_html += '''
    <hr style="margin: 10px 0;">
    <p style="text-align: center; font-weight: bold;">Total: ''' + str(len(df_valid)) + '''</p>
</div>
'''

m.get_root().html.add_child(folium.Element(legend_html))

# Add title
title_html = '''
<div style="position: fixed; 
            top: 10px; left: 50%; transform: translateX(-50%);
            width: 400px;
            background-color: white; z-index:9999; 
            border:2px solid grey; border-radius: 8px; 
            padding: 10px; text-align: center;
            box-shadow: 0 0 10px rgba(0,0,0,0.2);">
    <h3 style="margin: 0;">Chennai Healthcare Facilities</h3>
    <p style="margin: 5px 0; font-size: 12px; color: gray;">Interactive Map - Click markers for details</p>
</div>
'''
m.get_root().html.add_child(folium.Element(title_html))

# Save map
output_path = 'outputs/healthcare_facilities_map_working.html'
m.save(output_path)

print(f"\n{'='*60}")
print("MAP CREATED SUCCESSFULLY!")
print(f"{'='*60}")
print(f"Saved to: {output_path}")
print(f"Markers added: {added}")
print(f"Errors: {errors}")
print(f"\nOpen the file in your browser!")
print("The map should now display properly with correct sizing.")
