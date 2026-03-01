from dash import html, dcc
import plotly.graph_objects as go
import pandas as pd

from src.data_store import get_crash_results
from src.dashboard.utils.theme import apply_f1_theme


def layout_crash_analysis():

    df = get_crash_results()

    if df.empty:
        fig = go.Figure()
        fig.update_layout(
            title="No crash model results available.",
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            height=600,
        )
        return html.Div(
            className="page",
            children=[dcc.Graph(figure=apply_f1_theme(fig))]
        )

    df = df[df["Variable"] != "Intercept"].copy()
    df["abs_coef"] = df["Coefficient"].abs()
    df = df.sort_values("Coefficient")

    label_map = {
        "is_street_circuit": "Street Circuit",
        "qualifying_position": "Qualifying Position",
        "pit_stop_count": "Pit Stops",
        "log_pit_duration": "Pit Duration",
        "log_fastest_lap_time": "Fastest Lap",
        "log_temprature": "Track Temperature",
        "log_windspeed": "Wind Speed",
        "precipitation": "Weather Conditions",
    }

    df["Label"] = df["Variable"].replace(label_map)

    colors = [
        "#e10600" if coef > 0 else "#00c853"
        for coef in df["Coefficient"]
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["Coefficient"],
            y=df["Label"],
            orientation="h",
            marker_color=colors,
            hovertemplate="<b>%{y}</b><br>Effect on Crash Log-Odds: %{x:.3f}<extra></extra>",
        )
    )

    fig.add_vline(x=0, line_dash="dash", line_color="white")

    fig.update_layout(
        title="Relative Influence on Crash Risk (Logistic Model)",
        xaxis_title="Model Coefficient (Right = Higher Crash Risk, Left = Lower Risk)",
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

    strongest = df.sort_values("abs_coef", ascending=False).iloc[0]["Label"]

    summary = (
        f"The strongest association with crash risk is {strongest}. "
        f"Red bars indicate factors increasing crash likelihood, "
        f"green bars indicate factors reducing crash likelihood."
    )

    return html.Div(
        className="page",
        children=[

            html.H2(
                "Which Factors Matter Most for Crash Risk?",
                style={"fontWeight": "900", "fontSize": "36px"}
            ),

            html.Div(
                style={
                    "fontSize": "20px",
                    "color": "#9ca3af",
                    "marginBottom": "25px"
                },
                children="Results are based on a logistic regression model estimated on the full dataset."
            ),

            dcc.Graph(figure=fig),

            html.Div(
                style={
                    "marginTop": "20px",
                    "padding": "18px",
                    "backgroundColor": "#0b0f14",
                    "borderLeft": "4px solid #f5c400",
                    "fontSize": "18px",
                    "fontWeight": "600"
                },
                children=summary
            )
        ],
    )