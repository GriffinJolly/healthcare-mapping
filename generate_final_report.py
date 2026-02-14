import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

print("="*60)
print("GENERATING FINAL PROJECT REPORT")
print("="*60)

# Load data
facilities_df = pd.read_csv('data/processed/healthcare_facilities_clean.csv')
summary_stats = pd.read_csv('outputs/accessibility_summary.csv').iloc[0]
grid_df = pd.read_csv('data/processed/accessibility_grid.csv')

# Identify specific underserved areas
underserved_df = grid_df[grid_df['distance_to_any_km'] > 5].sort_values('distance_to_any_km', ascending=False)

print("\nGenerating comprehensive report...")

# Create report text
report = f"""
{'='*70}
CHENNAI HEALTHCARE ACCESSIBILITY ANALYSIS
Final Report
{'='*70}

Generated: {datetime.now().strftime('%B %d, %Y')}
Analyst: Griffin Jolly

{'='*70}
EXECUTIVE SUMMARY
{'='*70}

This analysis examines healthcare accessibility across Chennai by mapping
{int(summary_stats['total_facilities'])} healthcare facilities and calculating distance metrics
for 10,000 analysis points across the city.

KEY FINDINGS:
- {summary_stats['underserved_area_pct']:.1f}% of Chennai's area is more than 5km from healthcare
- Median distance to nearest facility: {summary_stats['median_distance_any_km']:.2f} km
- Only {summary_stats['coverage_2km_pct']:.1f}% of areas are within 2km of a facility
- Hospital access lags behind overall facility access

{'='*70}
METHODOLOGY
{'='*70}

Data Source: OpenStreetMap (OSM)
Study Area: Chennai, Tamil Nadu, India
Analysis Date: {datetime.now().strftime('%B %Y')}

Facilities Mapped:
  • Hospitals: {int(summary_stats['hospitals'])}
  • Clinics: {int(summary_stats['clinics'])}
  • Pharmacies: {int(summary_stats['pharmacies'])}
  • Total: {int(summary_stats['total_facilities'])}

Analysis Method:
  • Created 100x100 grid (10,000 analysis points) across Chennai
  • Calculated distance from each point to nearest facility using geospatial algorithms
  • Used KDTree data structure for efficient nearest-neighbor searches
  • Measured both straight-line (Euclidean) distances

{'='*70}
DETAILED FINDINGS
{'='*70}

1. DISTANCE METRICS

Average distance to nearest healthcare facility: {summary_stats['avg_distance_any_km']:.2f} km
Median distance: {summary_stats['median_distance_any_km']:.2f} km
Maximum distance (worst case): {summary_stats['max_distance_any_km']:.2f} km

The median of {summary_stats['median_distance_any_km']:.2f} km suggests most residents have reasonable 
access, but the maximum of {summary_stats['max_distance_any_km']:.2f} km indicates some areas face 
significant barriers to healthcare access.

2. COVERAGE ANALYSIS

Area within 1km of healthcare: {summary_stats['coverage_1km_pct']:.1f}%
Area within 2km of healthcare: {summary_stats['coverage_2km_pct']:.1f}%
Area within 5km of healthcare: {summary_stats['coverage_5km_pct']:.1f}%
Area within 10km of healthcare: {summary_stats['coverage_10km_pct']:.1f}%

INTERPRETATION:
- {100 - summary_stats['coverage_2km_pct']:.1f}% of Chennai requires >2km travel for healthcare
- At 2km (approximately 25-minute walk), this represents a significant barrier
- Nearly universal coverage (99.9%) within 10km, but distance still matters

3. HOSPITAL-SPECIFIC ACCESS

Average distance to nearest hospital: {summary_stats['avg_distance_hospital_km']:.2f} km
Median distance to hospital: {summary_stats['median_distance_hospital_km']:.2f} km
Area within 5km of hospital: {summary_stats['hospital_coverage_5km_pct']:.1f}%

Hospital access is slightly worse than overall facility access, suggesting
that hospitals are more centrally concentrated while clinics and pharmacies
provide better peripheral coverage.

4. UNDERSERVED AREAS

{summary_stats['underserved_area_pct']:.1f}% of Chennai ({len(underserved_df)} grid points) is more than 5km 
from the nearest healthcare facility.

Most underserved locations (furthest from healthcare):
"""

