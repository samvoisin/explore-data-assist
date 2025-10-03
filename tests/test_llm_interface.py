"""
Tests for the LLMInterface component.
"""

import pytest
import pandas as pd
from llm_interface import LLMInterface


class TestLLMInterface:
    """Test cases for LLMInterface functionality."""
    
    def test_initialization_with_key(self):
        """Test LLMInterface initialization with API key."""
        interface = LLMInterface(api_key="test-key")
        assert interface.client is not None
    
    def test_initialization_without_key(self, mock_openai_key):
        """Test LLMInterface initialization without API key (uses environment)."""
        interface = LLMInterface()
        assert interface.client is not None
    
    def test_execute_visualization_basic(self, sample_dataframe, mock_openai_key):
        """Test basic visualization code execution."""
        interface = LLMInterface()
        
        # Simple code that should execute successfully (without import)
        code = """
fig, ax = plt.subplots()
ax.bar(['A', 'B', 'C'], [1, 2, 3])
ax.set_title('Test Chart')
plt.close()
"""
        
        # Should not raise an exception
        interface.execute_visualization(code, sample_dataframe)
    
    def test_execute_visualization_with_dataframe(self, sample_dataframe, mock_openai_key):
        """Test visualization code execution that uses the DataFrame."""
        interface = LLMInterface()
        
        # Code that uses the DataFrame (without import)
        code = """
fig, ax = plt.subplots()
ax.bar(df['name'], df['age'])
ax.set_title('Age by Name')
plt.close()
"""
        
        # Should not raise an exception
        interface.execute_visualization(code, sample_dataframe)
    
    def test_execute_visualization_invalid_code(self, sample_dataframe, mock_openai_key):
        """Test visualization code execution with invalid code."""
        interface = LLMInterface()
        
        # Invalid code that should fail
        code = "invalid_function_that_does_not_exist()"
        
        with pytest.raises(Exception, match="Failed to execute visualization code"):
            interface.execute_visualization(code, sample_dataframe)
    
    def test_execute_visualization_restricted_access(self, sample_dataframe, mock_openai_key):
        """Test that restricted operations are blocked in code execution."""
        interface = LLMInterface()
        
        # Code that tries to use restricted operations
        code = "open('/etc/passwd', 'r')"  # Should be blocked
        
        with pytest.raises(Exception, match="Failed to execute visualization code"):
            interface.execute_visualization(code, sample_dataframe)
    
    @pytest.mark.skip(reason="Requires actual OpenAI API key and credits")
    def test_generate_visualization_code_real_api(self, sample_dataframe):
        """Test code generation with real OpenAI API (skipped by default)."""
        # This test would only run if OPENAI_API_KEY is actually set and valid
        import os
        if not os.getenv('OPENAI_API_KEY') or os.getenv('OPENAI_API_KEY') == 'test-key':
            pytest.skip("Real OpenAI API key required")
            
        interface = LLMInterface()
        context = "Test context"
        request = "Create a simple bar chart"
        
        code = interface.generate_visualization_code(context, request)
        assert isinstance(code, str)
        assert len(code) > 0