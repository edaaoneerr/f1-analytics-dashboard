from dash import html, dcc
import pandas as pd
from src.data_store import get_available_seasons, get_latest_season

available_seasons = get_available_seasons()
latest_season = get_latest_season()


season_dropdown = dcc.Dropdown(
    id="season-select",
    options=[{"label": str(y), "value": y} for y in available_seasons],
    value=latest_season,
    clearable=False,
    searchable=False,
    className="season-dropdown-min",
)

topbar = html.Div(
    className="topbar",
    children=[
        html.Button("☰", id="sidebar-toggle", className="sidebar-toggle"),
        html.Div(id="breadcrumb", className="breadcrumb"),

        html.Div(
            className="topbar-right",
            children=[
                html.Div(
                    id="season-wrap",
                    className="season-wrap",
                    children=[
                        html.Span("Season", className="season-label"),
                        season_dropdown,
                    ],
                )
            ],
        ),
    ],
)