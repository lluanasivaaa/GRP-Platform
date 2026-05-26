from decimal import Decimal

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from models.projeto import Projeto
from services.projeto_service import ProjetoService
from utils.projeto_status import (
    ACTIVE_PROJECT_STATUS,
    PROJECT_STATUS_OPTIONS,
    STATUS_COLORS,
    STATUS_DESCRIPTIONS,
    normalize_project_status,
)
from utils.ui_components import highlight_banner, inject_section_card_style, kpi_card, render_data_table, render_plotly_chart, section_card
from utils.bi_charts import EXECUTIVE_COLORS, apply_executive_layout, apply_line_style, month_trend, style_bar_traces


def _to_float(value):
    if isinstance(value, Decimal):
        return float(value)
    if value is None:
        return 0.0
    return float(value)


def _days_to_deadline(value):
    prazo = pd.to_datetime(value, errors="coerce")
    if pd.isna(prazo):
        return None
    return int((prazo.normalize() - pd.Timestamp.today().normalize()).days)


def _deadline_badge(days_left):
    if days_left is None:
        return ("Sem prazo", "#475569", "#e2e8f0")
    if days_left < 0:
        return (f"{abs(days_left)} dias em atraso", "#b91c1c", "#fee2e2")
    if days_left <= 7:
        return (f"Prazo em {days_left} dias", "#b45309", "#ffedd5")
    return (f"{days_left} dias restantes", "#166534", "#dcfce7")


