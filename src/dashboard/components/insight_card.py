from dash import html, dcc

def insight_card(
    title: str,
    highlight: str,
    subtitle: str,
    href: str,
    accent: str = "#ffffff",
    bg_image: str | None = None,
    variant: str = "default"
):
    return dcc.Link(
        href=href,
        className="panel-link",
        children=html.Div(
            className=f"insight-card insight-{variant}",
            children=[
                html.Div(
                    className="insight-bg",
                    style={
                        "backgroundImage": f"url({bg_image})" if bg_image else None
                    }
                ),
                html.Div(
                    className="insight-meta",
                    children=[
                        html.Div(title, className="insight-title"),
                        html.Div(
                            highlight,
                            className="insight-highlight",
                            style={"color": accent}
                        ),
                        html.Div(subtitle, className="insight-sub"),
                        html.Div("Explore →", className="insight-cta"),
                    ],
                ),
            ],
        ),
    )