from dash import html, dcc, Input, Output, callback
import plotly.express as px

from src.data_store import get_full_df
from src.dashboard.utils.theme import apply_f1_theme


def layout_team_performance():
    df = get_full_df()

    teams = sorted(df["constructor_name"].dropna().unique())

    return html.Div(
        className="page",
        children=[
            html.H2(
                "How Do Teams Perform Over Multiple Seasons?",
                style={"fontWeight": "900", "fontSize": "36px"}
            ),

            html.P("Select teams and a metric to compare trends over the last five seasons.",
                   style={
                    "fontSize": "20px",
                    "color": "#9ca3af",
                    "marginBottom": "25px"
                },),

            html.Div(
                className="control-row",
                children=[
                    dcc.Dropdown(
                        id="team-select",
                        options=[{"label": t, "value": t} for t in teams],
                        value=teams,
                        multi=True,
                        className="dash-dropdown",
                        style={"width": "320px"}
                    ),
                    dcc.Dropdown(
                        id="team-metric-select",
                        options=[
                            {"label": "Total Points", "value": "points"},
                            {"label": "Wins", "value": "wins"},
                            {"label": "Podiums", "value": "podiums"},
                            {"label": "Average Finish", "value": "avg_finish"},
                        ],
                        value="points",
                        clearable=False,
                        className="dash-dropdown",
                        style={"width": "260px"}
                    ),
                ],
            ),

            dcc.Graph(id="team-trend-graph"),
            html.Div(id="team-trend-insight", className="insight-box",
                     style={
                    "marginTop": "20px",
                    "padding": "18px",
                    "backgroundColor": "#0b0f14",
                    "borderLeft": "4px solid #f5c400",
                    "fontSize": "18px",
                    "fontWeight": "600"
                },)
        ],
    )


@callback(
    Output("team-trend-graph", "figure"),
    Output("team-trend-insight", "children"),
    Input("team-select", "value"),
    Input("team-metric-select", "value"),
    Input("season-select", "value"),
)
def update_team_trend(selected_teams, metric, season):
    df = get_full_df()

    if not selected_teams:
        return {}, "Select at least one team."

    end_year = int(season)
    years = list(range(end_year - 4, end_year + 1))

    filtered = df[df["constructor_name"].isin(selected_teams)].copy()
    filtered = filtered[filtered["year"].isin(years)]

    if filtered.empty:
        return {}, "No data for the selected teams in this season window."

    if metric == "points":
        agg = (
            filtered.groupby(["year", "constructor_name"], as_index=False)["points"]
            .sum()
        )
        y_col = "points"
        y_title = "Total Points"

    elif metric == "wins":
        filtered["win_flag"] = (filtered["finishing_position"] == 1).astype(int)
        agg = (
            filtered.groupby(["year", "constructor_name"], as_index=False)["win_flag"]
            .sum()
            .rename(columns={"win_flag": "wins"})
        )
        y_col = "wins"
        y_title = "Wins"

    elif metric == "podiums":
        filtered["podium_flag"] = (filtered["finishing_position"] <= 3).astype(int)
        agg = (
            filtered.groupby(["year", "constructor_name"], as_index=False)["podium_flag"]
            .sum()
            .rename(columns={"podium_flag": "podiums"})
        )
        y_col = "podiums"
        y_title = "Podiums"

    elif metric == "avg_finish":
        agg = (
            filtered.groupby(["year", "constructor_name"], as_index=False)["finishing_position"]
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
        color="constructor_name",
        markers=True,
    )

    fig.update_layout(
        title=f"Team Performance Over Time ({years[0]} to {years[-1]})",
        xaxis_title="Season",
        yaxis_title=y_title,
        height=600,
        legend_title_text="",
    )

    fig.update_xaxes(
        tickmode="linear",
        dtick=1,
        tickformat="d",
    )

    fig = apply_f1_theme(fig)

    latest = agg[agg["year"] == agg["year"].max()].copy()
    if metric == "avg_finish":
        best_team = latest.sort_values(y_col, ascending=True).iloc[0]["constructor_name"]
        insight = f"In {latest['year'].max()}, best (lowest) average finish: {best_team}."
    else:
        best_team = latest.sort_values(y_col, ascending=False).iloc[0]["constructor_name"]
        insight = f"In {latest['year'].max()}, highest {y_title.lower()}: {best_team}."

    return fig, insight