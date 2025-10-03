# explore-data-assist
A digital assistant for exploratory data analysis

## Overview

This application uses OpenAI LLMs to help analyze pandas datasets by producing data visualizations using the `matplotlib` library. You can describe the visualization you want to see with natural language and the LLM will produce the right code and execute it in Python.

## Features

- **Natural Language Interface**: Describe visualizations in plain English
- **Automatic Dataset Analysis**: Extracts metadata about columns, data types, and statistics
- **Smart Code Generation**: Uses OpenAI GPT models to generate appropriate matplotlib code
- **Multiple File Format Support**: CSV, Excel, JSON, Parquet files
- **Interactive Text-Based Interface**: Command-line interface for easy interaction
- **Safe Code Execution**: Sandboxed environment for running generated visualization code

## Installation

1. Clone the repository:
```bash
git clone https://github.com/samvoisin/explore-data-assist.git
cd explore-data-assist
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Usage

### Running the Assistant

Start the interactive assistant:
```bash
python main.py
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

Run the test suite to verify installation:
```bash
pytest tests/
```

Or run tests with verbose output:
```bash
pytest tests/ -v
```

## Project Structure

```
explore-data-assist/
├── src/
│   ├── __init__.py
│   ├── data_analyzer.py    # Dataset metadata extraction
│   ├── llm_interface.py    # OpenAI LLM integration
│   └── assistant.py        # Main assistant coordination
├── tests/                  # Test suite using pytest
│   ├── __init__.py
│   ├── conftest.py         # Pytest configuration and fixtures
│   ├── test_data_analyzer.py    # Tests for DataAnalyzer
│   ├── test_assistant.py        # Tests for DataVisualizationAssistant
│   └── test_llm_interface.py    # Tests for LLMInterface
├── sample_data/
│   └── sales_data.csv      # Sample dataset for testing
├── main.py                 # Main entry point
├── requirements.txt        # Python dependencies (includes pytest)
├── .env.example           # Environment variable template
└── README.md              # This file
```

## Future Enhancements

- **Whisper Integration**: Voice input using OpenAI's Whisper model
- **Web Interface**: Browser-based UI for better user experience

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.
