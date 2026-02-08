import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

base_path = os.getenv("raw_data_path")
out_path = os.getenv("data_path")


circuits = pd.read_csv(f"{base_path}/circuits.csv")

results = pd.read_csv(f"{base_path}/results.csv")
races = pd.read_csv(f"{base_path}/races.csv")
drivers = pd.read_csv(f"{base_path}/drivers.csv")
constructors = pd.read_csv(f"{base_path}/constructors.csv")
qualifying = pd.read_csv(f"{base_path}/qualifying.csv")
pit_stops = pd.read_csv(f"{base_path}/pit_stops.csv")
status = pd.read_csv(f"{base_path}/status.csv")
circuits = pd.read_csv(f"{base_path}/circuits.csv")

results = results[[
    "raceId", "driverId", "constructorId",
    "grid", "positionOrder", "points", "statusId"
]]

races_small = races[["raceId", "year", "circuitId"]]
df = results.merge(races_small, on="raceId", how="left")

drivers["driver_name"] = drivers["forename"] + " " + drivers["surname"]
df = df.merge(
    drivers[["driverId", "driver_name"]],
    on="driverId", how="left"
)

df = df.merge(
    constructors[["constructorId", "name"]]
    .rename(columns={"name": "constructor_name"}),
    on="constructorId", how="left"
)

df = df.merge(
    qualifying[["raceId", "driverId", "position"]]
    .rename(columns={"position": "qualifying_position"}),
    on=["raceId", "driverId"], how="left"
)

df["qualifying_position"] = pd.to_numeric(
    df["qualifying_position"], errors="coerce"
)

pit_agg = (
    pit_stops
    .groupby(["raceId", "driverId"])
    .agg(
        pit_stop_count=("stop", "count"),
        avg_pit_duration=("milliseconds", "mean")
    )
    .reset_index()
)

df = df.merge(pit_agg, on=["raceId", "driverId"], how="left")
df["pit_stop_count"] = df["pit_stop_count"].fillna(0)

df = df.merge(
    status[["statusId", "status"]],
    on="statusId", how="left"
)

df["crash"] = (
    df["status"]
    .str.contains("Accident|Collision|Crash", case=False, na=False)
    .astype(int)
)

df = df.merge(
    circuits[["circuitId", "name", "country"]]
    .rename(columns={"name": "circuit_name"}),
    on="circuitId", how="left"
)

street_keywords = ["Street", "Monaco", "Baku", "Marina Bay", "Valencia", "Detroit", "Phoenix", "Las Vegas", "Miami", "Jeddah"]

df["is_street_circuit"] = (
    df["circuit_name"]
    .str.contains("|".join(street_keywords), case=False, na=False)
    .astype(int)
)

final_df = df.rename(columns={
    "positionOrder": "finishing_position"
})[[
    "raceId", "year",
    "circuitId", "circuit_name", "is_street_circuit",
    "driverId", "driver_name", "constructor_name",
    "qualifying_position", "grid", "finishing_position",
    "points", "pit_stop_count", "avg_pit_duration", "crash"
]]

latest_year = final_df["year"].max()
final_df = final_df[final_df["year"] >= latest_year - 4]

final_df.to_csv(f"{out_path}/f1_single_analytical_dataset.csv", index=False)    