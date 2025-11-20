"""
Command-line interface for edagent.
"""

import os
import sys
from typing import Optional

import click
from dotenv import load_dotenv

from edagent.assistant import DataVisualizationAssistant


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
        click.echo("  3. Pass it: edagent --api-key your-key-here")
        sys.exit(1)
    return key


@click.command()
@click.argument("file_path", type=click.Path(exists=True), required=False)
@click.option("--api-key", help="OpenAI API key (or set OPENAI_API_KEY env var)")
@click.version_option(version="0.0.1", prog_name="edagent")
def cli(file_path, api_key):
    """
    edagent - AI-powered data visualization assistant.

    Start an interactive session to create matplotlib visualizations
    from your datasets using natural language.

    \b
    Interactive Commands:
        load <file_path> - Load a dataset
        info             - Show dataset information
        viz <request>    - Create a visualization
        voice [duration] - Record voice input (default: 5 seconds)
        quit             - Exit the assistant

    \b
    Examples:
        edagent
        edagent sample_data/sales_data.csv
        edagent --api-key your-key-here sample_data/sales_data.csv
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


if __name__ == "__main__":
    cli()
