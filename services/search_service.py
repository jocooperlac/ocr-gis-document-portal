import streamlit as st
from services.supabase_client import get_supabase_client


@st.cache_data(ttl=300)
def get_distinct_values(field_name):
    supabase = get_supabase_client()

    try:
        all_rows = []
        page_size = 1000
        start = 0

        while True:
            end = start + page_size - 1

            result = (
                supabase
                .table("documents")
                .select(field_name)
                .not_.is_(field_name, "null")
                .range(start, end)
                .execute()
            )

            rows = result.data or []
            all_rows.extend(rows)

            if len(rows) < page_size:
                break

            start += page_size

        return sorted({
            str(row.get(field_name)).strip()
            for row in all_rows
            if row.get(field_name) not in [None, ""]
        })

    except Exception as e:
        st.sidebar.error(f"Could not load {field_name} filter: {e}")
        return []


@st.cache_data(ttl=60)
def search_document_pages(search_term):
    supabase = get_supabase_client()

    if not search_term:
        return []

    try:
        result = (
            supabase
            .rpc(
                "search_document_pages",
                {"search_query": search_term}
            )
            .execute()
        )
        return result.data or []

    except Exception as e:
        st.error(f"Search error: {e}")
        return []


def filter_results(results, city, document_type, review_status, visibility):
    filtered = results

    if city and city != "All":
        filtered = [row for row in filtered if row.get("city") == city]

    if document_type and document_type != "All":
        filtered = [row for row in filtered if row.get("document_type") == document_type]

    if review_status and review_status != "All":
        filtered = [row for row in filtered if row.get("review_status") == review_status]

    if visibility and visibility != "All":
        filtered = [row for row in filtered if row.get("visibility") == visibility]

    return filtered