import os
import pandas as pd

def get_data_path():
    # Get the path to the src directory
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Go up one level to the project root
    project_root = os.path.dirname(current_dir)
    # Path to data directory
    data_dir = os.path.join(project_root, 'data', 'ipl_complete_dataset_2008-2024')
    return data_dir

def load_matches_data():
    data_dir = get_data_path()
    matches = pd.read_csv(os.path.join(data_dir, 'matches.csv'))
    return matches

def load_deliveries_data():
    data_dir = get_data_path()
    deliveries = pd.read_csv(os.path.join(data_dir, 'deliveries.csv'))
    return deliveries