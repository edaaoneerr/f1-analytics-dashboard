from dash import html
from src.data_store import get_seasons, get_driver_meta, get_team_asset
from src.dashboard.components.driver_card import driver_card

def layout_drivers(season: int):
    df = get_seasons(season)

    drivers = (
    df.groupby("driverId", as_index=False)
    .agg({
        "driver_name": "first",
        "constructor_name": "last",
        "points": "sum"
    })
    .sort_values("points", ascending=False)
)

    cards = []

    for i, (_, r) in enumerate(drivers.iterrows(), start=1):
        meta =  get_driver_meta(r["driverId"])
        team_data = get_team_asset(r["constructor_name"])
        if not meta:
            print("Missing driver meta:", r["driver_name"], r["driverId"])
            continue
        cards.append(
            driver_card(
                driver_name=r["driver_name"],
                team_name=r["constructor_name"],
                driver_number=meta["number"],
                image_url=meta["image"],
                team_logo_url = team_data["logo"] if team_data else None,
                accent_color = team_data["color"] if team_data else None,
                position=i,
            )
        )

    return html.Div(
        className="page",
        children=[
            html.Div(
                className="grid-3",
                children=cards,
            )
        ],
    )