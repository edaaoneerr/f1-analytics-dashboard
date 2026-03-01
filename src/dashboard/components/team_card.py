from dash import html


def team_card(
    team_name: str,
    chassis: str,
    color: str,
    logo_url: str,
    car_image_url: str,
    drivers: list[dict],  # [{"name": "...", "image": "..."}]
):
    return html.Div(
        className="team-card",
        style={
            "--accent": color,
            "--accent-soft": f"{color}33",
            "--accent-border": f"{color}55",
        },
        children=[

            # TOP INFO
            html.Div(
                className="team-card-header",
                children=[
                    html.Div(
                        className="team-title-wrap",
                        children=[
                            html.Span(team_name, className="team-name"),
                            html.Span(chassis, className="team-chassis"),
                            html.Span(
                                "Team profile →",
                                className="team-cta"
                            ),
                        ],
                    ),

                    # DRIVER AVATARS
                    html.Div(
                        className="team-driver-avatars",
                        children=[
                            html.Span(
                                className="driver-avatar",
                                style={"backgroundColor": color},
                                children=html.Img(
                                    src=d["image"],
                                    alt=d["name"]
                                )
                            )
                            for d in drivers[:2]
                            if d.get("image")
                        ],
                    ),
                ],
            ),

            # CAR IMAGE
            html.Div(
                className="team-car-wrap",
                children=[
                    html.Img(
                        src=car_image_url,
                        alt=f"{team_name} car",
                        className="team-car-img",
                    ),
                    html.Div(className="car-shadow"),
                ],
            ),

            # LOGO BACKGROUND
            html.Div(
                className="team-logo-bg",
                style={
                    "backgroundImage": f"url({logo_url})"
                },
            ),
        ],
    )