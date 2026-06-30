import pandas as pd
import streamlit as st
from utils.helpers import clean_value


def render_metrics(results, city_count=None):
    unique_docs = len({
        row.get("document_id")
        for row in results
        if row.get("document_id") is not None
    })

    page_hits = len(results)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Matching documents", unique_docs)

    with col2:
        st.metric("Matching pages", page_hits)

    with col3:
        st.metric("Cities in filter list", city_count if city_count is not None else "—")


def render_results_table(results):
    df = pd.DataFrame(results)

    display_columns = [
        "document_id",
        "document_title",
        "folder_name",
        "city",
        "document_type",
        "document_date",
        "ordinance_no",
        "resolution_no",
        "recorded_date",
        "page_number",
        "rank"
    ]

    existing_columns = [
        col for col in display_columns
        if col in df.columns
    ]

    st.dataframe(
        df[existing_columns],
        width="stretch",
        hide_index=True
    )


def render_search_results(results, public_demo_mode=False):
    st.divider()
    st.subheader("Search Results")

    for row in results:
        title = row.get("document_title") or row.get("folder_name") or "Untitled Document"
        page_number = row.get("page_number")
        document_id = row.get("document_id")

        with st.expander(
            f"{title} — Page {page_number}",
            expanded=False
        ):
            st.markdown(f"### {title}")

            meta_col1, meta_col2, meta_col3 = st.columns(3)

            with meta_col1:
                st.write(f"**City:** {clean_value(row.get('city'))}")

            with meta_col2:
                st.write(f"**Type:** {clean_value(row.get('document_type'))}")

            with meta_col3:
                st.write(f"**Matched page:** {clean_value(page_number)}")

            st.write(f"**Ordinance:** {clean_value(row.get('ordinance_no'))}")
            st.write(f"**Resolution:** {clean_value(row.get('resolution_no'))}")
            st.write(f"**Recorded date:** {clean_value(row.get('recorded_date'))}")

            snippet = row.get("snippet") or ""

            if snippet:
                st.markdown(snippet, unsafe_allow_html=True)

            pdf_url = row.get("original_pdf_path")
            exb_url = row.get("exb_url")

            button_col1, button_col2, button_col3 = st.columns(3)

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

            with button_col3:
                if st.button(
                    "Open details",
                    key=f"detail_{document_id}_{page_number}"
                ):
                    st.session_state["selected_document_id"] = document_id
                    st.session_state["selected_page_number"] = page_number
                    st.rerun()

            if not public_demo_mode:
                rank = row.get("rank")
                with st.expander("Technical details", expanded=False):
                    st.write(f"**Document ID:** {clean_value(document_id)}")
                    st.write(f"**Rank:** {round(rank, 4) if rank is not None else '—'}")