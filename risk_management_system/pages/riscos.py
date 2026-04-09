import pandas as pd
import streamlit as st

from models.risco import Risco
from services.projeto_service import ProjetoService
from services.risco_service import RiscoService


st.title("Gestão de Riscos")
st.caption("Mapeie eventos, acompanhe criticidade e mantenha a resposta aos riscos organizada.")

projetos = ProjetoService.listar_projetos()
projeto_options = ["Todos"] + [p["nome_projeto"] for p in projetos] if projetos else ["Todos"]
filtro_projeto = st.selectbox("Filtrar por Projeto", projeto_options)

status_options = ["Todos", "Ativo", "Mitigado", "Resolvido"]
filtro_status = st.selectbox("Filtrar por Status", status_options)

if filtro_projeto == "Todos":
    id_projeto = None
else:
    id_projeto = next((p["id_projeto"] for p in projetos if p["nome_projeto"] == filtro_projeto), None)

if filtro_status == "Todos":
    status_risco = None
else:
    status_risco = filtro_status

riscos = RiscoService.listar_riscos(id_projeto, status_risco)
if riscos:
    df = pd.DataFrame(riscos)
    st.dataframe(df, use_container_width=True)
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
    probabilidade = st.selectbox("Probabilidade", ["Baixa", "Média", "Alta"])
    impacto = st.selectbox("Impacto", ["Baixo", "Médio", "Alto"])
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
                ["Baixa", "Média", "Alta"],
                index=["Baixa", "Média", "Alta"].index(risco.probabilidade),
            )
            impacto = st.selectbox(
                "Impacto",
                ["Baixo", "Médio", "Alto"],
                index=["Baixo", "Médio", "Alto"].index(risco.impacto),
            )
            status_risco = st.selectbox(
                "Status",
                ["Ativo", "Mitigado", "Resolvido"],
                index=["Ativo", "Mitigado", "Resolvido"].index(risco.status_risco),
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
