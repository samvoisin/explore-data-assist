"""
Main assistant module that coordinates data analysis and visualization generation.
"""

import pandas as pd
from typing import Optional
try:
    from .data_analyzer import DataAnalyzer
    from .llm_interface import LLMInterface
except ImportError:
    from data_analyzer import DataAnalyzer
    from llm_interface import LLMInterface


class DataVisualizationAssistant:
    """Main class that coordinates the data visualization assistant."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.llm = LLMInterface(api_key)
        self.current_df = None
        self.analyzer = None
    
    def load_dataset(self, file_path: str) -> None:
        """Load a dataset from various file formats."""
        try:
            # Determine file format and load accordingly
            if file_path.endswith('.csv'):
                self.current_df = pd.read_csv(file_path)
            elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                self.current_df = pd.read_excel(file_path)
            elif file_path.endswith('.json'):
                self.current_df = pd.read_json(file_path)
            elif file_path.endswith('.parquet'):
                self.current_df = pd.read_parquet(file_path)
            else:
                # Default to CSV
                self.current_df = pd.read_csv(file_path)
            
            self.analyzer = DataAnalyzer(self.current_df)
            print(f"Dataset loaded successfully! Shape: {self.current_df.shape}")
            
        except Exception as e:
            raise Exception(f"Failed to load dataset: {str(e)}")
    
    def set_dataframe(self, df: pd.DataFrame) -> None:
        """Set a DataFrame directly."""
        self.current_df = df
        self.analyzer = DataAnalyzer(df)
        print(f"DataFrame set successfully! Shape: {df.shape}")
    
    def get_dataset_info(self) -> str:
        """Get formatted information about the current dataset."""
        if self.analyzer is None:
            return "No dataset loaded. Please load a dataset first."
        
        return self.analyzer.format_for_llm()
    
    def create_visualization(self, request: str) -> str:
        """Create a visualization based on natural language request."""
        if self.current_df is None or self.analyzer is None:
            raise Exception("No dataset loaded. Please load a dataset first.")
        
        # Get dataset context
        context = self.analyzer.format_for_llm()
        
        # Generate visualization code
        print("Generating visualization code...")
        code = self.llm.generate_visualization_code(context, request)
        
        print(f"Generated code:\n{code}")
        
        # Execute the visualization
        print("Executing visualization...")
        self.llm.execute_visualization(code, self.current_df)
        
        return code
    
    def interactive_session(self) -> None:
        """Start an interactive session with the assistant."""
        print("Welcome to the Data Visualization Assistant!")
        print("Commands:")
        print("  load <file_path> - Load a dataset")
        print("  info - Show dataset information") 
        print("  viz <request> - Create a visualization")
        print("  voice [duration] - Record voice input for visualization (default: 5 seconds)")
        print("  voice_file <audio_file_path> - Transcribe audio file for visualization")
        print("  quit - Exit the assistant")
        print()
        
        while True:
            try:
                user_input = input("Assistant> ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == 'quit':
                    print("Goodbye!")
                    break
                
                elif user_input.lower() == 'info':
                    print(self.get_dataset_info())
                
                elif user_input.startswith('load '):
                    file_path = user_input[5:].strip()
                    try:
                        self.load_dataset(file_path)
                    except Exception as e:
                        print(f"Error: {e}")
                
                elif user_input.startswith('viz '):
                    request = user_input[4:].strip()
                    try:
                        self.create_visualization(request)
                        print("Visualization created successfully!")
                    except Exception as e:
                        print(f"Error: {e}")
                
                elif user_input.startswith('voice_file '):
                    audio_file_path = user_input[11:].strip()
                    try:
                        print("Transcribing audio file...")
                        transcription = self.llm.transcribe_audio_file(audio_file_path)
                        print(f"Transcription: '{transcription}'")
                        
                        if transcription.strip():
                            self.create_visualization(transcription)
                            print("Visualization created successfully from voice input!")
                        else:
                            print("No speech detected in the audio file.")
                    except Exception as e:
                        print(f"Error: {e}")
                
                elif user_input.startswith('voice'):
                    # Parse optional duration parameter
                    parts = user_input.split()
                    duration = 5  # default duration
                    if len(parts) > 1:
                        try:
                            duration = int(parts[1])
                            if duration <= 0 or duration > 30:
                                print("Duration must be between 1 and 30 seconds")
                                continue
                        except ValueError:
                            print("Invalid duration. Using default 5 seconds.")
                    
                    try:
                        transcription = self.llm.record_and_transcribe_voice(duration)
                        print(f"Transcription: '{transcription}'")
                        
                        if transcription.strip():
                            self.create_visualization(transcription)
                            print("Visualization created successfully from voice input!")
                        else:
                            print("No speech detected. Please try again.")
                    except Exception as e:
                        print(f"Error: {e}")
                
                else:
                    print("Unknown command. Type 'quit' to exit.")
            
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")