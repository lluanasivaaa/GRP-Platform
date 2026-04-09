import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from services.projeto_service import ProjetoService
from services.risco_service import RiscoService
from utils.ui_components import highlight_banner, inject_section_card_style, kpi_card, section_card


def _prepare_project_lookup(projects):
    return {p["id_projeto"]: p["nome_projeto"] for p in projects} if projects else {}


def _chart_layout(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=50, b=10),
        font=dict(color="#0f172a"),
    )
    return fig


inject_section_card_style()

st.title("Dashboard Executivo")
st.caption("Acompanhe os principais indicadores do GRP Platform em tempo real.")

projetos = ProjetoService.listar_projetos() or []
riscos = RiscoService.listar_riscos() or []
project_lookup = _prepare_project_lookup(projetos)

df_riscos = pd.DataFrame(riscos) if riscos else pd.DataFrame()

total_projetos = len(projetos)
total_riscos = len(riscos)
total_riscos_ativos = len([r for r in riscos if r["status_risco"] == "Ativo"])
total_riscos_resolvidos = len([r for r in riscos if r["status_risco"] == "Resolvido"])
taxa_resolvidos = (total_riscos_resolvidos / total_riscos * 100) if total_riscos else 0
total_riscos_criticos = len(
    [r for r in riscos if str(r.get("nivel_criticidade", "")).lower() in {"alto", "alta", "crítico", "critico"}]
)

highlight_banner(
    "BI Operacional Integrado",
    "O sistema ainda não usa uma ferramenta externa de BI, mas o dashboard já entrega uma leitura analítica mais executiva dentro do próprio Streamlit.",
)

section_card(
    "Resumo da Exposição ao Risco",
    "Visualização consolidada para identificar volume de riscos, capacidade de resolução e concentração nos projetos mais sensíveis.",
)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    kpi_card("Projetos Monitorados", str(total_projetos), "Base total de iniciativas acompanhadas.")
with kpi2:
    kpi_card("Riscos Mapeados", str(total_riscos), "Inventário consolidado de eventos registrados.")
with kpi3:
    meta_ativos = f"{(total_riscos_ativos / total_riscos * 100):.1f}% da carteira." if total_riscos else "Sem riscos ativos."
    kpi_card("Riscos Ativos", str(total_riscos_ativos), meta_ativos)
with kpi4:
    kpi_card("Taxa de Resolução", f"{taxa_resolvidos:.1f}%", f"{total_riscos_resolvidos} riscos resolvidos.")

if not df_riscos.empty:
    if "id_projeto" in df_riscos.columns:
        df_riscos["projeto_nome"] = df_riscos["id_projeto"].map(project_lookup).fillna(df_riscos["id_projeto"].astype(str))

    criticidade_counts = (
        df_riscos["nivel_criticidade"].value_counts().reset_index(name="total").rename(columns={"index": "nivel_criticidade"})
        if "nivel_criticidade" in df_riscos.columns
        else pd.DataFrame(columns=["nivel_criticidade", "total"])
    )
    status_counts = (
        df_riscos["status_risco"].value_counts().reset_index(name="total").rename(columns={"index": "status_risco"})
        if "status_risco" in df_riscos.columns
        else pd.DataFrame(columns=["status_risco", "total"])
    )

    principal_col, side_col = st.columns([1.55, 1])

    with principal_col:
        st.subheader("Matriz de Criticidade")
        fig_criticidade = px.bar(
            criticidade_counts,
            x="nivel_criticidade",
            y="total",
            color="nivel_criticidade",
            text="total",
            color_discrete_map={
                "Baixo": "#22c55e",
                "Baixa": "#22c55e",
                "Médio": "#f59e0b",
                "Medio": "#f59e0b",
                "Alto": "#dc2626",
                "Alta": "#dc2626",
                "Crítico": "#7f1d1d",
                "Critico": "#7f1d1d",
            },
        )
        fig_criticidade.update_traces(textposition="outside")
        st.plotly_chart(_chart_layout(fig_criticidade), use_container_width=True)

    with side_col:
        st.subheader("Sinal Executivo")
        st.markdown(
            f"""
            <div class="grp-section-card">
                <h3>Atenção Prioritária</h3>
                <p><strong>{total_riscos_criticos}</strong> riscos em nível crítico/alto exigem resposta rápida.</p>
                <p style="margin-top:0.7rem;"><strong>{total_riscos_resolvidos}</strong> riscos resolvidos fortalecem a taxa de resolução do portfólio.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        fig_status = go.Figure(
            data=[
                go.Pie(
                    labels=status_counts["status_risco"],
                    values=status_counts["total"],
                    hole=0.65,
                    marker=dict(colors=["#166534", "#f59e0b", "#0f766e", "#94a3b8"]),
                    textinfo="label+percent",
                )
            ]
        )
        fig_status.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=False,
        )
        st.plotly_chart(fig_status, use_container_width=True)

    bottom_left, bottom_right = st.columns([1.2, 1])

    with bottom_left:
        st.subheader("Projetos com Maior Exposição")
        projeto_counts = df_riscos["projeto_nome"].value_counts().head(6).reset_index()
        projeto_counts.columns = ["Projeto", "Riscos"]
        fig_projetos = px.bar(
            projeto_counts.sort_values("Riscos", ascending=True),
            x="Riscos",
            y="Projeto",
            orientation="h",
            text="Riscos",
            color="Riscos",
            color_continuous_scale=["#bbf7d0", "#16a34a", "#14532d"],
        )
        fig_projetos.update_coloraxes(showscale=False)
        fig_projetos.update_traces(textposition="outside")
        st.plotly_chart(_chart_layout(fig_projetos), use_container_width=True)

    with bottom_right:
        st.subheader("Painel Analítico")
        resumo = pd.DataFrame(
            [
                {"Indicador": "Projetos monitorados", "Valor": total_projetos},
                {"Indicador": "Riscos ativos", "Valor": total_riscos_ativos},
                {"Indicador": "Riscos resolvidos", "Valor": total_riscos_resolvidos},
                {"Indicador": "Riscos críticos/altos", "Valor": total_riscos_criticos},
            ]
        )
        st.dataframe(resumo, use_container_width=True, hide_index=True)
else:
    st.info("Ainda não há riscos cadastrados para compor o dashboard.")
