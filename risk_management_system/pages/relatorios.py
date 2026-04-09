import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from services.mitigacao_service import MitigacaoService
from services.risco_service import RiscoService
from utils.ui_components import highlight_banner, inject_section_card_style, kpi_card, section_card


def _chart_layout(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=50, b=10),
        font=dict(color="#0f172a"),
    )
    return fig


inject_section_card_style()

st.title("Relatórios")
st.caption("Gere análises visuais para apoiar decisões de governança e resposta ao risco.")

riscos = RiscoService.listar_riscos() or []
mitigacoes = MitigacaoService.listar_mitigacoes() or []

df_riscos = pd.DataFrame(riscos) if riscos else pd.DataFrame()
df_mitigacoes = pd.DataFrame(mitigacoes) if mitigacoes else pd.DataFrame()

total_riscos_ativos = len([r for r in riscos if r["status_risco"] == "Ativo"])
total_riscos_resolvidos = len([r for r in riscos if r["status_risco"] == "Resolvido"])
total_categorias = df_riscos["categoria"].nunique() if "categoria" in df_riscos.columns else 0

highlight_banner(
    "Relatórios Analíticos",
    "Uma visão mais executiva para leitura rápida da exposição ao risco, categorias predominantes e andamento das ações de mitigação.",
)

st1, st2, st3 = st.columns(3)
with st1:
    kpi_card("Riscos Ativos", str(total_riscos_ativos), "Volume em tratamento no portfólio.")
with st2:
    kpi_card("Categorias Mapeadas", str(total_categorias), "Diversidade de frentes monitoradas.")
with st3:
    kpi_card("Ações de Mitigação", str(len(mitigacoes)), "Histórico total de ações registradas.")

tab1, tab2, tab3 = st.tabs(["📌 Visão Geral", "🧩 Categorias", "🛠️ Mitigação"])

with tab1:
    section_card(
        "Painel de Exposição",
        "Leitura executiva da distribuição por status para acelerar priorização e tomada de decisão.",
    )

    if not df_riscos.empty and "status_risco" in df_riscos.columns:
        status_counts = df_riscos["status_risco"].value_counts().reset_index(name="total")
        status_counts.columns = ["status_risco", "total"]

        col_a, col_b = st.columns([1.35, 1])
        with col_a:
            fig_status = px.bar(
                status_counts,
                x="status_risco",
                y="total",
                text="total",
                color="status_risco",
                color_discrete_sequence=["#166534", "#f59e0b", "#0f766e", "#94a3b8"],
            )
            fig_status.update_traces(textposition="outside")
            st.plotly_chart(_chart_layout(fig_status), use_container_width=True)

        with col_b:
            fig_donut = go.Figure(
                data=[
                    go.Pie(
                        labels=status_counts["status_risco"],
                        values=status_counts["total"],
                        hole=0.62,
                        textinfo="label+percent",
                        marker=dict(colors=["#166534", "#f59e0b", "#0f766e", "#94a3b8"]),
                    )
                ]
            )
            fig_donut.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=10, b=10),
                showlegend=False,
            )
            st.plotly_chart(fig_donut, use_container_width=True)
    else:
        st.info("Ainda não há riscos suficientes para exibir a visão geral.")

with tab2:
    section_card(
        "Riscos por Categoria",
        "Apresentação mais próxima de BI, com ranking visual, participação relativa e tabela de apoio.",
    )

    if not df_riscos.empty and "categoria" in df_riscos.columns:
        categoria_counts = df_riscos["categoria"].value_counts().reset_index(name="total")
        categoria_counts.columns = ["categoria", "total"]
        total_categoria = categoria_counts["total"].sum()
        categoria_counts["participação"] = (categoria_counts["total"] / total_categoria * 100).round(1)

        col_chart, col_share = st.columns([1.4, 1])
        with col_chart:
            fig_categoria = px.bar(
                categoria_counts.sort_values("total", ascending=True),
                x="total",
                y="categoria",
                orientation="h",
                text="total",
                color="participação",
                color_continuous_scale=["#dcfce7", "#22c55e", "#14532d"],
            )
            fig_categoria.update_coloraxes(showscale=False)
            fig_categoria.update_traces(textposition="outside")
            st.plotly_chart(_chart_layout(fig_categoria), use_container_width=True)

        with col_share:
            pie_colors = ["#dcfce7", "#86efac", "#22c55e", "#166534", "#14532d", "#052e16"]
            fig_share = go.Figure(
                data=[
                    go.Pie(
                        labels=categoria_counts["categoria"],
                        values=categoria_counts["total"],
                        hole=0.6,
                        textinfo="percent",
                        marker=dict(colors=pie_colors[: len(categoria_counts)]),
                    )
                ]
            )
            fig_share.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=10, b=10),
                showlegend=True,
                legend=dict(orientation="h", y=-0.18),
            )
            st.plotly_chart(fig_share, use_container_width=True)

        st.dataframe(
            categoria_counts.rename(
                columns={"categoria": "Categoria", "total": "Quantidade", "participação": "Participação (%)"}
            ),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("Ainda não há categorias suficientes para montar o ranking.")

with tab3:
    section_card(
        "Histórico de Mitigação",
        "Acompanhe a carga de ações e o andamento operacional da resposta aos riscos.",
    )

    if not df_mitigacoes.empty and "status_acao" in df_mitigacoes.columns:
        status_acao_counts = df_mitigacoes["status_acao"].value_counts().reset_index(name="total")
        status_acao_counts.columns = ["status_acao", "total"]

        col_left, col_right = st.columns([1.3, 1])
        with col_left:
            fig_mitigacao = px.area(
                status_acao_counts,
                x="status_acao",
                y="total",
                color="status_acao",
                color_discrete_sequence=["#0f766e", "#f59e0b", "#166534"],
            )
            st.plotly_chart(_chart_layout(fig_mitigacao), use_container_width=True)

        with col_right:
            st.dataframe(
                status_acao_counts.rename(columns={"status_acao": "Status", "total": "Quantidade"}),
                hide_index=True,
                use_container_width=True,
            )

        st.dataframe(df_mitigacoes, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhuma ação de mitigação registrada até o momento.")
