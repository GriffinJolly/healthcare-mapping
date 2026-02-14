import pandas as pd
import numpy as np
from geopy.distance import geodesic
from scipy.spatial import cKDTree
import matplotlib.pyplot as plt
import seaborn as sns

print("="*60)
print("HEALTHCARE ACCESSIBILITY ANALYSIS")
print("="*60)

# Load facility data
facilities_df = pd.read_csv('data/processed/healthcare_facilities_clean.csv')
print(f"\nLoaded {len(facilities_df)} healthcare facilities")

# Separate by type for specialized analysis
hospitals_df = facilities_df[facilities_df['category'] == 'Hospital']
clinics_df = facilities_df[facilities_df['category'] == 'Clinic']
pharmacies_df = facilities_df[facilities_df['category'] == 'Pharmacy']

print(f"  - Hospitals: {len(hospitals_df)}")
print(f"  - Clinics: {len(clinics_df)}")
print(f"  - Pharmacies: {len(pharmacies_df)}")

# Get bounds of the study area
lat_min, lat_max = facilities_df['latitude'].min(), facilities_df['latitude'].max()
lon_min, lon_max = facilities_df['longitude'].min(), facilities_df['longitude'].max()

# Add padding (roughly 2km in degrees)
padding = 0.02
lat_min -= padding
lat_max += padding
lon_min -= padding
lon_max += padding

print(f"\nStudy area bounds:")
print(f"  Latitude: {lat_min:.4f} to {lat_max:.4f}")
print(f"  Longitude: {lon_min:.4f} to {lon_max:.4f}")

# Create analysis grid
# Grid represents different locations across Chennai
grid_size = 100  # 100x100 = 10,000 sample points
lat_grid = np.linspace(lat_min, lat_max, grid_size)
lon_grid = np.linspace(lon_min, lon_max, grid_size)

print(f"\nCreating {grid_size}x{grid_size} analysis grid ({grid_size*grid_size} points)...")

# Generate all grid points
grid_points = []
for lat in lat_grid:
    for lon in lon_grid:
        grid_points.append({
            'latitude': lat,
            'longitude': lon
        })

grid_df = pd.DataFrame(grid_points)
print(f"✓ Grid created with {len(grid_df)} analysis points")

# Function to find nearest facility using KDTree (much faster than iterating)
def calculate_nearest_distances(grid_points, facilities, facility_type_name):
    """Calculate distance to nearest facility for each grid point"""
    print(f"\nCalculating distances to nearest {facility_type_name}...")
    
    # Convert to radians for KDTree
    facility_coords = np.radians(facilities[['latitude', 'longitude']].values)
    grid_coords = np.radians(grid_points[['latitude', 'longitude']].values)
    
    # Build KDTree
    tree = cKDTree(facility_coords)
    
    # Find nearest neighbor for each grid point
    distances_rad, indices = tree.query(grid_coords)
    
    # Convert radians to kilometers (approximate)
    # Earth radius ~ 6371 km
    distances_km = distances_rad * 6371
    
    # Get nearest facility names
    nearest_facilities = facilities.iloc[indices]['name'].values
    
    return distances_km, nearest_facilities

# Calculate distances to different facility types
print("\n" + "="*60)
print("CALCULATING DISTANCES...")
print("="*60)

# All facilities
all_distances, all_nearest = calculate_nearest_distances(
    grid_df, facilities_df, "any healthcare facility"
)
grid_df['distance_to_any_km'] = all_distances
grid_df['nearest_facility'] = all_nearest

# Hospitals only
hospital_distances, hospital_nearest = calculate_nearest_distances(
    grid_df, hospitals_df, "hospital"
)
grid_df['distance_to_hospital_km'] = hospital_distances
grid_df['nearest_hospital'] = hospital_nearest

# Clinics only
clinic_distances, clinic_nearest = calculate_nearest_distances(
    grid_df, clinics_df, "clinic"
)
grid_df['distance_to_clinic_km'] = clinic_distances
grid_df['nearest_clinic'] = clinic_nearest

