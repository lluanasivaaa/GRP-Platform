from decimal import Decimal

import pandas as pd
import streamlit as st

from models.projeto import Projeto
from services.projeto_service import ProjetoService


def _to_float(value):
    if isinstance(value, Decimal):
        return float(value)
    if value is None:
        return 0.0
    return float(value)


st.title("Gestão de Projetos")
st.caption("Cadastre, acompanhe e atualize os projetos monitorados pelo GRP Platform.")

status_options = ["Todos", "Ativo", "Concluído", "Cancelado"]
filtro_status = st.selectbox("Filtrar por Status", status_options)

if filtro_status == "Todos":
    projetos = ProjetoService.listar_projetos()
else:
    projetos = ProjetoService.listar_projetos(filtro_status)

if projetos:
    df = pd.DataFrame(projetos)
    st.dataframe(df, use_container_width=True)
else:
    st.info("Nenhum projeto encontrado para o filtro selecionado.")

with st.form("criar_projeto"):
    st.subheader("Criar Novo Projeto")
    nome = st.text_input("Nome do Projeto")
    responsavel = st.text_input("Responsável")
    prazo = st.date_input("Prazo Final")
    orcamento = st.number_input("Orçamento", min_value=0.0, step=0.01, format="%.2f")
    status = st.selectbox("Status", ["Ativo", "Concluído", "Cancelado"])
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
                ["Ativo", "Concluído", "Cancelado"],
                index=["Ativo", "Concluído", "Cancelado"].index(projeto.status),
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
