from __future__ import annotations

from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
# dashboard modules
from src.dashboard.layout.sidebar import sidebar
from src.dashboard.layout.topbar import topbar
from src.dashboard.pages.home import layout_home
from src.dashboard.pages.driver_standings import layout_driver_standings
from src.dashboard.pages.constructor_standings import layout_constructor_standings
from src.dashboard.pages.drivers import layout_drivers
from src.dashboard.pages.driver_models import layout_driver_models
from src.dashboard.pages.crash_analysis import layout_crash_analysis
from src.dashboard.pages.driver_performance import layout_driver_performance
from src.data_store import get_full_df, get_latest_season
from src.dashboard.utils.theme import apply_f1_theme
from src.dashboard.pages.team_performance import layout_team_performance
# -----------------------
# App
# -----------------------
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
    suppress_callback_exceptions=True,
)

# -----------------------
# Shell layout
# -----------------------
app.layout = html.Div(
    className="dash-shell",
    children=[
        dcc.Location(id="url"),
        dcc.Store(id="sidebar-state", data=True),

        sidebar,

        html.Div(
            id="main",
            className="main",
            children=[
                topbar,
                html.Div(id="dash-content", className="content"),
            ],
        ),
    ],
)

# -----------------------
# Routing
# -----------------------

@app.callback(
    Output("dash-content", "children"),
    Output("breadcrumb", "children"),
    Input("url", "pathname"),
    Input("season-select", "value"),
)
def route(pathname, season):

    if season is None:
        season = get_latest_season()

    if not pathname or pathname == "/dashboard":
        return layout_home(season), "Home"

    if pathname == "/drivers":
        return layout_drivers(season), "Drivers"

    if pathname == "/driver-standings":
        return layout_driver_standings(season), "Driver Standings"

    if pathname == "/q/team-performance":
        return layout_constructor_standings(season), "Constructor Standings"

    # Insights (NO season dependency)
    if pathname == "/q/driver-models":
        return layout_driver_models(), "Driver Performance Factors"

    if pathname == "/q/crash-risk":
        return layout_crash_analysis(), "Crash Risk Analysis"

    if pathname == "/q/driver-trend":
        return layout_driver_performance(), "Driver Performance Over Time"

    if pathname == "/q/team-trend":
        return layout_team_performance(), "Team Performance Over Time"

    return layout_home(season), "Home"


# -----------------------
# Sidebar toggle
# -----------------------
@app.callback(
    Output("sidebar", "className"),
    Output("main", "className"),
    Output("sidebar-state", "data"),
    Input("sidebar-toggle", "n_clicks"),
    State("sidebar-state", "data"),
    prevent_initial_call=True,
)
def toggle_sidebar(n_clicks, is_open):
    new_state = not is_open
    if new_state:
        return "sidebar", "main", True
    return "sidebar sidebar-closed", "main main-expanded", False



@app.callback(
    Output("driver-trend-graph", "figure"),
    Output("driver-trend-insight", "children"),
    Input("driver-select", "value"),
    Input("metric-select", "value"),
    Input("season-select", "value"),
)
def update_driver_performance(selected_drivers, metric, season):
    df = get_full_df()

    if not selected_drivers:
        return {}, "Select at least one driver."

    # seçilen sezondan geriye 5 sezon
    end_year = int(season) if season is not None else get_latest_season()
    years = list(range(end_year - 4, end_year + 1))
    filtered = df[df["year"].isin(years) & df["driver_name"].isin(selected_drivers)].copy()

    if filtered.empty:
        return {}, "No data for the selected drivers in this season window."

    if metric == "points":
        agg = (
            filtered.groupby(["year", "driver_name"], as_index=False)["points"]
            .sum()
        )
        y_col = "points"
        y_title = "Total Points"

    elif metric == "wins":
        filtered["win_flag"] = (filtered["finishing_position"] == 1).astype(int)
        agg = (
            filtered.groupby(["year", "driver_name"], as_index=False)["win_flag"]
            .sum()
            .rename(columns={"win_flag": "wins"})
        )
        y_col = "wins"
        y_title = "Wins"

    elif metric == "podiums":
        filtered["podium_flag"] = (filtered["finishing_position"] <= 3).astype(int)
        agg = (
            filtered.groupby(["year", "driver_name"], as_index=False)["podium_flag"]
            .sum()
            .rename(columns={"podium_flag": "podiums"})
        )
        y_col = "podiums"
        y_title = "Podium Finishes"

    elif metric == "avg_finish":
        agg = (
            filtered.groupby(["year", "driver_name"], as_index=False)["finishing_position"]
            .mean()
            .rename(columns={"finishing_position": "avg_finish"})
        )
        y_col = "avg_finish"
        y_title = "Average Finish"

    else:
        return {}, ""

    fig = px.line(
        agg,
        x="year",
        y=y_col,
        color="driver_name",
        markers=True,
    )

    fig.update_layout(
        title=f"Driver Performance Over Time ({years[0]} to {years[-1]})",
        xaxis_title="Season",
        yaxis_title=y_title,
        height=600,
        legend_title_text="",
    )
    
    # yıl ekseni: 2020, 2021 diye net görünsün
    fig.update_xaxes(
        tickmode="linear",
        dtick=1,
        tickformat="d",
    )

    fig = apply_f1_theme(fig)

    # insight basit ama doğru
    last_year = agg["year"].max()
    last_slice = agg[agg["year"] == last_year].copy()

    if metric == "avg_finish":
        best = last_slice.sort_values(y_col, ascending=True).iloc[0]["driver_name"]
        insight = f"In {last_year}, best (lowest) average finish among selected drivers: {best}."
    else:
        best = last_slice.sort_values(y_col, ascending=False).iloc[0]["driver_name"]
        insight = f"In {last_year}, highest {y_title.lower()} among selected drivers: {best}."

    return fig, insight

@app.callback(
    Output("season-wrap", "style"),
    Input("url", "pathname"),
)
def toggle_season_dropdown(pathname: str):
    # Insights pages: season dropdown hidden
    insight_paths = {
        "/q/driver-models",
        "/q/crash-risk",
    }

    if pathname in insight_paths:
        return {"display": "none"}

    # default: show
    return {"display": "flex", "alignItems": "center", "gap": "10px"}
# -----------------------
# Run
# -----------------------
if __name__ == "__main__":
    app.run(debug=True)