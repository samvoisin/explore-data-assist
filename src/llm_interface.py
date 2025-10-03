"""
Module for interfacing with OpenAI LLMs to generate data visualization code.
"""

import os
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd
from openai import OpenAI


class LLMInterface:
    """Interface for generating visualization code using OpenAI LLMs."""

    def __init__(self, api_key: Optional[str] = None):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    def generate_visualization_code(
        self, dataset_context: str, user_request: str
    ) -> str:
        """Generate matplotlib code for the requested visualization."""

        system_prompt = """You are a data visualization expert. Your task is to generate Python code using matplotlib to create visualizations based on user requests and dataset information.

Guidelines:
1. Always use the variable 'df' to refer to the pandas DataFrame
2. Always use matplotlib.pyplot (imported as plt) for visualizations
3. Include proper labels, titles, and formatting
4. Make the visualization clear and informative
5. Only return the Python code, no explanations
6. Always call plt.show() at the end to display the plot
7. Handle potential data type conversions if needed
8. Use appropriate plot types based on data types (categorical vs numerical)
9. You may assume necessary libraries (pandas, matplotlib) are already imported

The code should be ready to execute directly."""

        user_prompt = f"""Dataset Context:
{dataset_context}

User Request: {user_request}

Please generate matplotlib code to create this visualization."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=1000,
                temperature=0.1,
            )

            code = response.choices[0].message.content.strip()
            # Clean up the code to remove markdown formatting if present
            if code.startswith("```python"):
                code = code[9:-3] if code.endswith("```") else code[9:]
            elif code.startswith("```"):
                code = code[3:-3] if code.endswith("```") else code[3:]

            return code.strip()

        except Exception as e:
            raise Exception(f"Failed to generate visualization code: {str(e)}")

    def execute_visualization(self, code: str, df: pd.DataFrame) -> None:
        """Execute the generated visualization code safely."""
        # Create a safe execution environment
        exec_globals = {
            "df": df,
            "plt": plt,
            "pd": pd,
            "__builtins__": {},  # Restrict built-in functions for safety
        }

        # Add safe built-ins back
        safe_builtins = [
            "len",
            "str",
            "int",
            "float",
            "list",
            "dict",
            "range",
            "enumerate",
            "zip",
            "max",
            "min",
            "sum",
        ]
        for builtin in safe_builtins:
            exec_globals["__builtins__"][builtin] = eval(builtin)

        try:
            exec(code, exec_globals)
        except Exception as e:
            raise Exception(f"Failed to execute visualization code: {str(e)}")
