"""
Pytest configuration and shared fixtures for the Data Visualization Assistant tests.
"""

import os
import sys
import pandas as pd
import pytest

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

@pytest.fixture
def sample_dataframe():
    """Create a sample DataFrame for testing."""
    return pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie', 'Diana'],
        'age': [25, 30, 35, 28],
        'salary': [50000, 60000, 70000, 55000],
        'department': ['HR', 'IT', 'Finance', 'HR']
    })

@pytest.fixture
def sales_dataframe():
    """Create a sales DataFrame for testing."""
    return pd.DataFrame({
        'date': ['2023-01-01', '2023-01-02', '2023-01-03'],
        'sales': [100, 150, 200],
        'product': ['A', 'B', 'C']
    })

@pytest.fixture
def sample_csv_path():
    """Return path to sample CSV file if it exists."""
    path = 'sample_data/sales_data.csv'
    return path if os.path.exists(path) else None

@pytest.fixture
def mock_openai_key():
    """Temporarily set a mock OpenAI API key for testing."""
    original_key = os.environ.get('OPENAI_API_KEY')
    os.environ['OPENAI_API_KEY'] = 'test-key'
    yield 'test-key'
    # Cleanup
    if original_key is not None:
        os.environ['OPENAI_API_KEY'] = original_key
    elif 'OPENAI_API_KEY' in os.environ:
        del os.environ['OPENAI_API_KEY']