def _render_board_styles():
    st.markdown(
        """
        <style>
            .kanban-column {
                border-radius: 8px;
                padding: 1rem;
                min-height: 100%;
                background: rgba(255,255,255,0.78);
                border: 1px solid rgba(15, 23, 42, 0.08);
                box-shadow: 0 18px 40px rgba(15, 23, 42, 0.08);
            }
            .kanban-card {
                border-radius: 8px;
                padding: 0.95rem;
                margin-bottom: 0.85rem;
                background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
                border: 1px solid rgba(15, 23, 42, 0.08);
                box-shadow: 0 14px 28px rgba(15, 23, 42, 0.07);
            }
            .kanban-card h4 {
                margin: 0 0 0.35rem;
                color: #0f172a;
                font-size: 1rem;
            }
            .kanban-meta {
                color: #475569;
                font-size: 0.9rem;
                margin-bottom: 0.25rem;
            }
            .kanban-badge {
                display: inline-block;
                margin-top: 0.55rem;
                padding: 0.35rem 0.7rem;
                border-radius: 999px;
                font-size: 0.77rem;
                font-weight: 700;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_card(project):
    days_left = _days_to_deadline(project.get("prazo_final"))
    deadline_text, deadline_text_color, deadline_bg = _deadline_badge(days_left)
    budget = _to_float(project.get("orcamento"))

    st.markdown(
        f"""
        <div class="kanban-card">
            <h4>{project.get("nome_projeto", "Projeto sem nome")}</h4>
            <div class="kanban-meta"><strong>ID:</strong> #{project.get("id_projeto")}</div>
            <div class="kanban-meta"><strong>Responsável:</strong> {project.get("responsavel", "-")}</div>
            <div class="kanban-meta"><strong>Orçamento:</strong> R$ {budget:,.2f}</div>
            <div class="kanban-meta"><strong>Prazo:</strong> {project.get("prazo_final", "-")}</div>
            <span class="kanban-badge" style="color:{deadline_text_color};background:{deadline_bg};">{deadline_text}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


ProjetoService.garantir_fluxo_kanban()
inject_section_card_style()
_render_board_styles()

st.title("Kanban de Projetos")
st.caption("Movimente projetos entre etapas, monitore gargalos e acompanhe o fluxo da operação em tempo real.")

projetos = ProjetoService.listar_projetos() or []
for projeto in projetos:
    projeto["status"] = normalize_project_status(projeto.get("status"))

highlight_banner(
    "Fluxo Kanban Integrado",
    "Cada projeto cadastrado no GRP Platform agora pode ser gerenciado visualmente em um board interativo com foco em prioridade, execução e validação.",
)

total_projetos = len(projetos)
em_fluxo = len([p for p in projetos if p.get("status") in ACTIVE_PROJECT_STATUS])
concluidos = len([p for p in projetos if p.get("status") == "Concluído"])
atrasados = len([p for p in projetos if (_days_to_deadline(p.get("prazo_final")) or 0) < 0])

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    kpi_card("Projetos no Board", str(total_projetos), "Todos os projetos disponíveis no fluxo.")
with kpi2:
    kpi_card("Em Fluxo", str(em_fluxo), "Backlog, planejamento, execução e validação.")
with kpi3:
    kpi_card("Concluídos", str(concluidos), "Entregas finalizadas no portfólio.")
with kpi4:
    kpi_card("Atrasados", str(atrasados), "Projetos com prazo já vencido.")

section_card(
    "Gestão visual com ação rápida",
    "Use os filtros para focar em um responsável, mova projetos de etapa com um clique e cadastre novas iniciativas direto pelo Kanban.",
)

responsaveis = sorted({p.get("responsavel", "") for p in projetos if p.get("responsavel")})
topbar1, topbar2, topbar3 = st.columns([1.2, 1.2, 1])
with topbar1:
    filtro_responsavel = st.selectbox("Responsável", ["Todos"] + responsaveis)
with topbar2:
    filtro_prazo = st.selectbox("Recorte de prazo", ["Todos", "Atrasados", "Próximos 7 dias", "Sem atraso"])
with topbar3:
    mostrar_cancelados = st.toggle("Exibir cancelados", value=False)

projetos_filtrados = []
for projeto in projetos:
    status = projeto.get("status")
    days_left = _days_to_deadline(projeto.get("prazo_final"))

    if filtro_responsavel != "Todos" and projeto.get("responsavel") != filtro_responsavel:
        continue
    if not mostrar_cancelados and status == "Cancelado":
        continue
    if filtro_prazo == "Atrasados" and not (days_left is not None and days_left < 0):
        continue
    if filtro_prazo == "Próximos 7 dias" and not (days_left is not None and 0 <= days_left <= 7):
        continue
    if filtro_prazo == "Sem atraso" and not (days_left is None or days_left >= 0):
        continue
    projetos_filtrados.append(projeto)

tab_board, tab_analytics, tab_new = st.tabs(["Board Interativo", "Insights do Fluxo", "Novo Projeto"])

with tab_board:
    colunas = st.columns(len(PROJECT_STATUS_OPTIONS))
    for index, status in enumerate(PROJECT_STATUS_OPTIONS):
        with colunas[index]:
            cards = [p for p in projetos_filtrados if p.get("status") == status]
            st.markdown(
                f"""
                <div class="kanban-column">
                    <h3 style="color:{STATUS_COLORS[status]};">{status}</h3>
                    <p style="margin:0.3rem 0 0.8rem;color:#475569;font-size:0.9rem;">{STATUS_DESCRIPTIONS[status]}</p>
                    <p style="margin:0 0 1rem;font-weight:700;color:#0f172a;">{len(cards)} projeto(s)</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if not cards:
                st.info("Nenhum projeto nesta etapa.")
            for project in cards:
                _render_card(project)
                next_options = [option for option in PROJECT_STATUS_OPTIONS if option != status]
                target_status = st.selectbox(
                    f"Mover projeto #{project['id_projeto']}",
                    next_options,
                    key=f"target_{project['id_projeto']}",
                    label_visibility="collapsed",
                )
                if st.button("Atualizar etapa", key=f"move_{project['id_projeto']}", width="stretch"):
                    projeto_atual = ProjetoService.obter_projeto(project["id_projeto"])
                    if projeto_atual:
                        projeto_atual.status = target_status
                        ProjetoService.atualizar_projeto(projeto_atual)
                        st.success(f"Projeto #{project['id_projeto']} movido para {target_status}.")
                        st.rerun()

with tab_analytics:
    if projetos:
        df = pd.DataFrame(projetos)
        df["prazo_final"] = pd.to_datetime(df["prazo_final"], errors="coerce")
        df["orcamento_num"] = df["orcamento"].map(_to_float)
        status_order = pd.Categorical(df["status"], categories=PROJECT_STATUS_OPTIONS, ordered=True)
        df["status"] = status_order
        fluxo = df["status"].value_counts().reindex(PROJECT_STATUS_OPTIONS, fill_value=0).reset_index()
        fluxo.columns = ["Etapa", "Projetos"]

        analytics_cols = st.columns([1.25, 1])
        with analytics_cols[0]:
            section_card(
                "Fluxo por etapa",
                "Colunas evidenciam gargalos e concentração operacional no board.",
            )
            fig_fluxo = px.bar(
                fluxo,
                x="Etapa",
                y="Projetos",
                text="Projetos",
                color="Etapa",
                color_discrete_map=STATUS_COLORS,
                category_orders={"Etapa": PROJECT_STATUS_OPTIONS},
            )
            style_bar_traces(fig_fluxo)
            render_plotly_chart(apply_executive_layout(fig_fluxo, height=360, showlegend=False))

        with analytics_cols[1]:
            section_card(
                "Composição do fluxo",
                "Pizza para leitura rápida do peso de cada etapa no portfólio.",
            )
            fig_fluxo_pie = go.Figure(
                data=[
                    go.Pie(
                        labels=fluxo["Etapa"],
                        values=fluxo["Projetos"],
                        hole=0.55,
                        marker=dict(colors=[STATUS_COLORS.get(label, EXECUTIVE_COLORS["slate"]) for label in fluxo["Etapa"]]),
                        textinfo="percent",
                        hovertemplate="<b>%{label}</b><br>%{value} projeto(s)<extra></extra>",
                        sort=False,
                    )
                ]
            )
            render_plotly_chart(apply_executive_layout(fig_fluxo_pie, height=360))

        trend_cols = st.columns([1.2, 1])
        with trend_cols[0]:
            section_card(
                "Curva de entregas",
                "Tendência acumulada por prazo final para antecipar picos de validação e entrega.",
            )
            trend = month_trend(df, "prazo_final", "Projetos")
            fig_trend = px.line(
                trend,
                x="Mês",
                y="Acumulado",
                markers=True,
                color_discrete_sequence=[EXECUTIVE_COLORS["blue"]],
            )
            fig_trend.add_bar(
                x=trend["Mês"],
                y=trend["Projetos"],
                name="Projetos no mês",
                marker_color="rgba(37,99,235,0.18)",
            )
            apply_line_style(fig_trend)
            render_plotly_chart(apply_executive_layout(fig_trend, height=360))

        with trend_cols[1]:
            section_card(
                "Orçamento por etapa",
                "Colunas mostram a concentração financeira do fluxo.",
            )
            budget = df.groupby("status", as_index=False)["orcamento_num"].sum()
            budget.columns = ["Etapa", "Orçamento"]
            budget["Etapa"] = pd.Categorical(budget["Etapa"], categories=PROJECT_STATUS_OPTIONS, ordered=True)
            budget = budget.sort_values("Etapa")
            fig_budget = px.bar(
                budget,
                x="Etapa",
                y="Orçamento",
                text="Orçamento",
                color="Etapa",
                color_discrete_map=STATUS_COLORS,
            )
            fig_budget.update_traces(texttemplate="R$ %{y:,.0f}")
            style_bar_traces(fig_budget)
            render_plotly_chart(apply_executive_layout(fig_budget, height=360, showlegend=False))

        resumo_cols = st.columns(2)
        with resumo_cols[0]:
            render_data_table(
                fluxo,
                title="Tabela do fluxo",
                description="Resumo por etapa com leitura mais limpa para apoiar decisões rápidas no board.",
                column_config={
                    "Etapa": st.column_config.TextColumn(width="medium"),
                    "Projetos": st.column_config.NumberColumn(width="small"),
                },
            )
        with resumo_cols[1]:
            gargalo = fluxo.sort_values("Projetos", ascending=False).iloc[0]
            st.markdown(
                f"""
                <div class="grp-section-card">
                    <h3>Leitura rápida do fluxo</h3>
                    <p>A etapa com maior concentração atual é <strong>{gargalo["Etapa"]}</strong>, com <strong>{int(gargalo["Projetos"])}</strong> projeto(s).</p>
                    <p style="margin-top:0.6rem;">Use essa visão para redistribuir esforço, revisar prioridades e reduzir acúmulos no board.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info("Cadastre projetos para visualizar os insights do fluxo.")

with tab_new:
    with st.form("criar_projeto_kanban"):
        st.subheader("Adicionar projeto direto ao board")
        nome = st.text_input("Nome do Projeto")
        responsavel = st.text_input("Responsável")
        prazo = st.date_input("Prazo Final")
        orcamento = st.number_input("Orçamento", min_value=0.0, step=0.01, format="%.2f")
        status = st.selectbox("Etapa inicial", PROJECT_STATUS_OPTIONS, index=0)
        submitted = st.form_submit_button("Adicionar ao Kanban")

        if submitted:
            projeto = Projeto(
                nome_projeto=nome,
                responsavel=responsavel,
                prazo_final=str(prazo),
                orcamento=_to_float(orcamento),
                status=status,
            )
            ProjetoService.criar_projeto(projeto)
            st.success("Projeto adicionado ao board com sucesso!")
            st.rerun()
