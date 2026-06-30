import streamlit as st


def render_branding():
    st.markdown(
        """
        <style>
            .hero {
                padding: 1.5rem 1.75rem;
                border-radius: 16px;
                background: linear-gradient(135deg, #f5f7fa 0%, #e8eef5 100%);
                border: 1px solid #d9e2ec;
                margin-bottom: 1rem;
            }
            .hero-title {
                font-size: 2.1rem;
                font-weight: 750;
                margin-bottom: 0.25rem;
            }
            .hero-subtitle {
                font-size: 1rem;
                color: #4a5568;
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
                Search scanned legal records, review page-level OCR matches, open source PDFs,
                and view related GIS boundaries in Experience Builder.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.expander("About this prototype", expanded=False):
        st.markdown(
            """
            This prototype connects OCR text, document metadata, PDF links, and GIS boundary records
            into one searchable interface.

            Current capabilities include full-text OCR search, page-level results, PDF links,
            GIS map links, city/document filters, and internal review fields.
            """
        )