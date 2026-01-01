"""This file shows the minimal pattern for registering a Python function as a NAT tool."""

import os
import pandas as pd
from pydantic import BaseModel, Field
# Step 1: Import NAT components for tool registration
from nat.builder.builder import Builder
from nat.builder.function_info import FunctionInfo
from nat.cli.register_workflow import register_function
from nat.data_models.function import FunctionBaseConfig

# Step 2: Import our standalone function
from .simple_function import calculate_statistics

current_dir = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(current_dir, "..", "..", "..", "..", "resources", "climate_data", "temperature_annual.csv")

def load_climate_data(file_path: str = "temperature_annual.csv") -> pd.DataFrame:
    df = pd.read_csv(file_path)
    return df

class CalculateStatsInput(BaseModel):
    country: str = Field(
        default="",
        description="Country name to filter by (e.g., 'United States', 'France'). Leave empty for global statistics."
    )

class CalculateStatisticsConfig(FunctionBaseConfig, name="simple_calculate_statistics"):
    """Configuration for calculating climate statistics."""
    pass

@register_function(config_type=CalculateStatisticsConfig)
async def calculate_statistics_tool(config: CalculateStatisticsConfig, builder: Builder):
    """Register tool for calculating climate statistics."""
    # Load data once at startup
    df = load_climate_data(DATA_PATH)
    
    # 2. Wrapper uses pre-loaded data and ensures string output
    async def _wrapper(country: str = "") -> str:
        # Treat empty string as None for the underlying function
        country_param = None if country == "" else country
        result = calculate_statistics(df, country_param)
        return result  # Already returns JSON string
    
    # 3. Description tells LLM when to use the tool
    yield FunctionInfo.from_fn(
        _wrapper,
        input_schema=CalculateStatsInput,
        description=("Calculate temperature statistics globally or for a specific country. "
                     "Returns JSON with: mean_temperature (°C), min_temperature (°C), max_temperature (°C), "
                     "std_deviation (°C), num_records (count), trend_per_decade (°C/decade), "
                     "years_analyzed (e.g. '1950-2025'), and country (if specified).")
    )
