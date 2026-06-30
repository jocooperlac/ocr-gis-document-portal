import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client
from components.filters import render_filters
from components.results import (
    render_metrics,
    render_results_table,
    render_search_results
)
from components.document_detail import render_document_detail
from components.branding import render_branding
#from services.logging_service import log_search


# ----------------------------
# SETUP
# ----------------------------

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("Missing SUPABASE_URL or SUPABASE_KEY in your .env file.")
    st.stop()

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(
    page_title="Legal Document Search",
    layout="wide"
)


# ----------------------------
# HELPERS
# ----------------------------

def clean_value(value):
    if value is None or value == "":
        return "—"
    return value


@st.cache_data(ttl=300)
def get_distinct_values(field_name):
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

        values = sorted({
            str(row.get(field_name)).strip()
            for row in all_rows
            if row.get(field_name) not in [None, ""]
        })

        return values

    except Exception as e:
        st.sidebar.error(f"Could not load {field_name} filter: {e}")
        return []


@st.cache_data(ttl=60)
def search_document_pages(search_term):
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
        filtered = [
            row for row in filtered
            if row.get("city") == city
        ]

    if document_type and document_type != "All":
        filtered = [
            row for row in filtered
            if row.get("document_type") == document_type
        ]

    if review_status and review_status != "All":
        filtered = [
            row for row in filtered
            if row.get("review_status") == review_status
        ]

    if visibility and visibility != "All":
        filtered = [
            row for row in filtered
            if row.get("visibility") == visibility
        ]

    return filtered


@st.cache_data(ttl=60)
def get_document_pages(document_id):
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


# ----------------------------
# SIDEBAR
# ----------------------------
filters = render_filters()

city_filter = filters["city"]
document_type_filter = filters["document_type"]
review_status_filter = filters["review_status"]
visibility_filter = filters["visibility"]

#demo toggle
public_demo_mode = st.sidebar.toggle("Public Demo Mode", value=True)

# ----------------------------
# MAIN SEARCH
# ----------------------------

render_branding()

search_term = st.text_input(
    "Search OCR text",
    placeholder="Example: annexation, ordinance, City of Arcadia, Resolution No..."
)

if not search_term:
    st.info("Enter a search term to begin.")
    st.stop()

results = search_document_pages(search_term)
results = filter_results(
    results,
    city_filter,
    document_type_filter,
    review_status_filter,
    visibility_filter
)

#log_search(
#    search_term=search_term,
#    result_count=len(results),
#    city_filter=city_filter,
#    document_type_filter=document_type_filter,
#    review_status_filter=review_status_filter,
#    visibility_filter=visibility_filter
#) unused for now

#st.write(f"**Page hits:** {len(results)}")

render_metrics(results)

if not results:
    st.warning("No matching pages found.")
    st.stop()


if not public_demo_mode: 
    render_results_table(results)

render_document_detail()

render_search_results(
    results,
    public_demo_mode=public_demo_mode
)