# Add top 10 most underserved points
report += "\nTop 10 Most Underserved Locations:\n"
for i, row in underserved_df.head(10).iterrows():
    report += f"  {i+1}. Lat: {row['latitude']:.4f}, Lon: {row['longitude']:.4f}\n"
    report += f"     Distance to nearest facility: {row['distance_to_any_km']:.2f} km\n"
    report += f"     Nearest facility: {row['nearest_facility']}\n\n"

report += f"""
{'='*70}
RECOMMENDATIONS
{'='*70}

Based on this analysis, we recommend:

1. IMMEDIATE ACTIONS:
   • Investigate the {summary_stats['underserved_area_pct']:.1f}% underserved areas for new facility placement
   • Focus on regions >5km from current facilities
   • Prioritize areas with high population density among underserved zones

2. STRATEGIC PLANNING:
   • Aim to increase 2km coverage from {summary_stats['coverage_2km_pct']:.1f}% to >75%
   • Target locations that would serve multiple underserved grid points
   • Consider mobile health clinics for extremely remote areas

3. DATA QUALITY IMPROVEMENTS:
   • Validate OSM data with government health department records
   • Add population density data to weight accessibility metrics
   • Include public transportation routes for more realistic travel times

4. FUTURE ANALYSIS:
   • Compare accessibility with actual health outcomes
   • Analyze temporal patterns (facility operating hours)
   • Assess capacity and quality, not just location

{'='*70}
LIMITATIONS
{'='*70}

- Data completeness depends on OpenStreetMap contributor activity
- Analysis uses straight-line distance, not actual travel routes
- Does not account for facility capacity, quality, or specialization
- Grid-based analysis may not perfectly represent population distribution
- Some facilities may be missing or misclassified in OSM

{'='*70}
CONCLUSION
{'='*70}

Chennai demonstrates reasonable healthcare coverage overall, with a median
distance of {summary_stats['median_distance_any_km']:.2f} km to the nearest facility. However, {summary_stats['underserved_area_pct']:.1f}%
of the city's area remains underserved (>5km from healthcare), representing
a significant equity concern.

The concentration of hospitals in central areas while clinics provide better
peripheral coverage suggests opportunities for targeted intervention. Strategic
placement of just a few new facilities in identified underserved zones could
dramatically improve overall accessibility metrics.

This analysis provides a data-driven foundation for healthcare planning
decisions and can be replicated for other cities to identify and address
healthcare access gaps.

{'='*70}
TECHNICAL DETAILS
{'='*70}

Tools & Libraries Used:
  • Python 3.x
  • pandas (data manipulation)
  • geopandas (geospatial analysis)
  • scipy (KDTree for efficient distance calculations)
  • folium (interactive mapping)
  • matplotlib/seaborn (visualization)

Data Processing Pipeline:
  1. Data collection from OpenStreetMap via Overpass API
  2. Data cleaning and categorization
  3. Grid generation for spatial analysis
  4. Distance calculation using KDTree algorithm
  5. Statistical analysis and visualization
  6. Interactive map generation

Repository: https://github.com/GriffinJolly/healthcare-mapping


{'='*70}
END OF REPORT
{'='*70}
"""

# Save report
with open('outputs/FINAL_REPORT.txt', 'w', encoding='utf-8') as f:
    f.write(report)

print("✓ Report saved to: outputs/FINAL_REPORT.txt")

# Also create a summary for easy sharing
summary = f"""
CHENNAI HEALTHCARE ACCESSIBILITY - QUICK SUMMARY

Total Facilities Analyzed: {int(summary_stats['total_facilities'])}
Median Distance to Healthcare: {summary_stats['median_distance_any_km']:.2f} km
Underserved Areas (>5km): {summary_stats['underserved_area_pct']:.1f}%
Coverage within 2km: {summary_stats['coverage_2km_pct']:.1f}%

Key Insight: While most of Chennai has reasonable healthcare access,
{summary_stats['underserved_area_pct']:.1f}% of the city is significantly underserved, with some
areas up to {summary_stats['max_distance_any_km']:.1f} km from the nearest facility.
"""

with open('outputs/SUMMARY.txt', 'w', encoding='utf-8') as f:
    f.write(summary)

print("✓ Summary saved to: outputs/SUMMARY.txt")

print("\n" + "="*60)
print("REPORT GENERATION COMPLETE!")
print("="*60)
print("\nGenerated files:")
print("  • outputs/FINAL_REPORT.txt - Comprehensive analysis report")
print("  • outputs/SUMMARY.txt - Quick summary for sharing")