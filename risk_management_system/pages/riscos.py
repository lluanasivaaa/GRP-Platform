import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from models.risco import Risco
from services.projeto_service import ProjetoService
from services.risco_service import RiscoService
from utils.bi_charts import (
    EXECUTIVE_COLORS,
    RISK_LEVEL_COLORS,
    STATUS_RISK_COLORS,
    apply_executive_layout,
    style_bar_traces,
    style_horizontal_bar_traces,
)
from utils.calculo_risco import (
    IMPACT_LEVELS,
    PROBABILITY_LEVELS,
    calcular_score_risco,
    normalizar_impacto,
    normalizar_probabilidade,
)
from utils.ui_components import chart_card, inject_section_card_style, kpi_card, render_data_table, render_plotly_chart, section_card


def _risk_dataframe(riscos, projetos):
    df = pd.DataFrame(riscos) if riscos else pd.DataFrame()
    if df.empty:
        return df

    projeto_lookup = {projeto["id_projeto"]: projeto["nome_projeto"] for projeto in projetos} if projetos else {}
    df["Projeto"] = df["id_projeto"].map(lambda value: projeto_lookup.get(value, f"Projeto {value}"))
    df["Categoria"] = df["categoria"]
    df["Probabilidade"] = df["probabilidade"].map(normalizar_probabilidade)
    df["Impacto"] = df["impacto"].map(normalizar_impacto)
    df["Score"] = df.apply(lambda row: calcular_score_risco(row["Probabilidade"], row["Impacto"]), axis=1)
    df["Criticidade"] = df["Score"].map(lambda score: "Baixo" if score <= 2 else "Médio" if score <= 4 else "Alto")
    return df


def _risk_table(df):
    table = df.copy()
    table["Risco"] = table["id_risco"]
    table["Descrição"] = table["descricao"]
    table["Categoria"] = table["categoria"]
    table["Status"] = table["status_risco"]
    return table[["Risco", "Projeto", "Descrição", "Categoria", "Probabilidade", "Impacto", "Criticidade", "Status"]]


inject_section_card_style()

st.title("Gestão de Riscos")
st.caption("Análise executiva dos riscos por severidade, categoria e status de resposta.")

projetos = ProjetoService.listar_projetos() or []
projeto_options = ["Todos"] + [p["nome_projeto"] for p in projetos] if projetos else ["Todos"]
filtro_projeto = st.selectbox("Filtrar por Projeto", projeto_options)

status_options = ["Todos", "Ativo", "Mitigado", "Resolvido"]
filtro_status = st.selectbox("Filtrar por Status", status_options)

id_projeto = None if filtro_projeto == "Todos" else next(
    (p["id_projeto"] for p in projetos if p["nome_projeto"] == filtro_projeto),
    None,
)
status_risco = None if filtro_status == "Todos" else filtro_status

riscos = RiscoService.listar_riscos(id_projeto, status_risco) or []
df_riscos = _risk_dataframe(riscos, projetos)

if not df_riscos.empty:
    total_riscos = len(df_riscos)
    total_altos = int((df_riscos["Criticidade"] == "Alto").sum())
    score_medio = df_riscos["Score"].mean()
    taxa_resolvidos = (df_riscos["status_risco"].eq("Resolvido").sum() / total_riscos * 100) if total_riscos else 0

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        kpi_card("Riscos no recorte", str(total_riscos), "Total após filtros aplicados.")
    with kpi2:
        kpi_card("Alta criticidade", str(total_altos), "Prioridade executiva imediata.")
    with kpi3:
        kpi_card("Score médio", f"{score_medio:.1f}", "Intensidade média da exposição.")
    with kpi4:
        kpi_card("Resolvidos", f"{taxa_resolvidos:.1f}%", "Efetividade da resposta.")

    left, right = st.columns([1.35, 1])
    with left:
        chart_card(
            "Riscos por probabilidade e impacto",
            "Colunas empilhadas mostram como a exposição se distribui por probabilidade e impacto.",
        )
        grouped = (
            df_riscos.groupby(["Probabilidade", "Impacto"])
            .size()
            .reset_index(name="Riscos")
        )
        fig_prob_impact = px.bar(
            grouped,
            x="Probabilidade",
            y="Riscos",
            color="Impacto",
            text="Riscos",
            barmode="stack",
            category_orders={"Probabilidade": PROBABILITY_LEVELS, "Impacto": IMPACT_LEVELS},
            color_discrete_map={"Baixo": "#16a34a", "Médio": "#f59e0b", "Alto": "#dc2626"},
        )
        style_bar_traces(fig_prob_impact)
        render_plotly_chart(apply_executive_layout(fig_prob_impact, height=390))

    with right:
        chart_card(
            "Composição por criticidade",
            "Pizza executiva para visualizar o peso relativo de baixa, média e alta exposição.",
        )
        severity = df_riscos["Criticidade"].value_counts().reindex(["Baixo", "Médio", "Alto"], fill_value=0).reset_index()
        severity.columns = ["Criticidade", "Riscos"]
        fig_severity = go.Figure(
            data=[
                go.Pie(
                    labels=severity["Criticidade"],
                    values=severity["Riscos"],
                    hole=0.52,
                    marker=dict(colors=[RISK_LEVEL_COLORS[label] for label in severity["Criticidade"]]),
                    textinfo="label+percent",
                    hovertemplate="<b>%{label}</b><br>%{value} risco(s)<extra></extra>",
                    sort=False,
                )
            ]
        )
        render_plotly_chart(apply_executive_layout(fig_severity, height=390))

    bottom_left, bottom_right = st.columns([1.25, 1.1])
    with bottom_left:
        chart_card(
            "Categorias com maior pressão",
            "Ranking horizontal destaca temas que merecem decisão, investimento ou mitigação estruturada.",
        )
        categories = (
            df_riscos.groupby("Categoria")
            .agg(Riscos=("id_risco", "count"), Score=("Score", "sum"))
            .reset_index()
            .sort_values("Score", ascending=False)
            .head(10)
        )
        fig_categories = px.bar(
            categories.sort_values("Score", ascending=True),
            x="Score",
            y="Categoria",
            orientation="h",
            text="Riscos",
            color="Score",
            color_continuous_scale=["#dbeafe", "#f59e0b", "#dc2626"],
        )
        fig_categories.update_coloraxes(showscale=False)
        style_horizontal_bar_traces(fig_categories)
        render_plotly_chart(apply_executive_layout(fig_categories, height=390, showlegend=False))

    with bottom_right:
        chart_card(
            "Status da resposta",
            "Donut para acompanhar rapidamente o volume aberto, mitigado e resolvido.",
        )
        status = df_riscos["status_risco"].value_counts().reset_index()
        status.columns = ["Status", "Riscos"]
        fig_status = go.Figure(
            data=[
                go.Pie(
                    labels=status["Status"],
                    values=status["Riscos"],
                    hole=0.62,
                    marker=dict(colors=[STATUS_RISK_COLORS.get(label, EXECUTIVE_COLORS["slate"]) for label in status["Status"]]),
                    textinfo="percent",
                    hovertemplate="<b>%{label}</b><br>%{value} risco(s)<extra></extra>",
                )
            ]
        )
        render_plotly_chart(apply_executive_layout(fig_status, height=390))

    render_data_table(
        _risk_table(df_riscos),
        title="Tabela executiva de riscos",
        description="Base detalhada para conferir os dados por trás dos gráficos.",
        column_config={
            "Risco": st.column_config.NumberColumn(width="small"),
            "Projeto": st.column_config.TextColumn(width="medium"),
            "Descrição": st.column_config.TextColumn(width="large"),
            "Categoria": st.column_config.TextColumn(width="medium"),
            "Probabilidade": st.column_config.TextColumn(width="small"),
            "Impacto": st.column_config.TextColumn(width="small"),
            "Criticidade": st.column_config.TextColumn(width="small"),
            "Status": st.column_config.TextColumn(width="small"),
        },
    )
