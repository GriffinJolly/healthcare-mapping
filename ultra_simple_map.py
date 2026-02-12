import pandas as pd
import folium

df = pd.read_csv('data/processed/healthcare_facilities_clean.csv')

m = folium.Map(
    location=[df['latitude'].mean(), df['longitude'].mean()],
    zoom_start=11
)

# Just add circles - nothing fancy
for idx, row in df.iterrows():
    folium.Circle(
        location=[row['latitude'], row['longitude']],
        radius=100,
        color='red',
        fill=True,
        popup=str(row['name'])
    ).add_to(m)

m.save('outputs/ultra_simple.html')
print("Saved!")