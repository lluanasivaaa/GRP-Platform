from decimal import Decimal

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from models.projeto import Projeto
from services.projeto_service import ProjetoService
from utils.bi_charts import (
    EXECUTIVE_COLORS,
    apply_executive_layout,
    apply_line_style,
    month_trend,
    style_bar_traces,
    style_horizontal_bar_traces,
)
from utils.projeto_status import PROJECT_STATUS_OPTIONS, STATUS_COLORS, normalize_project_status
from utils.ui_components import chart_card, inject_section_card_style, kpi_card, render_data_table, render_plotly_chart, section_card


def _to_float(value):
    if isinstance(value, Decimal):
        return float(value)
    if value is None:
        return 0.0
    return float(value)


def _format_currency(value):
    return f"R$ {_to_float(value):,.2f}"


def _format_date(value):
    date_value = pd.to_datetime(value, errors="coerce")
    if pd.isna(date_value):
        return "Sem prazo"
    return date_value.strftime("%d/%m/%Y")


inject_section_card_style()


st.title("Gestão de Projetos")
st.caption("Cadastre, acompanhe e atualize os projetos monitorados pelo GRP Platform.")

status_options = ["Todos"] + PROJECT_STATUS_OPTIONS
filtro_status = st.selectbox("Filtrar por Status", status_options)

if filtro_status == "Todos":
    projetos = ProjetoService.listar_projetos()
else:
    projetos = ProjetoService.listar_projetos(filtro_status)

