"""
Module for analyzing pandas datasets and extracting metadata for LLM prompts.
"""

import pandas as pd
from typing import Dict, Any, List


class DataAnalyzer:
    """Analyzes pandas DataFrames to extract metadata for LLM context."""
    
    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe
    
    def get_metadata(self) -> Dict[str, Any]:
        """Extract comprehensive metadata about the dataset."""
        metadata = {
            'shape': self.df.shape,
            'columns': list(self.df.columns),
            'dtypes': self.df.dtypes.to_dict(),
            'null_counts': self.df.isnull().sum().to_dict(),
            'sample_data': self._get_sample_data(),
            'numerical_columns': self._get_numerical_columns(),
            'categorical_columns': self._get_categorical_columns(),
            'index_info': self._get_index_info(),
            'statistics': self._get_basic_statistics(),
            'categorical_statistics': self._get_categorical_statistics()
        }
        return metadata
    
    def _get_sample_data(self) -> Dict[str, List]:
        """Get first few rows as sample data."""
        sample_size = min(5, len(self.df))
        sample = self.df.head(sample_size)
        return {col: sample[col].tolist() for col in sample.columns}
    
    def _get_numerical_columns(self) -> List[str]:
        """Get list of numerical columns."""
        return self.df.select_dtypes(include=['number']).columns.tolist()
    
    def _get_categorical_columns(self) -> List[str]:
        """Get list of categorical/object columns."""
        return self.df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    def _get_index_info(self) -> Dict[str, Any]:
        """Get information about the DataFrame index."""
        return {
            'type': str(type(self.df.index)),
            'name': self.df.index.name,
            'length': len(self.df.index),
            'sample_values': self.df.index[:5].tolist() if len(self.df.index) > 0 else []
        }
    
    def _get_basic_statistics(self) -> Dict[str, Any]:
        """Get basic statistical information for numerical columns."""
        numerical_stats = {}
        for col in self._get_numerical_columns():
            numerical_stats[col] = {
                'mean': float(self.df[col].mean()) if not self.df[col].empty else None,
                'std': float(self.df[col].std()) if not self.df[col].empty else None,
                'min': float(self.df[col].min()) if not self.df[col].empty else None,
                'max': float(self.df[col].max()) if not self.df[col].empty else None,
                'unique_count': int(self.df[col].nunique())
            }
        return numerical_stats
    
    def _get_categorical_statistics(self) -> Dict[str, Any]:
        """Get basic statistical information for categorical columns."""
        categorical_stats = {}
        for col in self._get_categorical_columns():
            unique_values = self.df[col].value_counts()
            categorical_stats[col] = {
                'unique_count': int(self.df[col].nunique()),
                'most_frequent': str(unique_values.index[0]) if len(unique_values) > 0 else None,
                'most_frequent_count': int(unique_values.iloc[0]) if len(unique_values) > 0 else None,
                'unique_values': unique_values.head(10).to_dict()  # Top 10 most frequent values
            }
        return categorical_stats
    
    def format_for_llm(self) -> str:
        """Format the metadata as a string for LLM context."""
        metadata = self.get_metadata()
        
        context = f"""Dataset Information:
- Shape: {metadata['shape'][0]} rows, {metadata['shape'][1]} columns
- Columns: {', '.join(metadata['columns'])}

Data Types:
{chr(10).join([f"- {col}: {dtype}" for col, dtype in metadata['dtypes'].items()])}

Numerical Columns: {', '.join(metadata['numerical_columns'])}
Categorical Columns: {', '.join(metadata['categorical_columns'])}

Sample Data (first 5 rows):
{chr(10).join([f"- {col}: {values}" for col, values in metadata['sample_data'].items()])}

Basic Statistics for Numerical Columns:
{chr(10).join([f"- {col}: mean={stats.get('mean', 'N/A')}, min={stats.get('min', 'N/A')}, max={stats.get('max', 'N/A')}" for col, stats in metadata['statistics'].items()])}

Basic Statistics for Categorical Columns:
{chr(10).join([f"- {col}: unique_count={stats.get('unique_count', 'N/A')}, most_frequent='{stats.get('most_frequent', 'N/A')}' (appears {stats.get('most_frequent_count', 'N/A')} times)" for col, stats in metadata['categorical_statistics'].items()])}
"""
        return context