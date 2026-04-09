import streamlit as st


def inject_section_card_style():
    st.markdown(
        """
        <style>
            .grp-section-card {
                background: rgba(255, 255, 255, 0.84);
                border: 1px solid rgba(15, 23, 42, 0.08);
                border-radius: 22px;
                padding: 1.1rem 1.15rem;
                box-shadow: 0 16px 35px rgba(15, 23, 42, 0.06);
                backdrop-filter: blur(8px);
                margin-bottom: 1rem;
            }

            .grp-section-card h3 {
                margin: 0;
                font-size: 1.05rem;
                color: #0f172a;
            }

            .grp-section-card p {
                margin: 0.4rem 0 0;
                color: #475569;
                font-size: 0.94rem;
            }

            .grp-kpi {
                position: relative;
                overflow: hidden;
                padding: 1.1rem 1.15rem;
                border-radius: 22px;
                background: linear-gradient(145deg, #ffffff 0%, #f8fbf8 100%);
                border: 1px solid rgba(22, 101, 52, 0.10);
                box-shadow: 0 16px 40px rgba(15, 23, 42, 0.08);
                min-height: 142px;
            }

            .grp-kpi::after {
                content: "";
                position: absolute;
                inset: auto -30px -40px auto;
                width: 120px;
                height: 120px;
                border-radius: 50%;
                background: radial-gradient(circle, rgba(22, 163, 74, 0.18), transparent 68%);
            }

            .grp-kpi-label {
                font-size: 0.82rem;
                font-weight: 700;
                letter-spacing: 0.05em;
                text-transform: uppercase;
                color: #166534;
                margin-bottom: 0.45rem;
            }

            .grp-kpi-value {
                font-size: 2.15rem;
                line-height: 1;
                font-weight: 800;
                color: #0f172a;
                margin-bottom: 0.45rem;
            }

            .grp-kpi-meta {
                color: #475569;
                font-size: 0.92rem;
            }

            .grp-highlight {
                border-radius: 24px;
                padding: 1.35rem;
                color: #f8fafc;
                background: linear-gradient(135deg, #0f172a 0%, #16322a 45%, #166534 100%);
                box-shadow: 0 18px 45px rgba(15, 23, 42, 0.16);
                margin-bottom: 1rem;
            }

            .grp-highlight h2 {
                margin: 0 0 0.35rem;
                font-size: 1.55rem;
            }

            .grp-highlight p {
                margin: 0;
                color: rgba(248, 250, 252, 0.86);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def section_card(title: str, description: str):
    st.markdown(
        f"""
        <div class="grp-section-card">
            <h3>{title}</h3>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: str, meta: str):
    st.markdown(
        f"""
        <div class="grp-kpi">
            <div class="grp-kpi-label">{label}</div>
            <div class="grp-kpi-value">{value}</div>
            <div class="grp-kpi-meta">{meta}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def highlight_banner(title: str, description: str):
    st.markdown(
        f"""
        <div class="grp-highlight">
            <h2>{title}</h2>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
