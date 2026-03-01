# src/dashboard/pages/home.py
from dash import html
import pandas as pd

from src.data_store import get_seasons, get_team_asset, get_driver_meta
from src.dashboard.components.kpi import kpi_card
from src.dashboard.components.insight_card import insight_card
from src.dashboard.components.tables import table_card
from src.dashboard.components.cells import driver_cell, constructor_cell


def ms_to_laptime(ms: float) -> str:
    if ms is None or pd.isna(ms):
        return "-"
    ms = int(ms)
    minutes = ms // 60000
    seconds = (ms % 60000) / 1000
    return f"{minutes}:{seconds:06.2f}"


def layout_home(season: int):
    df = get_seasons(season)

    # -------------------------
    # Aggregations
    # -------------------------
    drivers = (
        df.groupby(["driverId", "driver_name", "constructor_name"], as_index=False)["points"]
        .sum()
        .sort_values("points", ascending=False)
        .reset_index(drop=True)
    )

    constructors = (
        df.groupby("constructor_name", as_index=False)["points"]
        .sum()
        .sort_values("points", ascending=False)
        .reset_index(drop=True)
    )

    top_driver = drivers.iloc[0]
    top_team = constructors.iloc[0]

    team = get_team_asset(top_team["constructor_name"])
    team_logo = team["logo"] if team else None

    winner_id = str(top_driver["driverId"])
    driver_meta = get_driver_meta(winner_id)
    driver_image = driver_meta["image"] if driver_meta else None
    winner_name = driver_meta["name"] if driver_meta else top_driver["driver_name"]

    driver_get_seasons = df[df["driverId"] == top_driver["driverId"]]
    wins = (driver_get_seasons["finishing_position"] == 1).sum()

    min_lap_time = driver_get_seasons["fastest_lap_time"].min()
    fastest_lap = ms_to_laptime(min_lap_time)

    best_finish = driver_get_seasons["finishing_position"].min()

    # -------------------------
    # Dynamic Insights (NO model fit)
    # -------------------------

    # Biggest performance factor: strongest Spearman association with points (season data)
    factor_cols = [
        "qualifying_position",
        "pit_stop_count",
        "is_street_circuit",
        "temperature",
        "windspeed",
        "precipitation",
    ]

    factor_labels = {
        "qualifying_position": "Qualifying Position",
        "pit_stop_count": "Pit Stops",
        "is_street_circuit": "Street Circuits",
        "temperature": "Track Temperature",
        "windspeed": "Wind Speed",
        "precipitation": "Weather Conditions",
    }

    corr_scores: dict[str, float] = {}
    for col in factor_cols:
        if col not in df.columns or "points" not in df.columns:
            continue
        s = df[[col, "points"]].dropna()
        if len(s) < 10 or s[col].nunique() <= 1:
            continue
        corr = s[col].corr(s["points"], method="spearman")
        if pd.notna(corr):
            corr_scores[col] = float(corr)

    if corr_scores:
        best_factor = max(corr_scores, key=lambda c: abs(corr_scores[c]))
        best_factor_label = factor_labels.get(best_factor, best_factor)
        best_factor_sub = "Strongest association with points"
    else:
        best_factor_label = "Qualifying Position"
        best_factor_sub = "Not enough data to estimate"

    # Highest crash environment: compare crash rate street vs non-street (season data)
    crash_label = "Street Circuits"
    crash_sub = "Higher crash rate"

    if "is_crash" in df.columns and "is_street_circuit" in df.columns:
        tmp = df[["is_crash", "is_street_circuit"]].dropna()
        if not tmp.empty and tmp["is_street_circuit"].nunique() > 1:
            rates = tmp.groupby("is_street_circuit")["is_crash"].mean()
            if 1 in rates.index and 0 in rates.index:
                crash_label = "Street Circuits" if rates.loc[1] >= rates.loc[0] else "Permanent Circuits"

    # -------------------------
    # Mini preview rows
    # -------------------------
    driver_rows = [
        [i + 1, driver_cell(r["driver_name"], r["constructor_name"]), int(r["points"])]
        for i, (_, r) in enumerate(drivers.head(5).iterrows())
    ]

    team_rows = [
        [i + 1, constructor_cell(r["constructor_name"]), int(r["points"])]
        for i, (_, r) in enumerate(constructors.head(5).iterrows())
    ]

    # -------------------------
    # Layout
    # -------------------------
    return html.Div(
        className="page page-home",
        children=[
            # KPI BAR
            html.Div(
                className="kpi-grid",
                children=[
                    kpi_card("Season", str(season)),
                    kpi_card("Drivers", str(df["driver_name"].nunique())),
                    kpi_card("Teams", str(df["constructor_name"].nunique())),
                    kpi_card("Total Points", str(int(df["points"].sum()))),
                ],
            ),

            # HERO INSIGHT
            html.Div(
                className="hero-insight",
                children=[
                    html.Div(
                        className="hero-left",
                        children=[
                            insight_card(
                                title="Top Performer Driver",
                                highlight=winner_name,
                                subtitle="Highest total driver points this season",
                                href="/q/driver-performance",
                                bg_image=driver_image,
                                variant="driver",
                            )
                        ],
                    ),
                    html.Div(
                        className="hero-right",
                        children=[
                            kpi_card("Wins", str(wins)),
                            kpi_card("Fastest Lap", str(fastest_lap)),
                            kpi_card("Best Finish", str(best_finish)),
                        ],
                    ),
                ],
            ),

            # SECONDARY INSIGHTS (dynamic)
            html.Div(
                className="grid-3",
                children=[
                    insight_card(
                        title="Biggest Performance Factor",
                        highlight=best_factor_label,
                        subtitle=best_factor_sub,
                        href="/q/driver-models",
                    ),
                    insight_card(
                        title="Highest Crash Environment",
                        highlight=crash_label,
                        subtitle=crash_sub,
                        href="/q/crash-risk",
                    ),
                    insight_card(
                        title="Top Performer Team",
                        highlight=top_team["constructor_name"],
                        subtitle="Highest total team points this season",
                        href="/q/team-performance",
                        bg_image=team_logo,
                        variant="team",
                    ),
                ],
            ),

            # MINI PREVIEW TABLES
            html.Div(
                className="grid-2",
                children=[
                    table_card(
                        "Top 5 Drivers",
                        ["Pos", "Driver", "Points"],
                        driver_rows,
                        href="/driver-standings",
                    ),
                    table_card(
                        "Top 5 Teams",
                        ["Pos", "Team", "Points"],
                        team_rows,
                        href="/q/team-performance",
                    ),
                ],
            ),
        ],
    )