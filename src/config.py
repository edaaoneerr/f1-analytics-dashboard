import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

DATA_DIR = os.path.join(BASE_DIR, "data")

PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
ANALYSIS_DIR = os.path.join(DATA_DIR, "analysis")
METADATA_DIR = os.path.join(DATA_DIR, "metadata")

F1_DATA_PATH = os.path.join(PROCESSED_DIR, "f1_single_analytical_dataset.csv")
DRIVER_META_PATH = os.path.join(METADATA_DIR, "driver_meta.json")
TEAM_ASSETS_PATH = os.path.join(METADATA_DIR, "team_assets.json")

CRASH_RESULTS_PATH = os.path.join(ANALYSIS_DIR, "crash_probability_results.json")
DRIVER_MODEL_RESULTS_PATH = os.path.join(ANALYSIS_DIR, "driver_regression_results.json")