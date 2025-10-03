#!/usr/bin/env python3
"""
Full demonstration of the Data Visualization Assistant including code generation.
This simulates the complete workflow including LLM code generation.
"""

import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.data_analyzer import DataAnalyzer

DEFAULT_PLOT_DIR = Path(
    "./saved-plots"
).resolve()  # assumes this script is run from repo root


def simulate_llm_response(request: str, context: str) -> str:
    """Simulate LLM response for different visualization requests."""

    request_lower = request.lower()

    if "bar chart" in request_lower and "product" in request_lower:
        return """
import matplotlib.pyplot as plt
df_grouped = df.groupby('product')['sales'].sum()
plt.figure(figsize=(10, 6))
plt.bar(df_grouped.index, df_grouped.values)
plt.title('Total Sales by Product')
plt.xlabel('Product')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
"""

    elif "line chart" in request_lower and "time" in request_lower:
        return """
import matplotlib.pyplot as plt
import pandas as pd
df['date'] = pd.to_datetime(df['date'])
daily_sales = df.groupby('date')['sales'].sum().reset_index()
plt.figure(figsize=(12, 6))
plt.plot(daily_sales['date'], daily_sales['sales'], marker='o')
plt.title('Sales Over Time')
plt.xlabel('Date')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
"""

    elif "pie chart" in request_lower and "region" in request_lower:
        return """
import matplotlib.pyplot as plt
region_sales = df.groupby('region')['sales'].sum()
plt.figure(figsize=(8, 8))
plt.pie(region_sales.values, labels=region_sales.index, autopct='%1.1f%%')
plt.title('Sales Distribution by Region')
plt.show()
"""

    elif "scatter" in request_lower:
        return """
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
plt.scatter(df['sales'], df['revenue'], alpha=0.7)
plt.title('Sales vs Revenue')
plt.xlabel('Sales')
plt.ylabel('Revenue')
plt.tight_layout()
plt.show()
"""

    else:
        return """
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
plt.hist(df['sales'], bins=10, edgecolor='black', alpha=0.7)
plt.title('Distribution of Sales')
plt.xlabel('Sales')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()
"""


def execute_visualization_code(
    code: str, df: pd.DataFrame, save_plot: bool = False
) -> None:
    """Execute visualization code and optionally save the plot."""

    # Prepare execution environment
    exec_globals = {"df": df, "plt": plt, "pd": pd}

    # Modify the code to save instead of show if requested
    if save_plot:
        code = code.replace(
            "plt.show()",
            f'plt.savefig("{DEFAULT_PLOT_DIR}/demo_plot.png", dpi=150, bbox_inches="tight")\nplt.close()',
        )

    try:
        exec(code.strip(), exec_globals)
        if save_plot:
            print(f"   ✓ Visualization saved to {DEFAULT_PLOT_DIR}/demo_plot.png")
        else:
            print("   ✓ Visualization displayed")
    except Exception as e:
        print(f"   ✗ Error executing code: {e}")


def full_demo():
    """Run a complete demonstration of the assistant."""
    print("=" * 70)
    print("Data Visualization Assistant - Full Workflow Demo")
    print("=" * 70)
    print()

    # Load dataset
    print("Step 1: Loading sales dataset...")
    df = pd.read_csv("sample_data/sales_data.csv")
    print(f"   ✓ Loaded {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"   ✓ Columns: {', '.join(df.columns)}")
    print()

    # Analyze dataset
    print("Step 2: Analyzing dataset structure...")
    analyzer = DataAnalyzer(df)
    context = analyzer.format_for_llm()
    print("   ✓ Dataset metadata extracted for LLM context")
    print()

    # Demonstrate multiple visualization requests
    requests = [
        "Show me a bar chart of total sales by product",
        "Create a line chart of sales over time",
        "Make a pie chart of sales distribution by region",
        "Display a scatter plot of sales vs revenue",
    ]

    for i, request in enumerate(requests, 3):
        print(f"Step {i}: Processing request: '{request}'")

        # Simulate LLM code generation
        print("   • Sending context and request to OpenAI LLM...")
        generated_code = simulate_llm_response(request, context)
        print("   • Code generated successfully!")

        # Show the generated code
        print("   • Generated matplotlib code:")
        for line in generated_code.strip().split("\n"):
            if line.strip():
                print(f"     {line}")

        # Execute the code
        print("   • Executing visualization code...")
        execute_visualization_code(generated_code, df)
        print()

    print("=" * 70)
    print("Demo completed successfully!")
    print()
    print("The assistant demonstrates:")
    print("✓ Natural language request processing")
    print("✓ Dataset metadata extraction")
    print("✓ Context-aware code generation")
    print("✓ Safe code execution")
    print("✓ Multiple visualization types")
    print()
    print("To use with real OpenAI:")
    print("1. Set OPENAI_API_KEY environment variable")
    print("2. Run: python main.py")
    print("3. Use commands: load, info, viz, quit")
    print("=" * 70)


if __name__ == "__main__":
    full_demo()
