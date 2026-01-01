"""
Prepare a smaller, course-friendly subset of the climate data.
This creates CSV files that are easier to work with in the course.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json

def prepare_sample_data():
    """Create a smaller, representative sample of the climate data."""
    
    # Paths
    base_path = Path(__file__).parent.parent.parent / "resources" / "climate_data" / "ghcnm.v4.0.1.20251008"
    data_path = base_path / "ghcnm.tavg.v4.0.1.20251008.qcf.dat"
    inv_path = base_path / "ghcnm.tavg.v4.0.1.20251008.qcf.inv"
    
    # Load country codes
    country_codes_path = Path(__file__).parent.parent.parent / "resources" / "climate_data" / "ghcnm-countries.txt"
    
    # Read country codes
    countries = {}
    with open(country_codes_path, 'r') as f:
        for line in f:
            if line.strip():
                code = line[:2]
                name = line[3:].strip()
                countries[code] = name
    
    # Select diverse stations from major countries
    target_countries = ['US', 'GB', 'FR', 'DE', 'JP', 'AU', 'BR', 'IN', 'CN', 'CA', 'MX', 'AR']
    stations_per_country = 3
    
    # Load station metadata
    print("Loading station metadata...")
    selected_stations = []
    
    with open(inv_path, 'r') as f:
        for line in f:
            station_id = line[0:11].strip()
            country_code = station_id[:2]
            
            if country_code in target_countries:
                lat = float(line[12:20].strip())
                lon = float(line[21:30].strip())
                elev = float(line[31:37].strip())
                name = line[38:68].strip()
                
                selected_stations.append({
                    'station_id': station_id,
                    'country_code': country_code,
                    'country_name': countries.get(country_code, 'Unknown'),
                    'latitude': lat,
                    'longitude': lon,
                    'elevation': elev,
                    'name': name
                })
    
    # Sample stations per country
    station_df = pd.DataFrame(selected_stations)
    sampled_stations = []
    for country in target_countries:
        country_stations = station_df[station_df['country_code'] == country]
        if len(country_stations) > 0:
            sampled = country_stations.sample(n=min(stations_per_country, len(country_stations)), 
                                            random_state=42)
            sampled_stations.append(sampled)
    
    final_stations = pd.concat(sampled_stations, ignore_index=True)
    station_ids = set(final_stations['station_id'])
    
    print(f"Selected {len(final_stations)} stations from {len(target_countries)} countries")
    
    # Load temperature data for selected stations
    print("Loading temperature data for selected stations...")
    records = []
    
    with open(data_path, 'r') as f:
        for line_num, line in enumerate(f):
            if line_num % 100000 == 0:
                print(f"  Processing line {line_num:,}...")
            
            station_id = line[0:11].strip()
            if station_id not in station_ids:
                continue
                
            year = int(line[11:15])
            element = line[15:19].strip()
            
            if element != 'TAVG':
                continue
            
            # Only keep data from 1950 onwards for simplicity
            if year < 1950:
                continue
            
            # Parse monthly values
            for month in range(12):
                start = 19 + month * 8
                value_str = line[start:start+5].strip()
                
                try:
                    value = int(value_str)
                    if value != -9999:  # Not missing
                        temperature = value / 100.0
                        records.append({
                            'station_id': station_id,
                            'year': year,
                            'month': month + 1,
                            'temperature': temperature
                        })
                except ValueError:
                    continue
    
    # Create temperature DataFrame
    temp_df = pd.DataFrame(records)
    
    # Merge with station info
    final_df = temp_df.merge(final_stations[['station_id', 'country_code', 'country_name', 
                                            'latitude', 'longitude', 'name']], 
                            on='station_id')
    
    # Calculate annual averages
    annual_df = final_df.groupby(['station_id', 'year', 'country_code', 'country_name', 
                                  'latitude', 'longitude', 'name'])['temperature'].mean().reset_index()
    annual_df = annual_df.rename(columns={'temperature': 'annual_temperature'})
    
    # Save the data
    output_dir = Path(__file__).parent.parent.parent / "resources" / "climate_data"
    
    # Save full monthly data
    monthly_file = output_dir / "temperature_monthly.csv"
    final_df.to_csv(monthly_file, index=False)
    print(f"\nSaved monthly data: {monthly_file}")
    print(f"  Records: {len(final_df):,}")
    print(f"  Years: {final_df['year'].min()} - {final_df['year'].max()}")
    
    # Save annual averages
    annual_file = output_dir / "temperature_annual.csv"
    annual_df.to_csv(annual_file, index=False)
    print(f"\nSaved annual data: {annual_file}")
    print(f"  Records: {len(annual_df):,}")
    
    # Save station metadata
    station_file = output_dir / "stations.csv"
    final_stations.to_csv(station_file, index=False)
    print(f"\nSaved station metadata: {station_file}")
    
    # Create a summary
    summary = {
        "data_description": "GHCN-Monthly temperature data subset for educational purposes",
        "source": "NOAA National Centers for Environmental Information",
        "license": "Public Domain (U.S. Government Work)",
        "stations": len(final_stations),
        "countries": len(final_stations['country_code'].unique()),
        "years": f"{final_df['year'].min()}-{final_df['year'].max()}",
        "monthly_records": len(final_df),
        "annual_records": len(annual_df),
        "files": {
            "temperature_monthly.csv": "Monthly temperature data with station information",
            "temperature_annual.csv": "Annual average temperatures by station",
            "stations.csv": "Station metadata (location, elevation, etc.)"
        }
    }
    
    summary_file = output_dir / "data_summary.json"
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"\nSaved data summary: {summary_file}")
    
    print("\n✅ Course data preparation complete!")
    
    # Show sample of the data
    print("\nSample of annual temperature data:")
    print(annual_df.head(10))

if __name__ == "__main__":
    prepare_sample_data()
