import streamlit as st


def render_branding():
    st.markdown(
        """
        <style>
        .hero {
            padding: 1.5rem 1.75rem;
            border-radius: 16px;
            background: rgba(120, 120, 120, 0.10);
            border: 1px solid rgba(120, 120, 120, 0.25);
            margin-bottom: 1rem;
        }
        .hero-title {
            font-size: 2.1rem;
            font-weight: 750;
            margin-bottom: 0.25rem;
        }
        .hero-subtitle {
            font-size: 1rem;
            opacity: 0.85;
            max-width: 900px;
        }
        mark {
            background-color: #fff3a3;
            padding: 0.05rem 0.15rem;
            border-radius: 4px;
        }
        </style>

        <div class="hero">
            <div class="hero-title">Legal Document & Boundary Records Portal</div>
            <div class="hero-subtitle">
                Search scanned legal records, review page-level OCR matches,
                open source PDFs, and view related GIS boundaries through
                integrated mapping tools.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.expander("About this prototype", expanded=False):
        st.markdown(
            """
            This prototype connects OCR text, document metadata, PDF retrieval,
            and GIS boundary records into one searchable system.

            Features include:

            - OCR full-text search
            - Page-level document matching
            - PDF retrieval
            - GIS map integration
            - Metadata filtering
            - Public and internal search modes
            """
        )