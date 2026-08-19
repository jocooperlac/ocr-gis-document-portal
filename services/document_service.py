import streamlit as st
from services.supabase_client import get_supabase_client


@st.cache_data(ttl=60)
def get_document_survey_references(document_id):
    supabase = get_supabase_client()

    try:
        result = (
            supabase
            .table("document_survey_links")
            .select(
                """
                id,
                source_page_number,
                source_text,
                confidence,
                review_status,
                survey_documents (
                    id,
                    survey_type,
                    survey_number,
                    book_number,
                    page_number,
                    sheet_number,
                    title,
                    source_agency,
                    document_url
                )
                """
            )
            .eq("document_id", document_id)
            .order("source_page_number")
            .execute()
        )

        return result.data or []

    except Exception as e:
        st.error(f"Could not load survey references: {e}")
        return []


@st.cache_data(ttl=60)
def get_document_place_references(document_id):
    supabase = get_supabase_client()

    try:
        result = (
            supabase
            .table("document_place_references")
            .select(
                """
                id,
                reference_type,
                reference_name,
                normalized_name,
                source_page_number,
                source_text,
                confidence,
                review_status
                """
            )
            .eq("document_id", document_id)
            .order("source_page_number")
            .execute()
        )

        return result.data or []

    except Exception as e:
        st.error(f"Could not load place references: {e}")
        return []