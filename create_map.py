import pandas as pd
import folium
from folium import plugins
import os
import html

print("="*60)
print("CREATING INTERACTIVE MAP")
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

# Create base map
m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=11,
    tiles='OpenStreetMap'
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

added = 0
for idx, row in df_valid.iterrows():
    if idx % 200 == 0:
        print(f"  Processing {idx}/{len(df_valid)}...")
    
    try:
        # Escape special characters that could break HTML/JavaScript
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
        print(f"  Error with row {idx}: {e}")

print(f"\n✓ Added {added} markers to map")

# Count by category
hospital_count = len(df_valid[df_valid['category']=='Hospital'])
clinic_count = len(df_valid[df_valid['category']=='Clinic'])
pharmacy_count = len(df_valid[df_valid['category']=='Pharmacy'])
health_center_count = len(df_valid[df_valid['category']=='Health Center'])
dental_count = len(df_valid[df_valid['category']=='Dental'])
lab_count = len(df_valid[df_valid['category']=='Laboratory'])

# Add legend - FIXED VERSION
legend_html = f'''
<div style="position: fixed; 
            bottom: 50px; left: 50px; width: 220px; 
            background-color: white; z-index:9999; 
            border:2px solid grey; border-radius: 8px; 
            padding: 15px; box-shadow: 0 0 10px rgba(0,0,0,0.2);">
    <h4 style="margin-top: 0; text-align: center;">Facility Types</h4>
    <p style="margin: 5px 0;"><span style="color:red; font-size: 20px;">●</span> Hospital ({hospital_count})</p>
    <p style="margin: 5px 0;"><span style="color:blue; font-size: 20px;">●</span> Clinic ({clinic_count})</p>
    <p style="margin: 5px 0;"><span style="color:green; font-size: 20px;">●</span> Pharmacy ({pharmacy_count})</p>
    <p style="margin: 5px 0;"><span style="color:orange; font-size: 20px;">●</span> Health Center ({health_center_count})</p>
    <p style="margin: 5px 0;"><span style="color:purple; font-size: 20px;">●</span> Dental ({dental_count})</p>
    <p style="margin: 5px 0;"><span style="color:darkblue; font-size: 20px;">●</span> Laboratory ({lab_count})</p>
    <hr style="margin: 10px 0;">
    <p style="text-align: center; font-weight: bold;">Total: {len(df_valid)}</p>
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

# Add title - FIXED VERSION
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
output_path = 'outputs/healthcare_facilities_map.html'
m.save(output_path)

print(f"\n{'='*60}")
print("MAP CREATED SUCCESSFULLY!")
print(f"{'='*60}")
print(f"Saved to: {output_path}")
print(f"Markers added: {added}")
print(f"\nOpen the file in your browser!")
print(f"You should now see all {added} markers as colored circles.")