print("✓ Distance calculations complete!")

# Calculate summary statistics
print("\n" + "="*60)
print("ACCESSIBILITY METRICS")
print("="*60)

def print_distance_stats(distances, facility_type):
    print(f"\n{facility_type}:")
    print(f"  Average distance: {np.mean(distances):.2f} km")
    print(f"  Median distance: {np.median(distances):.2f} km")
    print(f"  Maximum distance: {np.max(distances):.2f} km")
    print(f"  Minimum distance: {np.min(distances):.2f} km")
    print(f"  Std deviation: {np.std(distances):.2f} km")

print_distance_stats(all_distances, "Any Healthcare Facility")
print_distance_stats(hospital_distances, "Hospitals")
print_distance_stats(clinic_distances, "Clinics")

# Coverage analysis
print("\n" + "="*60)
print("COVERAGE ANALYSIS")
print("="*60)

def calculate_coverage(distances, thresholds=[1, 2, 5, 10]):
    """Calculate percentage of area within distance thresholds"""
    total = len(distances)
    coverage = {}
    
    for threshold in thresholds:
        within = np.sum(distances <= threshold)
        percentage = (within / total) * 100
        coverage[threshold] = percentage
    
    return coverage

# Coverage for any facility
any_coverage = calculate_coverage(all_distances)
print("\nArea within X km of ANY healthcare facility:")
for dist, pct in any_coverage.items():
    print(f"  Within {dist:2d} km: {pct:5.1f}%")

# Coverage for hospitals
hospital_coverage = calculate_coverage(hospital_distances)
print("\nArea within X km of a HOSPITAL:")
for dist, pct in hospital_coverage.items():
    print(f"  Within {dist:2d} km: {pct:5.1f}%")

# Identify underserved areas
underserved_threshold = 5  # km
underserved_points = grid_df[grid_df['distance_to_any_km'] > underserved_threshold]
underserved_percentage = (len(underserved_points) / len(grid_df)) * 100

print("\n" + "="*60)
print("UNDERSERVED AREAS")
print("="*60)
print(f"Areas more than {underserved_threshold}km from nearest facility: {underserved_percentage:.1f}%")
print(f"Number of underserved grid points: {len(underserved_points)}")

# Save results
grid_df.to_csv('data/processed/accessibility_grid.csv', index=False)
print(f"\n✓ Grid data saved to: data/processed/accessibility_grid.csv")

# Create summary statistics
summary_stats = {
    'total_facilities': len(facilities_df),
    'hospitals': len(hospitals_df),
    'clinics': len(clinics_df),
    'pharmacies': len(pharmacies_df),
    'avg_distance_any_km': np.mean(all_distances),
    'median_distance_any_km': np.median(all_distances),
    'max_distance_any_km': np.max(all_distances),
    'avg_distance_hospital_km': np.mean(hospital_distances),
    'median_distance_hospital_km': np.median(hospital_distances),
    'coverage_1km_pct': any_coverage[1],
    'coverage_2km_pct': any_coverage[2],
    'coverage_5km_pct': any_coverage[5],
    'coverage_10km_pct': any_coverage[10],
    'underserved_area_pct': underserved_percentage,
    'hospital_coverage_5km_pct': hospital_coverage[5],
}

summary_df = pd.DataFrame([summary_stats])
summary_df.to_csv('outputs/accessibility_summary.csv', index=False)
print(f"✓ Summary stats saved to: outputs/accessibility_summary.csv")

# Create visualizations
print("\n" + "="*60)
print("CREATING VISUALIZATIONS...")
print("="*60)

