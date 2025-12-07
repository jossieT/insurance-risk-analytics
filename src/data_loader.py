import pandas as pd
import os

def load_raw_data(filepath=None):
    """
    Loads the raw data from the specified filepath.
    If no filepath is provided, looks for the default path.
    """
    if filepath is None:
        # Assuming run from root or notebooks dir
        filepath = '../data/MachineLearningRating_v3.txt'
        if not os.path.exists(filepath):
            filepath = 'data/MachineLearningRating_v3.txt'
    
    try:
        df = pd.read_csv(filepath, sep='|', low_memory=False)
        print(f"Data loaded successfully. Shape: {df.shape}")
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def preview_data(df):
    """
    Displays the head, tail, and info of the dataframe.
    """
    if df is not None:
        print("--- Head ---")
        display(df.head())
        print("\n--- Info ---")
        print(df.info())
        print("\n--- Tail ---")
        display(df.tail())
    else:
        print("DataFrame is None")

