from dash import html, dcc, Input, Output, callback
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from src.data_store import get_driver_model_results
from src.dashboard.utils.theme import apply_f1_theme


def layout_driver_models():

    df = get_driver_model_results()
    drivers = sorted(df["driver_name"].dropna().unique())

    return html.Div(
        className="page",
        children=[

            html.H2(
                "What Impacts a Driver’s Performance?",
                style={"fontWeight": "900", "fontSize": "36px"}
            ),

            html.Div(
                className="control-row",
                style={"marginTop": "20px"},
                children=[
                    dcc.Dropdown(
                        id="driver-dropdown",
                        className="dash-dropdown",
                        options=[{"label": d, "value": d} for d in drivers],
                        value=drivers[0] if drivers else None,
                        clearable=False,
                        style={"width": "320px"}
                    )
                ]
            ),

            dcc.Graph(id="driver-impact-graph"),

            html.Div(
                id="driver-impact-summary",
                style={
                    "marginTop": "20px",
                    "padding": "18px",
                    "backgroundColor": "#0b0f14",
                    "borderLeft": "4px solid #e10600",
                    "fontSize": "18px",
                    "fontWeight": "600"
                }
            )
        ],
    )


@callback(
    Output("driver-impact-graph", "figure"),
    Output("driver-impact-summary", "children"),
    Input("driver-dropdown", "value"),
)
def update_driver_model(selected_driver):

    df = get_driver_model_results()
    row = df[df["driver_name"] == selected_driver]

    if row.empty:
        fig = go.Figure()
        fig.update_layout(
            title="No model results available for this driver.",
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            height=600,
        )
        return apply_f1_theme(fig), "No model results available."

    row = row.iloc[0]

    variables = [
        "qualifying_position",
        "pit_stop_count",
        "is_street_circuit",
        "temperature",
        "windspeed",
        "precipitation"
    ]

    label_map = {
        "qualifying_position": "Qualifying Position",
        "pit_stop_count": "Pit Stops",
        "is_street_circuit": "Street Circuit",
        "temperature": "Track Temperature",
        "windspeed": "Wind Speed",
        "precipitation": "Weather Conditions",
    }

    data = []

    for var in variables:
        coef = row.get(f"{var}_coef", 0.0)
        data.append({
            "Label": label_map[var],
            "Coefficient": float(coef)
        })

    coef_df = pd.DataFrame(data)
    coef_df["abs_coef"] = coef_df["Coefficient"].abs()
    coef_df = coef_df.sort_values("Coefficient")

    colors = [
        "#00c853" if c > 0 else "#e10600"
        for c in coef_df["Coefficient"]
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=coef_df["Coefficient"],
            y=coef_df["Label"],
            orientation="h",
            marker_color=colors,
            hovertemplate="<b>%{y}</b><br>Effect: %{x:.3f}<extra></extra>",
        )
    )

    fig.add_vline(x=0, line_dash="dash", line_color="white")

    fig.update_layout(
        title=f"Relative Influence on {selected_driver}'s Points (Model Based)",
        xaxis_title="Model Coefficient (Right = Higher Points, Left = Lower Points)",
        yaxis_title="",
        height=600,
    )

    fig.update_yaxes(
        tickfont=dict(size=16),
        automargin=True,
        ticklabelposition="outside",
        ticklabelstandoff=35,
    )

    fig = apply_f1_theme(fig)

    strongest = coef_df.sort_values("abs_coef", ascending=False).iloc[0]["Label"]

    summary = (
        f"The strongest relationship with {selected_driver}'s points is {strongest}. "
        f"Green bars increase expected points, red bars decrease expected points."
    )

    return fig, summary