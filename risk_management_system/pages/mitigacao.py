import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from models.mitigacao import Mitigacao
from services.mitigacao_service import MitigacaoService
from services.risco_service import RiscoService
from utils.bi_charts import (
    EXECUTIVE_COLORS,
    STATUS_ACTION_COLORS,
    apply_executive_layout,
    apply_line_style,
    month_trend,
    style_bar_traces,
)
from utils.ui_components import chart_card, highlight_banner, inject_section_card_style, kpi_card, render_plotly_chart, section_card


STATUS_ACAO_OPTIONS = ["Pendente", "Em Andamento", "Concluída"]
STATUS_BADGES = {
    "Pendente": {"label": "Pendente", "icon": "Aguardando", "color": "#b45309", "bg": "#fef3c7"},
    "Em Andamento": {"label": "Em andamento", "icon": "Execução", "color": "#0f766e", "bg": "#ccfbf1"},
    "Concluída": {"label": "Concluída", "icon": "Finalizada", "color": "#166534", "bg": "#dcfce7"},
}


def _inject_mitigation_styles():
    st.markdown(
        """
        <style>
            .mitig-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
                gap: 0.95rem;
                margin-bottom: 1rem;
            }

            .mitig-card {
                position: relative;
                overflow: hidden;
                background: linear-gradient(180deg, rgba(255,255,255,0.96) 0%, rgba(248,250,252,0.96) 100%);
                border: 1px solid rgba(15, 23, 42, 0.08);
                border-radius: 8px;
                padding: 1.1rem 1.15rem;
                box-shadow: 0 18px 40px rgba(15, 23, 42, 0.08);
                min-height: 220px;
            }

            .mitig-card-top {
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                gap: 0.75rem;
                margin-bottom: 0.9rem;
            }

            .mitig-card-id {
                font-size: 0.78rem;
                font-weight: 800;
                letter-spacing: 0.05em;
                text-transform: uppercase;
                color: #64748b;
            }

            .mitig-card-risk {
                margin-top: 0.2rem;
                color: #0f172a;
                font-size: 1rem;
                font-weight: 800;
            }

            .mitig-status {
                display: inline-flex;
                align-items: center;
                gap: 0.4rem;
                padding: 0.42rem 0.78rem;
                border-radius: 999px;
                font-size: 0.8rem;
                font-weight: 800;
                white-space: nowrap;
            }

            .mitig-desc {
                margin: 0;
                color: #334155;
                font-size: 0.94rem;
                line-height: 1.55;
                min-height: 72px;
            }

            .mitig-meta {
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 0.7rem;
                margin-top: 1rem;
            }

            .mitig-meta-block {
                border-radius: 8px;
                padding: 0.8rem 0.9rem;
                background: rgba(248, 250, 252, 0.92);
                border: 1px solid rgba(148, 163, 184, 0.18);
            }

            .mitig-meta-label {
                margin: 0 0 0.28rem;
                font-size: 0.74rem;
                font-weight: 800;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                color: #64748b;
            }

            .mitig-meta-value {
                margin: 0;
                color: #0f172a;
                font-size: 0.95rem;
                font-weight: 700;
            }

            .mitig-empty {
                border-radius: 8px;
                padding: 1.2rem 1.25rem;
                background: rgba(255,255,255,0.72);
                border: 1px dashed rgba(148, 163, 184, 0.55);
                color: #475569;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _format_date(value):
    date_value = pd.to_datetime(value, errors="coerce")
    if pd.isna(date_value):
        return "Sem prazo"
    return date_value.strftime("%d/%m/%Y")


def _deadline_label(value):
    date_value = pd.to_datetime(value, errors="coerce")
    if pd.isna(date_value):
        return "Sem prazo"

    days_remaining = (date_value.normalize() - pd.Timestamp.today().normalize()).days
    if days_remaining < 0:
        return f"Atrasada há {abs(days_remaining)} dia(s)"
    if days_remaining == 0:
        return "Vence hoje"
    if days_remaining <= 7:
        return f"Vence em {days_remaining} dia(s)"
    return "Dentro do prazo"


def _prepare_mitigation_dataframe(mitigacoes, riscos):
    risk_lookup = {risco["id_risco"]: risco["descricao"] for risco in riscos}
    df = pd.DataFrame(mitigacoes).copy()
    df["risco"] = df["id_risco"].map(lambda risk_id: risk_lookup.get(risk_id, f"Risco {risk_id}"))
    df["prazo_data"] = pd.to_datetime(df["prazo"], errors="coerce")
    df["prazo_formatado"] = df["prazo"].apply(_format_date)
    df["situacao_prazo"] = df["prazo"].apply(_deadline_label)
    df["status_visual"] = df["status_acao"].map(
        lambda status: {
            "Pendente": "Aguardando",
            "Em Andamento": "Em andamento",
            "Concluída": "Concluída",
        }.get(status, status)
    )
    df = df.sort_values(by=["prazo_data", "status_acao"], na_position="last")
    return df


def _render_action_cards(df):
    cards = []
    for _, row in df.iterrows():
        badge = STATUS_BADGES.get(row["status_acao"], STATUS_BADGES["Pendente"])
        cards.append(
            f"""
            <div class="mitig-card">
                <div class="mitig-card-top">
                    <div>
                        <div class="mitig-card-id">Ação #{row["id_acao"]}</div>
                        <div class="mitig-card-risk">{row["risco"]}</div>
                    </div>
                    <div class="mitig-status" style="color:{badge["color"]}; background:{badge["bg"]};">
                        <span>{badge["icon"]}</span>
                        <span>{badge["label"]}</span>
                    </div>
                </div>
                <p class="mitig-desc">{row["descricao_acao"]}</p>
                <div class="mitig-meta">
                    <div class="mitig-meta-block">
                        <p class="mitig-meta-label">Responsável</p>
                        <p class="mitig-meta-value">{row["responsavel"] or "Não definido"}</p>
                    </div>
                    <div class="mitig-meta-block">
                        <p class="mitig-meta-label">Prazo</p>
                        <p class="mitig-meta-value">{row["prazo_formatado"]}</p>
                    </div>
                    <div class="mitig-meta-block">
                        <p class="mitig-meta-label">Situação</p>
                        <p class="mitig-meta-value">{row["situacao_prazo"]}</p>
                    </div>
                    <div class="mitig-meta-block">
                        <p class="mitig-meta-label">Risco Vinculado</p>
                        <p class="mitig-meta-value">#{row["id_risco"]}</p>
                    </div>
                </div>
            </div>
            """
        )

    if cards:
        st.markdown(f'<div class="mitig-grid">{"".join(cards)}</div>', unsafe_allow_html=True)
    else:
        st.markdown(
            '<div class="mitig-empty">Nenhuma ação disponível para exibir na visão executiva.</div>',
            unsafe_allow_html=True,
        )


inject_section_card_style()
_inject_mitigation_styles()

st.title("Plano de Mitigação")
st.caption("Organize ações preventivas e corretivas com uma leitura visual mais clara, profissional e operacional.")

riscos = RiscoService.listar_riscos()

highlight_banner(
    "Mitigação com foco em execução",
    "Visualize prioridades, responsáveis, prazos e andamento das ações em uma experiência mais refinada e fácil de acompanhar.",
)

filtro_col_1, filtro_col_2 = st.columns([1.3, 1])
with filtro_col_1:
    risco_options = ["Todos"] + [f"{r['id_risco']} - {r['descricao'][:50]}" for r in riscos] if riscos else ["Todos"]
    filtro_risco = st.selectbox("Filtrar por Risco", risco_options)

with filtro_col_2:
    status_options = ["Todos"] + STATUS_ACAO_OPTIONS
    filtro_status = st.selectbox("Filtrar por Status", status_options)

if filtro_risco == "Todos":
    id_risco = None
else:
    id_risco = int(filtro_risco.split(" - ")[0])

if filtro_status == "Todos":
    status_acao = None
else:
    status_acao = filtro_status

mitigacoes = MitigacaoService.listar_mitigacoes(id_risco, status_acao)
df_mitigacoes = _prepare_mitigation_dataframe(mitigacoes, riscos) if mitigacoes else pd.DataFrame()

if not df_mitigacoes.empty:
    total_acoes = len(df_mitigacoes)
    pendentes = int((df_mitigacoes["status_acao"] == "Pendente").sum())
    em_andamento = int((df_mitigacoes["status_acao"] == "Em Andamento").sum())
    concluidas = int((df_mitigacoes["status_acao"] == "Concluída").sum())
    atrasadas = int(df_mitigacoes["situacao_prazo"].str.contains("Atrasada", na=False).sum())

    kpi_1, kpi_2, kpi_3, kpi_4 = st.columns(4)
    with kpi_1:
        kpi_card("Ações abertas", str(total_acoes), "Volume total filtrado na visão atual.")
    with kpi_2:
        kpi_card("Pendentes", str(pendentes), "Demandas aguardando início ou definição.")
    with kpi_3:
        kpi_card("Em execução", str(em_andamento), "Ações já em andamento pelo time.")
    with kpi_4:
        kpi_card("Atrasadas", str(atrasadas), "Itens que exigem atenção imediata.")

    chart_left, chart_right = st.columns([1.25, 1])
    with chart_left:
        chart_card(
            "Andamento das ações",
            "Colunas executivas mostram a maturidade do plano de mitigação.",
        )
        status_counts = df_mitigacoes["status_acao"].value_counts().reset_index()
        status_counts.columns = ["Status", "Ações"]
        fig_status = px.bar(
            status_counts,
            x="Status",
            y="Ações",
            text="Ações",
            color="Status",
            color_discrete_map=STATUS_ACTION_COLORS,
        )
        style_bar_traces(fig_status)
        render_plotly_chart(apply_executive_layout(fig_status, height=350))

    with chart_right:
        chart_card(
            "Composição da execução",
            "Pizza para leitura rápida do esforço pendente, em andamento e concluído.",
        )
        fig_pie = go.Figure(
            data=[
                go.Pie(
                    labels=status_counts["Status"],
                    values=status_counts["Ações"],
                    hole=0.55,
                    marker=dict(colors=[STATUS_ACTION_COLORS.get(label, EXECUTIVE_COLORS["slate"]) for label in status_counts["Status"]]),
                    textinfo="percent",
                    hovertemplate="<b>%{label}</b><br>%{value} ação(ões)<extra></extra>",
                )
            ]
        )
        render_plotly_chart(apply_executive_layout(fig_pie, height=350))

    chart_card(
        "Curva de tendência por prazo",
        "Linha acumulada antecipa concentração de vencimentos e risco de sobrecarga operacional.",
    )
    trend = month_trend(df_mitigacoes, "prazo_data", "Ações")
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
        marker_color="rgba(15,118,110,0.20)",
    )
    apply_line_style(fig_trend)
    render_plotly_chart(apply_executive_layout(fig_trend, height=350))

    overview_col, summary_col = st.columns([1.55, 1])
    with overview_col:
        section_card(
            "Painel Executivo",
            "Cartões com status, responsáveis e situação de prazo para facilitar leitura rápida sem perder o contexto da ação.",
        )
        _render_action_cards(df_mitigacoes)

    with summary_col:
        section_card(
            "Leitura da Operação",
            "Acompanhe a maturidade da execução e identifique rapidamente onde há acúmulo, atraso ou boas entregas concluídas.",
        )
        st.markdown(
            f"""
            <div class="grp-section-card">
                <h3>Status consolidado</h3>
                <p><strong>{pendentes}</strong> ação(ões) pendente(s).</p>
                <p><strong>{em_andamento}</strong> ação(ões) em andamento.</p>
                <p><strong>{concluidas}</strong> ação(ões) concluída(s).</p>
                <p><strong>{atrasadas}</strong> item(ns) com prazo vencido.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.subheader("Tabela detalhada")
    st.dataframe(
        df_mitigacoes[
            [
                "id_acao",
                "risco",
                "descricao_acao",
                "responsavel",
                "prazo_formatado",
                "situacao_prazo",
                "status_visual",
            ]
        ].rename(
            columns={
                "id_acao": "Ação",
                "risco": "Risco",
                "descricao_acao": "Descrição da Ação",
                "responsavel": "Responsável",
                "prazo_formatado": "Prazo",
                "situacao_prazo": "Situação do Prazo",
                "status_visual": "Status",
            }
        ),
        width="stretch",
        hide_index=True,
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
    st.info("Nenhuma ação de mitigação encontrada para os filtros aplicados.")

with st.form("criar_mitigacao"):
    st.subheader("Criar Nova Ação de Mitigação")
    if riscos:
        risco_desc = st.selectbox("Risco", [f"{r['id_risco']} - {r['descricao'][:50]}" for r in riscos])
        id_risc = int(risco_desc.split(" - ")[0])
    else:
        st.error("Nenhum risco cadastrado.")
        id_risc = None

    descricao_acao = st.text_area("Descrição da Ação")
    responsavel = st.text_input("Responsável")
    prazo = st.date_input("Prazo")
    status_acao = st.selectbox("Status", STATUS_ACAO_OPTIONS)
    submitted = st.form_submit_button("Criar")

    if submitted and id_risc:
        mitigacao = Mitigacao(
            id_risco=id_risc,
            descricao_acao=descricao_acao,
            responsavel=responsavel,
            prazo=str(prazo),
            status_acao=status_acao,
        )
        MitigacaoService.criar_mitigacao(mitigacao)
        st.success("Ação de mitigação criada com sucesso!")
        st.rerun()

if mitigacoes:
    st.subheader("Editar ou Excluir Ação de Mitigação")
    acao_ids = [m["id_acao"] for m in mitigacoes]
    selected_id = st.selectbox("Selecionar Ação", acao_ids, key="edit")
    mitigacao = MitigacaoService.obter_mitigacao(selected_id)

    if mitigacao:
        with st.form("editar_mitigacao"):
            risco_labels = [f"{r['id_risco']} - {r['descricao'][:50]}" for r in riscos]
            risco_atual = next(
                (f"{r['id_risco']} - {r['descricao'][:50]}" for r in riscos if r["id_risco"] == mitigacao.id_risco),
                "",
            )
            risco_desc = st.selectbox(
                "Risco",
                risco_labels,
                index=risco_labels.index(risco_atual) if risco_atual in risco_labels else 0,
            )
            id_risc = int(risco_desc.split(" - ")[0])
            descricao_acao = st.text_area("Descrição", value=mitigacao.descricao_acao)
            responsavel = st.text_input("Responsável", value=mitigacao.responsavel)
            prazo_atual = pd.to_datetime(mitigacao.prazo, errors="coerce")
            if pd.isna(prazo_atual):
                prazo_atual = pd.Timestamp.today()
            status_atual = mitigacao.status_acao if mitigacao.status_acao in STATUS_ACAO_OPTIONS else STATUS_ACAO_OPTIONS[0]
            prazo = st.date_input("Prazo", value=prazo_atual)
            status_acao = st.selectbox(
                "Status",
                STATUS_ACAO_OPTIONS,
                index=STATUS_ACAO_OPTIONS.index(status_atual),
            )
            col1, col2 = st.columns(2)

            with col1:
                update = st.form_submit_button("Atualizar")
            with col2:
                delete = st.form_submit_button("Excluir")

            if update:
                mitigacao.id_risco = id_risc
                mitigacao.descricao_acao = descricao_acao
                mitigacao.responsavel = responsavel
                mitigacao.prazo = str(prazo)
                mitigacao.status_acao = status_acao
                MitigacaoService.atualizar_mitigacao(mitigacao)
                st.success("Ação atualizada!")
                st.rerun()

            if delete:
                MitigacaoService.excluir_mitigacao(selected_id)
                st.success("Ação excluída!")
                st.rerun()
