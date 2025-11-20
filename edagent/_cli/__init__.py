"""
Command-line interface for edagent - Data Visualization Assistant.
"""

import os
import sys
from pathlib import Path
from typing import Optional

import click
from dotenv import load_dotenv

from edagent.assistant import DataVisualizationAssistant


# Load environment variables
load_dotenv()


def get_api_key(api_key: Optional[str] = None) -> str:
    """Get API key from CLI option, env var, or raise error."""
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        click.echo(
            click.style("Error: ", fg="red", bold=True)
            + "OpenAI API key not found. "
            + "Set OPENAI_API_KEY environment variable or use --api-key option."
        )
        click.echo("\nYou can:")
        click.echo("  1. Create a .env file with: OPENAI_API_KEY=your-key-here")
        click.echo("  2. Export it: export OPENAI_API_KEY=your-key-here")
        click.echo("  3. Pass it: edagent --api-key your-key-here <command>")
        sys.exit(1)
    return key


@click.group()
@click.version_option(version="0.0.1", prog_name="edagent")
@click.pass_context
def cli(ctx):
    """
    edagent - AI-powered data visualization assistant.

    Use natural language to create matplotlib visualizations from your datasets.

    \b
    Examples:
        edagent interactive sample_data/sales_data.csv
        edagent info sample_data/sales_data.csv
        edagent viz sample_data/sales_data.csv "show me a bar chart of sales by product"
    """
    ctx.ensure_object(dict)


@cli.command()
@click.argument("file_path", type=click.Path(exists=True), required=False)
@click.option("--api-key", help="OpenAI API key (or set OPENAI_API_KEY env var)")
def interactive(file_path, api_key):
    """
    Start an interactive session with the assistant.

    \b
    If FILE_PATH is provided, the dataset will be loaded automatically.
    Otherwise, use the 'load' command within the interactive session.

    \b
    Interactive Commands:
        load <file_path> - Load a dataset
        info             - Show dataset information
        viz <request>    - Create a visualization
        voice [duration] - Record voice input (default: 5 seconds)
        quit             - Exit the assistant

    \b
    Example:
        edagent interactive sample_data/sales_data.csv
    """
    api_key = get_api_key(api_key)
    assistant = DataVisualizationAssistant(api_key)

    # Auto-load dataset if provided
    if file_path:
        try:
            assistant.load_dataset(file_path)
            click.echo()
        except Exception as e:
            click.echo(click.style(f"Error loading dataset: {e}", fg="red"))
            sys.exit(1)

    # Start interactive session
    assistant.interactive_session()


@cli.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.option("--api-key", help="OpenAI API key (or set OPENAI_API_KEY env var)")
def info(file_path, api_key):
    """
    Display detailed information about a dataset.

    Shows dataset shape, columns, data types, statistics, and sample data.

    \b
    Example:
        edagent info sample_data/sales_data.csv
    """
    api_key = get_api_key(api_key)
    assistant = DataVisualizationAssistant(api_key)

    try:
        assistant.load_dataset(file_path)
        click.echo()
        click.echo(assistant.get_dataset_info())
    except Exception as e:
        click.echo(click.style(f"Error: {e}", fg="red"))
        sys.exit(1)


@cli.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.argument("request", nargs=-1, required=True)
@click.option("--api-key", help="OpenAI API key (or set OPENAI_API_KEY env var)")
@click.option(
    "--save",
    "-s",
    type=click.Path(),
    help="Save plot to file instead of displaying (e.g., plot.png)",
)
@click.option(
    "--dpi",
    default=150,
    type=int,
    help="Resolution for saved plots (default: 150)",
)
@click.option(
    "--show-code/--no-show-code",
    default=True,
    help="Display generated code (default: show)",
)
def viz(file_path, request, api_key, save, dpi, show_code):
    """
    Create a visualization from natural language request.

    The REQUEST can be provided as multiple arguments (will be joined).

    \b
    Examples:
        edagent viz data.csv "show me a bar chart of sales by product"
        edagent viz data.csv show me a scatter plot of age vs salary
        edagent viz data.csv "create a line chart" --save output.png --dpi 300
    """
    api_key = get_api_key(api_key)
    assistant = DataVisualizationAssistant(api_key)

    # Join request arguments
    request_text = " ".join(request)

    try:
        # Load dataset
        assistant.load_dataset(file_path)
        click.echo()

        # Modify request if saving to file
        if save:
            save_path = Path(save).resolve()
            request_text += f"\n\nIMPORTANT: Save the plot to '{save_path}' with dpi={dpi} instead of using plt.show()"

        # Create visualization
        code = assistant.create_visualization(request_text)

        if not show_code:
            # Code already printed by assistant, no need to repeat
            pass

        if save:
            click.echo(click.style(f"\n✓ Plot saved to: {save_path}", fg="green", bold=True))
        else:
            click.echo(click.style("\n✓ Visualization created successfully!", fg="green", bold=True))

    except Exception as e:
        click.echo(click.style(f"\nError: {e}", fg="red"))
        sys.exit(1)


