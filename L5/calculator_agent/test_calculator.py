#!/usr/bin/env python3
"""
Test script for the Multi-Step Calculator Agent
"""

import json
from calculator_agent import calculate


def test_calculator():
    """Run various test calculations"""
    
    print("=== Multi-Step Calculator Agent Test ===\n")
    
    test_cases = [
        {
            "name": "Compound Annual Growth Rate",
            "question": "What is the compound annual growth rate if global temperature increased from 14.2°C to 15.1°C over 10 years?",
            "expected_type": "CAGR calculation"
        },
        {
            "name": "Percentage Change",
            "question": "Calculate the percentage change in CO2 emissions from 35.2 gigatons to 28.7 gigatons",
            "expected_type": "Percentage decrease"
        },
        {
            "name": "Weighted Average",
            "question": "If three regions have warming rates of 0.12, 0.18, and 0.15 degrees per decade with populations of 150 million, 200 million, and 100 million respectively, what's the population-weighted average warming rate?",
            "expected_type": "Weighted average"
        },
        {
            "name": "Complex Calculation",
            "question": "If emissions were 30 gigatons in 2010 and 35 gigatons in 2020, what's the annual growth rate? Then, if we reduce emissions by 3% per year for 5 years from the 2020 level, what will emissions be in 2025?",
            "expected_type": "Multi-step calculation"
        },
        {
            "name": "Basic Arithmetic",
            "question": "Calculate (42.5 - 38.2) * 2.1 + 15.3",
            "expected_type": "Basic math"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case['name']}")
        print(f"Question: {test_case['question']}")
        print("-" * 80)
        
        try:
            result = calculate(test_case['question'])
            
            print(f"Calculation Steps:")
            for j, step in enumerate(result['steps'], 1):
                print(f"  {j}. {step}")
            
            print(f"\nFinal Result: {result['final_result']}")
            print(f"\nExplanation: {result['explanation'][:300]}...")
            
        except Exception as e:
            print(f"ERROR: {str(e)}")
        
        print("\n" + "=" * 80 + "\n")
    
    # Test error handling
    print("Test: Error Handling")
    print("Question: Calculate the percentage change from 0 to 10")
    print("-" * 80)
    try:
        result = calculate("Calculate the percentage change from 0 to 10")
        print(f"Result: {result}")
    except Exception as e:
        print(f"Expected error caught: {str(e)}")
    
    print("\n=== Test Complete ===")


if __name__ == "__main__":
    test_calculator()
