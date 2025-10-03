"""
Tests for the DataAnalyzer component.
"""

import pytest
from data_analyzer import DataAnalyzer


class TestDataAnalyzer:
    """Test cases for DataAnalyzer functionality."""
    
    def test_get_metadata_basic(self, sample_dataframe):
        """Test basic metadata extraction functionality."""
        analyzer = DataAnalyzer(sample_dataframe)
        metadata = analyzer.get_metadata()
        
        # Test shape
        assert metadata['shape'] == (4, 4)
        
        # Test columns
        expected_columns = ['name', 'age', 'salary', 'department']
        assert metadata['columns'] == expected_columns
        
        # Test numerical columns
        assert metadata['numerical_columns'] == ['age', 'salary']
        
        # Test categorical columns
        assert metadata['categorical_columns'] == ['name', 'department']
    
    def test_categorical_statistics(self, sample_dataframe):
        """Test categorical statistics functionality."""
        analyzer = DataAnalyzer(sample_dataframe)
        metadata = analyzer.get_metadata()
        
        cat_stats = metadata['categorical_statistics']
        
        # Test name column statistics
        assert 'name' in cat_stats
        assert cat_stats['name']['unique_count'] == 4
        
        # Test department column statistics
        assert 'department' in cat_stats
        assert cat_stats['department']['unique_count'] == 3
        assert cat_stats['department']['most_frequent'] == 'HR'
        assert cat_stats['department']['most_frequent_count'] == 2
    
    def test_format_for_llm(self, sample_dataframe):
        """Test LLM formatting functionality."""
        analyzer = DataAnalyzer(sample_dataframe)
        formatted_output = analyzer.format_for_llm()
        
        # Verify key sections are present
        assert "Dataset Information:" in formatted_output
        assert "Shape: 4 rows, 4 columns" in formatted_output
        assert "Data Types:" in formatted_output
        assert "Numerical Columns:" in formatted_output
        assert "Categorical Columns:" in formatted_output
        assert "Sample Data" in formatted_output
        assert "Basic Statistics for Numerical Columns:" in formatted_output
        assert "Basic Statistics for Categorical Columns:" in formatted_output
        
        # Verify categorical statistics are included
        assert "unique_count=" in formatted_output
    
    def test_numerical_statistics(self, sample_dataframe):
        """Test numerical statistics calculation."""
        analyzer = DataAnalyzer(sample_dataframe)
        metadata = analyzer.get_metadata()
        
        num_stats = metadata['statistics']
        
        # Test age statistics
        assert 'age' in num_stats
        assert num_stats['age']['mean'] == 29.5
        assert num_stats['age']['min'] == 25.0
        assert num_stats['age']['max'] == 35.0
        
        # Test salary statistics  
        assert 'salary' in num_stats
        assert num_stats['salary']['mean'] == 58750.0
        assert num_stats['salary']['min'] == 50000.0
        assert num_stats['salary']['max'] == 70000.0