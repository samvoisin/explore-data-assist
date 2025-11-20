# edagent
A digital assistant for exploratory data analysis

## Overview

**edagent** is a Python library that uses OpenAI LLMs to help analyze pandas datasets by producing data visualizations using the `matplotlib` library. You can describe the visualization you want to see with natural language and the LLM will produce the right code and execute it in Python.

## Features

- **Natural Language Interface**: Describe visualizations in plain English
- **Automatic Dataset Analysis**: Extracts metadata about columns, data types, and statistics
- **Smart Code Generation**: Uses OpenAI GPT models to generate appropriate matplotlib code
- **Multiple File Format Support**: CSV, Excel, JSON, Parquet files
- **Interactive Text-Based Interface**: Command-line interface for easy interaction
- **Safe Code Execution**: Sandboxed environment for running generated visualization code

## Installation

### Prerequisites

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Using uv (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/samvoisin/explore-data-assist.git
cd explore-data-assist
```

2. Initialize the virtual environment and install dependencies:
```bash
make init
```

This will:
- Create a virtual environment using uv
- Install all dependencies including dev tools
- Set up pre-commit hooks

3. Set up your OpenAI API key:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### Using pip

Alternatively, you can install using pip:

```bash
pip install -e .
```

## Usage

### Running the Assistant

Start the interactive assistant:
```bash
python main.py
```

Or, if installed as a package:
```bash
python -m edagent
```

### Commands

- `load <file_path>` - Load a dataset from file
- `info` - Show information about the loaded dataset
- `viz <description>` - Create a visualization based on natural language description
- `quit` - Exit the assistant

### Example Session

```
Welcome to the Data Visualization Assistant!

Assistant> load sample_data/sales_data.csv
Dataset loaded successfully! Shape: (21, 5)

Assistant> info
Dataset Information:
- Shape: 21 rows, 5 columns
- Columns: date, product, sales, region, revenue
...

Assistant> viz show me a bar chart of total sales by product
Generating visualization code...
Generated code:
import matplotlib.pyplot as plt
df_grouped = df.groupby('product')['sales'].sum()
plt.figure(figsize=(10, 6))
plt.bar(df_grouped.index, df_grouped.values)
plt.title('Total Sales by Product')
plt.xlabel('Product')
plt.ylabel('Total Sales')
plt.show()

Executing visualization...
Visualization created successfully!
```

## Sample Visualization Requests

Try these natural language requests with the sample data:

- "Show me a line chart of sales over time"
- "Create a scatter plot of sales vs revenue"
- "Make a pie chart showing sales distribution by region"
- "Display a histogram of revenue values"
- "Show me a bar chart comparing average sales by product"

## Testing

The project uses pytest for testing with coverage reporting.

### Run all tests:
```bash
make test
```

Or manually:
```bash
pytest tests/ -v
```

### Run tests with coverage:
```bash
pytest tests/ --cov=edagent --cov-report term-missing
```

The test suite includes:
- Unit tests for all core components
- Integration tests for the full workflow
- Mock tests that don't require OpenAI API credits

## Development

### Code Quality

This project uses several tools to maintain code quality:

- **ruff**: Linting and formatting (configured in `pyproject.toml`)
- **pytest**: Testing framework with coverage reporting
- **pre-commit**: Git hooks for automatic code quality checks

### Available Make Commands

```bash
make init          # Initialize development environment
make sync-venv     # Sync virtual environment with dependencies
make lint          # Run linting checks
make format        # Auto-format code
make test          # Run test suite with coverage
make clean         # Remove development artifacts
```

### Linting and Formatting

Check code style:
```bash
make lint
```

Auto-format code:
```bash
make format
```

## Project Structure

```
explore-data-assist/
├── edagent/                # Main package
│   ├── __init__.py
│   ├── assistant.py        # Main assistant coordination
│   ├── data_analyzer.py    # Dataset metadata extraction
│   └── llm_interface.py    # OpenAI LLM integration
├── tests/                  # Test suite
│   ├── __init__.py
│   ├── conftest.py         # Pytest fixtures and configuration
│   ├── test_assistant.py   # Tests for DataVisualizationAssistant
│   ├── test_data_analyzer.py    # Tests for DataAnalyzer
│   └── test_llm_interface.py    # Tests for LLMInterface
├── sample_data/            # Example datasets
│   ├── sales_data.csv
│   └── malvern_modeling_dataset.csv
├── saved-plots/            # Directory for saved visualizations
├── main.py                 # CLI entry point
├── demo.py                 # Basic demo script
├── full_demo.py            # Complete workflow demo
├── pyproject.toml          # Project configuration and dependencies
├── Makefile                # Development commands
├── .env.example            # Environment variable template
└── README.md               # This file
```

## Dependencies

### Core Dependencies
- **pandas** (>=1.5.0) - DataFrame operations and data loading
- **matplotlib** (>=3.5.0) - Visualization generation
- **openai** (>=1.0.0) - LLM integration
- **python-dotenv** (>=0.19.0) - Environment variable management
- **sounddevice** (>=0.4.6) - Audio recording for voice input
- **scipy** (>=1.9.0) - Scientific computing utilities

### Development Dependencies
- **pytest** (>=8.4.0) - Testing framework
- **pytest-cov** (>=6.1.1) - Coverage reporting
- **ruff** (>=0.11.12) - Linting and formatting
- **pre-commit** (>=4.2.0) - Git hooks for code quality

## Future Enhancements

- **Whisper Integration**: Voice input using OpenAI's Whisper model
- **Web Interface**: Browser-based UI for better user experience

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Run tests and linting:
   ```bash
   make test
   make lint
   ```
5. Commit your changes (pre-commit hooks will run automatically)
6. Push to your branch
7. Submit a pull request

### Code Standards

- Follow PEP 8 style guidelines (enforced by ruff)
- Add type hints to function signatures
- Write docstrings for all public methods and classes
- Maintain test coverage above 80%
- Ensure all tests pass before submitting PR

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.
