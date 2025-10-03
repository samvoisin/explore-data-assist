"""
Module for interfacing with OpenAI LLMs to generate data visualization code.
"""

import os
import tempfile
import time
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

    def transcribe_audio_file(self, audio_file_path: str) -> str:
        """Transcribe audio file using OpenAI speech-to-text API."""
        try:
            with open(audio_file_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
            return transcript.strip()
        except Exception as e:
            raise Exception(f"Failed to transcribe audio: {str(e)}")

    def record_and_transcribe_voice(self, duration: int = 5) -> str:
        """Record voice input and transcribe it using OpenAI speech-to-text API.
        
        Args:
            duration: Recording duration in seconds (default: 5)
            
        Returns:
            Transcribed text from the audio
        """
        try:
            # Try to import audio libraries
            import sounddevice as sd
            import scipy.io.wavfile
        except ImportError as e:
            raise Exception(
                f"Audio libraries not available: {str(e)}. "
                "Please use 'voice_file <path>' command to transcribe an audio file instead."
            )
        
        # Record audio to temporary file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
            try:
                sample_rate = 44100  # Standard sample rate
                print(f"Recording for {duration} seconds... Speak now!")
                
                # Record audio
                audio_data = sd.rec(int(duration * sample_rate), 
                                  samplerate=sample_rate, 
                                  channels=1, 
                                  dtype='int16')
                sd.wait()  # Wait for recording to complete
                print("Recording complete!")
                
                # Save to temporary file
                scipy.io.wavfile.write(temp_audio.name, sample_rate, audio_data)
                
                # Transcribe the audio file
                transcription = self.transcribe_audio_file(temp_audio.name)
                return transcription
                
            finally:
                # Clean up temporary file
                try:
                    os.unlink(temp_audio.name)
                except OSError:
                    pass  # Ignore errors if file doesn't exist
