from dash import html, dcc
from src.data_store import get_full_df

def layout_driver_performance():
    df = get_full_df()

    drivers = sorted(df["driver_name"].dropna().unique())

    return html.Div(
        className="page",
        children=[
            html.H2("Driver Performance Over the Last 5 Seasons",
                    style={"fontWeight": "900", "fontSize": "36px"}),

            html.P("Select drivers and a metric to explore performance trends over the last five seasons.",
                   style={
                    "fontSize": "20px",
                    "color": "#9ca3af",
                    "marginBottom": "25px"
                },),

            html.Div(
                className="control-row",
                children=[
                    dcc.Dropdown(
                        id="driver-select",
                        options=[{"label": d, "value": d} for d in drivers],
                        value=drivers[0:10],
                        multi=True,
                        clearable=False,
                        className="dash-dropdown",
                        style={"width": "340px"},
                    ),

                    dcc.Dropdown(
                        id="metric-select",
                        options=[
                            {"label": "Total Points", "value": "points"},
                            {"label": "Wins", "value": "wins"},
                            {"label": "Average Finish", "value": "avg_finish"},
                            {"label": "Podium Finishes", "value": "podiums"},
                        ],
                        value="points",
                        className="dash-dropdown",
                        style={"width": "260px"},
                        clearable=False,
                    ),
                ],
            ),

            dcc.Graph(id="driver-trend-graph"),
            html.Div(id="driver-trend-insight", 
                     className="insight-box",
                     style={
                    "marginTop": "20px",
                    "padding": "18px",
                    "backgroundColor": "#0b0f14",
                    "borderLeft": "4px solid #f5c400",
                    "fontSize": "18px",
                    "fontWeight": "600"
                },),
        ],
    )