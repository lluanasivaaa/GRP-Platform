import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from services.mitigacao_service import MitigacaoService
from services.projeto_service import ProjetoService
from services.risco_service import RiscoService
from utils.bi_charts import (
    EXECUTIVE_COLORS,
    RISK_LEVEL_COLORS,
    STATUS_ACTION_COLORS,
    STATUS_RISK_COLORS,
    apply_executive_layout,
    apply_line_style,
    month_trend,
    style_bar_traces,
    style_horizontal_bar_traces,
)
from utils.calculo_risco import calcular_score_risco, normalizar_impacto, normalizar_probabilidade
from utils.ui_components import (
    chart_card,
    highlight_banner,
    inject_section_card_style,
    kpi_card,
    render_data_table,
    render_plotly_chart,
    section_card,
)


def _prepare_risk_dataframe(riscos, projetos):
    df = pd.DataFrame(riscos) if riscos else pd.DataFrame()
    if df.empty:
        return df

    projeto_lookup = {p["id_projeto"]: p["nome_projeto"] for p in projetos} if projetos else {}
    df["Projeto"] = df["id_projeto"].map(lambda value: projeto_lookup.get(value, f"Projeto {value}"))
    df["Probabilidade"] = df["probabilidade"].map(normalizar_probabilidade)
    df["Impacto"] = df["impacto"].map(normalizar_impacto)
    df["Score"] = df.apply(lambda row: calcular_score_risco(row["Probabilidade"], row["Impacto"]), axis=1)
    df["Criticidade"] = df["Score"].map(lambda score: "Baixo" if score <= 2 else "Médio" if score <= 4 else "Alto")
    return df


def _prepare_project_dataframe(projetos):
    df = pd.DataFrame(projetos) if projetos else pd.DataFrame()
    if df.empty:
        return df
    df["prazo_final"] = pd.to_datetime(df["prazo_final"], errors="coerce")
    df["orcamento"] = pd.to_numeric(df["orcamento"], errors="coerce").fillna(0)
    return df


inject_section_card_style()

st.title("Dashboard Executivo")
st.caption("Visão de decisão sobre exposição, tendência e execução do portfólio.")

projetos = ProjetoService.listar_projetos() or []
riscos = RiscoService.listar_riscos() or []
mitigacoes = MitigacaoService.listar_mitigacoes() or []

df_projetos = _prepare_project_dataframe(projetos)
df_riscos = _prepare_risk_dataframe(riscos, projetos)
df_mitigacoes = pd.DataFrame(mitigacoes) if mitigacoes else pd.DataFrame()

total_projetos = len(projetos)
total_riscos = len(riscos)
total_riscos_ativos = int((df_riscos["status_risco"] == "Ativo").sum()) if not df_riscos.empty else 0
total_riscos_resolvidos = int((df_riscos["status_risco"] == "Resolvido").sum()) if not df_riscos.empty else 0
taxa_resolvidos = (total_riscos_resolvidos / total_riscos * 100) if total_riscos else 0
total_riscos_altos = int((df_riscos["Criticidade"] == "Alto").sum()) if not df_riscos.empty else 0

highlight_banner(
    "BI Executivo de Riscos e Portfólio",
    "Gráficos orientados à decisão: exposição por severidade, concentração por projeto, status de resposta e tendência de entregas.",
)

section_card(
    "Leitura executiva",
    "A página prioriza gráficos de coluna, composição e curva de tendência para apoiar decisões rápidas e leitura direta.",
)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    kpi_card("Projetos Monitorados", str(total_projetos), "Carteira total acompanhada.")
with kpi2:
    kpi_card("Riscos Mapeados", str(total_riscos), "Inventário consolidado de exposição.")
with kpi3:
    kpi_card("Riscos Ativos", str(total_riscos_ativos), "Itens ainda exigindo gestão.")
with kpi4:
    kpi_card("Taxa de Resolução", f"{taxa_resolvidos:.1f}%", f"{total_riscos_altos} risco(s) em alta criticidade.")

