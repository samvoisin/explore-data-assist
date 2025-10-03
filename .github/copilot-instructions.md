# GitHub Copilot Instructions for explore-data-assist

This repository contains a data visualization assistant that uses OpenAI LLMs to help analyze pandas datasets and generate matplotlib visualizations from natural language requests.

## Project Overview

The explore-data-assist project is a Python CLI application that:
- Loads datasets from multiple formats (CSV, Excel, JSON, Parquet)
- Extracts comprehensive metadata about pandas DataFrames
- Uses OpenAI LLMs to generate matplotlib visualization code from natural language requests
- Executes generated code safely in a sandboxed environment
- Provides an interactive command-line interface for data exploration

## Architecture

The project follows a modular architecture with three main components:

### Core Modules (`src/`)
- **`assistant.py`** - Main coordinator class (`DataVisualizationAssistant`)
- **`data_analyzer.py`** - DataFrame metadata extraction (`DataAnalyzer`)
- **`llm_interface.py`** - OpenAI LLM integration (`LLMInterface`)

### Key Classes and Their Responsibilities
- `DataVisualizationAssistant`: Main orchestrator, handles user interaction and coordinates other components
- `DataAnalyzer`: Extracts and formats dataset metadata for LLM context
- `LLMInterface`: Manages OpenAI API calls and safe code execution

## Dependencies and Libraries

### Core Dependencies
- **pandas** (>=1.5.0) - DataFrame operations and data loading
- **matplotlib** (>=3.5.0) - Visualization generation
- **openai** (>=1.0.0) - LLM integration for code generation
- **python-dotenv** (>=0.19.0) - Environment variable management

### Import Patterns
```python
# Relative imports with fallback for both package and script usage
try:
    from .data_analyzer import DataAnalyzer
    from .llm_interface import LLMInterface
except ImportError:
    from data_analyzer import DataAnalyzer
    from llm_interface import LLMInterface
```

## Coding Standards and Conventions

### Code Style
- Use type hints for function parameters and return types
- Include comprehensive docstrings for classes and public methods
- Follow PEP 8 naming conventions (snake_case for functions/variables)
- Use descriptive variable names that reflect the data visualization domain

### Error Handling
- Wrap file operations and API calls in try/except blocks
- Provide informative error messages that guide users
- Gracefully handle missing API keys and invalid datasets

### Data Processing Patterns
```python
# Standard dataset loading pattern
if file_path.endswith('.csv'):
    df = pd.read_csv(file_path)
elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
    df = pd.read_excel(file_path)
# ... handle other formats

# Safe code execution pattern
exec_globals = {
    'df': df,
    'plt': plt,
    'pd': pd,
    '__builtins__': {}  # Restrict for safety
}
```

## Testing Approach

### Test Structure
- Main test file: `test_assistant.py`
- Tests verify functionality without requiring OpenAI API keys
- Includes both unit tests for individual components and integration tests
- Demo scripts (`demo.py`, `full_demo.py`) simulate complete workflows

### Testing Patterns
```python
# Create sample DataFrames for testing
df = pd.DataFrame({
    'column1': ['value1', 'value2'],
    'column2': [1, 2]
})

# Test data analysis capabilities
analyzer = DataAnalyzer(df)
metadata = analyzer.get_metadata()
```

## LLM Integration Guidelines

### Prompt Engineering
- Format dataset context clearly for the LLM with structured information
- Include data types, column names, sample data, and basic statistics
- Use specific system prompts that emphasize matplotlib best practices

### Code Generation Expectations
- Generated code should always use the variable `df` for the DataFrame
- Include proper plot titles, labels, and formatting
- Always end with `plt.show()` for display
- Handle data type conversions when necessary

### Safety Considerations
- Restrict available built-ins in code execution environment
- Only allow safe operations (no file I/O, network access)
- Provide controlled access to pandas, matplotlib, and basic Python functions

## CLI Interface Patterns

### Command Structure
```
Assistant> load <file_path>    # Load dataset
Assistant> info               # Show dataset info
Assistant> viz <request>      # Generate visualization
Assistant> quit              # Exit
```

### User Interaction
- Provide clear command help and error messages
- Handle Ctrl+C gracefully in interactive sessions
- Show progress feedback during API calls and code execution

## File Organization

```
explore-data-assist/
├── src/                     # Core modules
│   ├── assistant.py         # Main coordinator
│   ├── data_analyzer.py     # Metadata extraction
│   └── llm_interface.py     # LLM integration
├── sample_data/             # Example datasets
├── main.py                  # CLI entry point
├── demo.py                  # Basic demo without API
├── full_demo.py             # Complete workflow demo
├── test_assistant.py        # Test suite
└── requirements.txt         # Dependencies
```

## Environment Configuration

- Uses `.env` file for API key management
- Provides `.env.example` template
- Graceful degradation when API keys are missing
- Environment variables loaded via `python-dotenv`

## Common Patterns to Follow

### Dataset Loading
Always support multiple file formats with clear error handling and use pandas' native methods for each format.

### Metadata Extraction  
Extract comprehensive information including shape, columns, data types, null counts, sample data, and basic statistics for numerical columns.

### Visualization Code Generation
Generate clean, well-formatted matplotlib code with proper labels, titles, and display commands. Focus on readability and educational value.

### Safe Execution
Use restricted execution environments and validate generated code before execution to prevent security issues.

When contributing to this project, maintain the clean separation between data analysis, LLM interaction, and user interface components.