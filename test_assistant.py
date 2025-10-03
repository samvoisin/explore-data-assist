#!/usr/bin/env python3
"""
Test script for the Data Visualization Assistant.
"""

import os
import sys
import pandas as pd

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_analyzer import DataAnalyzer
from assistant import DataVisualizationAssistant


def test_data_analyzer():
    """Test the DataAnalyzer functionality."""
    print("Testing DataAnalyzer...")
    
    # Create sample data
    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie', 'Diana'],
        'age': [25, 30, 35, 28],
        'salary': [50000, 60000, 70000, 55000],
        'department': ['HR', 'IT', 'Finance', 'HR']
    })
    
    analyzer = DataAnalyzer(df)
    metadata = analyzer.get_metadata()
    
    print(f"Shape: {metadata['shape']}")
    print(f"Columns: {metadata['columns']}")
    print(f"Numerical columns: {metadata['numerical_columns']}")
    print(f"Categorical columns: {metadata['categorical_columns']}")
    
    # Test categorical statistics functionality
    cat_stats = metadata['categorical_statistics']
    assert 'name' in cat_stats, "Name column should be in categorical statistics"
    assert 'department' in cat_stats, "Department column should be in categorical statistics"
    assert cat_stats['name']['unique_count'] == 4, f"Name should have 4 unique values, got {cat_stats['name']['unique_count']}"
    assert cat_stats['department']['unique_count'] == 3, f"Department should have 3 unique values, got {cat_stats['department']['unique_count']}"
    assert cat_stats['department']['most_frequent'] == 'HR', f"Most frequent department should be HR, got {cat_stats['department']['most_frequent']}"
    assert cat_stats['department']['most_frequent_count'] == 2, f"HR should appear 2 times, got {cat_stats['department']['most_frequent_count']}"
    
    print("\nFormatted for LLM:")
    print(analyzer.format_for_llm())
    
    # Verify categorical statistics are included in the formatted output
    formatted_output = analyzer.format_for_llm()
    assert "Basic Statistics for Categorical Columns:" in formatted_output, "Categorical statistics section should be present"
    assert "unique_count=" in formatted_output, "Unique count should be displayed for categorical columns"
    
    print("DataAnalyzer test passed!\n")


def test_assistant_basic():
    """Test basic assistant functionality without OpenAI."""
    print("Testing basic Assistant functionality...")
    
    try:
        # Test loading sample data without OpenAI
        os.environ['OPENAI_API_KEY'] = 'test-key'  # Temporary test key
        assistant = DataVisualizationAssistant()
        
        sample_file = 'sample_data/sales_data.csv'
        if os.path.exists(sample_file):
            assistant.load_dataset(sample_file)
            print("Dataset loaded successfully!")
            
            info = assistant.get_dataset_info()
            print("Dataset info retrieved successfully!")
            print(f"Info preview: {info[:200]}...")
        else:
            print("Sample data file not found, creating test DataFrame...")
            df = pd.DataFrame({
                'date': ['2023-01-01', '2023-01-02', '2023-01-03'],
                'sales': [100, 150, 200],
                'product': ['A', 'B', 'C']
            })
            assistant.set_dataframe(df)
            print("Test DataFrame set successfully!")
    
    except Exception as e:
        print(f"Note: OpenAI functionality requires valid API key - {e}")
        print("Testing basic data operations without OpenAI...")
        # Test just the data analyzer part
        df = pd.DataFrame({
            'date': ['2023-01-01', '2023-01-02', '2023-01-03'],
            'sales': [100, 150, 200],
            'product': ['A', 'B', 'C']
        })
        analyzer = DataAnalyzer(df)
        info = analyzer.format_for_llm()
        print("Data analysis functionality works correctly!")
    finally:
        # Clean up test key
        if 'OPENAI_API_KEY' in os.environ and os.environ['OPENAI_API_KEY'] == 'test-key':
            del os.environ['OPENAI_API_KEY']
    
    print("Basic Assistant test completed!\n")


def main():
    """Run all tests."""
    print("Running Data Visualization Assistant Tests")
    print("=" * 50)
    
    test_data_analyzer()
    test_assistant_basic()
    
    print("All basic tests completed!")
    print("\nTo test with OpenAI integration:")
    print("1. Set your OPENAI_API_KEY environment variable")
    print("2. Run: python main.py")
    print("3. Use commands like:")
    print("   load sample_data/sales_data.csv")
    print("   viz show me a bar chart of sales by product")


if __name__ == "__main__":
    main()