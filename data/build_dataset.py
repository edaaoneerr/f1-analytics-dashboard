import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

base_path = os.getenv("RAW_F1_DATA")
out_path = os.getenv("F1_DATA")

# --------------------
# Load raw data
# --------------------
circuits = pd.read_csv(f"{base_path}/circuits.csv")
results = pd.read_csv(f"{base_path}/results.csv")
races = pd.read_csv(f"{base_path}/races.csv")
drivers = pd.read_csv(f"{base_path}/drivers.csv")
constructors = pd.read_csv(f"{base_path}/constructors.csv")
qualifying = pd.read_csv(f"{base_path}/qualifying.csv")
pit_stops = pd.read_csv(f"{base_path}/pit_stops.csv")
lap_times = pd.read_csv(f"{base_path}/lap_times.csv")
status = pd.read_csv(f"{base_path}/status.csv")
weather = pd.read_csv(f"{base_path}/weather_features_v4.csv")

# --------------------
# Base race-driver frame
# --------------------
results = results[
    ["raceId","driverId","constructorId","grid",
     "positionOrder","points","statusId"]
]

races_small = races[
    ["raceId","year","round","circuitId","date"]
]

df = results.merge(races_small, on="raceId", how="left")

# --------------------
# Driver & constructor names
# --------------------
drivers["driver_name"] = drivers["forename"] + " " + drivers["surname"]

df = df.merge(
    drivers[["driverId","driver_name"]],
    on="driverId", how="left"
)

df = df.merge(
    constructors[["constructorId","name"]]
    .rename(columns={"name":"constructor_name"}),
    on="constructorId", how="left"
)

# Constructor normalization
team_mapping = {
    "Haas F1 Team": "Haas",
    "Alpine F1 Team": "Alpine",
    "Sauber": "Kick Sauber",
    "RB F1 Team": "Racing Bulls",
}

df["constructor_name"] = df["constructor_name"].replace(team_mapping)
df["constructor_name"] = df["constructor_name"].str.replace(
    " F1 Team","",regex=False
)

# --------------------
# Qualifying
# --------------------
df = df.merge(
    qualifying[["raceId","driverId","position"]]
    .rename(columns={"position":"qualifying_position"}),
    on=["raceId","driverId"],
    how="left"
)

# --------------------
# Pit features
# --------------------
pit_features = (
    pit_stops.groupby(["raceId","driverId"])
    .agg(
        pit_stop_count=("stop","count"),
        min_pit_duration=("milliseconds","min")
    )
    .reset_index()
)

df = df.merge(
    pit_features,
    on=["raceId","driverId"],
    how="left"
)


df["pit_stop_count"] = df["pit_stop_count"].fillna(0)

# --------------------
# Lap features
# --------------------
lap_features = (
    lap_times.groupby(["raceId","driverId"])
    .agg(
        fastest_lap_time=("milliseconds","min")
    )
    .reset_index()
)

df = df.merge(
    lap_features,
    on=["raceId","driverId"],
    how="left"
)

# --------------------
# Status logic
# --------------------
df = df.merge(
    status[["statusId","status"]],
    on="statusId",
    how="left"
)

df["is_crash"] = (
    df["status"]
    .str.contains("Accident|Collision|Crash",
                  case=False,
                  na=False)
    .astype(int)
)

df["is_dnf"] = (df["status"] != "Finished").astype(int)

# --------------------
# Circuit info
# --------------------
df = df.merge(
    circuits[["circuitId","name","country"]]
    .rename(columns={"name":"circuit_name"}),
    on="circuitId",
    how="left"
)

street_keywords = [
    "Street","Monaco","Baku","Marina Bay",
    "Valencia","Detroit","Phoenix",
    "Las Vegas","Miami","Jeddah"
]

df["is_street_circuit"] = (
    df["circuit_name"]
    .str.contains("|".join(street_keywords),
                  case=False,
                  na=False)
    .astype(int)
)

# --------------------
# Weather
# --------------------
weather["datetime"] = pd.to_datetime(weather["datetime"])
weather["year"] = weather["datetime"].dt.year

weather_feature_cols = [
    c for c in weather.columns
    if c not in ["datetime","year","round"]
]

weather_join = weather[["year","round"] + weather_feature_cols]

df = df.merge(
    weather_join,
    on=["year","round"],
    how="left"
)

# --------------------
# Rename finishing position
# --------------------
df = df.rename(columns={"positionOrder":"finishing_position"})

# --------------------
# Clean types
# --------------------
int_cols = [
    "raceId","year","round","circuitId","driverId",
    "qualifying_position","grid","finishing_position",
    "pit_stop_count",
    "is_crash","is_dnf"
]

for col in int_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

df["min_pit_duration"] = pd.to_numeric(
    df["min_pit_duration"], errors="coerce"
).astype("Int64")

df["fastest_lap_time"] = pd.to_numeric(
    df["fastest_lap_time"], errors="coerce"
).astype("Int64")

# --------------------
# Final column order
# --------------------
base_cols = [
    "raceId","year","round","date",
    "circuitId","circuit_name","country",
    "is_street_circuit",
    "driverId","driver_name","constructor_name",
    "qualifying_position","grid","finishing_position",
    "points",
    "pit_stop_count","min_pit_duration",
    "fastest_lap_time",
    "is_crash","is_dnf"
]

final_df = df[base_cols + weather_feature_cols]

# Last 5 seasons
latest_year = final_df["year"].max()
final_df = final_df[
    final_df["year"] >= latest_year - 4
]

# Rename race name
final_df = final_df.rename(columns={"name":"race_name"})

# --------------------
# Save
# --------------------
final_df.to_csv(
    f"{out_path}/f1_single_analytical_dataset.csv",
    index=False
)

# print("Dataset built successfully")