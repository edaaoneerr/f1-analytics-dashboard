import pandas as pd
import json
from src.config import (
    F1_DATA_PATH,
    DRIVER_META_PATH,
    TEAM_ASSETS_PATH,
    CRASH_RESULTS_PATH,
    DRIVER_MODEL_RESULTS_PATH
)
# ---------- TEAM NAME NORMALIZATION ----------
TEAM_NAME_MAP = {
    "Haas F1 Team": "Haas",
    "Alpine F1 Team": "Alpine",
    "Sauber": "Kick Sauber",
    "RB F1 Team": "Racing Bulls",
}

def normalize_team_name(name: str) -> str:
    return TEAM_NAME_MAP.get(name, name)


# ---------- LOAD ONCE ----------
df = pd.read_csv(F1_DATA_PATH)
df["constructor_name"] = df["constructor_name"].apply(normalize_team_name)

with open(DRIVER_META_PATH, "r") as f:
    DRIVER_META = json.load(f)

with open(TEAM_ASSETS_PATH, "r") as f:
    TEAM_ASSETS = json.load(f)

with open(CRASH_RESULTS_PATH, "r") as f:
    CRASH_RESULTS = json.load(f)

with open(DRIVER_MODEL_RESULTS_PATH, "r") as f:
    DRIVER_MODEL_RESULTS = json.load(f)


# ---------- PUBLIC API ----------
def get_full_df():
    return df.copy()

def get_seasons(year):
    return df[df["year"] == year].copy()


def get_available_seasons(start=2019):
    return sorted([y for y in df["year"].unique() if y >= start])

def get_latest_season(start=2019):
    seasons = get_available_seasons(start)
    return max(seasons)

def get_team_asset(constructor_name):
    return TEAM_ASSETS.get(constructor_name)


def get_driver_meta(driver_id):
    return DRIVER_META.get(str(driver_id))


def get_crash_results():
    return pd.DataFrame(CRASH_RESULTS)


def get_driver_model_results():
    return pd.DataFrame(DRIVER_MODEL_RESULTS)