else:
    st.info("Nenhum risco encontrado para os filtros aplicados.")

with st.form("criar_risco"):
    st.subheader("Criar Novo Risco")
    if projetos:
        projeto_nome = st.selectbox("Projeto", [p["nome_projeto"] for p in projetos])
        id_proj = next(p["id_projeto"] for p in projetos if p["nome_projeto"] == projeto_nome)
    else:
        st.error("Nenhum projeto cadastrado.")
        id_proj = None

    descricao = st.text_area("Descrição")
    categoria = st.text_input("Categoria")
    probabilidade = st.selectbox("Probabilidade", PROBABILITY_LEVELS)
    impacto = st.selectbox("Impacto", IMPACT_LEVELS)
    status_risco = st.selectbox("Status", ["Ativo", "Mitigado", "Resolvido"])
    submitted = st.form_submit_button("Criar")

    if submitted and id_proj:
        risco = Risco(
            id_projeto=id_proj,
            descricao=descricao,
            categoria=categoria,
            probabilidade=probabilidade,
            impacto=impacto,
            status_risco=status_risco,
        )
        RiscoService.criar_risco(risco)
        st.success("Risco criado com sucesso!")
        st.rerun()

if riscos:
    st.subheader("Editar ou Excluir Risco")
    risco_ids = [r["id_risco"] for r in riscos]
    selected_id = st.selectbox("Selecionar Risco", risco_ids, key="edit")
    risco = RiscoService.obter_risco(selected_id)

    if risco:
        with st.form("editar_risco"):
            nomes_projetos = [p["nome_projeto"] for p in projetos]
            projeto_atual = next((p["nome_projeto"] for p in projetos if p["id_projeto"] == risco.id_projeto), "")
            projeto_nome = st.selectbox(
                "Projeto",
                nomes_projetos,
                index=nomes_projetos.index(projeto_atual) if projeto_atual in nomes_projetos else 0,
            )
            id_proj = next(p["id_projeto"] for p in projetos if p["nome_projeto"] == projeto_nome)
            descricao = st.text_area("Descrição", value=risco.descricao)
            categoria = st.text_input("Categoria", value=risco.categoria)
            probabilidade = st.selectbox(
                "Probabilidade",
                PROBABILITY_LEVELS,
                index=PROBABILITY_LEVELS.index(normalizar_probabilidade(risco.probabilidade)),
            )
            impacto = st.selectbox(
                "Impacto",
                IMPACT_LEVELS,
                index=IMPACT_LEVELS.index(normalizar_impacto(risco.impacto)),
            )
            status_atual = risco.status_risco if risco.status_risco in ["Ativo", "Mitigado", "Resolvido"] else "Ativo"
            status_risco = st.selectbox(
                "Status",
                ["Ativo", "Mitigado", "Resolvido"],
                index=["Ativo", "Mitigado", "Resolvido"].index(status_atual),
            )
            col1, col2 = st.columns(2)

            with col1:
                update = st.form_submit_button("Atualizar")
            with col2:
                delete = st.form_submit_button("Excluir")

            if update:
                risco.id_projeto = id_proj
                risco.descricao = descricao
                risco.categoria = categoria
                risco.probabilidade = probabilidade
                risco.impacto = impacto
                risco.status_risco = status_risco
                RiscoService.atualizar_risco(risco)
                st.success("Risco atualizado!")
                st.rerun()

            if delete:
                RiscoService.excluir_risco(selected_id)
                st.success("Risco excluído!")
                st.rerun()
