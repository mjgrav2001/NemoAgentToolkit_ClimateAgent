#!/usr/bin/env python3
"""
Interactive demo of the Multi-Step Calculator Agent
"""

from calculator_agent import calculate


def demo():
    """Run an interactive demo of the calculator agent"""
    
    print("=== Multi-Step Calculator Agent Demo ===")
    print("This agent can handle complex mathematical calculations for climate data analysis.")
    print("\nExample questions you can ask:")
    print("- What is the compound annual growth rate if temperature increased from 14.2°C to 15.1°C over 10 years?")
    print("- Calculate the percentage change in emissions from 35.2 to 28.7 gigatons")
    print("- If warming rates are 0.12, 0.18, and 0.15 degrees with populations 150M, 200M, 100M, what's the weighted average?")
    print("- Calculate (42.5 - 38.2) * 2.1 + 15.3")
    print("\nType 'quit' to exit\n")
    
    while True:
        question = input("Enter your calculation question: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("\nGoodbye!")
            break
        
        if not question:
            print("Please enter a question.\n")
            continue
        
        print("\nProcessing...")
        try:
            result = calculate(question)
            
            print("\n" + "="*60)
            if result['steps']:
                print("Calculation Steps:")
                for i, step in enumerate(result['steps'], 1):
                    print(f"  {i}. {step}")
                print()
            
            if result['final_result'] is not None:
                print(f"Final Result: {result['final_result']}")
                print()
            
            print("Explanation:")
            print(result['explanation'])
            print("="*60 + "\n")
            
        except Exception as e:
            print(f"\nError: {str(e)}\n")


if __name__ == "__main__":
    demo()
