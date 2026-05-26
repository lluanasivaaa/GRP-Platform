from pathlib import Path
import runpy

import streamlit as st


APP_TITLE = "GRP Platform"
APP_SUBTITLE = "Governance & Risk Platform"


st.set_page_config(
    page_title=f"{APP_TITLE} | {APP_SUBTITLE}",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        :root {
            --grp-ink: #0f172a;
            --grp-muted: #475569;
            --grp-green: #166534;
            --grp-teal: #0f766e;
        }
        [data-testid="stSidebarNav"] { display: none; }
        .stApp {
            background: linear-gradient(180deg, #f4f8f4 0%, #edf3ee 100%);
        }
        .grp-hero {
            padding: 1.5rem 1.75rem;
            border-radius: 8px;
            color: #f8fafc;
            background: linear-gradient(135deg, #0f172a 0%, #16322a 52%, #166534 100%);
            box-shadow: 0 18px 45px rgba(15, 23, 42, 0.18);
            margin-bottom: 1.2rem;
        }
        .grp-hero h1 {
            margin: 0;
            font-size: 2.15rem;
            font-weight: 800;
            letter-spacing: 0;
        }
        .grp-hero p {
            margin: 0.35rem 0 0;
            font-size: 1rem;
            color: rgba(248, 250, 252, 0.88);
        }
        .grp-tag {
            display: inline-block;
            padding: 0.35rem 0.75rem;
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.14);
            font-size: 0.85rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            margin-bottom: 0.8rem;
        }
        .grp-panel {
            background: rgba(255, 255, 255, 0.82);
            border: 1px solid rgba(15, 23, 42, 0.08);
            border-radius: 8px;
            padding: 1rem 1.1rem;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
            backdrop-filter: blur(8px);
        }
        .grp-panel h3 { margin: 0 0 0.35rem; color: #0f172a; }
        .grp-panel p { margin: 0; color: #475569; }
        [data-testid="stSidebar"] { background: linear-gradient(180deg, #0f172a 0%, #142c24 100%); }
        [data-testid="stSidebar"] * { color: #f8fafc; }
        [data-testid="stSidebar"] .stRadio [role="radiogroup"] > label {
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 8px;
            padding: 0.7rem 0.85rem;
            background: rgba(255, 255, 255, 0.06);
            transition: 0.2s ease;
        }
        [data-testid="stSidebar"] .stRadio [role="radiogroup"] > label:hover {
            background: rgba(255, 255, 255, 0.12);
            border-color: rgba(255, 255, 255, 0.20);
        }
        [data-testid="stSidebar"] .stRadio [role="radiogroup"] > label:has(input:checked) {
            background: linear-gradient(135deg, rgba(22, 101, 52, 0.95), rgba(15, 118, 110, 0.95));
            border-color: rgba(255, 255, 255, 0.20);
            box-shadow: 0 12px 25px rgba(0, 0, 0, 0.18);
        }
        [data-testid="stMetric"], .stDataFrame, div[data-testid="stTable"] {
            background: rgba(255, 255, 255, 0.78);
            border-radius: 8px;
            border: 1px solid rgba(15, 23, 42, 0.08);
            overflow: hidden;
            box-shadow: 0 16px 38px rgba(15, 23, 42, 0.08);
            backdrop-filter: blur(10px);
        }
        .stDataFrame [data-testid="stDataFrameResizable"] {
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid rgba(148, 163, 184, 0.18);
            background: linear-gradient(180deg, rgba(255,255,255,0.98) 0%, rgba(248,250,252,0.94) 100%);
        }
        .stDataFrame [data-testid="stDataFrameGlideDataEditor"] {
            border-radius: 8px;
        }
        .stDataFrame [data-testid="stDataFrameGlideDataEditor"] [role="grid"] {
            background: transparent !important;
        }
        .stDataFrame [data-testid="stDataFrameGlideDataEditor"] [role="columnheader"] {
            background: linear-gradient(180deg, #f8fafc 0%, #eef5f0 100%) !important;
            color: #0f172a !important;
            font-weight: 800 !important;
            border-bottom: 1px solid rgba(148, 163, 184, 0.22) !important;
        }
        .stDataFrame [data-testid="stDataFrameGlideDataEditor"] [role="gridcell"] {
            background: rgba(255, 255, 255, 0.96) !important;
            color: #1e293b !important;
            border-bottom: 1px solid rgba(226, 232, 240, 0.72) !important;
        }
        .stDataFrame [data-testid="stDataFrameGlideDataEditor"] [role="row"]:hover [role="gridcell"] {
            background: #f5fbf7 !important;
        }
        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div,
        div[data-baseweb="textarea"] > div,
        .stDateInput > div,
        .stNumberInput > div { border-radius: 8px !important; }
        .stButton > button, .stDownloadButton > button, .stFormSubmitButton > button {
            border-radius: 8px;
            border: 0;
            background: linear-gradient(135deg, #166534 0%, #0f766e 100%);
            color: #ffffff;
            font-weight: 700;
            box-shadow: 0 10px 20px rgba(22, 101, 52, 0.20);
        }
        .stTabs [data-baseweb="tab-list"] { gap: 0.55rem; }
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.72);
            border: 1px solid rgba(15, 23, 42, 0.08);
            padding: 0.55rem 1rem;
            font-weight: 700;
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #166534 0%, #0f766e 100%) !important;
            color: #ffffff !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="grp-hero">
        <div class="grp-tag">GRP Platform</div>
        <h1>{APP_TITLE}</h1>
        <p>{APP_SUBTITLE}</p>
        <p>Central de governança, análise de riscos, projetos, mitigação e relatórios executivos.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown("## GRP Platform")
st.sidebar.caption("Governance & Risk Platform")
st.sidebar.markdown("---")

page_options = {
    "📊 Dashboard": "dashboard.py",
    "📁 Projetos": "projetos.py",
    "🧩 Kanban": "kanban.py",
    "⚠️ Riscos": "riscos.py",
    "🛡️ Mitigação": "mitigacao.py",
    "📈 Relatórios": "relatorios.py",
}

selected_page = st.sidebar.radio("Navegação", list(page_options.keys()), index=0)

st.sidebar.markdown(
    """
    <div class="grp-panel">
        <h3>Visão Integrada</h3>
        <p>Acompanhe operações, decisões e exposição ao risco em um único ambiente.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

page_path = Path(__file__).parent / "pages" / page_options[selected_page]
runpy.run_path(str(page_path), run_name="__main__")