# Set style
sns.set_style("whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# 1. Distance distribution histogram
axes[0, 0].hist(all_distances, bins=50, color='steelblue', edgecolor='black', alpha=0.7)
axes[0, 0].axvline(np.median(all_distances), color='red', linestyle='--', 
                   linewidth=2, label=f'Median: {np.median(all_distances):.2f} km')
axes[0, 0].set_xlabel('Distance to Nearest Facility (km)', fontsize=12)
axes[0, 0].set_ylabel('Frequency', fontsize=12)
axes[0, 0].set_title('Distribution of Distance to Nearest Healthcare Facility', 
                      fontsize=14, fontweight='bold')
axes[0, 0].legend()
axes[0, 0].grid(axis='y', alpha=0.3)

# 2. Coverage bar chart
coverage_data = {
    '1 km': any_coverage[1],
    '2 km': any_coverage[2],
    '5 km': any_coverage[5],
    '10 km': any_coverage[10]
}
bars = axes[0, 1].bar(coverage_data.keys(), coverage_data.values(), 
                      color=['#27ae60', '#f39c12', '#e74c3c', '#c0392b'],
                      edgecolor='black')
axes[0, 1].set_ylabel('Coverage (%)', fontsize=12)
axes[0, 1].set_title('Area Coverage by Distance Threshold', fontsize=14, fontweight='bold')
axes[0, 1].set_ylim([0, 100])
axes[0, 1].grid(axis='y', alpha=0.3)

# Add percentage labels on bars
for bar in bars:
    height = bar.get_height()
    axes[0, 1].text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')

# 3. Comparison: Any facility vs Hospital
comparison_data = {
    'Any Facility': [any_coverage[2], any_coverage[5]],
    'Hospital Only': [hospital_coverage[2], hospital_coverage[5]]
}
x = np.arange(2)
width = 0.35
axes[1, 0].bar(x - width/2, comparison_data['Any Facility'], width, 
               label='Any Facility', color='steelblue')
axes[1, 0].bar(x + width/2, comparison_data['Hospital Only'], width, 
               label='Hospital Only', color='crimson')
axes[1, 0].set_ylabel('Coverage (%)', fontsize=12)
axes[1, 0].set_title('Coverage Comparison: Any Facility vs Hospitals', 
                     fontsize=14, fontweight='bold')
axes[1, 0].set_xticks(x)
axes[1, 0].set_xticklabels(['Within 2km', 'Within 5km'])
axes[1, 0].legend()
axes[1, 0].grid(axis='y', alpha=0.3)

# 4. Key metrics summary
axes[1, 1].axis('off')
summary_text = f"""
KEY FINDINGS

Total Facilities: {len(facilities_df)}
  • Hospitals: {len(hospitals_df)}
  • Clinics: {len(clinics_df)}
  • Pharmacies: {len(pharmacies_df)}

Distance to Nearest Facility:
  • Average: {np.mean(all_distances):.2f} km
  • Median: {np.median(all_distances):.2f} km
  • Maximum: {np.max(all_distances):.2f} km

Coverage:
  • Within 2km: {any_coverage[2]:.1f}%
  • Within 5km: {any_coverage[5]:.1f}%
  • Within 10km: {any_coverage[10]:.1f}%

Underserved Areas (>5km): {underserved_percentage:.1f}%

Hospital Access:
  • Avg distance: {np.mean(hospital_distances):.2f} km
  • Within 5km: {hospital_coverage[5]:.1f}%
"""

axes[1, 1].text(0.1, 0.95, summary_text, transform=axes[1, 1].transAxes,
                fontsize=11, verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.suptitle('Chennai Healthcare Accessibility Analysis', 
             fontsize=16, fontweight='bold', y=0.995)
plt.tight_layout()

# Save figure
plt.savefig('outputs/accessibility_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Visualization saved to: outputs/accessibility_analysis.png")

plt.show()

print("\n" + "="*60)
print("ACCESSIBILITY ANALYSIS COMPLETE!")
print("="*60)
print("\nGenerated files:")
print("  1. data/processed/accessibility_grid.csv - Detailed grid data")
print("  2. outputs/accessibility_summary.csv - Summary statistics")
print("  3. outputs/accessibility_analysis.png - Visualizations")
print("\nNext step: Create accessibility heatmap")