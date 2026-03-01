from dash import html
from src.data_store import get_seasons
from src.dashboard.components.cells import driver_cell, constructor_cell
from src.dashboard.components.tables import table_card
from src.dashboard.components.kpi import kpi_card

def layout_driver_standings(season):
    df = get_seasons(season)

    drivers = (
    df.groupby("driverId", as_index=False)
    .agg({
        "driver_name": "first",
        "constructor_name": "last",  # sezon son takımı
        "points": "sum"
    })
    .sort_values("points", ascending=False)
    .reset_index(drop=True)
)

    driver_rows = [
        [i+1, driver_cell(r["driver_name"], r["constructor_name"]), int(r["points"])]
        for i, r in drivers.iterrows()
    ][0:10]

    return html.Div(
        className="page page-home",
        children=[
            html.Div(
                className="kpi-grid",
                children=[
                    kpi_card("Season", str(season)),
                    kpi_card("Drivers", str(drivers.shape[0]))
                ],
            ),

            html.Div(
                className="grid-2",
                children=[
                    table_card(
                        "Driver Standings (Top 10)",
                        ["Pos", "Driver", "Points"],
                        driver_rows,
                        href="/driver-standings",
                    ),
                ],
            ),
        ],
    )