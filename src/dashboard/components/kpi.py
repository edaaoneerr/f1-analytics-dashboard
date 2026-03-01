from dash import html, dcc

def kpi_card(title, value, subtitle="", href=None, accent="neutral", className=""):
    card = html.Div(
        className=f"kpi-card {className}",
        children=[
            html.Div(title, className="kpi-title"),
            html.Div(value, className="kpi-value"),
            html.Div(subtitle, className="kpi-subtitle") if subtitle else None,
        ],
    )

    if href:
        return dcc.Link(card, href=href, className="kpi-link")

    return card