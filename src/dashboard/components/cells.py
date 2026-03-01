from dash import html
from src.data_store import get_team_asset




def driver_cell(driver_name, constructor_name):
    team_data = get_team_asset(constructor_name)
    logo = team_data["logo"]
    color = team_data["color"]

    return html.Div(
        className="driver-cell",
        style={"--team-color": color} if color else None,
        children=[
            html.Img(
                src=logo,
                className="team-logo",
            ) if logo else None,

            html.Span(
                driver_name,
                className="driver-name",
            ),
        ],
    )

def constructor_cell(constructor_name):
    team_data = get_team_asset(constructor_name)
    logo = team_data["logo"]
    color = team_data["color"]

    return html.Div(
        className="driver-cell",
        style={"--team-color": color} if color else None,
        children=[
            html.Img(
                src=logo,
                className="team-logo",
            ) if logo else None,

            html.Span(
                constructor_name,
                className="driver-name",
            ),
        ],
    )