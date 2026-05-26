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
from utils.ui_components import chart_card, highlight_banner, inject_section_card_style, kpi_card, render_data_table, render_plotly_chart, section_card


def _format_date(value):
    date_value = pd.to_datetime(value, errors="coerce")
    if pd.isna(date_value):
        return "Sem prazo"
    return date_value.strftime("%d/%m/%Y")


def _deadline_status(value):
    date_value = pd.to_datetime(value, errors="coerce")
    if pd.isna(date_value):
        return "Sem prazo"
    days_left = (date_value.normalize() - pd.Timestamp.today().normalize()).days
    if days_left < 0:
        return f"Atrasada há {abs(days_left)} dia(s)"
    if days_left == 0:
        return "Vence hoje"
    if days_left <= 7:
        return f"Vence em {days_left} dia(s)"
    return "Dentro do prazo"


def _risk_dataframe(riscos):
    df = pd.DataFrame(riscos) if riscos else pd.DataFrame()
    if df.empty:
        return df
    df["Probabilidade"] = df["probabilidade"].map(normalizar_probabilidade)
    df["Impacto"] = df["impacto"].map(normalizar_impacto)
    df["Score"] = df.apply(lambda row: calcular_score_risco(row["Probabilidade"], row["Impacto"]), axis=1)
    df["Criticidade"] = df["Score"].map(lambda score: "Baixo" if score <= 2 else "Médio" if score <= 4 else "Alto")
    return df


inject_section_card_style()

st.title("Relatórios")
st.caption("Painéis de BI para apoiar decisões executivas sobre riscos, categorias, prazos e mitigação.")

projetos = ProjetoService.listar_projetos() or []
riscos = RiscoService.listar_riscos() or []
mitigacoes = MitigacaoService.listar_mitigacoes() or []
risk_lookup = {risco["id_risco"]: risco["descricao"] for risco in riscos}

df_projetos = pd.DataFrame(projetos) if projetos else pd.DataFrame()
df_riscos = _risk_dataframe(riscos)
df_mitigacoes = pd.DataFrame(mitigacoes) if mitigacoes else pd.DataFrame()

total_riscos_ativos = int((df_riscos["status_risco"] == "Ativo").sum()) if not df_riscos.empty else 0
total_riscos_altos = int((df_riscos["Criticidade"] == "Alto").sum()) if not df_riscos.empty else 0
total_categorias = df_riscos["categoria"].nunique() if "categoria" in df_riscos.columns else 0
total_mitigacoes_pendentes = int((df_mitigacoes["status_acao"] != "Concluída").sum()) if not df_mitigacoes.empty else 0

highlight_banner(
    "Relatórios Analíticos",
    "Visão executiva com colunas, pizzas e curvas de tendência para transformar dados operacionais em decisão.",
)

st1, st2, st3, st4 = st.columns(4)
with st1:
    kpi_card("Riscos Ativos", str(total_riscos_ativos), "Exposição ainda aberta.")
with st2:
    kpi_card("Alta Criticidade", str(total_riscos_altos), "Itens que pedem resposta prioritária.")
with st3:
    kpi_card("Categorias", str(total_categorias), "Frentes de risco monitoradas.")
with st4:
    kpi_card("Ações Abertas", str(total_mitigacoes_pendentes), "Carga de mitigação não concluída.")

tab1, tab2, tab3, tab4 = st.tabs(["Visão Geral", "Categorias", "Tendências", "Mitigação"])

with tab1:
    section_card(
        "Exposição e resposta",
        "O objetivo é revelar rapidamente o tamanho da exposição e o avanço da resposta aos riscos.",
    )

    if not df_riscos.empty:
        severity = df_riscos["Criticidade"].value_counts().reindex(["Baixo", "Médio", "Alto"], fill_value=0).reset_index()
        severity.columns = ["Criticidade", "Riscos"]
        status_counts = df_riscos["status_risco"].value_counts().reset_index()
        status_counts.columns = ["Status", "Riscos"]

        col_a, col_b = st.columns([1.3, 1])
        with col_a:
            chart_card(
                "Riscos por criticidade",
                "Colunas com prioridade visual clara para leitura de diretoria.",
            )
            fig_severity = px.bar(
                severity,
                x="Criticidade",
                y="Riscos",
                text="Riscos",
                color="Criticidade",
                color_discrete_map=RISK_LEVEL_COLORS,
                category_orders={"Criticidade": ["Baixo", "Médio", "Alto"]},
            )
            style_bar_traces(fig_severity)
            render_plotly_chart(apply_executive_layout(fig_severity, height=370, showlegend=False))

        with col_b:
            chart_card(
                "Status da carteira de riscos",
                "Pizza para acompanhar o equilíbrio entre riscos abertos, mitigados e resolvidos.",
            )
            fig_status = go.Figure(
                data=[
                    go.Pie(
                        labels=status_counts["Status"],
                        values=status_counts["Riscos"],
                        hole=0.56,
                        marker=dict(colors=[STATUS_RISK_COLORS.get(label, EXECUTIVE_COLORS["slate"]) for label in status_counts["Status"]]),
                        textinfo="label+percent",
                        hovertemplate="<b>%{label}</b><br>%{value} risco(s)<extra></extra>",
                    )
                ]
            )
            render_plotly_chart(apply_executive_layout(fig_status, height=370))
    else:
        st.info("Ainda não há riscos suficientes para exibir a visão geral.")

