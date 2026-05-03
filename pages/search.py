import streamlit as st
import pandas as pd
from services.db import load



def render():

    st.subheader("🔍 Search")

    df = load("records")

    if df is None or df.empty:
        st.warning("No records found")
        return

    df = df.copy()

    # =========================
    # SEARCH FILTER
    # =========================
    q = st.text_input("Search")

    if q:
        df = df[df.astype(str).apply(
            lambda x: x.str.contains(q, case=False, na=False)
        ).any(axis=1)]

    # =========================
    # COLUMN ORDER FIX
    # =========================
    priority = ["DRIVE_BY", "COMP", "BID", "TAX"]

    priority_cols = [c for c in priority if c in df.columns]
    other_cols = [c for c in df.columns if c not in priority_cols]

    df = df[priority_cols + other_cols]

    # =========================
    # DISPLAY
    # =========================
    st.dataframe(df, use_container_width=True)