#!/usr/bin/env python3
"""
Demo script showing how the Data Visualization Assistant works.
This demonstrates the application flow without requiring an OpenAI API key.
"""

import os
import sys

import pandas as pd

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.data_analyzer import DataAnalyzer


def demo_data_analysis():
    """Demonstrate the data analysis capabilities."""
    print("=" * 60)
    print("Data Visualization Assistant - Demo")
    print("=" * 60)
    print()

    # Load the sample dataset
    print("1. Loading sample sales dataset...")
    df = pd.read_csv("sample_data/sales_data.csv")
    print(f"   ✓ Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    print()

    # Analyze the dataset
    print("2. Analyzing dataset structure...")
    analyzer = DataAnalyzer(df)
    metadata = analyzer.get_metadata()

    print(f"   ✓ Columns: {', '.join(metadata['columns'])}")
    print(f"   ✓ Numerical columns: {', '.join(metadata['numerical_columns'])}")
    print(f"   ✓ Categorical columns: {', '.join(metadata['categorical_columns'])}")
    print()

    # Show dataset info formatted for LLM
    print("3. Dataset context that would be sent to OpenAI LLM:")
    print("-" * 50)
    context = analyzer.format_for_llm()
    print(context)
    print("-" * 50)
    print()

    # Show sample visualization requests
    print("4. Example visualization requests you could make:")
    print("   • 'Show me a bar chart of total sales by product'")
    print("   • 'Create a line chart of sales over time'")
    print("   • 'Make a pie chart of sales distribution by region'")
    print("   • 'Display a scatter plot of sales vs revenue'")
    print("   • 'Show me a histogram of revenue values'")
    print()

    # Show what the generated code might look like
    print("5. Example generated matplotlib code:")
    print("   For request: 'Show me a bar chart of total sales by product'")
    print()
    print("   Generated code would be:")
    print("   ```python")
    print("   import matplotlib.pyplot as plt")
    print("   df_grouped = df.groupby('product')['sales'].sum()")
    print("   plt.figure(figsize=(10, 6))")
    print("   plt.bar(df_grouped.index, df_grouped.values)")
    print("   plt.title('Total Sales by Product')")
    print("   plt.xlabel('Product')")
    print("   plt.ylabel('Total Sales')")
    print("   plt.xticks(rotation=45)")
    print("   plt.tight_layout()")
    print("   plt.show()")
    print("   ```")
    print()

    print("=" * 60)
    print("To use with real OpenAI integration:")
    print("1. Get an OpenAI API key from https://platform.openai.com/")
    print("2. Copy .env.example to .env")
    print("3. Add your API key to the .env file")
    print("4. Run: python main.py")
    print("=" * 60)


if __name__ == "__main__":
    demo_data_analysis()
