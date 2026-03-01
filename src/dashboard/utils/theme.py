
def apply_f1_theme(fig):
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="#05070b",
        paper_bgcolor="#05070b",
        font=dict(color="white"),
        margin=dict(l=40, r=20, t=60, b=40),
        title=dict(font=dict(size=18)),
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.06)"
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.06)"
    )

    return fig