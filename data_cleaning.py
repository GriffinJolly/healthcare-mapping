import pandas as pd
import matplotlib.pyplot as plt 
import os
df=pd.read_csv("data/raw/osm_healthcare_facilities.csv")
print("total records loaded: ",len(df))
print(f"Columns: {df.columns.tolist()}")
duplicates=df.duplicated(subset=["latitude","longitude"]).sum()
print(f"\nDuplicate locations found: {duplicates}")
df_clean=df.drop_duplicates(subset=["latitude","longitude"])
print(f"\nTotal records after removing duplicates: {len(df_clean)}")
#Data completeness
for col in df_clean.columns:
    non_null=df_clean[col].notna().sum()
    percentage=(non_null/len(df_clean))*100
    print(f"\nColumn: {col}")
    print(f"Non-null values: {non_null}")
    print(f"Percentage non-null: {percentage:.2f}%")
def categorize_facility(row):
    facility_type = str(row['type']).lower()
    
    if 'hospital' in facility_type:
        return 'Hospital'
    elif 'clinic' in facility_type or 'doctor' in facility_type:
        return 'Clinic'
    elif 'pharmacy' in facility_type:
        return 'Pharmacy'
    elif 'dentist' in facility_type:
        return 'Dental'
    elif 'laboratory' in facility_type or 'lab' in facility_type:
        return 'Laboratory'
    elif 'physiotherapist' in facility_type or 'occupational_therapist' in facility_type or 'speech_therapist' in facility_type:
        return 'Therapy'
    elif 'blood_donation' in facility_type or 'dialysis' in facility_type:
        return 'Specialized Care'
    elif 'health' in facility_type or 'centre' in facility_type or 'center' in facility_type:
        return 'Health Center'
    elif 'psychotherapist' in facility_type or 'alternative' in facility_type:
        return 'Alternative/Mental Health'
    else:
        return 'Other'

df_clean['category'] = df_clean.apply(categorize_facility, axis=1)
#categories of facilities
print("\n" + "="*60)
print("FACILITY CATEGORIES:")
print("="*60)
category_counts = df_clean['category'].value_counts()
for category, count in category_counts.items():
    percentage = (count / len(df_clean)) * 100
    print(f"{category:25s}: {count:4d} ({percentage:5.1f}%)")
#checking unnamed facilities
unnamed = df_clean[df_clean['name'] == 'Unnamed']
print(f"\nFacilities without names: {len(unnamed)} ({(len(unnamed)/len(df_clean))*100:.1f}%)")
#saving cleaned data
os.makedirs('data/processed', exist_ok=True)
df_clean.to_csv('data/processed/healthcare_facilities_clean.csv', index=False)
print(f"\nCleaned data saved to: data/processed/healthcare_facilities_clean.csv")
#visualisations
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Chart 1: Facility types bar chart
category_counts.plot(kind='bar', ax=axes[0], color='steelblue', edgecolor='black')
axes[0].set_title('Healthcare Facilities in Chennai by Category', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Facility Category', fontsize=12)
axes[0].set_ylabel('Count', fontsize=12)
axes[0].tick_params(axis='x', rotation=45)
axes[0].grid(axis='y', alpha=0.3)

# Add count labels on bars
for i, v in enumerate(category_counts):
    axes[0].text(i, v + 5, str(v), ha='center', va='bottom', fontweight='bold')

# Chart 2: Named vs Unnamed facilities
named_counts = df_clean['name'].ne('Unnamed').value_counts()
labels = ['Named', 'Unnamed']
colors = ['#2ecc71', '#e74c3c']
axes[1].pie([named_counts.get(True, 0), named_counts.get(False, 0)], 
            labels=labels, 
            autopct='%1.1f%%',
            colors=colors,
            startangle=90,
            textprops={'fontsize': 12, 'fontweight': 'bold'})
axes[1].set_title('Data Completeness: Facility Names', fontsize=14, fontweight='bold')

plt.tight_layout()

os.makedirs('outputs', exist_ok=True)
plt.savefig('outputs/01_data_quality_overview.png', dpi=300, bbox_inches='tight')
print(f"✓ Chart saved to: outputs/01_data_quality_overview.png")

plt.show()

print("\n" + "="*60)
print("DATA CLEANING COMPLETE!")
print("="*60)
print(f"\nSummary:")
print(f"  Original records: {len(df)}")
print(f"  Cleaned records: {len(df_clean)}")
print(f"  Duplicates removed: {len(df) - len(df_clean)}")
print(f"  Categories created: {len(category_counts)}")
print(f"\nReady for mapping and analysis!")
print("\nNext step: Run the mapping script to visualize facilities")
