from dash import html

def driver_card(
    driver_name: str,
    team_name: str,
    driver_number: int,
    image_url: str,
    team_logo_url: str,
    accent_color: str,
    variant: str = "default",
    position: int | None = None,
):
    return html.Div(
        className=f"driver-card {variant}",
        style={
            "--accent": accent_color,
            "--accent-soft": f"{accent_color}55",
            "--accent-ultra-soft": f"{accent_color}22",
            "--accent-border": f"{accent_color}66",
        },
        children=[

            # HEADER
            html.Div(
                className="driver-card-header",
                children=[
                    html.Div(
                        className="driver-name-wrap",
                        children=[
                            html.Span(
                                driver_name.split()[-1],
                                className="driver-lastname"
                            ),
                            html.Span(team_name, className="driver-team"),
                        ],
                    ),
                ],
            ),

            # DRIVER IMAGE
            html.Div(
                className="driver-image-wrap",
                children=html.Img(src=image_url, alt=driver_name),
            ),

            # TEAM LOGO BG
            html.Div(
                className="driver-team-bg",
                style={
                    "backgroundImage": f"url({team_logo_url})"
                },
            ),

            # DRIVER NUMBER
            html.Div(
                className="driver-number",
                children=str(driver_number),
            ),

            # POSITION
            html.Div(
                className="driver-position",
                children=str(position) if position else "",
            ),
        ],
    )