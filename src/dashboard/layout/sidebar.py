from dash import html
import dash_bootstrap_components as dbc

sidebar = html.Div(
    id="sidebar",
    className="sidebar",
    children=[
        html.Div(
            className="sidebar-brand",
            children=[
                html.Img(src="/assets/f1_icon.png", className="sidebar-logo"),
                html.Span("Formula 1 Dashboard", className="sidebar-brand-text"),
            ],
        ),

        html.Div("Menu", className="sidebar-section-title"),
        dbc.Nav(
            vertical=True,
            pills=True,
            className="sidebar-nav",
            children=[
                dbc.NavLink("Home", href="/dashboard", active="exact"),
                dbc.NavLink("Drivers", href="/drivers", active="exact"),
                dbc.NavLink("Driver Standings", href="/driver-standings", active="exact"),
                dbc.NavLink("Constructor Standings", href="/q/team-performance", active="exact"),
                html.Div("Insights", className="sidebar-section-title"),
                dbc.NavLink("Driver Performance Factors", href="/q/driver-models", active="exact"),
                dbc.NavLink("Crash Risk Analysis", href="/q/crash-risk", active="exact"),
                dbc.NavLink("Driver Performances", href="/q/driver-trend", active="exact"),
                dbc.NavLink("Team Performances", href="/q/team-trend", active="exact"),
            ],
        )
    ],
)