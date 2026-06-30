import os
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client


load_dotenv()


@st.cache_resource
def get_supabase_client():
    supabase_url = st.secrets.get("SUPABASE_URL", os.getenv("SUPABASE_URL"))
    supabase_key = st.secrets.get("SUPABASE_KEY", os.getenv("SUPABASE_KEY"))

    if not supabase_url or not supabase_key:
        st.error("Missing Supabase credentials.")
        st.stop()

    return create_client(supabase_url, supabase_key)