if not df_riscos.empty:
    severity_order = ["Baixo", "Médio", "Alto"]
    severity_counts = (
        df_riscos["Criticidade"]
        .value_counts()
        .reindex(severity_order, fill_value=0)
        .reset_index()
    )
    severity_counts.columns = ["Criticidade", "Riscos"]

    status_counts = df_riscos["status_risco"].value_counts().reset_index()
    status_counts.columns = ["Status", "Riscos"]

    top_left, top_right = st.columns([1.45, 1])
    with top_left:
        chart_card(
            "Exposição por criticidade",
            "Colunas ordenadas mostram a pressão real da carteira e destacam imediatamente riscos de alta severidade.",
        )
        fig_severity = px.bar(
            severity_counts,
            x="Criticidade",
            y="Riscos",
            text="Riscos",
            color="Criticidade",
            color_discrete_map=RISK_LEVEL_COLORS,
            category_orders={"Criticidade": severity_order},
        )
        style_bar_traces(fig_severity)
        render_plotly_chart(apply_executive_layout(fig_severity, height=380, showlegend=False))

    with top_right:
        chart_card(
            "Composição por status",
            "Donut executivo para medir rapidamente quanto da exposição está aberta, mitigada ou resolvida.",
        )
        fig_status = go.Figure(
            data=[
                go.Pie(
                    labels=status_counts["Status"],
                    values=status_counts["Riscos"],
                    hole=0.62,
                    marker=dict(colors=[STATUS_RISK_COLORS.get(label, EXECUTIVE_COLORS["slate"]) for label in status_counts["Status"]]),
                    textinfo="percent",
                    hovertemplate="<b>%{label}</b><br>%{value} risco(s)<br>%{percent}<extra></extra>",
                    sort=False,
                )
            ]
        )
        render_plotly_chart(apply_executive_layout(fig_status, height=380))

    middle_left, middle_right = st.columns([1.35, 1.05])
    with middle_left:
        chart_card(
            "Projetos com maior exposição ponderada",
            "Ranking combina volume e score de severidade para revelar onde a liderança deve concentrar atenção.",
        )
        exposure = (
            df_riscos.groupby("Projeto")
            .agg(Riscos=("id_risco", "count"), Exposição=("Score", "sum"), Score_médio=("Score", "mean"))
            .reset_index()
            .sort_values("Exposição", ascending=False)
            .head(8)
        )
        fig_exposure = px.bar(
            exposure.sort_values("Exposição", ascending=True),
            x="Exposição",
            y="Projeto",
            orientation="h",
            text="Exposição",
            color="Score_médio",
            color_continuous_scale=["#bbf7d0", "#f59e0b", "#dc2626"],
            custom_data=["Riscos", "Score_médio"],
        )
        fig_exposure.update_traces(
            hovertemplate="<b>%{y}</b><br>Exposição: %{x}<br>Riscos: %{customdata[0]}<br>Score médio: %{customdata[1]:.1f}<extra></extra>"
        )
        fig_exposure.update_coloraxes(showscale=False)
        style_horizontal_bar_traces(fig_exposure)
        render_plotly_chart(apply_executive_layout(fig_exposure, height=390, showlegend=False))

    with middle_right:
        chart_card(
            "Resposta por prazo",
            "Curva acumulada das ações de mitigação por vencimento para antecipar picos de trabalho.",
        )
        if not df_mitigacoes.empty and "prazo" in df_mitigacoes.columns:
            trend = month_trend(df_mitigacoes, "prazo", "Ações")
            fig_trend = px.line(
                trend,
                x="Mês",
                y="Acumulado",
                markers=True,
                color_discrete_sequence=[EXECUTIVE_COLORS["secondary"]],
            )
            fig_trend.add_bar(
                x=trend["Mês"],
                y=trend["Ações"],
                name="Ações no mês",
                marker_color="rgba(15,118,110,0.22)",
                hovertemplate="%{x|%b/%Y}<br>%{y} ação(ões)<extra></extra>",
            )
            apply_line_style(fig_trend)
            render_plotly_chart(apply_executive_layout(fig_trend, height=390))
        else:
            st.info("Cadastre ações de mitigação com prazo para formar a curva de tendência.")

    category_counts = df_riscos["categoria"].value_counts().head(8).reset_index()
    category_counts.columns = ["Categoria", "Riscos"]
    chart_card(
        "Categorias que mais pressionam o portfólio",
        "Pareto visual para separar temas recorrentes de ruído operacional.",
    )
    fig_categories = px.bar(
        category_counts,
        x="Categoria",
        y="Riscos",
        text="Riscos",
        color="Riscos",
        color_continuous_scale=["#dbeafe", "#2563eb", "#0f172a"],
    )
    fig_categories.update_coloraxes(showscale=False)
    style_bar_traces(fig_categories)
    render_plotly_chart(apply_executive_layout(fig_categories, height=360, showlegend=False))
else:
    st.info("Ainda não há riscos cadastrados para compor o dashboard executivo.")

if not df_projetos.empty:
    st.divider()
    chart_card(
        "Curva de entregas planejadas",
        "Tendência de conclusão por prazo final dos projetos, útil para visualizar concentração de entregas futuras.",
    )
    delivery_trend = month_trend(df_projetos, "prazo_final", "Projetos")
    fig_delivery = px.line(
        delivery_trend,
        x="Mês",
        y="Acumulado",
        markers=True,
        color_discrete_sequence=[EXECUTIVE_COLORS["blue"]],
    )
    fig_delivery.add_bar(
        x=delivery_trend["Mês"],
        y=delivery_trend["Projetos"],
        name="Projetos no mês",
        marker_color="rgba(37,99,235,0.20)",
    )
    apply_line_style(fig_delivery)
    render_plotly_chart(apply_executive_layout(fig_delivery, height=360))

resumo = pd.DataFrame(
    [
        {"Indicador": "Projetos monitorados", "Valor": total_projetos},
        {"Indicador": "Riscos ativos", "Valor": total_riscos_ativos},
        {"Indicador": "Riscos resolvidos", "Valor": total_riscos_resolvidos},
        {"Indicador": "Riscos de alta criticidade", "Valor": total_riscos_altos},
    ]
)
render_data_table(
    resumo,
    title="Resumo numérico",
    description="Valores de apoio para auditoria rápida dos gráficos executivos.",
    column_config={
        "Indicador": st.column_config.TextColumn(width="medium"),
        "Valor": st.column_config.NumberColumn(width="small"),
    },
)