with tab2:
    section_card(
        "Concentração por categoria",
        "Este painel identifica os temas mais recorrentes e os mais severos para orientar priorização de recursos.",
    )

    if not df_riscos.empty and "categoria" in df_riscos.columns:
        categoria_counts = (
            df_riscos.groupby("categoria")
            .agg(Riscos=("id_risco", "count"), Exposição=("Score", "sum"))
            .reset_index()
            .sort_values("Exposição", ascending=False)
        )
        total_categoria = categoria_counts["Riscos"].sum()
        categoria_counts["Participação (%)"] = (categoria_counts["Riscos"] / total_categoria * 100).round(1)

        col_chart, col_share = st.columns([1.35, 1])
        with col_chart:
            chart_card(
                "Ranking de exposição por categoria",
                "Barras horizontais ordenadas por exposição ponderada, não apenas por volume.",
            )
            fig_categoria = px.bar(
                categoria_counts.sort_values("Exposição", ascending=True),
                x="Exposição",
                y="categoria",
                orientation="h",
                text="Riscos",
                color="Exposição",
                color_continuous_scale=["#dbeafe", "#f59e0b", "#dc2626"],
            )
            fig_categoria.update_coloraxes(showscale=False)
            style_horizontal_bar_traces(fig_categoria)
            render_plotly_chart(apply_executive_layout(fig_categoria, height=390, showlegend=False))

        with col_share:
            chart_card(
                "Participação das categorias",
                "Pizza de composição para entender concentração temática da carteira.",
            )
            fig_share = go.Figure(
                data=[
                    go.Pie(
                        labels=categoria_counts["categoria"],
                        values=categoria_counts["Riscos"],
                        hole=0.50,
                        textinfo="percent",
                        hovertemplate="<b>%{label}</b><br>%{value} risco(s)<extra></extra>",
                    )
                ]
            )
            render_plotly_chart(apply_executive_layout(fig_share, height=390))

        render_data_table(
            categoria_counts.rename(columns={"categoria": "Categoria"}),
            title="Tabela de categorias",
            description="Detalhamento do ranking por volume, exposição e participação.",
            column_config={
                "Categoria": st.column_config.TextColumn(width="medium"),
                "Riscos": st.column_config.NumberColumn(width="small"),
                "Exposição": st.column_config.NumberColumn(width="small"),
                "Participação (%)": st.column_config.NumberColumn(format="%.1f%%", width="small"),
            },
        )
    else:
        st.info("Ainda não há categorias suficientes para montar o ranking.")

with tab3:
    section_card(
        "Curvas de tendência",
        "As curvas mostram concentração futura por prazo, permitindo antecipar gargalos de execução e governança.",
    )

    trend_cols = st.columns(2)
    with trend_cols[0]:
        chart_card(
            "Tendência de ações de mitigação",
            "Curva acumulada por mês de vencimento das ações.",
        )
        if not df_mitigacoes.empty and "prazo" in df_mitigacoes.columns:
            trend_mitigacao = month_trend(df_mitigacoes, "prazo", "Ações")
            fig_mitigacao_trend = px.line(
                trend_mitigacao,
                x="Mês",
                y="Acumulado",
                markers=True,
                color_discrete_sequence=[EXECUTIVE_COLORS["secondary"]],
            )
            fig_mitigacao_trend.add_bar(
                x=trend_mitigacao["Mês"],
                y=trend_mitigacao["Ações"],
                name="Ações no mês",
                marker_color="rgba(15,118,110,0.20)",
            )
            apply_line_style(fig_mitigacao_trend)
            render_plotly_chart(apply_executive_layout(fig_mitigacao_trend, height=380))
        else:
            st.info("Cadastre ações com prazo para formar a tendência.")

    with trend_cols[1]:
        chart_card(
            "Tendência de entregas do portfólio",
            "Curva acumulada por prazo final dos projetos.",
        )
        if not df_projetos.empty and "prazo_final" in df_projetos.columns:
            trend_projetos = month_trend(df_projetos, "prazo_final", "Projetos")
            fig_project_trend = px.line(
                trend_projetos,
                x="Mês",
                y="Acumulado",
                markers=True,
                color_discrete_sequence=[EXECUTIVE_COLORS["blue"]],
            )
            fig_project_trend.add_bar(
                x=trend_projetos["Mês"],
                y=trend_projetos["Projetos"],
                name="Projetos no mês",
                marker_color="rgba(37,99,235,0.18)",
            )
            apply_line_style(fig_project_trend)
            render_plotly_chart(apply_executive_layout(fig_project_trend, height=380))
        else:
            st.info("Cadastre projetos com prazo final para formar a tendência.")

