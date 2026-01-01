# Multi-Step Calculator Agent

A LangGraph-based agent that handles complex mathematical calculations for climate data analysis.

## Overview

This calculator agent can:
- Perform basic arithmetic operations
- Calculate percentage changes
- Compute compound annual growth rates (CAGR)
- Calculate weighted averages
- Handle multi-step calculations

## Files

- `calculator_agent.py` - Main calculator agent implementation using LangGraph
- `test_calculator.py` - Test suite with various calculation scenarios
- `demo_calculator.py` - Interactive demo script

## Tools Available

1. **basic_math** - Evaluate arithmetic expressions (+, -, *, /, **, parentheses)
2. **percentage_change** - Calculate % change between two values
3. **compound_growth_rate** - Calculate CAGR given initial, final, and periods
4. **weighted_average** - Calculate weighted average of multiple values
5. **calculate_final_value** - Project future values based on growth rates

## Running the Agent

### Run Tests
```bash
python test_calculator.py
```

### Interactive Demo
```bash
python demo_calculator.py
```

## Example Usage

```python
from calculator_agent import calculate

# Simple calculation
result = calculate("What is the CAGR if temperature increased from 14.2°C to 15.1°C over 10 years?")
print(f"Result: {result['final_result']}%")  # Result: 0.62%

# Complex calculation
result = calculate("Calculate the percentage change in emissions from 35.2 to 28.7 gigatons")
print(f"Steps: {result['steps']}")
print(f"Explanation: {result['explanation']}")
```

## Integration with NAT

This agent will be registered as a NAT tool in the main workflow, allowing the climate analysis system to delegate complex mathematical calculations to this specialized agent.
