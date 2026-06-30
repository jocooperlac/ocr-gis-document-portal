import streamlit as st
from services.supabase_client import get_supabase_client


@st.cache_data(ttl=60)
def get_document_pages(document_id):
    supabase = get_supabase_client()

    try:
        result = (
            supabase
            .table("document_pages")
            .select("page_number, page_md_path, page_image_path, page_text")
            .eq("document_id", document_id)
            .order("page_number")
            .limit(500)
            .execute()
        )
        return result.data or []

    except Exception as e:
        st.error(f"Could not load pages: {e}")
        return []


@st.cache_data(ttl=60)
def get_document_detail(document_id):
    supabase = get_supabase_client()

    try:
        result = (
            supabase
            .table("documents")
            .select("*")
            .eq("id", document_id)
            .limit(1)
            .execute()
        )

        if result.data:
            return result.data[0]

        return None

    except Exception as e:
        st.error(f"Could not load document detail: {e}")
        return None