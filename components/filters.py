import streamlit as st
from services.search_service import get_distinct_values


def render_filters():
    st.sidebar.title("Filters")

    if st.sidebar.button("Clear cache / refresh filters"):
        st.cache_data.clear()
        st.rerun()

    cities = ["All"] + get_distinct_values("city")
    document_types = ["All"] + get_distinct_values("document_type")

    city_filter = st.sidebar.selectbox("City", cities)
    document_type_filter = st.sidebar.selectbox("Document type", document_types)

    review_status_filter = st.sidebar.selectbox(
        "Review status",
        ["All", "unreviewed", "needs_review", "verified", "published"]
    )

    visibility_filter = st.sidebar.selectbox(
        "Visibility",
        ["All", "internal", "public", "restricted"]
    )

    return {
        "city": city_filter,
        "document_type": document_type_filter,
        "review_status": review_status_filter,
        "visibility": visibility_filter,
    }