@cli.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.argument("request", nargs=-1, required=True)
@click.option("--api-key", help="OpenAI API key (or set OPENAI_API_KEY env var)")
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    help="Output file for generated code (default: stdout)",
)
def export_code(file_path, request, api_key, output):
    """
    Generate visualization code without executing it.

    Useful for reviewing or manually modifying the generated code.

    \b
    Examples:
        edagent export-code data.csv "bar chart of sales"
        edagent export-code data.csv "scatter plot" --output viz_code.py
    """
    api_key = get_api_key(api_key)
    assistant = DataVisualizationAssistant(api_key)

    # Join request arguments
    request_text = " ".join(request)

    try:
        # Load dataset
        assistant.load_dataset(file_path)

        # Get dataset context
        if assistant.analyzer is None:
            raise Exception("Failed to analyze dataset")
        context = assistant.analyzer.format_for_llm()

        # Generate code without executing
        click.echo("Generating visualization code...")
        code = assistant.llm.generate_visualization_code(context, request_text)

        if output:
            with open(output, "w") as f:
                f.write(code)
            click.echo(click.style(f"\n✓ Code saved to: {output}", fg="green", bold=True))
        else:
            click.echo("\n" + "=" * 60)
            click.echo("Generated Code:")
            click.echo("=" * 60)
            click.echo(code)
            click.echo("=" * 60)

    except Exception as e:
        click.echo(click.style(f"Error: {e}", fg="red"))
        sys.exit(1)


@cli.command()
@click.argument("file_path", type=click.Path(exists=True))
def analyze(file_path):
    """
    Perform quick statistical analysis on a dataset.

    Displays comprehensive information including shape, data types,
    missing values, and statistics for numerical and categorical columns.

    \b
    Example:
        edagent analyze sample_data/sales_data.csv
    """
    try:
        import pandas as pd

        from edagent.data_analyzer import DataAnalyzer

        # Load dataset without requiring API key
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_path.endswith(".xlsx") or file_path.endswith(".xls"):
            df = pd.read_excel(file_path)
        elif file_path.endswith(".json"):
            df = pd.read_json(file_path)
        elif file_path.endswith(".parquet"):
            df = pd.read_parquet(file_path)
        else:
            df = pd.read_csv(file_path)

        click.echo(click.style(f"\nDataset: {file_path}", fg="cyan", bold=True))
        click.echo(click.style(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns\n", fg="cyan"))

        analyzer = DataAnalyzer(df)
        click.echo(analyzer.format_for_llm())

    except Exception as e:
        click.echo(click.style(f"Error: {e}", fg="red"))
        sys.exit(1)


@cli.command()
@click.option(
    "--dataset",
    type=click.Path(exists=True),
    help="Path to dataset (default: sample_data/sales_data.csv)",
)
@click.option("--api-key", help="OpenAI API key (or set OPENAI_API_KEY env var)")
def demo(dataset, api_key):
    """
    Run a demonstration of edagent capabilities.

    Shows examples of dataset loading, analysis, and visualization generation.

    \b
    Example:
        edagent demo
        edagent demo --dataset my_data.csv
    """
    api_key = get_api_key(api_key)

    # Use default dataset if not provided
    if not dataset:
        dataset = "sample_data/sales_data.csv"
        if not Path(dataset).exists():
            click.echo(click.style("Error: Default sample dataset not found.", fg="red"))
            click.echo("Please provide a dataset with --dataset option.")
            sys.exit(1)

    click.echo(click.style("\n🚀 edagent Demo\n", fg="cyan", bold=True))
    click.echo(f"Dataset: {dataset}\n")

    assistant = DataVisualizationAssistant(api_key)

    try:
        # Step 1: Load dataset
        click.echo(click.style("Step 1: Loading dataset...", fg="yellow"))
        assistant.load_dataset(dataset)
        click.echo()

        # Step 2: Show info
        click.echo(click.style("Step 2: Dataset information:", fg="yellow"))
        click.echo(assistant.get_dataset_info())
        click.echo()

        # Step 3: Create a simple visualization
        click.echo(click.style("Step 3: Creating a sample visualization...", fg="yellow"))
        click.echo("Request: 'Create a simple bar chart of the first numerical column'")
        click.echo()

        assistant.create_visualization("Create a simple bar chart of the first numerical column")
        click.echo(click.style("\n✓ Demo completed successfully!", fg="green", bold=True))

    except Exception as e:
        click.echo(click.style(f"\nError during demo: {e}", fg="red"))
        sys.exit(1)


@cli.command()
def version():
    """Display version information."""
    click.echo("edagent version 0.0.1")
    click.echo("AI-powered data visualization assistant")


if __name__ == "__main__":
    cli()
