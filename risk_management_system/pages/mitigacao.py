import pandas as pd
import streamlit as st

from models.mitigacao import Mitigacao
from services.mitigacao_service import MitigacaoService
from services.risco_service import RiscoService


STATUS_ACAO_OPTIONS = ["Pendente", "Em Andamento", "Concluída"]


st.title("Plano de Mitigação")
st.caption("Acompanhe ações corretivas e preventivas com responsáveis, prazos e status.")

riscos = RiscoService.listar_riscos()
risco_options = ["Todos"] + [f"{r['id_risco']} - {r['descricao'][:50]}" for r in riscos] if riscos else ["Todos"]
filtro_risco = st.selectbox("Filtrar por Risco", risco_options)

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
if mitigacoes:
    df = pd.DataFrame(mitigacoes)
    st.dataframe(df, width="stretch")
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
