from dash import html
from src.data_store import get_seasons
from src.dashboard.components.cells import driver_cell, constructor_cell
from src.dashboard.components.tables import table_card
from src.dashboard.components.kpi import kpi_card

def layout_constructor_standings(season):
    df = get_seasons(season)

    constructors = (
        df.groupby("constructor_name")["points"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    constructor_rows = [
        [i+1, constructor_cell(r["constructor_name"]), int(r["points"])]
        for i, r in constructors.iterrows()
    ][0:10]

    return html.Div(
        className="page page-home",
        children=[
            html.Div(
                className="kpi-grid",
                children=[
                    kpi_card("Season", str(season)),
                    kpi_card("Teams", str(constructors.shape[0])),
                ],
            ),

            html.Div(
                className="grid-2",
                children=[
                    table_card(
                        "Constructor Standings (Top 10)",
                        ["Pos", "Constructor", "Points"],
                        constructor_rows,
                        href="/q/team-performance",
                    ),
                ],
            ),
        ],
    )