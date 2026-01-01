# A simple standalone function
import json
from typing import Optional
import pandas as pd
import numpy as np

def calculate_statistics(df: pd.DataFrame, country: Optional[str] = None) -> str:
    """
    Calculate basic statistics from temperature data.
    
    Args:
        df: DataFrame with temperature data
        country: Optional country name to filter by
        
    Returns:
        JSON string with statistics
    """
    # Filter by country if specified
    if country and 'country_name' in df.columns:
        df = df[df['country_name'] == country]
        if df.empty:
            return json.dumps({"error": f"No data found for country: {country}"})
    
    # Determine temperature column
    temp_col = 'annual_temperature' if 'annual_temperature' in df.columns else 'temperature'
    
    stats = {
        "mean_temperature": round(float(df[temp_col].mean()), 2),
        "min_temperature": round(float(df[temp_col].min()), 2),
        "max_temperature": round(float(df[temp_col].max()), 2),
        "std_deviation": round(float(df[temp_col].std()), 2),
        "num_records": len(df)
    }
    
    # Calculate trend if we have yearly data
    if 'year' in df.columns and 'annual_temperature' in df.columns:
        yearly_global = df.groupby('year')['annual_temperature'].mean()
        if len(yearly_global) > 1:
            years = yearly_global.index.values
            temps = yearly_global.values
            z = np.polyfit(years, temps, 1)
            stats['trend_per_decade'] = round(float(z[0] * 10), 3)
            stats['years_analyzed'] = f"{years.min()}-{years.max()}"
    
    if country:
        stats['country'] = country
        
    return json.dumps(stats, indent=2)
