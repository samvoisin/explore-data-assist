"""
Tests for the DataVisualizationAssistant component.
"""

import pytest
import os
from assistant import DataVisualizationAssistant


class TestDataVisualizationAssistant:
    """Test cases for DataVisualizationAssistant functionality."""
    
    def test_initialization(self, mock_openai_key):
        """Test assistant initialization."""
        assistant = DataVisualizationAssistant()
        assert assistant.current_df is None
        assert assistant.analyzer is None
        assert assistant.llm is not None
    
    def test_set_dataframe(self, sample_dataframe, mock_openai_key):
        """Test setting a DataFrame directly."""
        assistant = DataVisualizationAssistant()
        assistant.set_dataframe(sample_dataframe)
        
        assert assistant.current_df is not None
        assert assistant.analyzer is not None
        assert assistant.current_df.shape == (4, 4)
    
    def test_load_dataset_csv(self, sample_csv_path, mock_openai_key):
        """Test loading a CSV dataset."""
        if sample_csv_path is None:
            pytest.skip("Sample CSV file not available")
            
        assistant = DataVisualizationAssistant()
        assistant.load_dataset(sample_csv_path)
        
        assert assistant.current_df is not None
        assert assistant.analyzer is not None
        assert assistant.current_df.shape[0] > 0  # Should have some rows
    
    def test_get_dataset_info_no_data(self, mock_openai_key):
        """Test getting dataset info when no data is loaded."""
        assistant = DataVisualizationAssistant()
        info = assistant.get_dataset_info()
        
        assert "No dataset loaded" in info
    
    def test_get_dataset_info_with_data(self, sample_dataframe, mock_openai_key):
        """Test getting dataset info when data is loaded."""
        assistant = DataVisualizationAssistant()
        assistant.set_dataframe(sample_dataframe)
        
        info = assistant.get_dataset_info()
        
        assert "Dataset Information:" in info
        assert "Shape: 4 rows, 4 columns" in info
        assert "Columns: name, age, salary, department" in info
    
    def test_create_visualization_no_data(self, mock_openai_key):
        """Test creating visualization when no dataset is loaded."""
        assistant = DataVisualizationAssistant()
        
        with pytest.raises(Exception, match="No dataset loaded"):
            assistant.create_visualization("show me a chart")
    
    def test_load_dataset_invalid_file(self, mock_openai_key):
        """Test loading an invalid dataset file."""
        assistant = DataVisualizationAssistant()
        
        with pytest.raises(Exception, match="Failed to load dataset"):
            assistant.load_dataset("nonexistent_file.csv")
    
    def test_load_dataset_different_formats(self, sales_dataframe, mock_openai_key, tmp_path):
        """Test loading datasets in different formats."""
        assistant = DataVisualizationAssistant()
        
        # Create a temporary CSV file
        csv_file = tmp_path / "test.csv"
        sales_dataframe.to_csv(csv_file, index=False)
        
        assistant.load_dataset(str(csv_file))
        
        assert assistant.current_df is not None
        assert assistant.current_df.shape == (3, 3)
        assert list(assistant.current_df.columns) == ['date', 'sales', 'product']
    
    def test_voice_integration_no_dataset(self, mock_openai_key):
        """Test that voice input requires a dataset to be loaded first."""
        assistant = DataVisualizationAssistant()
        
        # Mock the transcription to avoid actual API call
        assistant.llm.transcribe_audio_file = lambda x: "create a bar chart"
        
        # Since no dataset is loaded, create_visualization should raise an exception
        # We can't easily test the interactive session, but we can test the underlying method
        with pytest.raises(Exception, match="No dataset loaded"):
            assistant.create_visualization("create a bar chart")