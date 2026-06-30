import streamlit as st
from utils.helpers import clean_value
from services.document_service import (
    get_document_detail,
    get_document_pages
)


def render_document_detail():

    if "selected_document_id" not in st.session_state:
        return

    st.divider()
    st.subheader("Selected Document Detail")

    selected_document_id = st.session_state["selected_document_id"]
    selected_page_number = st.session_state.get("selected_page_number")

    document = get_document_detail(selected_document_id)

    if not document:
        st.warning("Could not load document.")
        return

    left, right = st.columns([2, 1])

    with left:
        st.markdown(
            f"### {clean_value(document.get('document_title') or document.get('folder_name'))}"
        )

        st.write(f"**Document ID:** {clean_value(document.get('id'))}")
        st.write(f"**City:** {clean_value(document.get('city'))}")
        st.write(f"**District:** {clean_value(document.get('district'))}")
        st.write(f"**Document type:** {clean_value(document.get('document_type'))}")
        st.write(f"**Document date:** {clean_value(document.get('document_date'))}")
        st.write(f"**Recorded date:** {clean_value(document.get('recorded_date'))}")
        st.write(f"**Ordinance no.:** {clean_value(document.get('ordinance_no'))}")
        st.write(f"**Resolution no.:** {clean_value(document.get('resolution_no'))}")
        st.write(f"**Index no.:** {clean_value(document.get('index_no'))}")

    with right:
        st.write(f"**Review status:** {clean_value(document.get('review_status'))}")
        st.write(f"**Visibility:** {clean_value(document.get('visibility'))}")
        st.write(f"**Public:** {clean_value(document.get('is_public'))}")

        pdf_url = document.get("original_pdf_path") or document.get("public_pdf_url")
        exb_url = document.get("exb_url")

        button_col1, button_col2 = st.columns(2)

        with button_col1:
            if pdf_url:
                st.link_button("Open PDF", pdf_url)
            else:
                st.caption("No PDF")

        with button_col2:
            if exb_url:
                st.link_button("Open Map", exb_url)
            else:
                st.caption("No Map")

        with st.expander("Stored links / paths"):
            st.write("**PDF URL / path**")
            st.code(clean_value(pdf_url))

            st.write("**Experience Builder URL**")
            st.code(clean_value(exb_url))

    pages = get_document_pages(selected_document_id)

    if not pages:
        st.info("No page records found.")
        return

    st.divider()
    st.subheader("Page Viewer")

    page_numbers = [page["page_number"] for page in pages]

    default_index = 0

    if selected_page_number in page_numbers:
        default_index = page_numbers.index(selected_page_number)

    chosen_page_number = st.selectbox(
        "Select page",
        page_numbers,
        index=default_index
    )

    page = next(
        p for p in pages
        if p["page_number"] == chosen_page_number
    )

    st.write(f"**Page:** {chosen_page_number}")

    if page.get("page_image_path"):
        st.write("**Page image path:**")
        st.code(page.get("page_image_path"))

    st.text_area(
        "Page text",
        page.get("page_text") or "",
        height=500
    )