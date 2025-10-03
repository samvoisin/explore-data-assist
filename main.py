#!/usr/bin/env python3
"""
Main entry point for the Data Visualization Assistant.
"""

import os
import sys
from dotenv import load_dotenv

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from assistant import DataVisualizationAssistant


def main():
    """Main function to start the assistant."""
    # Load environment variables
    load_dotenv()
    
    # Check for OpenAI API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Warning: OPENAI_API_KEY not found in environment variables.")
        print("Please set your OpenAI API key in a .env file or as an environment variable.")
        print("You can copy .env.example to .env and add your key there.")
        return
    
    # Start the assistant
    assistant = DataVisualizationAssistant(api_key)
    assistant.interactive_session()


if __name__ == "__main__":
    main()