"""
DVC pipeline stage: Load and clean data.
"""
import pandas as pd
import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_and_clean_data():
    """Load and clean insurance data."""
    # Load raw data
    raw_path = Path("data/raw/MachineLearningRating_v3.txt")
    logger.info(f"Loading data from {raw_path}")
    
    # Load with appropriate delimiter
    try:
        df = pd.read_csv(raw_path, delimiter='\t', low_memory=False)
    except:
        df = pd.read_csv(raw_path, low_memory=False)
    
    # Save cleaned data
    processed_dir = Path("data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    cleaned_path = processed_dir / "cleaned_data.csv"
    df.to_csv(cleaned_path, index=False)
    logger.info(f"Saved cleaned data to {cleaned_path}")
    
    # Create data info
    info = {
        'shape': list(df.shape),
        'columns': df.columns.tolist(),
        'missing_percentage': (df.isnull().sum() / len(df) * 100).to_dict()
    }
    
    info_path = processed_dir / "data_info.json"
    with open(info_path, 'w') as f:
        json.dump(info, f, indent=4)
    
    # Create metrics
    metrics = {
        'rows_loaded': len(df),
        'columns_loaded': len(df.columns),
        'memory_mb': df.memory_usage(deep=True).sum() / 1024**2
    }
    
    metrics_path = Path("reports/load_metrics.json")
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=4)
    
    logger.info("Data loading complete!")

if __name__ == "__main__":
    load_and_clean_data()