if projetos:
    for projeto in projetos:
        projeto["status"] = normalize_project_status(projeto.get("status"))
    df = pd.DataFrame(projetos).copy()
    df["prazo_final"] = pd.to_datetime(df["prazo_final"], errors="coerce")
    df["orcamento_num"] = df["orcamento"].apply(_to_float)
    df["Projeto"] = df["nome_projeto"]
    df["Responsável"] = df["responsavel"]
    df["Prazo Final"] = df["prazo_final"].apply(_format_date)
    df["Orçamento"] = df["orcamento"].apply(_format_currency)
    df["Status"] = df["status"]

    total_orcamento = df["orcamento_num"].sum()
    prazo_vencido = int((df["prazo_final"] < pd.Timestamp.today().normalize()).sum())
    em_fluxo = int(df["Status"].isin(PROJECT_STATUS_OPTIONS[:4]).sum())

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        kpi_card("Projetos", str(len(df)), "Total no recorte atual.")
    with kpi2:
        kpi_card("Em fluxo", str(em_fluxo), "Ainda em execução ou preparação.")
    with kpi3:
        kpi_card("Orçamento", _format_currency(total_orcamento), "Valor total monitorado.")
    with kpi4:
        kpi_card("Prazos vencidos", str(prazo_vencido), "Projetos exigindo atenção.")

    chart_col_1, chart_col_2 = st.columns([1.25, 1])
    with chart_col_1:
        chart_card(
            "Projetos por etapa",
            "Colunas mostram gargalos do fluxo e concentração de iniciativas por estágio.",
        )
        fluxo = df["Status"].value_counts().reindex(PROJECT_STATUS_OPTIONS, fill_value=0).reset_index()
        fluxo.columns = ["Etapa", "Projetos"]
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
        render_plotly_chart(apply_executive_layout(fig_fluxo, height=370, showlegend=False))

    with chart_col_2:
        chart_card(
            "Composição do portfólio",
            "Pizza para leitura rápida do peso relativo de cada etapa.",
        )
        fig_status = go.Figure(
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
        render_plotly_chart(apply_executive_layout(fig_status, height=370))

    budget_col, trend_col = st.columns([1.25, 1])
    with budget_col:
        chart_card(
            "Orçamento por etapa",
            "Ranking horizontal mostra onde está alocado o investimento do portfólio.",
        )
        budget = df.groupby("Status", as_index=False)["orcamento_num"].sum()
        budget["Status"] = pd.Categorical(budget["Status"], categories=PROJECT_STATUS_OPTIONS, ordered=True)
        budget = budget.sort_values("orcamento_num", ascending=True)
        fig_budget = px.bar(
            budget,
            x="orcamento_num",
            y="Status",
            orientation="h",
            text="orcamento_num",
            color="Status",
            color_discrete_map=STATUS_COLORS,
        )
        fig_budget.update_traces(texttemplate="R$ %{x:,.0f}")
        style_horizontal_bar_traces(fig_budget)
        render_plotly_chart(apply_executive_layout(fig_budget, height=360, showlegend=False))

    with trend_col:
        chart_card(
            "Curva de entregas planejadas",
            "Tendência acumulada de projetos por prazo final.",
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

    section_card(
        "Portfólio de projetos",
        "Tabela reorganizada para destacar prazo, orçamento, responsável e estágio do projeto de forma mais clara.",
    )
    render_data_table(
        df[[column for column in ["id_projeto", "Projeto", "Responsável", "Prazo Final", "Orçamento", "Status"] if column in df.columns]].rename(columns={"id_projeto": "ID"}),
        column_config={
            "ID": st.column_config.NumberColumn(width="small"),
            "Projeto": st.column_config.TextColumn(width="large"),
            "Responsável": st.column_config.TextColumn(width="medium"),
            "Prazo Final": st.column_config.TextColumn(width="small"),
            "Orçamento": st.column_config.TextColumn(width="small"),
            "Status": st.column_config.TextColumn(width="small"),
        },
    )
else:
    st.info("Nenhum projeto encontrado para o filtro selecionado.")

with st.form("criar_projeto"):
    st.subheader("Criar Novo Projeto")
    nome = st.text_input("Nome do Projeto")
    responsavel = st.text_input("Responsável")
    prazo = st.date_input("Prazo Final")
    orcamento = st.number_input("Orçamento", min_value=0.0, step=0.01, format="%.2f")
    status = st.selectbox("Status", PROJECT_STATUS_OPTIONS)
    submitted = st.form_submit_button("Criar")

    if submitted:
        projeto = Projeto(
            nome_projeto=nome,
            responsavel=responsavel,
            prazo_final=str(prazo),
            orcamento=_to_float(orcamento),
            status=status,
        )
        ProjetoService.criar_projeto(projeto)
        st.success("Projeto criado com sucesso!")
        st.rerun()

legend_cols = st.columns(len(PROJECT_STATUS_OPTIONS))
for index, status_label in enumerate(PROJECT_STATUS_OPTIONS):
    with legend_cols[index]:
        st.markdown(
            f"""
            <div style="padding:0.85rem;border-radius:16px;background:{STATUS_COLORS[status_label]}14;border:1px solid {STATUS_COLORS[status_label]}33;">
                <div style="font-size:0.8rem;font-weight:700;color:{STATUS_COLORS[status_label]};text-transform:uppercase;">Fluxo</div>
                <div style="font-size:1rem;font-weight:800;color:#0f172a;">{status_label}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

if projetos:
    st.subheader("Editar ou Excluir Projeto")
    projeto_ids = [p["id_projeto"] for p in projetos]
    selected_id = st.selectbox("Selecionar Projeto", projeto_ids, key="edit")
    projeto = ProjetoService.obter_projeto(selected_id)

    if projeto:
        orcamento_atual = _to_float(projeto.orcamento)

        with st.form("editar_projeto"):
            nome = st.text_input("Nome", value=projeto.nome_projeto)
            responsavel = st.text_input("Responsável", value=projeto.responsavel)
            prazo = st.date_input("Prazo", value=pd.to_datetime(projeto.prazo_final))
            orcamento = st.number_input(
                "Orçamento",
                min_value=0.0,
                step=0.01,
                value=orcamento_atual,
                format="%.2f",
            )
            status = st.selectbox(
                "Status",
                PROJECT_STATUS_OPTIONS,
                index=PROJECT_STATUS_OPTIONS.index(normalize_project_status(projeto.status)),
            )
            col1, col2 = st.columns(2)

            with col1:
                update = st.form_submit_button("Atualizar")
            with col2:
                delete = st.form_submit_button("Excluir")

            if update:
                projeto.nome_projeto = nome
                projeto.responsavel = responsavel
                projeto.prazo_final = str(prazo)
                projeto.orcamento = _to_float(orcamento)
                projeto.status = status
                ProjetoService.atualizar_projeto(projeto)
                st.success("Projeto atualizado!")
                st.rerun()

            if delete:
                ProjetoService.excluir_projeto(selected_id)
                st.success("Projeto excluído!")
                st.rerun()