with tab4:
    section_card(
        "Execução das mitigações",
        "Acompanhe a maturidade da resposta aos riscos e os prazos que podem virar gargalo.",
    )

    if not df_mitigacoes.empty and "status_acao" in df_mitigacoes.columns:
        status_acao_counts = df_mitigacoes["status_acao"].value_counts().reset_index()
        status_acao_counts.columns = ["Status", "Ações"]

        col_left, col_right = st.columns([1.25, 1])
        with col_left:
            chart_card(
                "Andamento das ações",
                "Colunas por status para leitura objetiva da execução.",
            )
            fig_mitigacao = px.bar(
                status_acao_counts,
                x="Status",
                y="Ações",
                text="Ações",
                color="Status",
                color_discrete_map=STATUS_ACTION_COLORS,
            )
            style_bar_traces(fig_mitigacao)
            render_plotly_chart(apply_executive_layout(fig_mitigacao, height=360))

        with col_right:
            chart_card(
                "Composição das ações",
                "Pizza de execução para identificar esforço parado, em andamento ou concluído.",
            )
            fig_action_status = go.Figure(
                data=[
                    go.Pie(
                        labels=status_acao_counts["Status"],
                        values=status_acao_counts["Ações"],
                        hole=0.55,
                        marker=dict(colors=[STATUS_ACTION_COLORS.get(label, EXECUTIVE_COLORS["slate"]) for label in status_acao_counts["Status"]]),
                        textinfo="label+percent",
                        hovertemplate="<b>%{label}</b><br>%{value} ação(ões)<extra></extra>",
                    )
                ]
            )
            render_plotly_chart(apply_executive_layout(fig_action_status, height=360))

        df_mitigacoes_view = df_mitigacoes.copy()
        df_mitigacoes_view["Ação"] = df_mitigacoes_view["id_acao"]
        df_mitigacoes_view["Risco"] = df_mitigacoes_view["id_risco"].map(
            lambda value: risk_lookup.get(value, f"Risco {value}")
        )
        df_mitigacoes_view["Descrição da Ação"] = df_mitigacoes_view["descricao_acao"]
        df_mitigacoes_view["Responsável"] = df_mitigacoes_view["responsavel"]
        df_mitigacoes_view["Prazo"] = df_mitigacoes_view["prazo"].apply(_format_date)
        df_mitigacoes_view["Situação do Prazo"] = df_mitigacoes_view["prazo"].apply(_deadline_status)
        df_mitigacoes_view["Status"] = df_mitigacoes_view["status_acao"]
        render_data_table(
            df_mitigacoes_view[
                [
                    "Ação",
                    "Risco",
                    "Descrição da Ação",
                    "Responsável",
                    "Prazo",
                    "Situação do Prazo",
                    "Status",
                ]
            ],
            title="Tabela completa de mitigação",
            description="Base operacional para auditoria e acompanhamento do plano.",
            column_config={
                "Ação": st.column_config.NumberColumn(width="small"),
                "Risco": st.column_config.TextColumn(width="medium"),
                "Descrição da Ação": st.column_config.TextColumn(width="large"),
                "Responsável": st.column_config.TextColumn(width="medium"),
                "Prazo": st.column_config.TextColumn(width="small"),
                "Situação do Prazo": st.column_config.TextColumn(width="medium"),
                "Status": st.column_config.TextColumn(width="small"),
            },
        )
    else:
        st.info("Nenhuma ação de mitigação registrada até o momento.")
