import pandas as pd


EXECUTIVE_COLORS = {
    "primary": "#166534",
    "secondary": "#0f766e",
    "blue": "#2563eb",
    "amber": "#f59e0b",
    "red": "#dc2626",
    "slate": "#475569",
    "green_soft": "#bbf7d0",
    "teal_soft": "#99f6e4",
}

RISK_LEVEL_COLORS = {
    "Baixo": "#16a34a",
    "Médio": "#f59e0b",
    "Alto": "#dc2626",
}

STATUS_RISK_COLORS = {
    "Ativo": "#dc2626",
    "Mitigado": "#f59e0b",
    "Resolvido": "#166534",
}

STATUS_ACTION_COLORS = {
    "Pendente": "#f59e0b",
    "Em Andamento": "#2563eb",
    "Concluída": "#166534",
}


def apply_executive_layout(fig, *, height=380, showlegend=True):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=height,
        margin=dict(l=20, r=20, t=24, b=28),
        font=dict(color="#0f172a", family="Arial"),
        hoverlabel=dict(bgcolor="#ffffff", font_color="#0f172a", bordercolor="rgba(15,23,42,0.12)"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            font=dict(size=12),
        ),
        showlegend=showlegend,
    )
    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        linecolor="rgba(148,163,184,0.24)",
        tickfont=dict(size=12),
        title_font=dict(size=12),
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgba(148,163,184,0.16)",
        zeroline=False,
        tickfont=dict(size=12),
        title_font=dict(size=12),
    )
    return fig


def style_bar_traces(fig):
    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
        marker_line_color="rgba(255,255,255,0.72)",
        marker_line_width=1.2,
        hovertemplate="%{x}<br>%{y}<extra></extra>",
    )
    return fig


def style_horizontal_bar_traces(fig):
    fig.update_traces(
        textposition="outside",
        cliponaxis=False,
        marker_line_color="rgba(255,255,255,0.72)",
        marker_line_width=1.2,
        hovertemplate="%{y}<br>%{x}<extra></extra>",
    )
    return fig


def apply_line_style(fig):
    fig.update_traces(
        mode="lines+markers",
        line=dict(width=3),
        marker=dict(size=8, line=dict(width=1.5, color="#ffffff")),
        hovertemplate="%{x|%b/%Y}<br>%{y}<extra></extra>",
        selector=dict(type="scatter"),
    )
    return fig


def month_trend(df, date_column, value_name="Total"):
    if df.empty or date_column not in df.columns:
        return pd.DataFrame(columns=["Mês", value_name, "Acumulado"])

    trend = df.copy()
    trend[date_column] = pd.to_datetime(trend[date_column], errors="coerce")
    trend = trend.dropna(subset=[date_column])
    if trend.empty:
        return pd.DataFrame(columns=["Mês", value_name, "Acumulado"])

    trend["Mês"] = trend[date_column].dt.to_period("M").dt.to_timestamp()
    trend = trend.groupby("Mês").size().reset_index(name=value_name).sort_values("Mês")
    trend["Acumulado"] = trend[value_name].cumsum()
    return trend
