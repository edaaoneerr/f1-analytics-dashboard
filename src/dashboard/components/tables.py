from dash import html, dcc

def table_card(title, columns, rows, href=None):
    head = html.Div(
        className="card-head",
        children=[
            html.Div(title, className="card-title"),
            html.Div("↗", className="card-action") if href else None,
        ],
    )

    table = html.Table(
        className="mini-table",
        children=[
            html.Thead(html.Tr([html.Th(c) for c in columns])),
            html.Tbody(
                [html.Tr([html.Td(cell) for cell in row]) for row in rows]
            ),
        ],
    )

    card = html.Div(className="panel-card", children=[head, table])

    if href:
        return dcc.Link(card, href=href, className="panel-link")

    return card