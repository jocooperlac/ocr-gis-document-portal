import streamlit as st
from services.document_service import (
    get_document_place_references,
    get_document_survey_references,
)
from utils.helpers import clean_value


def format_survey_type(value):
    if not value:
        return "Survey Document"

    return value.replace("_", " ").title()


def render_document_references(document_id):
    survey_links = get_document_survey_references(document_id)
    place_references = get_document_place_references(document_id)

    st.divider()
    st.subheader("Related Records and References")

    st.markdown("### Survey Documents")

    if not survey_links:
        st.caption("No survey documents have been linked.")
    else:
        for link in survey_links:
            survey = link.get("survey_documents") or {}

            survey_type = format_survey_type(survey.get("survey_type"))
            survey_number = survey.get("survey_number")
            title = survey.get("title")

            heading = title or " ".join(
                part for part in [survey_type, survey_number] if part
            )

            with st.container(border=True):
                st.markdown(f"#### {heading}")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.write(
                        f"**Book:** {clean_value(survey.get('book_number'))}"
                    )

                with col2:
                    st.write(
                        f"**Page(s):** {clean_value(survey.get('page_number'))}"
                    )

                with col3:
                    st.write(
                        f"**Referenced on page:** "
                        f"{clean_value(link.get('source_page_number'))}"
                    )

                survey_url = survey.get("document_url")

                if survey_url:
                    st.link_button("Open Survey Document", survey_url)

                if link.get("source_text"):
                    with st.expander("View source reference"):
                        st.write(link["source_text"])

    st.markdown("### Streets, Cities, and Other Places")

    if not place_references:
        st.caption("No place references have been extracted.")
    else:
        for reference in place_references:
            display_name = (
                reference.get("normalized_name")
                or reference.get("reference_name")
            )

            st.write(
                f"- **{clean_value(display_name)}** "
                f"— {clean_value(reference.get('reference_type')).title()} "
                f"— page {clean_value(reference.get('source_page_number'))}"
            )